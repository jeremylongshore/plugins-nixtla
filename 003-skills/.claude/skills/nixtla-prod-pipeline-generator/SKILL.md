---
name: nixtla-prod-pipeline-generator
description: "Transform forecasting experiments into production Airflow DAGs, Prefect flows, or cron scripts with scheduling, drift-detection alerts, and retry monitoring. Use when deploying forecasts to production or automating inference pipelines. Trigger with 'generate pipeline', 'create Airflow DAG', 'deploy forecast', 'production pipeline'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Production Pipeline Generator

Transform validated forecasting experiments into production-ready inference pipelines with proper orchestration, monitoring, and error handling.

## Prerequisites

**Required**:
- Python 3.8+
- Completed experiment in `forecasting/config.yml`
- One of: Airflow, Prefect, or cron access

**Environment Variables**:
- `NIXTLA_API_KEY`: TimeGPT API key (if using TimeGPT)
- `FORECAST_DATA_SOURCE`: Production data connection string
- `FORECAST_DESTINATION`: Output destination for forecasts

**Installation**:
```bash
pip install nixtla pandas statsforecast  # Core
pip install apache-airflow  # For Airflow
pip install prefect  # For Prefect
```

## Instructions

### Step 1: Read Experiment Config

Load experiment from `forecasting/config.yml`:
```bash
python {baseDir}/scripts/read_experiment.py --config forecasting/config.yml
```

### Step 2: Generate and validate pipeline

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform airflow \
    --output pipelines/
```

Platforms: `airflow` (enterprise), `prefect` (Python-native, better local testing), `cron` (simple single-machine).

Verify the generated pipeline before deploying:
```bash
python pipelines/forecast_dag.py --dry-run
```

### Step 3: Add Monitoring

```bash
python {baseDir}/scripts/add_monitoring.py \
    --pipeline pipelines/forecast_dag.py \
    --metrics smape,mase
```

### Step 4: Deploy

Follow generated `pipelines/README.md` for deployment instructions.

## Output

- **pipelines/forecast_dag.py**: Main pipeline file (Airflow/Prefect/Cron)
- **pipelines/monitoring.py**: Quality checks and fallback logic
- **pipelines/README.md**: Deployment instructions
- **pipelines/requirements.txt**: Dependencies

## Examples

### Example 1: Airflow DAG

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform airflow \
    --schedule "0 6 * * *" \
    --output pipelines/
```

**Output**:
```
Generated: pipelines/forecast_dag.py
Schedule: Daily at 6am
Tasks: extract -> transform -> forecast -> load -> monitor
```

### Example 2: Simple Cron Script

```bash
python {baseDir}/scripts/generate_pipeline.py \
    --config forecasting/config.yml \
    --platform cron \
    --output pipelines/
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/assets/templates/`
- Nixtla Docs: https://nixtla.github.io/

**Related Skills**:
- `nixtla-experiment-architect`: Creates experiments to productionize
- `nixtla-timegpt-finetune-lab`: Fine-tuned models for pipelines
- `nixtla-usage-optimizer`: Cost-effective routing strategies
