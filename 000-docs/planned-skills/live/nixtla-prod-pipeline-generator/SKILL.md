---
name: nixtla-prod-pipeline-generator
description: |
  Transforms experiments into production pipelines with Airflow/Prefect.
  Use when deploying time series models or managing complex data workflows.
  Trigger with "productionize model", "create pipeline", "deploy forecasting".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla Production Pipeline Generator

Transforms forecasting experiments into robust production pipelines.

## Purpose

Automates the creation of Airflow or Prefect workflows to deploy time series models.

## Overview

Analyzes experiment configurations and generates production-ready pipeline code.
Supports integration with TimeGPT API for seamless model deployment. Facilitates
scheduling, monitoring, and version control of forecasting pipelines. Outputs
Python code for Airflow/Prefect DAGs and associated configuration files.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install airflow prefect nixtla
```

## Instructions

### Step 1: Load experiment

Read experiment configuration file (e.g., YAML, JSON).

### Step 2: Select framework

Choose target framework (Airflow or Prefect).

### Step 3: Generate pipeline

Run: `python {baseDir}/scripts/pipeline_generator.py --config experiment.yaml --framework airflow`

### Step 4: Deploy pipeline

Deploy generated code to Airflow or Prefect environment.

## Output

- **dags/**: Airflow DAG Python files
- **flows/**: Prefect flow Python files
- **config.yaml**: Pipeline configuration file
- **README.md**: Deployment instructions

## Error Handling

1. **Error**: `Invalid framework specified`
   **Solution**: Choose either 'airflow' or 'prefect'

2. **Error**: `Experiment config not found`
   **Solution**: Ensure the config file exists and path is correct

3. **Error**: `Missing TimeGPT API key`
   **Solution**: Set `NIXTLA_TIMEGPT_API_KEY` environment variable

4. **Error**: `Invalid experiment configuration`
   **Solution**: Check the experiment config file for errors

## Examples

### Example 1: Airflow deployment

**Input**: `experiment.yaml` (specifying TimeGPT model, data location, and schedule)

**Output**: Airflow DAG Python files in `dags/` folder ready for deployment

### Example 2: Prefect deployment

**Input**: `experiment.yaml` (specifying TimeGPT model, data location, and schedule)

**Output**: Prefect flow Python files in `flows/` folder ready for deployment

## Resources

- Scripts: `{baseDir}/scripts/`
- Templates: `{baseDir}/templates/`
- Examples: `{baseDir}/examples/`