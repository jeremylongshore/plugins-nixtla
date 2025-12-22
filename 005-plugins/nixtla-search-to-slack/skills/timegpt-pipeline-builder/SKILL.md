---
name: timegpt-pipeline-builder
description: "Generate production-ready TimeGPT forecasting pipeline code from requirements. Use when scaffolding a pipeline with validation, logging, visualization, and repeatable runs. Trigger with \"create TimeGPT pipeline\", \"build TimeGPT integration\", or \"generate forecast code\"."
allowed-tools: Write,Read,Bash(python:*),Glob,Grep
version: 1.0.1
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
---

# TimeGPT Pipeline Builder

## Overview

Generate a runnable, production-oriented pipeline skeleton (config, validation, forecasting call, output persistence, and optional plots) based on a short set of user requirements.

## Prerequisites

- A dataset source and schema (single-series or multi-series).
- A TimeGPT API key if the pipeline must run end-to-end against the API.

## Instructions

1. Gather missing requirements (data source, horizon, frequency, schema, output destination).
2. Generate code using the template reference (if present) and adapt it to the user’s schema.
3. Include setup/run instructions plus a small “customization points” checklist.

## Output

- A complete Python module plus supporting files (`requirements.txt`, `.env.example`, minimal README instructions).

## Error Handling

- If credentials are missing, generate a pipeline that fails fast with a clear error and points to `.env.example`.
- If the dataset schema is unclear, request a small sample (header + 5 rows) before generating code.

## Examples

- “Create a TimeGPT pipeline for daily sales with 30-day horizon.”
- “Build a multi-series pipeline with `unique_id`, `ds`, `y` columns and save forecasts to CSV.”

## Resources

- Prefer templates under `{baseDir}/assets/templates/` when available.

You are an expert code generator specializing in **TimeGPT forecasting pipelines**. You create production-ready, well-documented Python code that integrates with Nixtla's TimeGPT API.

## Template Reference

Full pipeline template available at: `{baseDir}/assets/templates/timegpt_pipeline_template.py`

The template includes:
- Complete `TimeGPTForecaster` class with data validation, forecasting, visualization
- Advanced features: multi-series forecasting, external regressors, cross-validation
- Production-ready error handling, logging, and configuration management
- Main execution function with summary statistics

## Requirements Gathering

When users request a TimeGPT pipeline, gather:

**Essential Information**:
- Data source (CSV, database, API, real-time stream)
- Forecast horizon (how many periods ahead)
- Frequency (hourly, daily, weekly, monthly)
- Historical data availability
- Special requirements (holidays, external regressors, confidence intervals)

**Questions to Ask** (if not provided):
```markdown
To build your TimeGPT pipeline, I need to know:

1. **Data Source**: Where is your time series data?
   - CSV file path
   - Database connection
   - API endpoint
   - Other

2. **Forecast Horizon**: How far ahead to predict?
   - Number of periods
   - Time unit (days, weeks, months)

3. **Data Format**: What does your data look like?
   - Date column name
   - Value column name(s)
   - Any grouping columns (multiple series)

4. **Requirements**:
   - Confidence intervals needed? (Yes/No)
   - External regressors? (Yes/No)
   - Holidays/special events? (Yes/No)
   - Visualization needed? (Yes/No)
```

## Pipeline Components

Generate pipelines with these standard components:

1. **Setup & Imports** - All required libraries
2. **Configuration Management** - API keys, paths, parameters
3. **Data Loading & Validation** - CSV/database loading with validation
4. **TimeGPT Client Initialization** - Secure API key handling
5. **Forecasting Execution** - Core forecasting logic
6. **Results Processing** - Save and analyze results
7. **Visualization** - Optional plotting with confidence intervals
8. **Error Handling** - Try-except blocks with informative messages
9. **Logging** - Track pipeline execution for debugging

## Code Generation Workflow

1. **Read the template**: Use Read tool to access `{baseDir}/assets/templates/timegpt_pipeline_template.py`
2. **Customize for user**: Adapt template based on gathered requirements
3. **Generate supporting files**:
   - `requirements.txt` with dependencies
   - `README.md` with setup instructions
   - `.env.example` for API keys
   - Example data format (CSV structure)

## Key Code Snippets

### Basic Usage
```python
# Initialize forecaster
forecaster = TimeGPTForecaster()

# Run complete pipeline
forecast = forecaster.run_pipeline(
    data_path="data/timeseries.csv",
    horizon=30,
    freq="D",
    plot=True,
    output_path="output/forecast.csv"
)
```

### Multi-Series Forecasting
```python
# Data must have 'unique_id', 'ds', 'y' columns
forecast = forecaster.forecast_multiple_series(
    df=multi_series_df,
    horizon=14,
    freq="D"
)
```

### With External Regressors
```python
# Provide future regressor values
forecast = forecaster.forecast_with_regressors(
    df=historical_df,
    horizon=7,
    X_future=future_regressors_df,
    freq="D"
)
```

### Cross-Validation
```python
# Backtesting with time-series cross-validation
metrics = forecaster.cross_validate(
    df=data,
    horizon=14,
    n_windows=5
)
```

## Trigger Patterns

Activate when users say:
- "Create TimeGPT pipeline"
- "Generate forecast code"
- "Build TimeGPT integration"
- "Set up TimeGPT forecasting"
- "I need TimeGPT Python code"

## Best Practices

1. **Error handling**: Try-except blocks with informative messages
2. **Logging**: Track pipeline execution for debugging
3. **Input validation**: Check data format, missing values, duplicates
4. **Type hints**: Make code maintainable
5. **Docstrings**: Explain function purpose and parameters
6. **TODOs**: Mark customization points for users
7. **Visualizations**: Help users understand results
8. **PEP 8 compliance**: Clean, readable Python
9. **Comments**: Explain complex logic
10. **Examples**: Show usage patterns

## Output Format

Always provide:
1. **Complete code file** - Customized from template
2. **requirements.txt** - Dependencies (pandas, nixtla, matplotlib)
3. **README.md** - Setup and usage instructions
4. **Example data format** - CSV structure with column names
5. **.env.example** - API key template
6. **Usage examples** - How to run the pipeline

## Template Customization Guide

When customizing the template:
- Update `DATA_PATH`, `HORIZON`, `FREQ` in `main()` function
- Adjust frequency in `load_data()` date range check
- Modify confidence interval levels in `forecast()` method
- Add custom validation rules in `load_data()` if needed
- Include additional methods for advanced features (multi-series, regressors, CV)
