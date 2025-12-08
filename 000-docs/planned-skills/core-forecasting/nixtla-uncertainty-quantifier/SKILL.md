---
name: nixtla-uncertainty-quantifier
description: |
  Quantifies prediction uncertainty using conformal prediction.
  Use when risk assessment, scenario planning, or decision-making under uncertainty is required.
  Trigger with "quantify uncertainty", "generate prediction intervals", "confidence bands".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Uncertainty Quantifier

Generates prediction intervals and confidence bands for time series forecasts using conformal prediction.

## Purpose

Provides a measure of the uncertainty associated with time series forecasts, enabling more informed decision-making.

## Overview

Calculates prediction intervals and confidence bands around point forecasts, leveraging conformal prediction techniques. Requires a trained forecasting model (e.g., TimeGPT, StatsForecast) and historical data.  Use when point forecasts alone are insufficient and an understanding of forecast uncertainty is needed. Outputs CSV files containing the forecast with uncertainty bounds and visualizations.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**:
* Requires access to a trained forecasting model (e.g., TimeGPT API Key or StatsForecast model).
* `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT).

**Packages**:
```bash
pip install nixtla pandas statsforecast
```

## Instructions

### Step 1: Prepare data

Load historical data and generate point forecasts using TimeGPT or StatsForecast. Ensure the data includes `unique_id`, `ds` (timestamp), and `y` (target variable) columns.

### Step 2: Configure parameters

Set desired confidence level (e.g., 90% or 95%) and conformal prediction method (e.g., quantile regression, jackknife+).

### Step 3: Execute uncertainty quantification

Run: `python {baseDir}/scripts/uncertainty.py --input forecast.csv --confidence 0.90 --method quantile`

### Step 4: Generate output

Save forecast CSV with prediction intervals and create visualization plot.

## Output

- **forecast_with_uncertainty.csv**: Predictions with lower and upper bounds of the prediction interval.
- **uncertainty_plot.png**: Visualization of the forecast with confidence bands.
- **calibration_metrics.json**: Metrics evaluating the calibration of the prediction intervals.

## Error Handling

1. **Error**: `Input file not found`
   **Solution**: Verify the file path specified in the `--input` argument is correct.

2. **Error**: `Invalid confidence level`
   **Solution**:  Specify a confidence level between 0 and 1 (e.g., 0.95 for 95% confidence).

3. **Error**: `Unsupported conformal prediction method`
   **Solution**: Choose a valid conformal prediction method, such as 'quantile' or 'jackknife+'.

4. **Error**: `Forecast file does not contain required columns`
   **Solution**: Ensure the input CSV file contains `unique_id`, `ds`, and forecast columns (e.g., 'TimeGPT').

## Examples

### Example 1: Sales forecast with 90% confidence

**Input**: (forecast.csv)
```
unique_id,ds,TimeGPT
store_1,2024-01-01,100
store_1,2024-01-02,120
```

**Output**: (forecast_with_uncertainty.csv)
```
unique_id,ds,TimeGPT,lower_bound_90,upper_bound_90
store_1,2024-01-01,100,80,120
store_1,2024-01-02,120,100,140
```

### Example 2: Demand forecast with 95% confidence

**Input**: (forecast.csv)
```
unique_id,ds,TimeGPT
grid_1,2024-01-01 00:00,5000
grid_1,2024-01-01 01:00,5100
```

**Output**: (forecast_with_uncertainty.csv)
```
unique_id,ds,TimeGPT,lower_bound_95,upper_bound_95
grid_1,2024-01-01 00:00,5000,4800,5200
grid_1,2024-01-01 01:00,5100,4900,5300
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Docs: `{baseDir}/references/`