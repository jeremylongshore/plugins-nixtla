---
name: nixtla-cross-validator
description: |
  Performs rigorous time series cross-validation using expanding and sliding windows.
  Use when needing to evaluate the performance of time series models on unseen data.
  Trigger with "cross validate time series", "evaluate forecasting model", "time series backtesting".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Cross-Validator Skill

Evaluates time series model performance using cross-validation.

## Purpose

To rigorously assess how well a time series model generalizes to unseen data by simulating future predictions.

## Overview

This skill automates time series cross-validation by splitting historical data into multiple training and validation sets based on expanding or sliding window techniques. It integrates with TimeGPT and StatsForecast to evaluate model performance across various time periods. It reports key accuracy metrics, helping users select the best model.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (if using TimeGPT)

**Packages**:
```bash
pip install nixtla pandas statsforecast
```

## Instructions

### Step 1: Prepare data

Read time series data from CSV file into a pandas DataFrame.

### Step 2: Configure cross-validation

Define parameters like window size, step size, and number of folds.

### Step 3: Execute cross-validation

Run: `python {baseDir}/scripts/cross_validate.py --input data.csv --model timegpt --window 30 --folds 3`

### Step 4: Analyze results

Calculate and output cross-validation metrics (e.g., MAE, RMSE).

## Output

- **cv_results.csv**: CSV file containing the cross-validation results for each fold.
- **metrics.json**: JSON file containing overall performance metrics across all folds.
- **plots/**: Directory containing plots comparing actual vs. predicted values for each fold (optional).

## Error Handling

1. **Error**: `Input file not found`
   **Solution**: Ensure the specified input CSV file exists at the given path.

2. **Error**: `Invalid model name`
   **Solution**: Use a supported model name: 'timegpt', 'arima', 'ets'.

3. **Error**: `Insufficient data for cross-validation`
   **Solution**: Increase the length of the input time series or reduce the window size.

4. **Error**: `Missing required parameter`
   **Solution**: Specify all required parameters: input, model, window, folds.

## Examples

### Example 1: Cross-validating TimeGPT on daily sales

**Input**:
```
unique_id,ds,y
store_1,2023-01-01,10
store_1,2023-01-02,12
store_1,2023-01-03,15
...
store_1,2023-12-31,20
```

**Output**:
```
cv_results.csv: (example)
fold,unique_id,ds,y,y_hat
1,store_1,2023-11-01,18,17.5
1,store_1,2023-11-02,20,19.2
...
```

### Example 2: Cross-validating ARIMA on monthly demand

**Input**:
```
unique_id,ds,y
product_1,2020-01-01,100
product_1,2020-02-01,110
...
product_1,2023-12-01,125
```

**Output**:
```
metrics.json:
{
 "MAE": 5.2,
 "RMSE": 7.1
}
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Documentation: `{baseDir}/references/`
