# Nixtla Forecast Explainer

Real post-hoc explainability for TimeGPT forecasts. STL decomposition into trend / seasonal / residual + Hyndman strength metrics. Pearson correlation driver analysis with lag scanning (predictor leads target by 0..N periods). Executive narrative + markdown report composition.

**Version**: 1.0.0 · **Status**: Working · **API key needed**: None (pure local computation)

---

## 30-second pitch

Nixtla customers ship a forecast. The CFO asks "why does it predict $1.4M next quarter?" This plugin answers. STL decomposition tells them how much of the level is trend (e.g., 0.78 strength) vs seasonality (0.42 strength) vs noise. Driver analysis tells them which exogenous variable (holiday flag, promo on, weather, whatever they tracked) most influenced the forecast and at what lag. Then it composes a one-page narrative the CFO can actually read.

---

## Quick start (under 5 minutes)

```bash
cd 005-plugins/nixtla-forecast-explainer
pip install -r scripts/requirements.txt

# In Claude Code:
# "Decompose this forecast: [your time-series data]"
# Claude calls decompose_forecast → identify_drivers → generate_narrative → generate_report
```

---

## What you get back

`decompose_forecast` returns a real STL output (uses `statsmodels.tsa.seasonal.STL` with `robust=True`):

```json
{
  "trend": [101.2, 101.7, 102.3, ...],
  "seasonal": [-3.4, 8.1, 0.2, ...],
  "residual": [0.8, -1.1, 0.5, ...],
  "strength_of_trend": 0.78,
  "strength_of_seasonality": 0.42,
  "period": 7,
  "n_obs": 60
}
```

Strength metrics follow Hyndman & Athanasopoulos (Forecasting: Principles and Practice, 3e, Ch 6.7): `1 - var(residual) / var(component + residual)`. Values in [0, 1].

`identify_drivers` returns drivers ranked by `|correlation|`:

```json
{
  "drivers": [
    {"name": "promo_active", "correlation": 0.91, "p_value": 0.0001, "lag_optimal": 0},
    {"name": "weather_temp", "correlation": -0.42, "p_value": 0.012, "lag_optimal": 2},
    {"name": "noise", "correlation": 0.05, "p_value": 0.78, "lag_optimal": 5}
  ],
  "n_candidates": 3,
  "max_lag": 7
}
```

Lag 0 = contemporaneous; lag k > 0 = predictor at time t-k aligns with target at t (predictor leads).

---

## MCP tools

| Tool | What it does |
|---|---|
| `decompose_forecast` | STL decomposition + Hyndman strength metrics |
| `identify_drivers` | Pearson correlation analysis with lag scanning |
| `generate_narrative` | Plain-English executive summary |
| `generate_report` | Compose markdown report from prior outputs |
| `assess_risk_factors` | Flag high-uncertainty periods |

---

## Inputs accepted

`decompose_forecast` and `identify_drivers` accept any of:

- List of dicts: `[{"ds": "2026-01-01", "y": 12.5}, ...]`
- Dict of arrays: `{"ds": [...], "y": [...]}`
- pandas DataFrame with `ds` + `y` columns
- Plain list of floats: `[12.5, 13.1, 11.9, ...]`
- pandas Series

When `ds` is parseable as datetime, it's used as the index (enables seasonal-period inference).

---

## Edge cases handled

- **Too few observations**: `decompose_forecast` requires ≥ 4 obs and ≥ 2 full seasonal cycles. Raises `ValueError` with a clear message.
- **No DatetimeIndex**: `_infer_period` falls back to `default=7` (weekly).
- **NaN values in candidates**: `identify_drivers` masks NaN and computes correlation only on aligned valid pairs.
- **Constant series**: skipped (zero variance can't produce correlation).
- **Negative `max_lag`**: raises `ValueError`.

---

## Tests

```bash
cd 005-plugins/nixtla-forecast-explainer
PYTHONPATH=scripts pytest tests/ --cov=explainer_mcp -v
```

33 tests across 7 classes covering input coercion, period inference, strength metric, STL decomposition with synthetic seasonality verification, driver identification with known-correlation fixtures, narrative + report generation, and async MCP dispatch.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: statsmodels` | `pip install -r scripts/requirements.txt` |
| `STL requires at least 4 observations` | Provide more data (or check your input format) |
| `STL requires at least 2 full seasonal cycles` | Either use a smaller `period` or provide more data |
| Drivers list is empty | All candidates had < 3 valid observations or zero variance — verify inputs |

---

## License

MIT — Jeremy Longshore.
