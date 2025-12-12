# Schema: nixtla-vs-statsforecast-benchmark

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Planned (Business Growth)

---

## Directory Tree (Planned)

```
nixtla-vs-statsforecast-benchmark/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   └── nixtla-benchmark.md        # Slash command: Run benchmark
├── scripts/
│   ├── benchmark_mcp.py           # MCP server (4 tools exposed)
│   ├── statsforecast_runner.py    # Local SF model runner
│   ├── timegpt_runner.py          # API-based TG runner
│   ├── metrics_calculator.py      # sMAPE, MASE, RMSE
│   ├── report_generator.py        # HTML/Markdown reports
│   └── requirements.txt           # Python dependencies
├── templates/
│   ├── benchmark_report.html      # HTML report template
│   └── comparison_chart.py        # Plotly chart generator
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (Planned plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-vs-statsforecast-benchmark | Required |
| description | Automated benchmarking: TimeGPT vs StatsForecast... | Required |
| version | 0.1.0 | Required |
| author.name | Intent Solutions | Required |

---

## MCP Tools (4 planned)

| Tool Name | Purpose |
|-----------|---------|
| run_benchmark | Execute benchmark comparison |
| get_metrics | Retrieve accuracy metrics |
| generate_report | Create HTML/Markdown report |
| recommend_model | Get data-driven recommendation |

---

## Slash Commands (1 planned)

| Command | Purpose |
|---------|---------|
| /nixtla-benchmark | Run side-by-side comparison |

---

## Metrics Calculated

| Metric | Description |
|--------|-------------|
| sMAPE | Symmetric Mean Absolute Percentage Error |
| MASE | Mean Absolute Scaled Error |
| RMSE | Root Mean Squared Error |
| Coverage | Prediction interval accuracy |
| Execution Time | Speed comparison |

---

## Models Compared

| Source | Models |
|--------|--------|
| StatsForecast | AutoARIMA, AutoETS, AutoTheta, SeasonalNaive |
| TimeGPT | Default parameters (API) |

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Benchmark 1K series | <5 minutes |
| Report generation | <30 seconds |
| Cost warning threshold | Configurable |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** ML practitioners, researchers
- **What:** Benchmarking tool comparing TimeGPT vs StatsForecast
- **When:** Model selection, performance comparison
- **Target Goal:** Generate benchmark report comparing 3+ models
- **Production:** false (planned-business-growth)
