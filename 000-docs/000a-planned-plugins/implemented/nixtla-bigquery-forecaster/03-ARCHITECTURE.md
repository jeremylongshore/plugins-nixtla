# BigQuery Forecaster - Architecture

**Plugin:** nixtla-bigquery-forecaster
**Version:** Demo
**Last Updated:** 2025-12-12

---

## System Context

```
┌──────────────┐     HTTP POST      ┌─────────────────────┐
│   Client     │───────────────────▶│  Cloud Functions    │
│  (curl/API)  │◀──────────────────│  (Gen2, Python 3.12)│
└──────────────┘     JSON Response  └─────────────────────┘
                                            │
                                            │ BigQuery API
                                            ▼
                                    ┌─────────────────────┐
                                    │     BigQuery        │
                                    │   (Read/Write)      │
                                    └─────────────────────┘
                                            │
                                            ▼
                                    ┌─────────────────────┐
                                    │   StatsForecast     │
                                    │  (AutoETS, Theta)   │
                                    └─────────────────────┘
```

---

## Component Design

### Cloud Function (`src/main.py`)

HTTP handler that orchestrates the pipeline:

1. Parse JSON request
2. Validate required parameters
3. Call BigQueryConnector to read data
4. Call NixtlaForecaster to generate forecasts
5. Optionally write results back to BigQuery
6. Return JSON response

### BigQueryConnector (`src/bigquery_connector.py`)

Handles BigQuery operations:

| Method | Purpose |
|--------|---------|
| `read_timeseries()` | Query time series data with filters |
| `write_forecasts()` | Write forecast results to table |

### NixtlaForecaster (`src/forecaster.py`)

Wraps statsforecast models:

| Method | Purpose |
|--------|---------|
| `forecast()` | Run models and return predictions |
| `get_models()` | Return configured model instances |

---

## Data Flow

1. **Client** sends POST request with table details and horizon
2. **Cloud Function** validates request parameters
3. **BigQueryConnector** queries source table with SQL
4. **NixtlaForecaster** fits AutoETS/AutoTheta on data
5. **NixtlaForecaster** generates forecast for specified horizon
6. **BigQueryConnector** (optionally) writes forecasts to output table
7. **Cloud Function** returns JSON with forecasts and metadata

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  deploy-bigquery-forecaster.yml                      │   │
│  │  - Checkout code                                     │   │
│  │  - Authenticate via Workload Identity Federation     │   │
│  │  - Deploy to Cloud Functions Gen2                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     Google Cloud                            │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Cloud Functions │  │ BigQuery        │                  │
│  │ (Gen2)          │◀▶│ (Source/Target) │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
005-plugins/nixtla-bigquery-forecaster/
├── README.md
├── QUICKSTART.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── main.py                # Cloud Function entry
│   ├── bigquery_connector.py  # BigQuery operations
│   └── forecaster.py          # Nixtla model wrapper
├── 000-docs/
│   ├── 001-DR-REFR-google-timeseries-insights-api.md
│   ├── 002-DR-QREF-max-quick-start-guide.md
│   └── 003-AT-ARCH-plugin-architecture.md
├── commands/
│   └── nixtla-full-workflow.md
├── scripts/
│   └── test_local.py
└── .venv/                     # Local development venv
```

---

## Security Model

**Current (Demo):**
- Cloud Functions default authentication
- Service account with BigQuery permissions
- Workload Identity Federation for GitHub Actions

**Not Implemented:**
- API key authentication
- Rate limiting
- Request validation beyond type checks
- IP allowlisting

---

## Technical Constraints

- **Memory:** 512MB-1GB Cloud Functions memory
- **Timeout:** 540 seconds max for Cloud Functions
- **Cold Start:** ~5-10 seconds on first invocation
- **Region:** Single region deployment
- **Concurrency:** Limited by Cloud Functions quotas
