# Nixtla vs StatsForecast Benchmark

Head-to-head benchmark of TimeGPT against open-source StatsForecast on your data. Real model fits, real metrics (sMAPE / MASE / MAE / RMSE), wall-time comparison, rule-based recommendations on which engine to use for which workload.

**Version**: 1.0.0 · **Status**: Working · **API key needed**: Optional (TimeGPT path requires `NIXTLA_API_KEY`; statsforecast path is offline)

---

## 30-second pitch

A Nixtla customer is on the fence: pay for TimeGPT or stay on free statsforecast? This plugin runs both engines against their actual data with the same train/test split, computes the same metrics on both, times each, and tells them which wins by how much. No marketing, no hand-waving — real numbers.

---

## Quick start (under 5 minutes)

```bash
cd 005-plugins/nixtla-vs-statsforecast-benchmark
pip install -r scripts/requirements.txt

# Optional — enable the TimeGPT side of the comparison
export NIXTLA_API_KEY="your-key-here"

# In Claude Code:
# "Benchmark TimeGPT vs statsforecast on this CSV: <path>; horizon 14, daily."
# Claude calls load_data → run_benchmark → get_recommendations → generate_report.
```

If `NIXTLA_API_KEY` is unset, only statsforecast runs; the report says so explicitly with a `skipped_reason`.

---

## What you get back

`run_benchmark` returns:

```json
{
  "statsforecast": {
    "models": {
      "AutoETS":       {"smape": 9.2,  "mase": 0.91, "mae": 4.3, "rmse": 5.1},
      "AutoTheta":     {"smape": 10.1, "mase": 1.02, "mae": 4.7, "rmse": 5.6},
      "SeasonalNaive": {"smape": 14.8, "mase": 1.50, "mae": 7.0, "rmse": 8.2}
    },
    "wall_time_seconds": 2.3,
    "best_model": "AutoETS"
  },
  "timegpt": {
    "metrics": {"smape": 8.4, "mase": 0.84, "mae": 3.9, "rmse": 4.7},
    "wall_time_seconds": 11.7
  },
  "horizon": 14,
  "n_series": 12,
  "freq": "D",
  "winner": "timegpt",
  "winner_rationale": "TimeGPT 8.4% sMAPE beats best statsforecast model (AutoETS, 9.2%) by 8.7%; ..."
}
```

`get_recommendations` reads the result and returns concrete, rule-based guidance: when to use TimeGPT (long horizons, high stakes, exogenous variables) vs when to keep statsforecast (short horizons, deterministic seasonality, real-time SLA, cost-sensitive).

`generate_report` composes a markdown report: methodology, per-model metrics table, wall-time comparison, winner verdict, recommendations, raw numbers appendix.

---

## Required input format

A long-format DataFrame (or CSV path) with columns: `unique_id`, `ds`, `y`. Same shape statsforecast and Nixtla both accept natively. Multiple series share one DataFrame.

```csv
unique_id,ds,y
sales_seriesA,2026-01-01,123.4
sales_seriesA,2026-01-02,127.1
sales_seriesB,2026-01-01,98.2
...
```

---

## Metrics

| Metric | Formula | Range |
|---|---|---|
| **sMAPE** | mean(2·|y - ŷ| / (|y| + |ŷ|)) × 100 (M4 definition) | 0–200% |
| **MASE** | mean(|y - ŷ|) / mean(|y_train[s:] - y_train[:-s]|) where s = seasonality | ≥ 0 |
| **MAE** | mean(|y - ŷ|) | ≥ 0 |
| **RMSE** | sqrt(mean((y - ŷ)²)) | ≥ 0 |

Lower is better for all four. Returns `NaN` for MASE when the in-sample seasonal-naive denominator is zero (constant training series — the metric is not meaningful in that case).

---

## Tests

```bash
cd 005-plugins/nixtla-vs-statsforecast-benchmark
PYTHONPATH=scripts pytest tests/ --cov=benchmark_mcp -v
```

33 tests covering metric helpers (with known values), seasonality-from-frequency mapping, data loading + CSV path + missing-column errors, train/test split correctness (no overlap, last-N per series), `run_benchmark` integration with mocked engines (no real model fits required to test), and async MCP dispatch.

---

## Environment variables

| Variable | When you need it | What it's for |
|---|---|---|
| `NIXTLA_API_KEY` | TimeGPT side of the benchmark | TimeGPT API authentication |

When unset, the TimeGPT side is skipped and the report records `skipped_reason="NIXTLA_API_KEY not set"`. The statsforecast side always runs.

---

## License

MIT — Jeremy Longshore.
