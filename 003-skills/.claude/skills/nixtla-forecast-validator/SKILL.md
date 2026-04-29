---
name: nixtla-forecast-validator
description: "Validate forecast quality by comparing MASE and sMAPE against configurable thresholds, detect model degradation across multiple series, and generate alert reports with visualizations. Use when detecting model degradation, auditing forecast accuracy, or comparing model performance over time. Trigger with 'validate forecast', 'check forecast quality', 'compare model metrics', 'detect degradation'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Nixtla Forecast Validator

Validates time series forecast quality metrics and detects performance degradation using statistical measures. Compares current forecast accuracy against historical benchmarks to identify significant deviations in MASE and sMAPE metrics.

## Prerequisites

- `pandas`, `matplotlib`
- No API keys required (operates on CSV metrics files)

## Instructions

### Step 1: Prepare metrics data

Ensure you have two CSV files containing forecast metrics:
- Historical metrics CSV (baseline performance)
- Current metrics CSV (recent performance to validate)

Each CSV must have columns: `model`, `MASE`, `sMAPE`

**Example format**:
```
model,MASE,sMAPE
model_A,1.2,0.15
model_B,0.8,0.10
```

### Step 2: Set validation thresholds

Configure acceptable deviation thresholds for MASE and sMAPE metrics. Default thresholds are 0.2 (20% increase), but these can be adjusted based on business requirements and model characteristics.

**Recommended thresholds**:
- Conservative: 0.1 (10% increase triggers alert)
- Standard: 0.2 (20% increase triggers alert)
- Lenient: 0.3 (30% increase triggers alert)

### Step 3: Execute validation

Run the validation script to compare current metrics against historical benchmarks:

```bash
python {baseDir}/scripts/validate_forecast.py \
  --historical historical_metrics.csv \
  --current current_metrics.csv \
  --mase_threshold 0.2 \
  --smape_threshold 0.2
```

The script performs:
1. Loads historical and current metrics from CSV files
2. Calculates percentage increase for each metric per model
3. Compares increases against configured thresholds
4. Generates validation report, comparison CSV, alert log, and visualization

### Step 4: Review validation outputs

Analyze the generated outputs to identify forecast quality issues:
- Read `validation_report.txt` for summary of findings
- Check `alert.log` for models requiring immediate attention
- Review `metrics_comparison.csv` for detailed metric changes
- Examine `metrics_visualization.png` for visual comparison

If `alert.log` contains warnings, either adjust thresholds for volatile series or investigate data quality and concept drift before re-running.

## Output

| File | Purpose |
|------|---------|
| `validation_report.txt` | Summary of which models show degradation |
| `metrics_comparison.csv` | Historical vs current metrics side-by-side |
| `alert.log` | Models exceeding thresholds |
| `metrics_visualization.png` | Bar chart comparing MASE/sMAPE |

## Examples

### Example 1: Significant MASE degradation detected

**Input** (historical_metrics.csv):
```
model,MASE,sMAPE
model_A,1.2,0.15
```

**Input** (current_metrics.csv):
```
model,MASE,sMAPE
model_A,1.8,0.18
```

**Command**:
```bash
python scripts/validate_forecast.py --historical historical_metrics.csv --current current_metrics.csv
```

**Output**: `WARNING: Significant increase in MASE detected for model model_A.` (50% increase exceeds 20% threshold)

### Example 2: Custom thresholds for volatile models

**Command**:
```bash
python scripts/validate_forecast.py \
  --historical multi_model_historical.csv \
  --current multi_model_current.csv \
  --mase_threshold 0.3 \
  --smape_threshold 0.25
```

Uses more lenient thresholds (30% for MASE, 25% for sMAPE) suitable for volatile forecasts or experimental models.

## Resources

**Script**: `{baseDir}/scripts/validate_forecast.py`

**Metrics**: MASE (Mean Absolute Scaled Error), sMAPE (symmetric Mean Absolute Percentage Error)

**Related skills**: `nixtla-timegpt-lab`, `nixtla-experiment-architect`, `nixtla-schema-mapper`
