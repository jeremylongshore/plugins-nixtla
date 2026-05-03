"""Unit tests for nixtla-forecast-explainer MCP server.

Covers:
    * _coerce_series — input shape coercion
    * _infer_period — seasonal period detection
    * _strength — Hyndman strength metric
    * decompose_forecast — STL decomposition + edge cases
    * identify_drivers — Pearson correlation with lag scan
    * generate_narrative — text output
    * generate_report — markdown composition
    * call_tool — async dispatch
"""

from __future__ import annotations

import asyncio
import json

import explainer_mcp as mcp
import numpy as np
import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# _coerce_series
# ---------------------------------------------------------------------------


class TestCoerceSeries:
    def test_list_of_floats(self):
        result = mcp._coerce_series([1.0, 2.0, 3.0])
        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert result.iloc[0] == 1.0

    def test_list_of_dicts(self):
        result = mcp._coerce_series(
            [{"ds": "2026-01-01", "y": 5.0}, {"ds": "2026-01-02", "y": 7.0}]
        )
        assert len(result) == 2
        assert list(result.values) == [5.0, 7.0]

    def test_dataframe_with_ds_y(self):
        df = pd.DataFrame({"ds": ["2026-01-01", "2026-01-02"], "y": [10.0, 20.0]})
        result = mcp._coerce_series(df)
        assert len(result) == 2
        assert isinstance(result.index, pd.DatetimeIndex)

    def test_dict_input(self):
        result = mcp._coerce_series({"ds": ["2026-01-01"], "y": [42.0]})
        assert len(result) == 1
        assert result.iloc[0] == 42.0

    def test_series_passthrough(self):
        s = pd.Series([1.0, 2.0])
        result = mcp._coerce_series(s)
        assert len(result) == 2

    def test_missing_value_key_raises(self):
        with pytest.raises(ValueError, match="missing"):
            mcp._coerce_series({"ds": ["2026-01-01"]})

    def test_unsupported_type_raises(self):
        with pytest.raises(TypeError):
            mcp._coerce_series(42)


# ---------------------------------------------------------------------------
# _infer_period
# ---------------------------------------------------------------------------


class TestInferPeriod:
    def test_daily_index_returns_7(self):
        idx = pd.date_range("2026-01-01", periods=14, freq="D")
        s = pd.Series(range(14), index=idx, dtype=float)
        assert mcp._infer_period(s) == 7

    def test_no_datetime_index_returns_default(self):
        s = pd.Series([1.0, 2.0, 3.0])
        assert mcp._infer_period(s, default=12) == 12

    def test_minimum_period_is_2(self):
        s = pd.Series([1.0, 2.0, 3.0])
        result = mcp._infer_period(s)
        assert result >= 2


# ---------------------------------------------------------------------------
# _strength
# ---------------------------------------------------------------------------


class TestStrength:
    def test_perfect_strength_when_no_residual(self):
        component = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        residual = np.zeros_like(component)
        assert mcp._strength(component, residual) == pytest.approx(1.0)

    def test_zero_strength_when_pure_noise(self):
        component = np.zeros(100)
        residual = np.random.default_rng(0).normal(0, 1, 100)
        assert mcp._strength(component, residual) <= 0.01

    def test_returns_float_in_unit_interval(self):
        rng = np.random.default_rng(1)
        component = rng.normal(0, 1, 50)
        residual = rng.normal(0, 1, 50)
        result = mcp._strength(component, residual)
        assert 0.0 <= result <= 1.0


# ---------------------------------------------------------------------------
# decompose_forecast
# ---------------------------------------------------------------------------


class TestDecomposeForecast:
    def test_basic_decomposition(self, synthetic_seasonal_series):
        result = mcp.decompose_forecast(synthetic_seasonal_series, period=7)
        assert set(result.keys()) >= {
            "trend",
            "seasonal",
            "residual",
            "strength_of_trend",
            "strength_of_seasonality",
            "period",
            "n_obs",
        }

    def test_components_have_same_length(self, synthetic_seasonal_series):
        result = mcp.decompose_forecast(synthetic_seasonal_series, period=7)
        n = result["n_obs"]
        assert len(result["trend"]) == n
        assert len(result["seasonal"]) == n
        assert len(result["residual"]) == n

    def test_strength_metrics_in_unit_interval(self, synthetic_seasonal_series):
        result = mcp.decompose_forecast(synthetic_seasonal_series, period=7)
        assert 0.0 <= result["strength_of_trend"] <= 1.0
        assert 0.0 <= result["strength_of_seasonality"] <= 1.0

    def test_synthetic_data_has_high_seasonality_strength(self, synthetic_seasonal_series):
        # The synthetic fixture has explicit weekly seasonality of amplitude 10.
        result = mcp.decompose_forecast(synthetic_seasonal_series, period=7)
        assert result["strength_of_seasonality"] > 0.5

    def test_too_few_observations_raises(self):
        with pytest.raises(ValueError, match="at least 4"):
            mcp.decompose_forecast([1.0, 2.0])

    def test_period_below_2_raises(self, synthetic_seasonal_series):
        with pytest.raises(ValueError, match=">= 2"):
            mcp.decompose_forecast(synthetic_seasonal_series, period=1)

    def test_too_few_cycles_raises(self):
        # 5 obs with period=7 → not enough cycles.
        data = [{"ds": f"2026-01-0{i+1}", "y": float(i)} for i in range(5)]
        with pytest.raises(ValueError, match="seasonal cycles"):
            mcp.decompose_forecast(data, period=7)


# ---------------------------------------------------------------------------
# identify_drivers
# ---------------------------------------------------------------------------


class TestIdentifyDrivers:
    def test_strong_correlation_ranks_first(self, synthetic_target_and_drivers):
        result = mcp.identify_drivers(
            synthetic_target_and_drivers["target"],
            synthetic_target_and_drivers["candidates"],
        )
        assert "drivers" in result
        # The first ranked driver should be 'strong_pos' or 'inverse' (both |corr| ~1).
        assert result["drivers"][0]["name"] in {"strong_pos", "inverse"}

    def test_n_candidates_reflects_input(self, synthetic_target_and_drivers):
        result = mcp.identify_drivers(
            synthetic_target_and_drivers["target"],
            synthetic_target_and_drivers["candidates"],
        )
        assert result["n_candidates"] == 3

    def test_strong_pos_has_positive_correlation(self, synthetic_target_and_drivers):
        result = mcp.identify_drivers(
            synthetic_target_and_drivers["target"],
            synthetic_target_and_drivers["candidates"],
        )
        for d in result["drivers"]:
            if d["name"] == "strong_pos":
                assert d["correlation"] > 0.9

    def test_inverse_has_negative_correlation(self, synthetic_target_and_drivers):
        result = mcp.identify_drivers(
            synthetic_target_and_drivers["target"],
            synthetic_target_and_drivers["candidates"],
        )
        for d in result["drivers"]:
            if d["name"] == "inverse":
                assert d["correlation"] < -0.9

    def test_max_lag_negative_raises(self, synthetic_target_and_drivers):
        with pytest.raises(ValueError, match="max_lag"):
            mcp.identify_drivers(
                synthetic_target_and_drivers["target"],
                synthetic_target_and_drivers["candidates"],
                max_lag=-1,
            )

    def test_short_target_raises(self):
        with pytest.raises(ValueError, match="3 target"):
            mcp.identify_drivers([1.0, 2.0], {"x": [1.0, 2.0]})

    def test_results_sorted_by_abs_correlation(self, synthetic_target_and_drivers):
        result = mcp.identify_drivers(
            synthetic_target_and_drivers["target"],
            synthetic_target_and_drivers["candidates"],
        )
        abs_corrs = [abs(d["correlation"]) for d in result["drivers"]]
        assert abs_corrs == sorted(abs_corrs, reverse=True)


# ---------------------------------------------------------------------------
# generate_narrative
# ---------------------------------------------------------------------------


class TestGenerateNarrative:
    def test_executive_audience_returns_string(self):
        result = mcp.generate_narrative(
            {"forecast_value": 100, "trend": "up", "confidence": 0.85}, audience="executive"
        )
        assert isinstance(result, str)
        assert len(result) > 10


# ---------------------------------------------------------------------------
# generate_report
# ---------------------------------------------------------------------------


class TestGenerateReport:
    def test_returns_markdown_string(self, synthetic_seasonal_series):
        decomp = mcp.decompose_forecast(synthetic_seasonal_series, period=7)
        narrative = mcp.generate_narrative(
            {"forecast_value": 150, "trend": "up", "confidence": 0.9}
        )
        result = mcp.generate_report(
            decomposition=decomp,
            narrative=narrative,
            drivers={"drivers": [], "n_candidates": 0, "max_lag": 7},
        )
        # Either returns a string OR a dict with markdown.
        if isinstance(result, dict):
            assert "report" in result or "markdown" in result or "content" in result
        else:
            assert isinstance(result, str)


# ---------------------------------------------------------------------------
# call_tool dispatch
# ---------------------------------------------------------------------------


class TestCallTool:
    @pytest.fixture
    def run(self):
        def _run(coro):
            return asyncio.run(coro)

        return _run

    def test_decompose_forecast_dispatch(self, run, synthetic_seasonal_series):
        result = run(
            mcp.call_tool(
                "decompose_forecast",
                {"data": synthetic_seasonal_series, "period": 7},
            )
        )
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert "trend" in parsed

    def test_identify_drivers_dispatch(self, run, synthetic_target_and_drivers):
        result = run(
            mcp.call_tool(
                "identify_drivers",
                {
                    "target": synthetic_target_and_drivers["target"],
                    "candidates": synthetic_target_and_drivers["candidates"],
                },
            )
        )
        parsed = json.loads(result[0].text)
        assert "drivers" in parsed

    def test_unknown_tool_returns_error(self, run):
        result = run(mcp.call_tool("nonexistent_xyz", {}))
        assert "Unknown" in result[0].text or "error" in result[0].text.lower()

    def test_list_tools_includes_all_expected(self, run):
        tools = run(mcp.list_tools())
        names = {t.name for t in tools}
        assert "decompose_forecast" in names
        assert "identify_drivers" in names
        assert "generate_narrative" in names
        assert "generate_report" in names
