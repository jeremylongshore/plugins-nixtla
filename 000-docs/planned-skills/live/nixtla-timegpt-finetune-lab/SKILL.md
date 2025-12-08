---
name: nixtla-timegpt-finetune-lab
description: |
  Fine-tunes TimeGPT on custom datasets to improve forecasting accuracy.
  Use when TimeGPT's zero-shot performance is insufficient or domain-specific accuracy is needed.
  Trigger with "finetune TimeGPT", "train TimeGPT", "adapt TimeGPT".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla TimeGPT Fine-Tuning Lab

Adapts the TimeGPT model to specific datasets for enhanced forecasting performance.

## Purpose

Improves forecasting accuracy by fine-tuning the pre-trained TimeGPT model on custom time series data.

## Overview

This skill guides users through the process of fine-tuning TimeGPT on their own datasets. It handles data preprocessing, training configuration, and evaluation. Use when domain-specific accuracy is crucial or when the general TimeGPT model underperforms. It outputs a fine-tuned model and performance metrics.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas scikit-learn
```

## Instructions

### Step 1: Prepare Data
Load and preprocess the time series data into a suitable format (unique_id, ds, y).

### Step 2: Configure Training
Define the fine-tuning parameters (e.g., learning rate, number of epochs) and training settings.

### Step 3: Execute Fine-Tuning
Run: `python {baseDir}/scripts/finetune.py --input data.csv --config config.json`

### Step 4: Evaluate and Save
Evaluate the fine-tuned model on a held-out dataset and save the trained model.

## Output

- **finetuned_model.pkl**: Fine-tuned TimeGPT model
- **metrics.json**: Evaluation metrics (e.g., MASE, RMSE)
- **training_log.txt**: Log of the training process

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_api_key`

2. **Error**: `Invalid data format`
   **Solution**: Ensure data has columns: unique_id, ds, y

3. **Error**: `Insufficient training data`
   **Solution**: Provide a larger training dataset (at least 50 time series points per series)

4. **Error**: `Fine-tuning failed`
   **Solution**: Adjust the fine-tuning parameters (learning rate, epochs) in the config.json

## Examples

### Example 1: Fine-tuning on Retail Sales Data

**Input**:
```
unique_id,ds,y
store_1,2023-01-01,100
store_1,2023-01-02,110
...
```

**Output**:
`finetuned_model.pkl` (a serialized, fine-tuned TimeGPT model)

### Example 2: Fine-tuning on Energy Consumption Data

**Input**:
```
unique_id,ds,y
building_1,2023-01-01 00:00,50
building_1,2023-01-01 01:00,55
...
```

**Output**:
`metrics.json` (performance metrics of the fine-tuned model)

## Resources

- Scripts: `{baseDir}/scripts/`
- Config: `{baseDir}/config/`
- Data: `{baseDir}/data/`