# Nixtla BigQuery Forecaster - Architecture

**Document**: 003-AT-ARCH-plugin-architecture.md
**Created**: 2025-11-29
**Purpose**: Technical architecture overview for developers

---

## System Architecture

```
┌─────────────┐
│   User/API  │
└──────┬──────┘
       │ HTTP POST
       ▼
┌────────────────────────────────────┐
│  Cloud Function (nixtla-bigquery) │
│  ┌──────────────────────────────┐  │
│  │   forecast_handler()         │  │
│  │   (main.py)                  │  │
│  └───────────┬──────────────────┘  │
│              │                     │
│              ▼                     │
│  ┌───────────────────────────┐    │
│  │   BigQueryConnector        │    │
│  │   (bigquery_connector.py)  │    │
│  └───────────┬───────────────┘    │
│              │                     │
│              ▼                     │
│  ┌───────────────────────────┐    │
│  │   NixtlaForecaster        │    │
│  │   (forecaster.py)         │    │
│  │   - AutoETS               │    │
│  │   - AutoTheta             │    │
│  │   - TimeGPT (optional)    │    │
│  └───────────┬───────────────┘    │
│              │                     │
│              ▼                     │
│  ┌───────────────────────────┐    │
│  │   Response (JSON)          │    │
│  └────────────────────────────┘   │
└────────────────────────────────────┘
       │
       ▼
┌────────────────────┐
│   BigQuery Tables  │
│   - Source data    │
│   - Forecast output│
└────────────────────┘
```

---

## Component Breakdown

### 1. Cloud Function Entry Point
**File**: `src/main.py`
**Function**: `forecast_handler(request: Request)`

**Responsibilities**:
- Parse HTTP request (JSON payload)
- Validate required parameters
- Coordinate forecasting pipeline
- Return JSON response

**Triggers**:
- HTTP POST request
- Authenticated via Workload Identity (GitHub Actions)
- Public access for demo purposes

### 2. BigQuery Connector
**File**: `src/bigquery_connector.py`
**Class**: `BigQueryConnector`

**Key Methods**:
- `read_timeseries()` - Query BigQuery, return Nixtla-format DataFrame
- `write_forecasts()` - Write forecast results back to BigQuery
- `get_table_info()` - Fetch table metadata

**Data Flow**:
```
BigQuery Table → SQL Query → DataFrame (unique_id, ds, y)
```

**Transformations**:
- Cast timestamps to DATE
- Group by dimensions
- Aggregate values (SUM/AVG/COUNT)
- Apply WHERE filters
- Enforce row limits

### 3. Nixtla Forecaster
**File**: `src/forecaster.py`
**Class**: `NixtlaForecaster`

**Supported Models**:
- **AutoETS**: Exponential smoothing, auto parameter tuning
- **AutoTheta**: Theta method for seasonal data
- **SeasonalNaive**: Baseline (previous season's value)
- **TimeGPT** (optional): Foundation model via API

**Key Methods**:
- `forecast(df, horizon, models)` - Generate forecasts
- `backtest(df, horizon, n_windows)` - Cross-validation

**Forecasting Pipeline**:
```
Input DataFrame → StatsForecast → Forecast DataFrame
(unique_id, ds, y)    (fit + predict)   (unique_id, ds, AutoETS, AutoTheta, ...)
```

---

## Data Flow

### Input Payload
```json
{
  "project_id": "bigquery-public-data",
  "dataset": "chicago_taxi_trips",
  "table": "taxi_trips",
  "timestamp_col": "trip_start_timestamp",
  "value_col": "trip_total",
  "group_by": "payment_type",
  "horizon": 7,
  "models": ["AutoETS", "AutoTheta"],
  "limit": 1000
}
```

### Step 1: BigQuery Query
```sql
SELECT
  payment_type as unique_id,
  CAST(trip_start_timestamp AS DATE) as ds,
  SUM(trip_total) as y
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
GROUP BY unique_id, ds
ORDER BY unique_id, ds
LIMIT 1000
```

### Step 2: DataFrame Format
```
unique_id        ds          y
---------------------------------
Cash        2025-11-01    1250.45
Cash        2025-11-02    1180.32
Credit Card 2025-11-01    3450.12
Credit Card 2025-11-02    3520.88
```

### Step 3: Forecast Execution
```python
sf = StatsForecast(
    models=[AutoETS(season_length=7), AutoTheta(season_length=7)],
    freq='D'
)
forecasts = sf.forecast(df, h=7)
```

### Step 4: Output Format
```json
{
  "status": "success",
  "metadata": {
    "rows_read": 1000,
    "unique_series": 4,
    "forecast_points_generated": 56
  },
  "forecasts": [
    {
      "unique_id": "Cash",
      "ds": "2025-11-30",
      "AutoETS": 12.45,
      "AutoTheta": 12.38
    }
  ]
}
```

---

## Deployment Architecture

### CI/CD Pipeline

```
┌──────────────┐
│ Git Push     │
│ (main branch)│
└──────┬───────┘
       │
       ▼
┌────────────────────────────────┐
│  GitHub Actions Workflow       │
│  (.github/workflows/deploy-*)  │
│  ┌──────────────────────────┐  │
│  │ 1. Authenticate (WIF)    │  │
│  │ 2. Install dependencies  │  │
│  │ 3. Deploy Cloud Function │  │
│  │ 4. Run integration test  │  │
│  └──────────────────────────┘  │
└───────────┬────────────────────┘
            │
            ▼
    ┌──────────────────┐
    │  GCP Project     │
    │  nixtla-         │
    │  playground-01   │
    └──────────────────┘
```

### Infrastructure Components

| Component | Type | Purpose |
|-----------|------|---------|
| Cloud Function | Serverless compute | Run forecasting code |
| BigQuery | Data warehouse | Source/destination tables |
| Workload Identity | Authentication | Keyless GitHub Actions |
| Cloud Build | CI/CD | Build and deploy |
| Artifact Registry | Container storage | Function images |

---

## Security Model

### Authentication Flow (Workload Identity Federation)

```
GitHub Actions
     │
     │ 1. Request OIDC token from GitHub
     │
     ▼
GitHub OIDC Provider
     │
     │ 2. Issue signed JWT token
     │
     ▼
Google Cloud Workload Identity
     │
     │ 3. Exchange JWT for GCP access token
     │
     ▼
Service Account: nixtla-github-deployer
     │
     │ 4. Deploy Cloud Function with granted permissions
     │
     ▼
Cloud Function deployed successfully
```

**Benefits**:
- ✅ No JSON keys to manage
- ✅ No secrets stored in code
- ✅ Automatic rotation
- ✅ Audit trail

### IAM Permissions

**Service Account**: `nixtla-github-deployer@nixtla-playground-01.iam.gserviceaccount.com`

**Roles**:
- `roles/cloudfunctions.admin` - Deploy functions
- `roles/run.admin` - Manage Cloud Run
- `roles/bigquery.admin` - Read/write BigQuery
- `roles/iam.serviceAccountUser` - Use service accounts
- `roles/artifactregistry.admin` - Manage images
- `roles/storage.admin` - Access Cloud Storage

---

## Performance Characteristics

### Latency Breakdown

| Phase | Time | Notes |
|-------|------|-------|
| BigQuery query | 0.5-2s | Depends on data volume |
| Data processing | 0.1-0.5s | Pandas transformations |
| Model fitting | 1-5s | Per unique_id series |
| Forecast generation | 0.1-1s | Fast once fitted |
| Response formatting | <0.1s | JSON serialization |
| **Total** | **2-10s** | For 1K rows, 4 series |

### Scalability

**Vertical**:
- Cloud Function memory: 2GB (configurable up to 32GB)
- Timeout: 540s (9 minutes max)

**Horizontal**:
- Max instances: 10 (configurable up to 1000)
- Auto-scaling: Based on request volume

**BigQuery**:
- Query limit: 1TB/month (free tier)
- Storage limit: 10GB (free tier)
- Concurrent queries: 100

---

## Error Handling

### Input Validation
```python
missing_fields = []
if not project_id:
    missing_fields.append("project_id")
if not dataset:
    missing_fields.append("dataset")
# ... etc

if missing_fields:
    return jsonify({"error": f"Missing: {', '.join(missing_fields)}"}), 400
```

### Exception Handling
```python
try:
    df = bq_connector.read_timeseries(...)
    forecasts = forecaster.forecast(df, ...)
    return jsonify({"status": "success", ...}), 200
except Exception as e:
    logger.error(f"Error: {str(e)}", exc_info=True)
    return jsonify({"error": str(e), "type": type(e).__name__}), 500
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `No data found` | WHERE clause too restrictive | Remove/adjust filters |
| `Table not found` | Invalid dataset/table | Verify BigQuery path |
| `Timeout` | Too much data | Reduce `limit` parameter |
| `Insufficient data` | < 2 data points | Increase date range |

---

## Monitoring & Observability

### Cloud Logging
```bash
gcloud functions logs read nixtla-bigquery-forecast \
  --region=us-central1 \
  --limit=50
```

### Metrics Available
- Invocation count
- Execution time
- Error rate
- Memory usage
- BigQuery bytes processed

### Health Check
```bash
curl -X POST "FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "bigquery-public-data", ...}'
```

Expected: HTTP 200, `"status": "success"`

---

## Cost Model

### Per-Request Cost

**Compute** (Cloud Functions):
- 2GB RAM, 2s avg execution
- Cost: ~$0.0001 per request
- Free tier: 2M requests/month

**Data Processing** (BigQuery):
- 1000 rows query ≈ 0.001 GB processed
- Cost: ~$0.000005 per request
- Free tier: 1TB/month

**Total**: ~$0.0001 per request (basically free)

**At scale** (1M requests/month):
- Compute: ~$100
- BigQuery: ~$5
- **Total**: ~$105/month

---

## Extension Points

### Adding New Models

```python
# In forecaster.py
from statsforecast.models import ARIMA

model_map = {
    "AutoETS": AutoETS(season_length=7),
    "AutoTheta": AutoTheta(season_length=7),
    "ARIMA": ARIMA(order=(1,1,1))  # Add new model
}
```

### Custom Preprocessing

```python
# In bigquery_connector.py
def read_timeseries(self, ...):
    query = f"... your custom SQL ..."
    df = self.client.query(query).to_dataframe()
    # Add custom transformations
    df = self.custom_preprocessing(df)
    return df
```

### Output Destinations

```python
# Write to Cloud Storage
from google.cloud import storage
client = storage.Client()
bucket = client.bucket("forecast-results")
blob = bucket.blob("forecast.json")
blob.upload_from_string(json.dumps(forecasts))
```

---

## References

- **Nixtla statsforecast**: https://nixtla.github.io/statsforecast/
- **Google Cloud Functions**: https://cloud.google.com/functions/docs
- **BigQuery Python Client**: https://cloud.google.com/bigquery/docs/reference/libraries
- **Workload Identity Federation**: https://cloud.google.com/iam/docs/workload-identity-federation

---

**Last Updated**: 2025-11-29
