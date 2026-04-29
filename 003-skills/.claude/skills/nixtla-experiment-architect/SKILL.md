---
name: nixtla-experiment-architect
description: "Generate production-ready forecasting experiments that create train/test splits, run cross-validation pipelines, and produce accuracy comparison tables using StatsForecast, MLForecast, and TimeGPT. Use when setting up model benchmarking or cross-validation. Trigger with 'scaffold experiment', 'compare models', 'benchmark forecasts', 'cross-validate'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Experiment Architect

Design and scaffold complete forecasting experiments using Nixtla's libraries.

## Prerequisites

**Required**:
- Python 3.8+
- `statsforecast`, `utilsforecast`

**Optional**:
- `mlforecast`: For ML models
- `nixtla`: For TimeGPT
- `NIXTLA_API_KEY`: TimeGPT access

**Installation**:
```bash
pip install statsforecast mlforecast nixtla utilsforecast pyyaml
```

## Instructions

### Step 1: Gather Requirements

Collect experiment parameters:
- Data source path
- Target column name
- Forecast horizon (e.g., 14 days)
- Frequency (D, H, W, M)
- Unique ID column (optional)

### Step 2: Generate Configuration

```bash
python {baseDir}/scripts/generate_config.py \
    --data data/sales.csv \
    --target sales \
    --horizon 14 \
    --freq D \
    --output forecasting/config.yml
```

### Step 3: Scaffold and validate experiment

```bash
python {baseDir}/scripts/scaffold_experiment.py \
    --config forecasting/config.yml \
    --output forecasting/experiments.py
```

Verify the generated harness imports correctly before running:
```bash
python -c "import ast; ast.parse(open('forecasting/experiments.py').read()); print('OK')"
```

### Step 4: Run Experiment

```bash
python forecasting/experiments.py
```

### Step 5: Review Results

```bash
cat forecasting/results/metrics_summary.csv
```

## Output

- **forecasting/config.yml**: Experiment configuration
- **forecasting/experiments.py**: Runnable experiment harness
- **forecasting/results/**: Metrics and forecasts (after running)

## Examples

### Example 1: Daily Sales Forecast

```bash
python {baseDir}/scripts/generate_config.py \
    --data data/sales.csv \
    --target revenue \
    --horizon 30 \
    --freq D \
    --id_col store_id
```

**Output config.yml**:
```yaml
data:
  source: data/sales.csv
  target: revenue
  unique_id: store_id
forecasting:
  horizon: 30
  freq: D
models:
  - SeasonalNaive
  - AutoETS
  - AutoARIMA
```

### Example 2: Hourly Energy Forecast

```bash
python {baseDir}/scripts/generate_config.py \
    --data data/energy.csv \
    --target consumption \
    --horizon 24 \
    --freq H
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/assets/templates/`
- Nixtla Docs: https://nixtla.github.io/

**Related Skills**:
- `nixtla-timegpt-lab`: Core forecasting guidance
- `nixtla-schema-mapper`: Data transformation
- `nixtla-prod-pipeline-generator`: Production deployment
