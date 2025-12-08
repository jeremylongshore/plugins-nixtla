---
name: nixtla-market-risk-analyzer
description: |
  Analyzes market risk by calculating VaR, volatility, drawdown, and position sizing.
  Use when assessing investment risk, managing portfolios, or determining position sizes.
  Trigger with "analyze market risk", "calculate portfolio risk", "determine position size".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Market Risk Analyzer

Calculates key market risk metrics and recommends position sizes.

## Overview

This skill uses historical market data to calculate Value at Risk (VaR),
volatility, maximum drawdown, and optimal position sizes. It provides insights for
managing investment risk and optimizing portfolio allocation. The skill reads CSV
data, uses TimeGPT for volatility forecasts, and outputs risk metrics and
position sizing recommendations.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas numpy
```

## Instructions

### Step 1: Load Data

Read historical price data from a CSV file (columns: `date`, `price`).

### Step 2: Calculate Metrics

Run the analysis script to calculate VaR, volatility, and drawdown.

### Step 3: Determine Position Size

Use the calculated risk metrics and TimeGPT for volatility forecasts to determine the recommended position size.

### Step 4: Generate Report

Write the analysis results, including risk metrics and position size recommendations, to a report file.

## Output

- **risk_report.txt**: A text report containing VaR, volatility, drawdown, and position sizing recommendations.
- **var.png**: Plot of the VaR over time.
- **drawdown.png**: Plot of the drawdown over time.

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `Input file not found`
   **Solution**: Verify the file path and name are correct.

3. **Error**: `Invalid data format`
   **Solution**: Ensure the input CSV has 'date' and 'price' columns.

4. **Error**: `Insufficient data for analysis`
   **Solution**: Provide a longer history of price data (minimum 30 data points).

## Examples

### Example 1: Analyzing Stock Risk

**Input**:
```
date,price
2024-01-01,150.00
2024-01-02,152.50
```

**Output**:
```
VaR: 0.05
Volatility: 0.10
Recommended Position Size: 100 shares
```

### Example 2: Analyzing Portfolio Risk

**Input**:
```
date,price
2024-01-01,1000.00
2024-01-02,1005.00
```

**Output**:
```
VaR: 0.02
Volatility: 0.05
Recommended Position Size: 5 units
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Docs: `{baseDir}/references/`