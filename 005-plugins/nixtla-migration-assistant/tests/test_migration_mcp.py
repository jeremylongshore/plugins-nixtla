"""Unit tests for nixtla-migration-assistant MCP server."""

from __future__ import annotations

import asyncio
import json

import migration_mcp as mcp
import pytest

# ---------------------------------------------------------------------------
# analyze_code
# ---------------------------------------------------------------------------


class TestAnalyzeCode:
    def test_invalid_syntax_returns_error(self):
        result = mcp.analyze_code("def broken(:")
        assert "error" in result

    def test_detects_prophet(self, prophet_source):
        result = mcp.analyze_code(prophet_source)
        names = {p["library"] for p in result["patterns"]}
        assert "Prophet" in names

    def test_detects_statsmodels_arima(self, statsmodels_arima_source):
        result = mcp.analyze_code(statsmodels_arima_source)
        names = {p["library"] for p in result["patterns"]}
        assert "statsmodels.ARIMA" in names

    def test_detects_statsmodels_ets(self, statsmodels_ets_source):
        result = mcp.analyze_code(statsmodels_ets_source)
        names = {p["library"] for p in result["patterns"]}
        assert "statsmodels.ExponentialSmoothing" in names

    def test_detects_sklearn(self, sklearn_source):
        result = mcp.analyze_code(sklearn_source)
        names = {p["library"] for p in result["patterns"]}
        assert "sklearn" in names

    def test_no_forecasting_lib_returns_empty_patterns(self):
        result = mcp.analyze_code("import os\nprint('hello')")
        assert result["patterns"] == []
        assert result["complexity"] == "low"

    def test_complexity_high_for_many_patterns(self, prophet_source, statsmodels_arima_source):
        combined = (
            prophet_source + "\n" + statsmodels_arima_source + "\n" + statsmodels_arima_source
        )
        result = mcp.analyze_code(combined)
        # Combined sources >= 2 patterns -> at least medium.
        assert result["complexity"] in {"medium", "high"}

    def test_line_count_reported(self, prophet_source):
        result = mcp.analyze_code(prophet_source)
        assert result["line_count"] > 0


# ---------------------------------------------------------------------------
# transform_data
# ---------------------------------------------------------------------------


class TestTransformData:
    def test_missing_file_returns_error(self):
        result = mcp.transform_data("/nonexistent/path.csv")
        assert result["status"] == "error"
        assert "not found" in result["message"].lower()

    def test_basic_transform_succeeds(self, synthetic_csv):
        result = mcp.transform_data(
            synthetic_csv, timestamp_col="date", value_col="sales", group_col="store"
        )
        assert result["status"] == "success"
        assert result["output_columns"] == ["unique_id", "ds", "y"]
        assert result["n_series"] == 2

    def test_rows_in_matches_csv(self, synthetic_csv):
        result = mcp.transform_data(
            synthetic_csv, timestamp_col="date", value_col="sales", group_col="store"
        )
        assert result["rows_in"] == 120  # 2 groups * 60 rows

    def test_default_unique_id_when_no_group_col(self, synthetic_csv):
        result = mcp.transform_data(synthetic_csv, timestamp_col="date", value_col="sales")
        # No group_col -> all rows assigned 'series_0', so n_series == 1.
        assert result["n_series"] == 1
        assert any("series_0" in w or "single-series" in w for w in result["warnings"])

    def test_missing_required_column(self, synthetic_csv):
        result = mcp.transform_data(synthetic_csv, timestamp_col="nonexistent_col")
        assert result["status"] == "error"
        assert "missing" in result["message"].lower()

    def test_nan_interpolation(self, csv_with_nans):
        result = mcp.transform_data(csv_with_nans, timestamp_col="ds", value_col="y")
        # interpolate strategy fills NaNs.
        assert result["status"] == "success"
        any_warned_about_nans = any("NaN" in w for w in result["warnings"])
        assert any_warned_about_nans

    def test_preview_returned(self, synthetic_csv):
        result = mcp.transform_data(
            synthetic_csv, timestamp_col="date", value_col="sales", group_col="store"
        )
        assert "transformed_preview" in result
        assert len(result["transformed_preview"]) <= 5


# ---------------------------------------------------------------------------
# generate_code
# ---------------------------------------------------------------------------


class TestGenerateCode:
    def test_prophet_to_timegpt(self):
        result = mcp.generate_code(source_library="prophet", target_library="timegpt")
        assert result["status"] == "success"
        assert "from nixtla import NixtlaClient" in result["code"]
        assert "client.forecast" in result["code"]

    def test_prophet_to_statsforecast(self):
        result = mcp.generate_code(source_library="prophet", target_library="statsforecast")
        assert result["status"] == "success"
        assert "from statsforecast import StatsForecast" in result["code"]
        assert "AutoETS" in result["code"]

    def test_statsmodels_arima_to_statsforecast(self):
        result = mcp.generate_code(
            source_library="statsmodels.arima", target_library="statsforecast"
        )
        assert result["status"] == "success"
        assert "AutoARIMA" in result["code"]

    def test_unknown_combo_returns_error_with_available(self):
        result = mcp.generate_code(source_library="prophet", target_library="oracle")
        assert result["status"] == "error"
        assert "available_combos" in result

    def test_horizon_and_freq_substituted(self):
        result = mcp.generate_code(
            source_library="prophet", target_library="timegpt", horizon=42, freq="W"
        )
        assert "h=42" in result["code"]
        assert "'W'" in result["code"]


# ---------------------------------------------------------------------------
# generate_plan
# ---------------------------------------------------------------------------


class TestGeneratePlan:
    def test_low_complexity_smaller_total_hours(self):
        low = {
            "patterns": [{"library": "Prophet"}],
            "complexity": "low",
            "line_count": 50,
            "n_patterns": 1,
        }
        high = {
            "patterns": [{"library": "Prophet"}, {"library": "ARIMA"}, {"library": "ETS"}],
            "complexity": "high",
            "line_count": 1000,
            "n_patterns": 3,
        }
        plan_low = mcp.generate_plan(low)
        plan_high = mcp.generate_plan(high)
        assert plan_low["total_estimated_hours"] < plan_high["total_estimated_hours"]

    def test_four_phases(self):
        plan = mcp.generate_plan({"patterns": [], "complexity": "low", "line_count": 0})
        assert len(plan["phases"]) == 4
        assert [p["phase"] for p in plan["phases"]] == [1, 2, 3, 4]

    def test_each_phase_has_tasks_and_validation(self):
        plan = mcp.generate_plan({"patterns": [{"library": "Prophet"}], "complexity": "medium"})
        for ph in plan["phases"]:
            assert len(ph["tasks"]) > 0
            assert len(ph["validation"]) > 0
            assert "rollback" in ph

    def test_risk_scales_with_complexity(self):
        low = mcp.generate_plan({"patterns": [], "complexity": "low"})
        high = mcp.generate_plan({"patterns": [], "complexity": "high"})
        assert low["risk_level"] == "low"
        assert high["risk_level"] == "high"


# ---------------------------------------------------------------------------
# compare_accuracy
# ---------------------------------------------------------------------------


class TestCompareAccuracy:
    def test_missing_file(self):
        result = mcp.compare_accuracy("/nonexistent.csv")
        assert result["status"] == "error"

    def test_too_few_rows(self, tmp_path):
        import pandas as pd

        small = pd.DataFrame({"ds": pd.date_range("2026-01-01", periods=5), "y": [1.0] * 5})
        p = tmp_path / "small.csv"
        small.to_csv(p, index=False)
        result = mcp.compare_accuracy(str(p), horizon=14)
        assert result["status"] == "error"
        assert "Need" in result["message"]

    def test_handles_missing_optional_deps_gracefully(self, synthetic_csv):
        # On a system without prophet / statsmodels / nixtla / statsforecast installed,
        # the function still returns a dict; both engines may report "error".
        result = mcp.compare_accuracy(
            synthetic_csv,
            timestamp_col="date",
            value_col="sales",
            horizon=14,
            source_engine="prophet",
            target_engine="statsforecast",
        )
        # No crash; status is either 'success' (if both ran) or 'error' (if neither did).
        assert "status" in result
        assert "source" in result
        assert "target" in result


# ---------------------------------------------------------------------------
# call_tool dispatch
# ---------------------------------------------------------------------------


class TestCallTool:
    @pytest.fixture
    def run(self):
        def _run(coro):
            return asyncio.run(coro)

        return _run

    def test_analyze_code_dispatch(self, run, prophet_source):
        result = run(mcp.call_tool("analyze_code", {"code": prophet_source}))
        parsed = json.loads(result[0].text)
        assert "patterns" in parsed

    def test_generate_code_dispatch(self, run):
        result = run(
            mcp.call_tool(
                "generate_code", {"source_library": "prophet", "target_library": "timegpt"}
            )
        )
        parsed = json.loads(result[0].text)
        assert parsed["status"] == "success"

    def test_unknown_tool(self, run):
        result = run(mcp.call_tool("xyz", {}))
        assert "Unknown" in result[0].text

    def test_list_tools_includes_all_five(self, run):
        tools = run(mcp.list_tools())
        names = {t.name for t in tools}
        assert names == {
            "analyze_code",
            "generate_plan",
            "transform_data",
            "generate_code",
            "compare_accuracy",
        }
