# Deploying nixtla-bigquery-forecaster

This is the operations guide for running the BigQuery forecaster as a
scheduled job in Google Cloud. The plugin itself is a Claude Code MCP
plugin — but the same Python module under `src/` is designed to run
unattended in Cloud Run / Cloud Functions / Cloud Composer.

The recipe below has been validated against `google-cloud-bigquery
3.10+` and Python 3.10+.

## Prerequisites

| Item | Why |
|---|---|
| GCP project with billing enabled | BigQuery + Cloud Run API charges |
| Service account with BigQuery roles | At minimum: `roles/bigquery.dataViewer`, `roles/bigquery.jobUser` for read; `roles/bigquery.dataEditor` for write |
| `gcloud` CLI authenticated locally | Deploy target |
| (Optional) `NIXTLA_TIMEGPT_API_KEY` | Only if you want TimeGPT alongside the offline statsforecast baselines |

## Production posture (v1.0)

The v1.0 release added two production-grade safety nets:

### 1. SQL identifier validation

Every BigQuery identifier (project, dataset, table, column, group_by) is
validated against the BigQuery identifier regex
(`^[A-Za-z_][A-Za-z0-9_]{0,1023}$`) before interpolation. Untrusted
input cannot inject into the constructed query.

For WHERE-clause values, prefer the new structured `filters` parameter
(it routes values through `safe_where_value` which only accepts
YYYY-MM-DD dates and numeric literals):

```python
# Safe — every identifier validated, every value rendered through
# safe_where_value().
df = connector.read_timeseries(
    dataset="my_dataset",
    table="orders",
    timestamp_col="created_at",
    value_col="total",
    group_by="store_id",
    filters={"region": "us-east-1", "active": 1},
    limit=10000,
)
```

The legacy `where_clause` string parameter still works but emits a
`DeprecationWarning` and is the caller's responsibility to keep
SQL-safe. **For arbitrary user-supplied values, use BigQuery's
parameterized queries** (`bigquery.QueryJobConfig(query_parameters=
[bigquery.ScalarQueryParameter(...)])`) — neither this plugin's
validators nor any string-based approach is sufficient for fully
arbitrary input.

### 2. Retry on transient GCP errors

Every BigQuery API call (`read_timeseries`, `write_forecasts`,
`get_table_info`) is wrapped with `@retry_on_transient` from
`src/retry.py`. The decorator retries on:

- `google.api_core.exceptions.ServiceUnavailable` (503)
- `google.api_core.exceptions.TooManyRequests` (429)
- `google.api_core.exceptions.InternalServerError` (500)
- `google.api_core.exceptions.GatewayTimeout` (504)
- `google.api_core.exceptions.DeadlineExceeded`

Default policy: 5 attempts, exponential backoff `1s → 2s → 4s → 8s →
16s` (capped at `max_backoff_s=30s`), with ±50% jitter. Non-transient
errors (auth failures, permission denied, invalid query) are not
retried.

Override the policy at the call site:

```python
from src.retry import retry_on_transient

@retry_on_transient(max_attempts=10, initial_backoff_s=2.0, max_backoff_s=60.0)
def my_long_running_load(...):
    ...
```

## Cloud Run deployment (recommended)

Cloud Run gives you stateless scheduled jobs with no infrastructure to
manage. Pair it with Cloud Scheduler (cron) for daily / hourly runs.

### 1. Create a service account

```bash
PROJECT_ID="your-project-id"
SA_NAME="nixtla-forecaster"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud iam service-accounts create $SA_NAME \
  --display-name="Nixtla BigQuery Forecaster" \
  --project=$PROJECT_ID

# Read source data
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/bigquery.dataViewer"

# Run query jobs
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/bigquery.jobUser"

# Write forecasts back
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/bigquery.dataEditor"
```

### 2. Build a container image

A minimal `Dockerfile` (place at the plugin root):

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# Cloud Run expects HTTP on $PORT. Use Flask/FastAPI to wrap the
# forecaster in a request handler, or schedule via Cloud Run Jobs
# (which doesn't require HTTP).
CMD ["python", "-m", "src.main"]
```

```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/nixtla-forecaster:1.0.0
```

### 3. Deploy as a Cloud Run Job

Cloud Run Jobs are the right primitive for scheduled batch work:

```bash
gcloud run jobs create nixtla-forecaster \
  --image=gcr.io/$PROJECT_ID/nixtla-forecaster:1.0.0 \
  --service-account=$SA_EMAIL \
  --region=us-central1 \
  --set-env-vars="GCP_PROJECT=$PROJECT_ID" \
  --set-secrets="NIXTLA_TIMEGPT_API_KEY=nixtla-api-key:latest" \
  --max-retries=3 \
  --task-timeout=30m
```

### 4. Schedule via Cloud Scheduler

```bash
gcloud scheduler jobs create http nixtla-daily \
  --location=us-central1 \
  --schedule="0 6 * * *" \
  --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/nixtla-forecaster:run" \
  --http-method=POST \
  --oauth-service-account-email=$SA_EMAIL
```

## Cloud Functions alternative (lighter weight)

For sub-1m forecasting workloads, Cloud Functions Gen 2 is simpler:

```bash
gcloud functions deploy nixtla-forecaster \
  --gen2 \
  --runtime=python312 \
  --entry-point=run \
  --region=us-central1 \
  --service-account=$SA_EMAIL \
  --memory=2GiB \
  --timeout=540s \
  --trigger-http \
  --no-allow-unauthenticated \
  --set-env-vars="GCP_PROJECT=$PROJECT_ID"
```

## Secrets

Use **Secret Manager** for the TimeGPT API key — never hardcode it,
never bake it into the container image, never log it.

```bash
echo -n "your-timegpt-api-key" | gcloud secrets create nixtla-api-key \
  --data-file=- --project=$PROJECT_ID

gcloud secrets add-iam-policy-binding nixtla-api-key \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"
```

Reference the secret from the Cloud Run Job:
`--set-secrets="NIXTLA_TIMEGPT_API_KEY=nixtla-api-key:latest"`

The plugin reads `NIXTLA_TIMEGPT_API_KEY` from the environment
(`os.environ.get(...)`), and the absence of the key falls back to
offline statsforecast baselines.

## Observability

Cloud Run / Cloud Functions stream stdout to Cloud Logging
automatically. The plugin uses Python's `logging` module at INFO level
by default — set `LOG_LEVEL=DEBUG` to see the constructed SQL queries
and retry-decorator decisions.

Recommended dashboards:

- **BigQuery slot utilization** (`bigquery.googleapis.com/slots`)
- **Cloud Run job execution count + duration**
  (`run.googleapis.com/job/completed_execution_count`)
- **Retry warnings** — filter logs for `attempt %d/%d failed` to spot
  GCP-side flakiness

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `InvalidIdentifierError: Invalid dataset 'foo-bar': must match BigQuery identifier rules` | BigQuery dataset name uses a hyphen | Rename the dataset (BQ datasets cannot contain hyphens — only underscores) |
| `BigQuery call failed after 5 attempts: ServiceUnavailable` | Sustained 503 from BigQuery | GCP incident — check status.cloud.google.com; bump `max_attempts` if expected to be temporary |
| `403 Permission denied` (no retry) | Service account missing role | Re-grant `bigquery.jobUser` + `bigquery.dataViewer` |
| Container starts but exits immediately | `src/main.py` doesn't open the HTTP listener | Use Cloud Run Jobs (no HTTP needed) instead of Cloud Run Services |
| `nixtla` import error in container | `requirements.txt` not pulled into image | Verify `COPY requirements.txt` line in Dockerfile |
| TimeGPT skipped, only statsforecast runs | `NIXTLA_TIMEGPT_API_KEY` env var not set | Bind via `--set-secrets` from Secret Manager |

## Cost notes

- **BigQuery query cost** = `bytes_processed * $5/TB`. Use the `limit`
  parameter on `read_timeseries` for development/testing runs.
- **Cloud Run Jobs**: ~$0.00002 / vCPU-second. A 30-minute, 2-vCPU job
  costs ~$0.07.
- **Cloud Scheduler**: 3 free jobs / month, then $0.10 / job / month.

For low-volume daily forecasting (one job, 5–10 minutes), expect
< $5 / month total in compute. BigQuery query cost dominates.
