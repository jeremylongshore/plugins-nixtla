---
name: nixtla-exogenous-integrator
description: |
  Incorporates external variables (holidays, weather, events) into TimeGPT forecasts to improve accuracy.
  Use when forecasts require external data, holidays impact sales, or weather affects demand.
  Trigger with "include holidays", "add weather data", "integrate events".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla Exogenous Integrator

Augments TimeGPT forecasts with exogenous variables for increased accuracy.

## Purpose

Enhances time series predictions by integrating external data sources like holidays, weather, and events.

## Overview

This skill enriches TimeGPT forecasts by considering external factors influencing time series data.
It reads exogenous data from CSV files, aligns it with the historical data, and passes both to the TimeGPT API.
This integration improves forecast accuracy, especially when events or external conditions affect the time series.
The skill outputs an augmented forecast incorporating the impact of these exogenous variables.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

## Instructions

### Step 1: Prepare data

Read historical time series CSV and exogenous variables CSVs. Ensure they have a common date ('ds') column.

### Step 2: Align data

Merge historical and exogenous dataframes based on the 'ds' column.

### Step 3: Configure API call

Prepare the TimeGPT API call with the historical data and the merged exogenous variables.

### Step 4: Generate forecast

Run: `python {baseDir}/scripts/integrate_exogenous.py --input data.csv --exogenous holidays.csv --horizon 14`

## Output

- **forecast_exogenous.csv**: Predictions with integrated exogenous variables.
- **exogenous_variables.json**: Summary of exogenous variables used and their impact.

## Error Handling

1. **Error**: `Exogenous data missing 'ds' column`
   **Solution**: Rename the date column in the exogenous data to 'ds'.

2. **Error**: `Mismatch in date range between historical and exogenous data`
   **Solution**: Ensure the exogenous data covers the entire historical and forecast period.

3. **Error**: `Exogenous variables have NaN values in the forecast horizon`
   **Solution**: Provide future values for exogenous variables for the entire forecast horizon.

4. **Error**: `TimeGPT API rejected exogenous variables (Check data types)`
   **Solution**: Ensure exogenous variables are numeric and compatible with the TimeGPT API schema.

## Examples

### Example 1: Holiday impact on sales

**Input (data.csv)**:
```
unique_id,ds,y
store_1,2024-01-01,100
store_1,2024-01-02,120
```

**Input (holidays.csv)**:
```
ds,holiday
2024-01-01,New Year's Day
2024-02-14,Valentine's Day
```

**Output (forecast_exogenous.csv)**:
```
unique_id,ds,TimeGPT,TimeGPT-lo-90,TimeGPT-hi-90
store_1,2024-01-03,130,115,145
store_1,2024-01-04,125,110,140
```

### Example 2: Weather affecting demand

**Input (data.csv)**:
```
unique_id,ds,y
grid_1,2024-01-01 00:00,5000
grid_1,2024-01-01 01:00,5100
```

**Input (weather.csv)**:
```
ds,temperature
2024-01-01 00:00,10
2024-01-01 01:00,8
```

**Output (forecast_exogenous.csv)**:
```
unique_id,ds,TimeGPT
grid_1,2024-01-01 02:00,5200
grid_1,2024-01-01 03:00,5150
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Docs: `{baseDir}/references/`