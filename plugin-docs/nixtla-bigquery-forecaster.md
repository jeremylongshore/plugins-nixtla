# Nixtla BigQuery Forecaster Plugin

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          🌩️  NIXTLA BIGQUERY FORECASTER PLUGIN              ║
║        Cloud-Scale Forecasting with BigQuery Integration      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## Plugin Structure

```
🌩️  nixtla-bigquery-forecaster/
│
├── 📚 000-docs/
│   ├── 📄 001-DR-REFR-google-timeseries-insights-api.md
│   ├── 📄 002-DR-QREF-max-quick-start-guide.md
│   └── 📄 003-AT-ARCH-plugin-architecture.md
│
├── 📖 README.md
├── 📦 requirements.txt
│
├── 🔧 scripts/
│   └── 🐍 test_local.py
│
└── 💻 src/
    ├── 🐍 __init__.py
    ├── 🐍 bigquery_connector.py 🔌
    ├── 🐍 forecaster.py 📈
    └── 🐍 main.py ⚡
```

---

## What It Does

**Nixtla BigQuery Forecaster** is a production-ready plugin that brings Nixtla's forecasting capabilities directly to Google BigQuery. It enables cloud-scale time-series forecasting on millions of records without moving data out of BigQuery.

**Who It Helps**:
- 🏢 Enterprise teams with data in BigQuery
- 📊 Data analysts working with large-scale time-series
- 🌐 Cloud-first organizations
- ⚡ Teams needing fast, scalable forecasting pipelines

**Key Value**: Forecast millions of time series directly in BigQuery without data export - leveraging cloud compute and storage.

---

## Branch-by-Branch Description

### 📚 000-docs/

**Purpose**: Comprehensive technical documentation

#### `001-DR-REFR-google-timeseries-insights-api.md`

**What it does**:
- Documents Google Cloud's Time Series Insights API
- Integration patterns with BigQuery
- API authentication and quota management
- Example queries and responses

**Who reads it**: Developers integrating with Google Cloud APIs.

#### `002-DR-QREF-max-quick-start-guide.md`

**What it does**:
- Quick reference guide for getting started
- Common commands and patterns
- Troubleshooting tips
- Performance optimization guidelines

**Who reads it**: Users who want rapid setup (5-10 minutes).

#### `003-AT-ARCH-plugin-architecture.md`

**What it does**:
- Plugin architecture overview
- Component diagram
- Data flow documentation
- Design decisions and trade-offs

**Who reads it**: Technical leads evaluating the plugin, developers extending functionality.

---

### 🔧 scripts/

**Purpose**: Testing and utility scripts

#### `test_local.py`

**What it does**:
- Local testing without BigQuery connection
- Validates plugin functionality
- Mock data generation
- Unit test runner

**Usage**: Development and CI/CD testing before deploying to BigQuery.

**Key Functions**:
- `test_connector()` - Test BigQuery connection
- `test_forecaster()` - Test forecasting logic
- `test_end_to_end()` - Full pipeline test

---

### 💻 src/

**Purpose**: Core plugin source code

#### `__init__.py`

**What it does**:
- Package initialization
- Exports public API
- Version information

**Contents**:
```python
from .bigquery_connector import BigQueryConnector
from .forecaster import Forecaster
from .main import run_forecast

__version__ = "1.7.0"
```

#### `bigquery_connector.py` 🔌

**What it does**:
- Manages BigQuery authentication
- Executes SQL queries
- Handles data streaming
- Error handling and retry logic

**Key Functions**:
- `connect()` - Establish BigQuery connection
- `fetch_time_series()` - Query time-series data
- `write_forecasts()` - Write predictions back to BigQuery
- `create_forecast_table()` - Set up output tables

**Authentication Methods**:
- Service account JSON key
- Application Default Credentials (ADC)
- Workload Identity (GKE)

**Example Usage**:
```python
connector = BigQueryConnector(project_id="my-project")
data = connector.fetch_time_series(
    dataset="sales",
    table="daily_revenue",
    unique_id="store_id",
    timestamp="date",
    value="revenue"
)
```

#### `forecaster.py` 📈

**What it does**:
- Core forecasting engine
- Model selection and training
- Prediction generation
- Accuracy metrics calculation

**Supported Models**:
- AutoETS (Exponential Smoothing)
- AutoARIMA (Autoregressive Integrated Moving Average)
- AutoTheta (Theta method)
- SeasonalNaive (Baseline)
- TimeGPT (via API, optional)

**Key Functions**:
- `fit()` - Train models on historical data
- `predict()` - Generate forecasts
- `cross_validate()` - Validate model performance
- `calculate_metrics()` - Compute sMAPE, MASE, MAE, RMSE

**Example Usage**:
```python
forecaster = Forecaster(models=["AutoETS", "AutoARIMA"])
forecaster.fit(data)
predictions = forecaster.predict(horizon=30)
metrics = forecaster.calculate_metrics()
```

#### `main.py` ⚡

**What it does**:
- Entry point for the plugin
- Orchestrates workflow
- CLI argument parsing
- Error handling and logging

**Workflow**:
1. Connect to BigQuery
2. Fetch time-series data
3. Train forecasting models
4. Generate predictions
5. Write results back to BigQuery
6. Calculate and report metrics

**CLI Interface**:
```bash
python src/main.py \
  --project my-gcp-project \
  --dataset sales_data \
  --table daily_revenue \
  --horizon 30 \
  --models AutoETS,AutoARIMA
```

---

## Terminal How-To Guide

### Initial Setup

```bash
# Navigate to plugin directory
cd /home/jeremy/000-projects/nixtla/005-plugins/nixtla-bigquery-forecaster

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "google-cloud-bigquery|statsforecast"
```

**Expected packages**:
- google-cloud-bigquery
- statsforecast
- pandas
- numpy

---

### Authenticating with Google Cloud

#### Method 1: Service Account (Recommended for Production)

```bash
# Download service account key from Google Cloud Console
# Save as service-account.json

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Verify authentication
gcloud auth application-default login --quiet
```

#### Method 2: User Account (Development)

```bash
# Login with your Google account
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

#### Method 3: Workload Identity (GKE/Cloud Run)

```bash
# Already configured automatically in GKE/Cloud Run
# No additional setup needed
```

---

### Running Local Tests

```bash
# Run all tests
python scripts/test_local.py

# Run specific test
python scripts/test_local.py --test connector

# Verbose output
python scripts/test_local.py --verbose

# Save test results
python scripts/test_local.py > test_results.txt 2>&1
```

**Expected output**:
```
✓ BigQuery connector test passed
✓ Forecaster logic test passed
✓ End-to-end pipeline test passed
All tests completed successfully
```

---

### Forecasting with BigQuery Data

#### Step 1: Verify Your Data

```bash
# Check if your BigQuery table exists
bq show YOUR_PROJECT:YOUR_DATASET.YOUR_TABLE

# Sample your data
bq query --nouse_legacy_sql \
  'SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.YOUR_TABLE` LIMIT 10'
```

**Required schema**:
- `unique_id` column (STRING) - Series identifier (e.g., "store_001")
- `ds` column (DATE/TIMESTAMP) - Date/timestamp
- `y` column (FLOAT64) - Value to forecast

#### Step 2: Run Forecast

```bash
# Basic forecast (30 days ahead)
python src/main.py \
  --project YOUR_PROJECT \
  --dataset YOUR_DATASET \
  --table YOUR_TABLE \
  --horizon 30

# Forecast with specific models
python src/main.py \
  --project YOUR_PROJECT \
  --dataset YOUR_DATASET \
  --table YOUR_TABLE \
  --horizon 30 \
  --models AutoETS,AutoARIMA,AutoTheta

# Forecast with custom output table
python src/main.py \
  --project YOUR_PROJECT \
  --dataset YOUR_DATASET \
  --table YOUR_TABLE \
  --horizon 30 \
  --output-table forecasts_2024_12
```

#### Step 3: View Results

```bash
# Query forecast results
bq query --nouse_legacy_sql \
  'SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.forecasts` LIMIT 100'

# Export to CSV
bq extract \
  --destination_format CSV \
  YOUR_PROJECT:YOUR_DATASET.forecasts \
  gs://your-bucket/forecasts.csv

# Download locally
gsutil cp gs://your-bucket/forecasts.csv ./forecasts.csv
```

---

### Working with Large Datasets

#### Batch Processing

```bash
# Process in batches (recommended for >1M rows)
python src/main.py \
  --project YOUR_PROJECT \
  --dataset YOUR_DATASET \
  --table YOUR_TABLE \
  --horizon 30 \
  --batch-size 10000 \
  --parallel-jobs 4
```

**Performance**:
- 10K series: ~5 minutes
- 100K series: ~30 minutes
- 1M series: ~3 hours

#### Filtering Data

```bash
# Forecast only specific series
python src/main.py \
  --project YOUR_PROJECT \
  --dataset YOUR_DATASET \
  --table YOUR_TABLE \
  --horizon 30 \
  --filter "store_id IN ('001', '002', '003')"

# Forecast recent data only
python src/main.py \
  --project YOUR_PROJECT \
  --dataset YOUR_DATASET \
  --table YOUR_TABLE \
  --horizon 30 \
  --filter "date >= '2023-01-01'"
```

---

### Monitoring and Logging

```bash
# Enable verbose logging
python src/main.py \
  --project YOUR_PROJECT \
  --dataset YOUR_DATASET \
  --table YOUR_TABLE \
  --horizon 30 \
  --log-level DEBUG

# Save logs to file
python src/main.py \
  --project YOUR_PROJECT \
  --dataset YOUR_DATASET \
  --table YOUR_TABLE \
  --horizon 30 \
  2>&1 | tee forecast_$(date +%Y%m%d).log

# Monitor BigQuery jobs
bq ls -j --max_results 10
```

---

### Cost Management

```bash
# Estimate query cost (dry run)
bq query --dry_run --nouse_legacy_sql \
  'SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.YOUR_TABLE`'

# Check BigQuery usage
bq ls --project_id YOUR_PROJECT

# Set up cost alerts (in Google Cloud Console)
# Billing > Budgets & Alerts
```

**Cost Optimization Tips**:
- Use partitioned tables (reduces scan costs)
- Filter data by date range
- Process in batches during off-peak hours
- Use preemptible VMs for compute

---

### Troubleshooting

#### Error: "Permission denied"

```bash
# Solution 1: Check IAM roles
gcloud projects get-iam-policy YOUR_PROJECT

# Required roles:
# - roles/bigquery.dataViewer (read data)
# - roles/bigquery.jobUser (run queries)
# - roles/bigquery.dataEditor (write forecasts)

# Solution 2: Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT" \
  --role="roles/bigquery.dataEditor"
```

#### Error: "Table not found"

```bash
# Solution: Verify table exists
bq ls YOUR_PROJECT:YOUR_DATASET

# Create table if needed
bq mk --table YOUR_PROJECT:YOUR_DATASET.YOUR_TABLE \
  unique_id:STRING,ds:DATE,y:FLOAT64
```

#### Error: "Quota exceeded"

```bash
# Solution 1: Check quotas
gcloud compute project-info describe --project YOUR_PROJECT

# Solution 2: Request quota increase
# Google Cloud Console > IAM & Admin > Quotas

# Solution 3: Use batch processing
python src/main.py ... --batch-size 5000 --rate-limit 10
```

#### Error: "Invalid schema"

```bash
# Solution: Validate your data schema
bq show --schema --format=prettyjson YOUR_PROJECT:YOUR_DATASET.YOUR_TABLE

# Transform data to required format
bq query --destination_table YOUR_DATASET.formatted_table \
  --nouse_legacy_sql \
  'SELECT
    store_id AS unique_id,
    DATE(timestamp) AS ds,
    CAST(revenue AS FLOAT64) AS y
  FROM `YOUR_PROJECT.YOUR_DATASET.raw_table`'
```

---

## Performance Benchmarks

| Dataset Size | Records | Runtime | BigQuery Cost | Memory |
|--------------|---------|---------|---------------|--------|
| Small | 10K series | ~5 min | ~$0.01 | 2GB |
| Medium | 100K series | ~30 min | ~$0.10 | 8GB |
| Large | 1M series | ~3 hours | ~$1.00 | 32GB |
| X-Large | 10M series | ~24 hours | ~$10.00 | 128GB |

*Costs are approximate and vary by region and data size*

---

## Common Use Cases

### Use Case 1: Daily Sales Forecasting

```bash
# Forecast next 30 days of sales for all stores
python src/main.py \
  --project my-retail-project \
  --dataset sales \
  --table daily_store_sales \
  --horizon 30 \
  --models AutoETS,AutoTheta
```

**Result**: 30-day forecast for each store in BigQuery table `sales.forecasts`.

---

### Use Case 2: Inventory Planning

```bash
# Forecast next 90 days to plan inventory
python src/main.py \
  --project my-warehouse-project \
  --dataset inventory \
  --table product_demand \
  --horizon 90 \
  --models AutoARIMA \
  --output-table inventory_forecast_q1
```

**Result**: Quarterly inventory forecasts for procurement planning.

---

### Use Case 3: Cloud Cost Forecasting

```bash
# Forecast cloud spending for budget planning
python src/main.py \
  --project my-billing-project \
  --dataset billing \
  --table daily_costs \
  --horizon 60 \
  --models AutoETS,AutoTheta,SeasonalNaive
```

**Result**: 60-day cloud cost predictions for budget allocation.

---

## Integration with Other Plugins

**Works with**:
- `nixtla-baseline-lab` - Compare BigQuery forecasts vs baselines
- `nixtla-search-to-slack` - Alert team when forecasts are ready
- `nixtla-timegpt-lab` - Hybrid BigQuery + TimeGPT forecasting

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                  BIGQUERY FORECASTER FLOW                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │  BigQuery    │                                           │
│  │  Input Table │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         │ SQL Query                                          │
│         │                                                    │
│  ┌──────▼──────────┐                                        │
│  │  BigQuery       │                                        │
│  │  Connector      │◄─── Auth (Service Account/ADC)        │
│  └──────┬──────────┘                                        │
│         │                                                    │
│         │ pandas DataFrame                                   │
│         │                                                    │
│  ┌──────▼──────────┐                                        │
│  │  Forecaster     │                                        │
│  │  Engine         │◄─── Models (AutoETS/ARIMA/Theta)      │
│  └──────┬──────────┘                                        │
│         │                                                    │
│         │ Predictions                                        │
│         │                                                    │
│  ┌──────▼──────────┐                                        │
│  │  BigQuery       │                                        │
│  │  Output Table   │                                        │
│  └─────────────────┘                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Support & Resources

- **Architecture Doc**: `005-plugins/nixtla-bigquery-forecaster/000-docs/003-AT-ARCH-plugin-architecture.md`
- **Quick Start**: `005-plugins/nixtla-bigquery-forecaster/000-docs/002-DR-QREF-max-quick-start-guide.md`
- **API Reference**: `005-plugins/nixtla-bigquery-forecaster/000-docs/001-DR-REFR-google-timeseries-insights-api.md`

---

**Version**: 1.7.0
**Status**: ✅ Production Ready
**Last Updated**: 2025-12-09
