# Baseline Lab - Technical Specification

**Plugin:** nixtla-baseline-lab
**Version:** 0.8.0
**Last Updated:** 2025-12-12

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Runtime | Python | 3.10+ |
| Forecasting | statsforecast | >=1.5.0 |
| Data | pandas | >=2.0.0 |
| Numeric | numpy | >=1.24.0 |
| Plotting | matplotlib | >=3.7.0 |
| M4 Data | datasetsforecast | >=0.0.8 |
| TimeGPT (optional) | nixtla | >=0.5.0 |

---

## API Reference

### MCP Tool: `run_baselines`

**Purpose:** Execute forecasting models on data

**Parameters:**
```python
{
    "data_path": str,      # Path to CSV or M4 preset
    "horizon": int,        # Forecast horizon (default: 7)
    "models": list,        # Models to run (default: all)
    "limit": int           # Max series (default: None)
}
```

**Returns:**
```python
{
    "status": "success",
    "results_path": str,   # Path to metrics CSV
    "summary": dict        # Aggregated metrics
}
```

### MCP Tool: `get_nixtla_compatibility_info`

**Purpose:** Check installed library versions

**Returns:**
```python
{
    "statsforecast": "1.7.0",
    "nixtla": "0.5.1",
    "pandas": "2.0.3",
    "python": "3.10.12"
}
```

### MCP Tool: `generate_benchmark_report`

**Purpose:** Create markdown report from results

**Parameters:**
```python
{
    "results_path": str,   # Path to metrics CSV
    "title": str           # Report title
}
```

**Returns:** Markdown string

### MCP Tool: `generate_github_issue_draft`

**Purpose:** Generate GitHub issue template

**Parameters:**
```python
{
    "title": str,
    "metrics": dict,
    "context": str
}
```

**Returns:** Markdown issue template

---

## Configuration

### Environment Variables

```bash
# Optional - only needed for TimeGPT comparison
NIXTLA_TIMEGPT_API_KEY=your-api-key
```

### Model Presets

| Preset | Series | Horizon | Description |
|--------|--------|---------|-------------|
| `m4_daily_small` | 5 | 7 | Quick validation |
| `m4_daily_full` | 4,227 | 14 | Full M4 Daily |
| `m4_hourly_small` | 5 | 24 | Hourly quick test |
| `m4_monthly_small` | 5 | 6 | Monthly quick test |

---

## File Structure

```
005-plugins/nixtla-baseline-lab/
├── README.md                         # Overview
├── QUICKSTART.md                     # 4-line setup
├── agents/
│   └── nixtla-baseline-analyst.md    # AI agent definition
├── commands/
│   ├── nixtla-baseline-m4.md         # Slash command
│   └── nixtla-baseline-setup.md      # Setup command
├── data/
│   └── m4/
│       ├── M4-Daily.csv
│       ├── M4-Hourly.csv
│       ├── M4-Monthly.csv
│       └── M4-Weekly.csv
├── scripts/
│   ├── nixtla_baseline_mcp.py        # MCP server (4 tools)
│   ├── timegpt_client.py             # TimeGPT wrapper
│   ├── requirements.txt              # Dependencies
│   └── setup_nixtla_env.sh           # Setup script
├── skills/
│   └── nixtla-baseline-review/
│       ├── SKILL.md
│       └── resources/
│           ├── METRIC_INTERPRETATION.md
│           ├── GITHUB_ISSUES.md
│           └── TIMEGPT_COMPARISON.md
└── tests/
    ├── run_baseline_m4_smoke.py      # Golden task test
    ├── golden_tasks/                 # Task definitions
    ├── csv_test/                     # Custom CSV tests
    ├── custom/                       # User scenarios
    ├── m4_test/                      # M4 test outputs
    └── data/                         # Test fixtures
```

---

## Testing

### Smoke Test

```bash
python tests/run_baseline_m4_smoke.py
```

**Pass Criteria:**
- Exit code 0
- "GOLDEN TASK PASSED" in output
- Results CSV generated
- sMAPE < 5% for AutoETS

### CI/CD

Workflow: `.github/workflows/nixtla-baseline-lab-ci.yml`

- Runs on push to `005-plugins/nixtla-baseline-lab/**`
- Python 3.10, 3.11, 3.12 matrix
- Installs dependencies from requirements.txt
- Executes smoke test

---

## Metrics Specification

### sMAPE (Symmetric Mean Absolute Percentage Error)

```
sMAPE = (2/n) * Σ |Actual - Forecast| / (|Actual| + |Forecast|) * 100
```

- Range: 0% to 200%
- Lower is better
- < 2%: Excellent
- 2-5%: Good
- > 10%: Poor

### MASE (Mean Absolute Scaled Error)

```
MASE = MAE / MAE_naive
```

- < 1.0: Beats naive baseline
- = 1.0: Same as naive
- > 1.0: Worse than naive

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Import error | Missing deps | `pip install -r requirements.txt` |
| Memory error | Too many series | Use `limit` parameter |
| Slow execution | Large dataset | Start with `_small` presets |
| MASE = inf | Zero naive error | Check data for constant series |
