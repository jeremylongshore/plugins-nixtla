# Nixtla Migration Assistant

Real migration assistant for moving production forecasting code from Prophet / statsmodels / sklearn to Nixtla TimeGPT or StatsForecast. AST-based code analysis, pandas-based data transformation, multi-template code generation, real side-by-side accuracy comparison, and a phased migration plan with concrete tasks + validation criteria + rollback per phase.

**Version**: 1.0.0 · **Status**: Working · **API key needed**: Optional (only `compare_accuracy` against TimeGPT needs `NIXTLA_API_KEY`)

---

## 30-second pitch

Most Nixtla migration projects stall at "we have 47 Prophet scripts; do we rewrite them all?" This plugin reads each script (real AST parsing), tells you exactly what to migrate to and why, generates the replacement code from a real template, and benchmarks the new code against the old on the same data so you can show your director the sMAPE delta before committing.

---

## Quick start

```bash
cd 005-plugins/nixtla-migration-assistant
pip install -r scripts/requirements.txt

# In Claude Code:
# 1. "Analyze this Prophet script: /path/to/prophet_model.py"
# 2. "Generate a migration plan from that analysis."
# 3. "Transform sales.csv to Nixtla format (timestamp_col=date, value_col=sales, group_col=store)."
# 4. "Generate the equivalent Nixtla code for prophet → statsforecast."
# 5. "Compare accuracy on sales.csv: prophet vs statsforecast, horizon=14."
```

---

## MCP tools

| Tool | What it does |
|---|---|
| `analyze_code` | AST detection of Prophet, statsmodels (ARIMA / ExponentialSmoothing / statespace), sklearn |
| `transform_data` | pandas reshape: source CSV → canonical `unique_id, ds, y` with NaN strategy + datetime coercion |
| `generate_code` | Template-driven code generation across 5 source/target combos |
| `generate_plan` | 4-phase migration plan: setup + pilot + full + decommission, with hours scaled to complexity |
| `compare_accuracy` | Real prophet/statsmodels vs real statsforecast/TimeGPT on same train/test, sMAPE + MAE + winner verdict |

---

## Supported source → target combinations

`generate_code` produces real, runnable Python for these combos:

| Source library | → | Target |
|---|---|---|
| `prophet` | → | `timegpt` |
| `prophet` | → | `statsforecast` |
| `statsmodels.arima` | → | `statsforecast` (AutoARIMA) |
| `statsmodels.ets` | → | `statsforecast` (AutoETS) |
| `sklearn` | → | `statsforecast` (AutoETS + AutoTheta) |

Unknown combos return a structured error with the available list — no template gets fabricated.

---

## What `compare_accuracy` does

Takes a CSV + horizon. Splits the last `horizon` rows as test. Runs:

- **Source engine** (`prophet` or `statsmodels` ARIMA): real `.fit()` + `.forecast(steps=horizon)`. Reports sMAPE + MAE.
- **Target engine** (`statsforecast` AutoETS or `timegpt`): real model fit + forecast. Reports sMAPE + MAE.

Returns:

```json
{
  "status": "success",
  "source": {"engine": "prophet", "smape": 9.2, "mae": 4.1},
  "target": {"engine": "statsforecast", "smape": 7.8, "mae": 3.5},
  "improvement": {"smape_pct": 15.2, "winner": "statsforecast"},
  "recommendation": "MIGRATE — meaningful accuracy improvement",
  "horizon": 14,
  "n_train": 86,
  "n_test": 14
}
```

If `prophet` / `statsmodels` / `nixtla` is not installed, that engine reports an `error` field instead of crashing — the function still returns a partial result.

---

## Migration plan phases (from `generate_plan`)

Hours scale to detected complexity:

| Complexity | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Total |
|---|---|---|---|---|---|
| low | 1 | 2 | 2 | 1 | 6 hrs |
| medium | 2 | 4 | 6 | 2 | 14 hrs |
| high | 4 | 8 | 16 | 4 | 32 hrs |

Each phase comes with: concrete tasks (3-7 each), validation criteria, and an explicit rollback plan. No wishful "Phase 1 - Code Analysis - status: complete" placeholders.

---

## Tests

```bash
cd 005-plugins/nixtla-migration-assistant
PYTHONPATH=scripts pytest tests/ --cov=migration_mcp -v
```

31 tests covering AST detection of all 4 source libraries, code transformation with synthetic CSVs (multi-series, NaN handling, missing columns), code generation across all 5 source/target combos, plan generation phase scaling + risk levels, and graceful handling of missing optional deps in compare_accuracy.

---

## License

MIT — Jeremy Longshore.
