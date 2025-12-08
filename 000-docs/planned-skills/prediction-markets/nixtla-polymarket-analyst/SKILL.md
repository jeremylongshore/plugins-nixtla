---
name: nixtla-polymarket-analyst
description: |
  Analyzes Polymarket contracts and forecasts price movements.
  Use when needing to understand market sentiment and predict contract outcomes.
  Trigger with "Polymarket analysis", "predict contract odds", "forecast Polymarket".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebFetch"
version: "1.0.0"
---

# Polymarket Analyst

Analyzes and forecasts Polymarket contract prices using historical data.

## Overview

Fetches Polymarket contract data, transforms it into a time series, and generates forecasts.
Provides insights into potential contract outcomes and market trends.  This skill is useful for traders and analysts
who want to gain an edge in Polymarket prediction markets.  It utilizes the Polymarket API and TimeGPT for analysis. Output includes price forecasts and visualizations.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas requests
```

## Instructions

### Step 1: Fetch contract data

Fetch historical price data from Polymarket API for a given contract ID.

### Step 2: Transform to time series

Convert fetched data into a time series format (ds, y).

### Step 3: Forecast prices

Run: `python {baseDir}/scripts/polymarket_forecast.py --contract_id <contract_id> --horizon 14`

### Step 4: Generate output

Save forecast CSV and create visualization plot.

## Output

- **forecast.csv**: Predictions with confidence intervals for the contract price.
- **plot.png**: Actual vs predicted visualization of the contract price.
- **metadata.json**: Metadata about the contract.

## Error Handling

1. **Error**: `Invalid contract ID`
   **Solution**: Provide a valid Polymarket contract ID.

2. **Error**: `API request failed`
   **Solution**: Check your internet connection and API key, retry after a brief delay.

3. **Error**: `Insufficient data`
   **Solution**: The contract may be new and lack historical data for forecasting.

4. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

## Examples

### Example 1: Predict ETH price

**Input**:
```
Contract ID: 0xabc123
```

**Output**:
```
forecast.csv: Predictions for ETH contract price
plot.png: Visualization of ETH contract price forecast
```

### Example 2: Predict US election outcome

**Input**:
```
Contract ID: 0xdef456
```

**Output**:
```
forecast.csv: Predictions for US election outcome contract
plot.png: Visualization of election outcome contract forecast
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Docs: `{baseDir}/references/`