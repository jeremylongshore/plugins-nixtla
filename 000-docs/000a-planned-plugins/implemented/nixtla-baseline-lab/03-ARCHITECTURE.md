# Baseline Lab - Architecture

**Plugin:** nixtla-baseline-lab
**Version:** 0.8.0
**Last Updated:** 2025-12-12

---

## System Context

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Claude Code   │────▶│  MCP Server      │────▶│  StatsForecast  │
│   (Client)      │     │  (4 tools)       │     │  (Models)       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  M4 Data Files   │
                        │  (CSV)           │
                        └──────────────────┘
```

---

## Component Design

### MCP Server (`scripts/nixtla_baseline_mcp.py`)

Exposes 4 tools to Claude Code:

| Tool | Purpose | Inputs | Outputs |
|------|---------|--------|---------|
| `run_baselines` | Execute models on data | CSV path, horizon | Metrics CSV |
| `get_nixtla_compatibility_info` | Check library versions | None | Version dict |
| `generate_benchmark_report` | Create markdown report | Metrics CSV | Markdown |
| `generate_github_issue_draft` | Generate issue template | Metrics, context | Markdown |

### Data Layer

M4 competition data stored locally:

```
data/m4/
├── M4-Daily.csv     # 4,227 series
├── M4-Hourly.csv    # 414 series
├── M4-Monthly.csv   # 48,000 series
└── M4-Weekly.csv    # 359 series
```

### Model Layer

Uses Nixtla's open-source statsforecast:

```python
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

sf = StatsForecast(
    models=[AutoETS(), AutoTheta(), SeasonalNaive(season_length=7)],
    freq='D'
)
forecasts = sf.forecast(df=df_train, h=horizon)
```

---

## Data Flow

1. **Input**: Claude Code invokes `run_baselines` with data path and horizon
2. **Load**: MCP server loads M4 or custom CSV data
3. **Split**: Data split into train/test based on horizon
4. **Forecast**: StatsForecast runs AutoETS, AutoTheta, SeasonalNaive
5. **Evaluate**: sMAPE and MASE calculated against test set
6. **Output**: Results CSV and summary returned to Claude Code

---

## File Structure

```
005-plugins/nixtla-baseline-lab/
├── README.md
├── QUICKSTART.md
├── agents/
│   └── nixtla-baseline-analyst.md
├── commands/
│   ├── nixtla-baseline-m4.md
│   └── nixtla-baseline-setup.md
├── data/m4/
├── scripts/
│   ├── nixtla_baseline_mcp.py    # MCP server
│   ├── timegpt_client.py         # Optional TimeGPT
│   ├── requirements.txt
│   └── setup_nixtla_env.sh
├── skills/
│   └── nixtla-baseline-review/
└── tests/
    ├── run_baseline_m4_smoke.py  # Golden task
    ├── golden_tasks/
    └── m4_test/
```

---

## Dependencies

```
statsforecast>=1.5.0
datasetsforecast>=0.0.8
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
nixtla>=0.5.0  # Optional
```

---

## Technical Constraints

- **Python 3.10+**: Required for statsforecast compatibility
- **Memory**: ~2GB RAM for full M4 Daily dataset
- **No API Keys**: Fully offline operation with statsforecast
- **Local Execution**: Not designed for cloud deployment
