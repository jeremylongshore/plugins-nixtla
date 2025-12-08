---
name: nixtla-experiment-architect
description: |
  Scaffolds production-ready forecasting experiments with configuration files.
  Use when designing a new forecasting project, comparing models, or automating pipelines.
  Trigger with "design experiment", "setup forecasting project", "create forecasting configs".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla Experiment Architect

Automates the creation of forecasting experiment configurations.

## Overview

Creates standardized configuration files for forecasting experiments, including dataset definitions, model selections (TimeGPT, StatsForecast), evaluation metrics, and pipeline settings. This simplifies experiment design, promotes reproducibility, and facilitates model comparison. Outputs a directory structure with pre-configured YAML files and Python scripts.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY` (for TimeGPT experiments)

**Packages**:
```bash
pip install nixtla statsforecast
```

## Instructions

### Step 1: Define experiment parameters

Read user inputs (dataset path, model types, horizon).

### Step 2: Generate config files

Write YAML configs for data loading, model training, and evaluation.

### Step 3: Create scripts

Generate Python scripts for running the experiment pipeline.

### Step 4: Output experiment directory

Save configs and scripts in a structured directory.

## Output

- **config.yaml**: Experiment configuration file.
- **data.yaml**: Data loading configuration.
- **models.yaml**: Model selection configuration.
- **pipeline.py**: Python script to run the experiment.
- **README.md**: Instructions for running the experiment.

## Error Handling

1. **Error**: `Invalid model type`
   **Solution**: Use valid model names (TimeGPT, AutoARIMA, etc.)

2. **Error**: `Dataset path not found`
   **Solution**: Verify the dataset file path exists.

3. **Error**: `Missing horizon`
   **Solution**: Specify the forecasting horizon.

4. **Error**: `Invalid metric`
   **Solution**: Use valid evaluation metrics (MASE, sMAPE).

## Examples

### Example 1: TimeGPT experiment

**Input**:
```
dataset_path=sales.csv, model_type=TimeGPT, horizon=30
```

**Output**:
A directory with config files and scripts for a TimeGPT forecasting experiment on sales.csv with a horizon of 30.

### Example 2: StatsForecast experiment

**Input**:
```
dataset_path=demand.csv, model_type=AutoARIMA, horizon=7
```

**Output**:
A directory with config files and scripts for an AutoARIMA forecasting experiment on demand.csv with a horizon of 7.

## Resources

- Config Templates: `{baseDir}/templates/`
- Example Scripts: `{baseDir}/examples/`
