---
name: nixtla-contract-schema-mapper
description: |
  Transforms prediction market data to Nixtla format (unique_id, ds, y).
  Use when preparing prediction market datasets for Nixtla's forecasting tools.
  Trigger with "convert to Nixtla format", "Nixtla schema", "transform data".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla Contract Schema Mapper

Transforms prediction market data into the Nixtla-compatible format (unique_id, ds, y).

## Overview

Converts prediction market datasets with varying schemas into a standardized Nixtla format. This enables the data to be ingested by Nixtla's forecasting models. Analyzes the input schema, maps relevant fields to 'unique_id', 'ds', and 'y', and outputs a CSV file in the Nixtla format. Useful for preparing datasets with time series information associated with unique entities.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Packages**:
```bash
pip install pandas
```

## Instructions

### Step 1: Load Data

Read the prediction market data from a CSV file.

### Step 2: Analyze Schema

Identify the columns corresponding to unique ID, date, and target variable.

### Step 3: Transform Data

Run the script: `python {baseDir}/scripts/transform.py --input input.csv --id_col id_column --date_col date_column --target_col target_column`

### Step 4: Generate Output

Save the transformed data in Nixtla format (unique_id, ds, y) to a new CSV file.

## Output

- **nixtla_data.csv**: Transformed data in Nixtla format (unique_id, ds, y).

## Error Handling

1. **Error**: `Missing required argument: --input`
   **Solution**: Provide the input CSV file path using `--input input.csv`.

2. **Error**: `Column not found: id_column`
   **Solution**: Ensure the specified ID column exists in the input CSV file.

3. **Error**: `Invalid date format in date_column`
   **Solution**: Correct the date format in the specified column or use a custom date parser.

4. **Error**: `Non-numeric data in target_column`
   **Solution**: Ensure the target column contains only numeric data.

## Examples

### Example 1: Basic Conversion

**Input**:
```
contract_id,date,volume
contract_1,2024-01-01,100
contract_1,2024-01-02,120
```

**Output**:
```
unique_id,ds,y
contract_1,2024-01-01,100
contract_1,2024-01-02,120
```

### Example 2: Renaming Columns

**Input**:
```
id,timestamp,price
market_1,2024-01-01,0.75
market_1,2024-01-02,0.80
```

**Output**:
```
unique_id,ds,y
market_1,2024-01-01,0.75
market_1,2024-01-02,0.80
```

## Resources

- Scripts: `{baseDir}/scripts/transform.py`
- Example Data: `{baseDir}/data/`