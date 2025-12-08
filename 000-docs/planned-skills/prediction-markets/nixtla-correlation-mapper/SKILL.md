---
name: nixtla-correlation-mapper
description: |
  Analyzes multi-contract correlations and generates hedge recommendations.
  Use when managing a portfolio of correlated assets and needing to mitigate risk.
  Trigger with "analyze correlations", "suggest hedge", "portfolio risk assessment".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla Correlation Mapper

Identifies correlations between multiple contracts and generates hedging strategies.

## Purpose

Analyzes the relationships between assets in a portfolio to suggest hedging strategies.

## Overview

Takes CSV data representing multiple time series of contract values. Calculates
the correlation matrix between these contracts. Using correlation coefficients, it
suggests optimal hedging strategies to reduce portfolio risk. Outputs correlation matrix
and hedging recommendations in a user-friendly format.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install pandas numpy scipy
```

## Instructions

### Step 1: Load contract data

Read the input CSV containing time series data for multiple contracts (unique_id, ds, y).

### Step 2: Calculate correlation matrix

Run the correlation analysis script: `python {baseDir}/scripts/correlation_analysis.py --input contracts.csv`

### Step 3: Generate hedge recommendations

Analyze correlation matrix and suggest hedge ratios.

### Step 4: Output results

Save correlation matrix and hedge recommendations to CSV files.

## Output

- **correlation_matrix.csv**: Matrix showing correlations between contracts.
- **hedge_recommendations.csv**: Suggested hedge ratios for each contract pair.
- **report.txt**: Summary report of analysis and recommendations.

## Error Handling

1. **Error**: `Input file not found`
   **Solution**: Verify the file path and ensure the file exists.

2. **Error**: `Missing required columns`
   **Solution**: Ensure input CSV contains 'unique_id', 'ds', and 'y' columns.

3. **Error**: `Insufficient data points`
   **Solution**: Provide more historical data for accurate correlation calculation.

4. **Error**: `Invalid data format`
   **Solution**: Check data types in CSV and ensure they are numeric where expected.

## Examples

### Example 1: Hedging Gold and Silver

**Input**:
```
unique_id,ds,y
Gold,2024-01-01,2000
Silver,2024-01-01,25
Gold,2024-01-02,2010
Silver,2024-01-02,25.5
```

**Output**:
```
correlation_matrix.csv: (Gold-Silver correlation value)
hedge_recommendations.csv: (Hedge ratio for Gold vs Silver)
```

### Example 2: Hedging Oil and Gas

**Input**:
```
unique_id,ds,y
Oil,2024-01-01,70
Gas,2024-01-01,3
Oil,2024-01-02,71
Gas,2024-01-02,3.1
```

**Output**:
```
correlation_matrix.csv: (Oil-Gas correlation value)
hedge_recommendations.csv: (Hedge ratio for Oil vs Gas)
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Documentation: `{baseDir}/docs/correlation_analysis.md`