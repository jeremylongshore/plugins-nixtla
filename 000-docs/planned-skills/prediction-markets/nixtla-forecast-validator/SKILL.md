---
name: nixtla-forecast-validator
description: |
  Validates the quality of time series forecast metrics.
  Use when evaluating forecast accuracy, detecting performance degradation, or comparing different models.
  Trigger with "validate forecast", "check forecast quality", "assess forecast metrics".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla Forecast Validator

Validates time series forecast quality metrics and detects degradation using Nixtla's TimeGPT API and standard statistical measures.

## Purpose

Evaluates the accuracy and reliability of time series forecasts by comparing current performance against historical benchmarks.

## Overview

Analyzes forecast quality metrics such as MASE (Mean Absolute Scaled Error) and sMAPE (symmetric Mean Absolute Percentage Error). Detects significant deviations from expected performance, indicating potential model degradation or data anomalies. Outputs a report highlighting any detected issues and suggesting possible corrective actions. Use when you need automated monitoring of forecast accuracy or comparison of different forecast models.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install pandas
```

## Instructions

### Step 1: Load data

Read historical and current forecast metrics data (MASE, sMAPE) from CSV files.

### Step 2: Configure validation parameters

Set thresholds for acceptable metric deviation and the historical baseline period.

### Step 3: Execute validation script

Run: `python {baseDir}/scripts/validate_forecast.py --historical historical_metrics.csv --current current_metrics.csv`

### Step 4: Generate report

Analyze the validation results and create a report highlighting any detected degradation.

## Output

- **validation_report.txt**: Textual report summarizing the validation results.
- **metrics_comparison.csv**: CSV file containing a comparison of historical and current metrics.
- **alert.log**: Log file containing alerts if significant degradation is detected.

## Error Handling

1. **Error**: `Missing required metrics column (MASE or sMAPE)`
   **Solution**: Ensure input CSV files contain columns 'MASE' and 'sMAPE'.

2. **Error**: `Invalid threshold value`
   **Solution**: Provide a valid numerical threshold value for metric deviation.

3. **Error**: `Historical data unavailable`
   **Solution**: Ensure a valid historical metrics CSV file is provided.

4. **Error**: `API Key not found`
   **Solution**: Set the `NIXTLA_TIMEGPT_API_KEY` environment variable.

## Examples

### Example 1: Increased MASE

**Input (historical_metrics.csv)**:
```
model,MASE,sMAPE
model_A,1.2,0.15
```

**Input (current_metrics.csv)**:
```
model,MASE,sMAPE
model_A,1.8,0.18
```

**Output (validation_report.txt)**:
```
WARNING: Significant increase in MASE detected for model_A.
```

### Example 2: Stable performance

**Input (historical_metrics.csv)**:
```
model,MASE,sMAPE
model_B,0.8,0.10
```

**Input (current_metrics.csv)**:
```
model,MASE,sMAPE
model_B,0.85,0.11
```

**Output (validation_report.txt)**:
```
Forecast validation passed. No significant degradation detected.
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Documentation: `{baseDir}/docs/validation.pdf`
