---
name: nixtla-batch-forecaster
description: "Forecast multiple time series in parallel using TimeGPT with rate-limited batch processing, automatic fallback for failed series, and portfolio-level aggregation. Use when processing 10-100+ contracts efficiently or scaling forecasts across many series. Trigger with 'batch forecast', 'parallel forecasting', 'bulk prediction', 'multiple series forecast'."
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
---

# Nixtla Batch Forecaster

Process multiple time series forecasts in parallel with optimized throughput.

## Prerequisites

**Required**:
- Python 3.8+
- `nixtla`, `pandas`, `tqdm` packages

**Environment Variables**:
- `NIXTLA_TIMEGPT_API_KEY`: Your TimeGPT API key

**Installation**:
```bash
pip install nixtla pandas tqdm
```

## Instructions

### Step 1: Prepare Input Data

Your CSV must have the Nixtla schema columns:

| Column | Type | Description |
|--------|------|-------------|
| `unique_id` | string | Series identifier (contract ID) |
| `ds` | datetime | Timestamp |
| `y` | numeric | Value to forecast |

Validate your data before proceeding:
```bash
python {baseDir}/scripts/prepare_data.py your_data.csv
```

Verify the output reports no errors before continuing.

### Step 2: Set API Key

```bash
export NIXTLA_TIMEGPT_API_KEY=your_api_key_here
```

### Step 3: Run Batch Forecast

Execute the batch forecasting engine:
```bash
python {baseDir}/scripts/batch_forecast.py your_data.csv --horizon 14 --freq D
```

**Available options**:
- `--horizon`: Forecast horizon (default: 14)
- `--freq`: Frequency D/H/W/M (default: D)
- `--batch-size`: Series per batch (default: 20)
- `--output-dir`: Output directory (default: forecasts)
- `--aggregate`: Create portfolio aggregation
- `--delay`: Rate limit delay in seconds (default: 1.0)

### Step 4: Verify and report

Check the summary for batch failures, then generate the report:
```bash
cat forecasts/summary.json | python -m json.tool
python {baseDir}/scripts/generate_report.py forecasts/
```

The core API call used per batch:
```python
from nixtla import NixtlaClient
client = NixtlaClient()
forecast = client.forecast(df=batch_df, h=14, freq='D')
```

## Output

- **forecasts/all_forecasts.csv**: Combined forecasts for all series
- **forecasts/{series}_forecast.csv**: Individual series forecasts
- **forecasts/summary.json**: Processing metadata
- **forecasts/aggregated_forecast.csv**: Portfolio aggregation (if --aggregate)
- **forecasts/batch_report.md**: Human-readable summary

## Examples

### Example 1: Forecast 50 Daily Contracts

```bash
python {baseDir}/scripts/batch_forecast.py contracts.csv \
    --horizon 14 \
    --freq D \
    --batch-size 10 \
    --output-dir forecasts/
```

**Output**:
```
Batch Forecast Complete
Series forecasted: 50/50
Success rate: 100.0%
```

### Example 2: Hourly Portfolio with Aggregation

```bash
python {baseDir}/scripts/batch_forecast.py portfolio.csv \
    --horizon 24 \
    --freq H \
    --aggregate \
    --output-dir portfolio_forecasts/
```

## Resources

- Scripts:
  - `{baseDir}/scripts/prepare_data.py` - Data validation and analysis
  - `{baseDir}/scripts/batch_forecast.py` - Main forecasting engine
  - `{baseDir}/scripts/generate_report.py` - Report generation
- Nixtla Docs: https://nixtla.github.io/
