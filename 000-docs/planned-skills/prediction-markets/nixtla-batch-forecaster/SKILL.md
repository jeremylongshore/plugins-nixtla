---
name: nixtla-batch-forecaster
description: |
  Forecasts multiple time series in parallel batches using the TimeGPT API.
  Use when processing 10-100 contracts, performing portfolio aggregation, or needing efficient forecasting of large datasets.
  Trigger with "batch forecast", "portfolio forecast", "parallel forecasting".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Batch Forecaster

Processes multiple time series forecasts in parallel, optimizing throughput.

## Purpose

To generate forecasts for a batch of time series efficiently, handling portfolio aggregation where necessary.

## Overview

This skill leverages the TimeGPT API to produce forecasts for multiple time series concurrently. It optimizes performance by processing contracts in parallel batches.  Use when you need to forecast a large number of time series, like a portfolio of contracts.  It supports portfolio aggregation to generate forecasts at a higher level.  The skill outputs individual forecast files and optionally an aggregated forecast.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

## Instructions

### Step 1: Prepare input data

Read input CSV containing multiple time series with columns (unique_id, ds, y).

### Step 2: Configure parameters

Set the forecast horizon and batch size.  Specify portfolio aggregation settings if applicable.

### Step 3: Execute batch forecast

Run: `python {baseDir}/scripts/batch_forecast.py --input data.csv --horizon 30 --batch_size 20`

### Step 4: Generate output

Save individual forecast CSVs and the aggregated forecast CSV (if aggregation is enabled).

## Output

- **forecasts/{unique_id}.csv**: Individual forecasts for each time series
- **aggregated_forecast.csv**: Aggregated forecast (if enabled)
- **summary.json**: Summary of the batch forecasting process

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `Input file not found`
   **Solution**: Verify the file path provided using --input.

3. **Error**: `API Rate Limit Exceeded`
   **Solution**: Reduce the batch size or implement retry logic.

4. **Error**: `Invalid data format in input CSV`
   **Solution**: Ensure the CSV contains 'unique_id', 'ds', and 'y' columns.

## Examples

### Example 1: Forecasting 20 contracts daily

**Input**: `contracts.csv` (contains 20 contracts with daily data)

**Command**: `python {baseDir}/scripts/batch_forecast.py --input contracts.csv --horizon 14 --freq D --batch_size 10`

**Output**: 20 individual forecast files in `forecasts/` directory.

### Example 2: Portfolio aggregation of hourly data

**Input**: `energy_grids.csv` (contains hourly demand for 50 energy grids)

**Command**: `python {baseDir}/scripts/batch_forecast.py --input energy_grids.csv --horizon 24 --freq H --batch_size 25 --aggregate True`

**Output**: 50 individual forecast files in `forecasts/` directory and an `aggregated_forecast.csv`.

## Resources

- Scripts: `{baseDir}/scripts/`
- Docs: `{baseDir}/references/`