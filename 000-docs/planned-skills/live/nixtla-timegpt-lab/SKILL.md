---
name: nixtla-timegpt-lab
description: |
  Provides expert time series forecasting capabilities by leveraging TimeGPT, StatsForecast, and MLForecast.
  Use when forecasting time series data, analyzing past trends, or generating predictions.
  Trigger with "time series forecast", "predict future values", "analyze time trends".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla TimeGPT Lab

Provides accurate time series forecasting using TimeGPT, StatsForecast, and MLForecast.

## Purpose

To generate forecasts from historical time series data.

## Overview

This skill allows users to perform time series forecasting using the Nixtla ecosystem. It encompasses data handling, model training/inference (TimeGPT/StatsForecast/MLForecast), and result visualization. Use it when predictions are required for various time series data. The Skill outputs forecasts in CSV format, along with visualizations, and key metrics.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT)

**Packages**:
```bash
pip install nixtla pandas statsforecast mlforecast
```

## Instructions

### Step 1: Load and prepare data

Read input CSV and ensure correct format (unique_id, ds, y). Handle missing values.

### Step 2: Select model and parameters

Choose forecasting model (TimeGPT, StatsForecast, MLForecast) and set parameters like horizon, frequency.

### Step 3: Execute forecasting

Run: `python {baseDir}/scripts/forecast_timegpt.py --input data.csv --model timegpt --horizon 14` (or use statsforecast/mlforecast)

### Step 4: Generate output

Save forecast CSV, visualization plot, and metrics.

## Output

- **forecast.csv**: Predictions with confidence intervals
- **plot.png**: Actual vs predicted visualization
- **metrics.json**: Accuracy metrics (e.g., MAE, RMSE)

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `Invalid input format`
   **Solution**: Ensure CSV has columns named 'unique_id', 'ds', and 'y'.

3. **Error**: `Unsupported frequency`
   **Solution**:  Specify frequency using --freq parameter (e.g., 'D', 'W', 'M', 'H').

4. **Error**: `Model training failed`
   **Solution**:  Check input data for errors, try different model parameters or a different model.

## Examples

### Example 1: Predicting daily sales

**Input**:
```
unique_id,ds,y
store_1,2024-01-01,100
store_1,2024-01-02,120
```

**Output**:
```
unique_id,ds,TimeGPT
store_1,2024-01-03,130
```

### Example 2: Forecasting hourly demand

**Input**:
```
unique_id,ds,y
grid_1,2024-01-01 00:00,5000
```

**Output**:
```
unique_id,ds,TimeGPT
grid_1,2024-01-01 01:00,5100
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Docs: `{baseDir}/references/`