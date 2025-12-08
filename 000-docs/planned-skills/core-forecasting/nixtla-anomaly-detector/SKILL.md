---
name: nixtla-anomaly-detector
description: |
  Detects anomalies in time series data using TimeGPT.
  Use when identifying outliers, level shifts, or trend breaks in time series.
  Trigger with "detect anomalies", "find outliers", "anomaly detection".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Anomaly Detector Skill

Identifies anomalies in time series data using the Nixtla TimeGPT API.

## Purpose

To automatically detect and flag anomalies within time series data, providing insights into potential issues, unusual events, or data errors.

## Overview

Leverages TimeGPT to identify outliers, level shifts, and trend breaks without requiring model training. Accepts time series data as input, analyzes it using TimeGPT's anomaly detection capabilities, and outputs a report highlighting detected anomalies with their timestamps and anomaly types. Returns a CSV file containing anomaly information and a visualization plot.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

## Instructions

### Step 1: Load data

Read the input CSV file containing the time series data (unique_id, ds, y).

### Step 2: Configure detection parameters

Set detection sensitivity.

### Step 3: Execute anomaly detection

Run: `python {baseDir}/scripts/detect_anomalies.py --input data.csv`

### Step 4: Generate output

Save anomaly CSV and create visualization plot.

## Output

- **anomalies.csv**: Contains detected anomalies with timestamps and type (outlier, level shift, trend break)
- **plot.png**: Visualization of the time series data with anomalies highlighted
- **summary.txt**: A summary of the number and types of anomalies detected.

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `Invalid input data format`
   **Solution**: Ensure CSV contains 'unique_id', 'ds', and 'y' columns.

3. **Error**: `No anomalies detected`
   **Solution**: Lower sensitivity parameter or ensure there is sufficient anomalous behavior.

4. **Error**: `Connection error to TimeGPT API`
   **Solution**: Check network connection and TimeGPT API status.

## Examples

### Example 1: Detecting outliers in website traffic

**Input**:
```
unique_id,ds,y
website_1,2024-01-01,1000
website_1,2024-01-02,1050
website_1,2024-01-03,300
```

**Output**:
```
unique_id,ds,anomaly_type
website_1,2024-01-03,outlier
```

### Example 2: Identifying a trend break in sales data

**Input**:
```
unique_id,ds,y
store_1,2023-12-29,50
store_1,2023-12-30,60
store_1,2023-12-31,150
```

**Output**:
```
unique_id,ds,anomaly_type
store_1,2023-12-31,trend_break
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Docs: `{baseDir}/references/`