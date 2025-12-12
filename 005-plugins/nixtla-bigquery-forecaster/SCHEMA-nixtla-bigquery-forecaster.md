# Schema: nixtla-bigquery-forecaster

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Partial Production (Live)

---

## Directory Tree

```
nixtla-bigquery-forecaster/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── 000-docs/
│   ├── 001-DR-REFR-google-timeseries-insights-api.md  # Google API reference
│   ├── 002-DR-QREF-max-quick-start-guide.md           # Quick start guide
│   └── 003-AT-ARCH-plugin-architecture.md             # Architecture docs
├── commands/
│   └── nixtla-full-workflow.md    # Slash command: End-to-end workflow
├── scripts/
│   ├── extract_sample.py          # Extract sample data from BigQuery
│   ├── full_workflow.py           # Complete workflow runner
│   └── test_local.py              # Local testing utility
├── src/
│   ├── __init__.py                # Package init
│   ├── bigquery_connector.py      # BigQuery connection/query logic
│   ├── forecaster.py              # Forecast orchestration
│   └── main.py                    # Cloud Function entry point
├── nixtla_workflow_output/
│   ├── baseline_results/          # Test run outputs
│   ├── sample.csv                 # Sample data
│   ├── winning_model_config.json  # Best model config
│   └── workflow_results.json      # Workflow execution results
├── requirements.txt               # Python dependencies
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-bigquery-forecaster | Required |
| description | Run Nixtla statsforecast models on BigQuery... | Required |
| version | 0.1.0 | Required |
| author.name | Jeremy Longshore | Required |
| homepage | https://github.com/intent-solutions-io/plugins-nixtla | Optional |
| repository | https://github.com/intent-solutions-io/plugins-nixtla | Optional |
| license | MIT | Optional |

---

## Slash Commands (1)

| Command | Purpose |
|---------|---------|
| /nixtla-full-workflow | End-to-end BigQuery to forecast workflow |

---

## Source Modules (4)

| Module | Purpose |
|--------|---------|
| src/main.py | Cloud Function HTTP entry point |
| src/bigquery_connector.py | BigQuery connection and query execution |
| src/forecaster.py | Forecast model orchestration |
| scripts/full_workflow.py | Complete workflow runner script |

---

## Key Files

| File | Lines | Purpose |
|------|-------|---------|
| src/main.py | ~100 | Cloud Function Gen2 entry point |
| src/bigquery_connector.py | ~200 | BigQuery connector with retry logic |
| src/forecaster.py | ~150 | StatsForecast model wrapper |
| scripts/full_workflow.py | ~300 | End-to-end workflow orchestration |

---

## Deployment Target

- **Platform:** Google Cloud Functions (Gen2)
- **Runtime:** Python 3.12
- **Trigger:** HTTP
- **Output:** JSON response with forecasts

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Data engineers, Google Cloud users
- **What:** Query BigQuery datasets, run statsforecast models, return forecasts as JSON
- **When:** BigQuery pipeline integration, serverless forecast generation
- **Target Goal:** Process 1000 rows in < 10 seconds; deploy via CI/CD
- **Production:** partial
