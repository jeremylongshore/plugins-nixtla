# BigQuery Forecaster - User Journey

**Plugin:** nixtla-bigquery-forecaster
**Last Updated:** 2025-12-12

---

## Demo Journey (Chicago Taxi Data)

### Step 1: Deploy Function

Deployment is automatic via GitHub Actions on push to main.

Manual deploy (if needed):
```bash
gcloud functions deploy nixtla-bigquery-forecaster \
  --gen2 \
  --runtime python312 \
  --source 005-plugins/nixtla-bigquery-forecaster \
  --entry-point forecast_handler \
  --trigger-http \
  --region us-central1
```

### Step 2: Test with Public Data

```bash
curl -X POST "https://YOUR-FUNCTION-URL" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "bigquery-public-data",
    "dataset": "chicago_taxi_trips",
    "table": "taxi_trips",
    "timestamp_col": "trip_start_timestamp",
    "value_col": "trip_total",
    "group_by": "payment_type",
    "horizon": 7,
    "limit": 1000,
    "source_project": "bigquery-public-data"
  }'
```

### Step 3: Review Results

```json
{
  "status": "success",
  "metadata": {
    "rows_read": 210,
    "unique_series": 7,
    "forecast_points_generated": 49
  },
  "forecasts": [
    {
      "unique_id": "Cash",
      "ds": "2023-02-01",
      "AutoETS": 69918.06,
      "AutoTheta": 56865.52
    }
  ]
}
```

---

## Using Your Own Data

### Prerequisites

1. BigQuery table with time series data
2. Cloud Function deployed with BigQuery permissions
3. Proper authentication (or public endpoint for testing)

### Request Format

```json
{
    "project_id": "your-project",
    "dataset": "your_dataset",
    "table": "your_table",
    "timestamp_col": "timestamp",
    "value_col": "sales",
    "group_by": "store_id",
    "horizon": 30
}
```

### Writing Results to BigQuery

Add output parameters to write forecasts:

```json
{
    "project_id": "your-project",
    "dataset": "your_dataset",
    "table": "your_table",
    "timestamp_col": "timestamp",
    "value_col": "sales",
    "horizon": 30,
    "output_dataset": "forecast_results",
    "output_table": "my_forecasts"
}
```

---

## Local Development

### Setup

```bash
cd 005-plugins/nixtla-bigquery-forecaster
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Local Server

```bash
python scripts/test_local.py
```

Server runs at `http://localhost:8080`

### Test Local

```bash
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"project_id": "bigquery-public-data", ...}'
```

---

## Error Scenarios

### "Missing required fields"

Ensure all required parameters are included:
- project_id
- dataset
- table
- timestamp_col
- value_col
- horizon

### "No data found"

- Check table name and column names
- Verify BigQuery permissions
- Try adding `limit` to test with smaller dataset

### "Permission denied"

- Ensure service account has BigQuery Data Viewer role
- For public datasets, use `source_project` parameter

### Cold Start Latency

First request after deployment may take 5-10 seconds. Subsequent requests are faster.

---

## Tips

1. **Start small**: Use `limit: 100` for initial testing
2. **Public data**: Chicago taxi dataset is great for demos
3. **Check logs**: Cloud Functions logs show detailed errors
4. **Cost**: ~$0.01 per request for typical workloads
