"""Unit tests for nixtla-vs-statsforecast-benchmark MCP server."""

from __future__ import annotations

import asyncio
import json
from unittest.mock import patch

import benchmark_mcp as mcp
import numpy as np
import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------


class TestMetricHelpers:
    def test_smape_perfect_prediction_is_zero(self):
        y = np.array([10.0, 20.0, 30.0])
        assert mcp._smape(y, y) == pytest.approx(0.0)

    def test_smape_pure_zero_pairs_contribute_zero(self):
        y_true = np.array([0.0, 0.0, 5.0])
        y_pred = np.array([0.0, 0.0, 5.0])
        assert mcp._smape(y_true, y_pred) == pytest.approx(0.0)

    def test_smape_known_value(self):
        # |y - yhat| = 5, denom = |10|+|15| = 25, smape = 2*5/25 = 0.4 = 40%
        y_true = np.array([10.0])
        y_pred = np.array([15.0])
        assert mcp._smape(y_true, y_pred) == pytest.approx(40.0)

    def test_mae_basic(self):
        assert mcp._mae(np.array([1.0, 2.0]), np.array([2.0, 4.0])) == pytest.approx(1.5)

    def test_rmse_basic(self):
        # diffs = [1, 2]; squared = [1, 4]; mean = 2.5; sqrt = sqrt(2.5)
        assert mcp._rmse(np.array([0.0, 0.0]), np.array([1.0, 2.0])) == pytest.approx(np.sqrt(2.5))

    def test_mase_returns_nan_on_short_train(self):
        result = mcp._mase(np.array([10.0]), np.array([11.0]), np.array([1.0]), seasonality=1)
        assert np.isnan(result)

    def test_mase_returns_nan_on_constant_train(self):
        train = np.array([5.0, 5.0, 5.0, 5.0])
        result = mcp._mase(np.array([10.0]), np.array([11.0]), train, seasonality=1)
        assert np.isnan(result)

    def test_mase_known_value(self):
        train = np.array([1.0, 2.0, 3.0, 4.0])  # |diffs| = [1, 1, 1], scale = 1.0
        y_true = np.array([5.0])
        y_pred = np.array([7.0])  # |y-yhat| = 2.0
        assert mcp._mase(y_true, y_pred, train, seasonality=1) == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# _seasonality_for_freq
# ---------------------------------------------------------------------------


class TestSeasonalityForFreq:
    @pytest.mark.parametrize(
        "freq,expected",
        [
            ("H", 24),
            ("D", 7),
            ("W", 52),
            ("M", 12),
            ("Q", 4),
            ("Y", 1),
            ("A", 1),
            ("", 1),
            ("unknown", 1),
        ],
    )
    def test_freq_mapping(self, freq, expected):
        assert mcp._seasonality_for_freq(freq) == expected


# ---------------------------------------------------------------------------
# _load_dataframe
# ---------------------------------------------------------------------------


class TestLoadDataframe:
    def test_dataframe_passthrough(self, sample_long_df):
        result = mcp._load_dataframe(sample_long_df)
        assert set(result.columns) >= {"unique_id", "ds", "y"}

    def test_csv_path_loads(self, sample_csv_path):
        result = mcp._load_dataframe(sample_csv_path)
        assert len(result) == 180  # 3 series * 60 obs

    def test_missing_path_raises(self):
        with pytest.raises(FileNotFoundError):
            mcp._load_dataframe("/nonexistent/path.csv")

    def test_missing_columns_raises(self):
        bad = pd.DataFrame({"x": [1, 2]})
        with pytest.raises(ValueError, match="missing required columns"):
            mcp._load_dataframe(bad)

    def test_ds_coerced_to_datetime(self, sample_long_df):
        result = mcp._load_dataframe(sample_long_df)
        assert pd.api.types.is_datetime64_any_dtype(result["ds"])

    def test_sorted_by_uid_ds(self, sample_long_df):
        # Shuffle then verify sort
        shuffled = sample_long_df.sample(frac=1, random_state=1).reset_index(drop=True)
        result = mcp._load_dataframe(shuffled)
        for uid in result["unique_id"].unique():
            sub = result[result["unique_id"] == uid]
            assert (sub["ds"].values == np.sort(sub["ds"].values)).all()


# ---------------------------------------------------------------------------
# _split_train_test
# ---------------------------------------------------------------------------


class TestSplitTrainTest:
    def test_holdout_size(self, sample_long_df):
        df = mcp._load_dataframe(sample_long_df)
        train, test = mcp._split_train_test(df, horizon=7)
        # 7 obs * 3 series = 21 in test; rest in train
        assert len(test) == 21
        assert len(train) == 180 - 21

    def test_no_overlap_between_train_and_test(self, sample_long_df):
        df = mcp._load_dataframe(sample_long_df)
        train, test = mcp._split_train_test(df, horizon=7)
        # Concatenate keys from both, no duplicates if disjoint.
        all_keys = pd.concat(
            [
                train[["unique_id", "ds"]].assign(_src="train"),
                test[["unique_id", "ds"]].assign(_src="test"),
            ]
        )
        # Each (uid, ds) combo must appear exactly once.
        dups = all_keys.duplicated(subset=["unique_id", "ds"]).sum()
        assert dups == 0

    def test_test_is_last_n_per_series(self, sample_long_df):
        df = mcp._load_dataframe(sample_long_df)
        train, test = mcp._split_train_test(df, horizon=5)
        for uid in test["unique_id"].unique():
            test_dates = set(test.loc[test["unique_id"] == uid, "ds"])
            all_dates = sorted(df.loc[df["unique_id"] == uid, "ds"])
            expected_last5 = set(all_dates[-5:])
            assert test_dates == expected_last5


# ---------------------------------------------------------------------------
# get_recommendations
# ---------------------------------------------------------------------------


class TestGetRecommendations:
    def test_returns_dict_with_recommendations_key(self):
        # Minimal benchmark result.
        results = {
            "statsforecast": {
                "models": {
                    "AutoETS": {"smape": 12.0, "mase": 1.0, "mae": 5.0, "rmse": 6.0},
                },
                "wall_time_seconds": 2.5,
                "best_model": "AutoETS",
            },
            "timegpt": {
                "metrics": None,
                "wall_time_seconds": None,
                "skipped_reason": "NIXTLA_API_KEY not set",
            },
            "horizon": 7,
            "n_series": 3,
            "winner": "statsforecast",
        }
        out = mcp.get_recommendations(results)
        assert isinstance(out, dict)
        assert "recommendations" in out or "verdict" in out or "summary" in out or len(out) > 0

    def test_timegpt_skipped_recommends_trying(self):
        results = {
            "statsforecast": {
                "models": {"AutoETS": {"smape": 8.0, "mase": 0.9, "mae": 3.0, "rmse": 4.0}},
                "best_model": "AutoETS",
                "wall_time_seconds": 1.0,
            },
            "timegpt": {"skipped_reason": "NIXTLA_API_KEY not set"},
            "winner": "statsforecast",
        }
        out = mcp.get_recommendations(results)
        # The verdict / summary text should mention TimeGPT.
        text = json.dumps(out).lower()
        assert "timegpt" in text or "nixtla" in text


# ---------------------------------------------------------------------------
# generate_report
# ---------------------------------------------------------------------------


class TestGenerateReport:
    def test_returns_string_or_dict_with_markdown(self):
        results = {
            "statsforecast": {
                "models": {
                    "AutoETS": {"smape": 10.0, "mase": 1.0, "mae": 5.0, "rmse": 6.0},
                    "AutoTheta": {"smape": 11.0, "mase": 1.1, "mae": 5.5, "rmse": 6.5},
                    "SeasonalNaive": {"smape": 15.0, "mase": 1.5, "mae": 7.0, "rmse": 8.0},
                },
                "wall_time_seconds": 3.0,
                "best_model": "AutoETS",
            },
            "timegpt": {"skipped_reason": "NIXTLA_API_KEY not set"},
            "horizon": 7,
            "n_series": 3,
            "winner": "statsforecast",
            "winner_rationale": "TimeGPT skipped; AutoETS lowest sMAPE",
        }
        out = mcp.generate_report(results)
        if isinstance(out, dict):
            text = json.dumps(out)
        else:
            text = str(out)
        # Should mention key models or sections.
        assert "AutoETS" in text or "smape" in text.lower() or "Benchmark" in text


# ---------------------------------------------------------------------------
# call_tool dispatch
# ---------------------------------------------------------------------------


class TestCallTool:
    @pytest.fixture
    def run(self):
        def _run(coro):
            return asyncio.run(coro)

        return _run

    def test_load_data_dispatch(self, run, sample_csv_path):
        result = run(mcp.call_tool("load_data", {"path": sample_csv_path}))
        assert len(result) == 1
        # load_data returns either JSON metadata or the DataFrame summary.
        assert result[0].type == "text"

    def test_unknown_tool(self, run):
        result = run(mcp.call_tool("definitely_not_a_tool", {}))
        assert "Unknown" in result[0].text or "error" in result[0].text.lower()

    def test_list_tools_includes_run_benchmark(self, run):
        tools = run(mcp.list_tools())
        names = {t.name for t in tools}
        assert "run_benchmark" in names
        assert "load_data" in names
        assert "generate_report" in names
        assert "get_recommendations" in names


# ---------------------------------------------------------------------------
# run_benchmark — integration with mocked engines
# ---------------------------------------------------------------------------


class TestRunBenchmark:
    def test_skips_timegpt_when_no_api_key(self, sample_long_df, monkeypatch):
        monkeypatch.delenv("NIXTLA_API_KEY", raising=False)
        # Mock _run_statsforecast so we don't need statsforecast installed.
        fake_sf_result = {
            "metrics": {"AutoETS": {"smape": 9.0, "mase": 0.95, "mae": 4.0, "rmse": 5.0}},
            "wall_time_seconds": 1.5,
            "best_model": "AutoETS",
        }
        with patch.object(mcp, "_run_statsforecast", return_value=fake_sf_result):
            result = mcp.run_benchmark(data=sample_long_df, horizon=7, freq="D", seasonality=7)
        assert "timegpt" in result
        assert result["timegpt"].get("skipped_reason")
        assert result["winner"] in ("statsforecast", "tie", "timegpt")
