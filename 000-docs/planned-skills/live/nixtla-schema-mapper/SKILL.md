---
name: nixtla-schema-mapper
description: |
  Transforms tabular data into the Nixtla format (unique_id, ds, y).
  Use when needing to prepare time series data for Nixtla forecasting models.
  Trigger with "convert to Nixtla format", "Nixtla data schema", "prepare time series data".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla Schema Mapper

Converts data into the Nixtla-compatible (unique_id, ds, y) format.

## Overview

Analyzes input data, infers the mapping between columns and the `unique_id`, `ds` (datetime), and `y` (target) fields, and transforms the data accordingly. Useful when needing to process data for use with Nixtla's time series models or tools. Automatically detects date formats and handles missing values. Outputs a CSV file in the Nixtla format.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Packages**:
```bash
pip install pandas
```

## Instructions

### Step 1: Load data

Read the input CSV file using the `Read` tool.

### Step 2: Analyze schema

Analyze the data to automatically infer mappings for `unique_id`, `ds`, and `y` columns.

### Step 3: Transform data

Run the transformation script: `python {baseDir}/scripts/schema_mapper.py --input input.csv --output output.csv`

### Step 4: Generate output

Write the transformed data to a new CSV file in Nixtla format.

## Output

- **output.csv**: Transformed data in Nixtla format (unique_id, ds, y)

## Error Handling

1. **Error**: `Could not infer mapping`
   **Solution**: Specify column mappings using `--id_col`, `--date_col`, `--target_col` arguments.

2. **Error**: `Date parsing failed`
   **Solution**: Specify the date format using the `--date_format` argument (e.g., '%Y-%m-%d').

3. **Error**: `Missing values in target column`
   **Solution**: Handle missing values by either removing rows or using imputation techniques before running the script.

4. **Error**: `Input file not found`
   **Solution**: Ensure the input file exists at the specified path.

## Examples

### Example 1: Sales Data

**Input**:
```
store_id,date,sales
A1,2023-01-01,100
A1,2023-01-02,110
```

**Output**:
```
unique_id,ds,y
A1,2023-01-01,100
A1,2023-01-02,110
```

### Example 2: Energy Consumption

**Input**:
```
id,timestamp,consumption
X1,2023-01-01 00:00:00,50
X1,2023-01-01 01:00:00,55
```

**Output**:
```
unique_id,ds,y
X1,2023-01-01 00:00:00,50
X1,2023-01-01 01:00:00,55
```

## Resources

- Scripts: `{baseDir}/scripts/schema_mapper.py`
- Example Data: `{baseDir}/examples/`