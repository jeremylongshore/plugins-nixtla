---
name: nixtla-liquidity-forecaster
description: |
  Forecasts orderbook depth and spreads to optimize trade execution timing.
  Use when needing to estimate market liquidity for large orders.
  Trigger with "forecast liquidity", "predict orderbook", "estimate depth".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebFetch"
version: "1.0.0"
---

# Liquidity Forecaster

Predicts future orderbook depth and bid-ask spreads using historical market data and TimeGPT.

## Overview

Analyzes historical trade data and orderbook snapshots from Polymarket to forecast liquidity conditions. Predicts near-term changes in orderbook depth and bid-ask spreads. Use when determining optimal trade execution timing based on expected liquidity. Generates CSV files with predicted depth and spread values.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas requests
```

## Instructions

### Step 1: Fetch data

Fetch historical orderbook data from the Polymarket API.

### Step 2: Preprocess data

Clean and format the orderbook data for TimeGPT input.

### Step 3: Execute forecast

Run: `python {baseDir}/scripts/liquidity_forecast.py --market_id polymarket_market_id --horizon 12`

### Step 4: Generate output

Save forecast CSV with predicted depth and spread.

## Output

- **depth_forecast.csv**: Predictions for orderbook depth.
- **spread_forecast.csv**: Predictions for bid-ask spread.
- **report.txt**: Summary of the forecasting process.

## Error Handling

1. **Error**: `Invalid Polymarket Market ID`
   **Solution**: Verify the Market ID with the Polymarket API.

2. **Error**: `TimeGPT API Key missing`
   **Solution**: Set the `NIXTLA_TIMEGPT_API_KEY` environment variable.

3. **Error**: `Insufficient data from Polymarket API`
   **Solution**: Check data availability for the specified Market ID and time range.

4. **Error**: `TimeGPT forecast failed`
   **Solution**: Check the TimeGPT API status and input data format.

## Examples

### Example 1: Forecast Depth for "Will Trump Win?" Market

**Input**:
`--market_id 123 --horizon 6`

**Output**:
`depth_forecast.csv` containing 6 forecasted depth values.

### Example 2: Forecast Spread for "Ethereum Price Above $3000?" Market

**Input**:
`--market_id 456 --horizon 24`

**Output**:
`spread_forecast.csv` containing 24 forecasted spread values.

## Resources

- Scripts: `{baseDir}/scripts/`
- API Docs: `{baseDir}/api_docs/`
- Config: `{baseDir}/config/`