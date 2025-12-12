# BigQuery Forecaster - Technical Specification

**Plugin:** nixtla-bigquery-forecaster
**Version:** Demo
**Last Updated:** 2025-12-12

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Runtime | Python | 3.12 |
| Platform | Cloud Functions | Gen2 |
| Forecasting | statsforecast | 2.0.3 |
| TimeGPT (optional) | nixtla | 0.7.1 |
| Data | google-cloud-bigquery | latest |
| HTTP | functions-framework | latest |

---

## API Reference

### Endpoint

```
POST https://<REGION>-<PROJECT>.cloudfunctions.net/nixtla-bigquery-forecaster
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | string | Yes | GCP project containing target table |
| `dataset` | string | Yes | BigQuery dataset name |
| `table` | string | Yes | BigQuery table name |
| `timestamp_col` | string | Yes | Column containing timestamps |
| `value_col` | string | Yes | Column containing values to forecast |
| `horizon` | int | Yes | Number of periods to forecast |
| `group_by` | string | No | Column to group series by |
| `models` | array | No | Models to use (default: AutoETS, AutoTheta) |
| `include_timegpt` | bool | No | Include TimeGPT (requires API key) |
| `output_dataset` | string | No | Write results to this dataset |
| `output_table` | string | No | Write results to this table |
| `limit` | int | No | Limit input rows |
| `where_clause` | string | No | SQL WHERE clause for filtering |
| `source_project` | string | No | Source project for public datasets |

### Response Format

```json
{
    "status": "success|error",
    "metadata": {
        "source_table": "project.dataset.table",
        "rows_read": 1000,
        "unique_series": 5,
        "horizon": 7,
        "models_used": ["AutoETS", "AutoTheta"],
        "timegpt_included": false,
        "forecast_points_generated": 35
    },
    "forecasts": [
        {
            "unique_id": "series_1",
            "ds": "2024-01-01",
            "AutoETS": 123.45,
            "AutoTheta": 120.32
        }
    ],
    "output_table": "project.dataset.table",
    "error": "error message if status=error"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (missing/invalid parameters) |
| 404 | No data found |
| 500 | Internal server error |

---

## File Structure

```
005-plugins/nixtla-bigquery-forecaster/
├── README.md                    # Overview and usage
├── QUICKSTART.md                # 4-line quick start
├── requirements.txt             # Python dependencies
├── src/
│   ├── __init__.py
│   ├── main.py                  # Cloud Function entry point
│   ├── bigquery_connector.py    # BigQuery read/write
│   └── forecaster.py            # Nixtla model wrapper
├── 000-docs/
│   ├── 001-DR-REFR-*.md         # Reference docs
│   ├── 002-DR-QREF-*.md         # Quick reference
│   └── 003-AT-ARCH-*.md         # Architecture
├── commands/
│   └── nixtla-full-workflow.md  # Slash command
├── scripts/
│   └── test_local.py            # Local testing
└── .venv/                       # Virtual environment
```

---

## Dependencies

```
statsforecast==2.0.3
nixtla==0.7.1
google-cloud-bigquery
pandas>=2.0.0
numpy>=1.24.0
functions-framework
flask
```

---

## Deployment

### GitHub Actions Workflow

File: `.github/workflows/deploy-bigquery-forecaster.yml`

Triggers on:
- Push to `005-plugins/nixtla-bigquery-forecaster/**`
- Manual dispatch

Steps:
1. Checkout code
2. Authenticate with Workload Identity Federation
3. Deploy to Cloud Functions Gen2
4. Output function URL

### Manual Deployment

```bash
gcloud functions deploy nixtla-bigquery-forecaster \
  --gen2 \
  --runtime python312 \
  --source 005-plugins/nixtla-bigquery-forecaster \
  --entry-point forecast_handler \
  --trigger-http \
  --region us-central1 \
  --memory 512MB \
  --timeout 540s
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NIXTLA_TIMEGPT_API_KEY` | No | TimeGPT API key (for TimeGPT model) |
| `GOOGLE_CLOUD_PROJECT` | Auto | Set by Cloud Functions |

---

## Testing

### Local Test

```bash
cd 005-plugins/nixtla-bigquery-forecaster
source .venv/bin/activate
python scripts/test_local.py
```

### Deployed Test

```bash
curl -X POST "https://FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "bigquery-public-data", ...}'
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 400 Missing fields | Required param missing | Check all required params |
| 404 No data | Empty query result | Check table/filters |
| 500 Internal error | Code exception | Check Cloud Functions logs |
| Slow response | Cold start | First request after deploy |
| Permission denied | IAM issue | Grant BigQuery access |
