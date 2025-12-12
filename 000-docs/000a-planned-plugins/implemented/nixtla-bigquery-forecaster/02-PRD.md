# BigQuery Forecaster - Product Requirements Document

**Plugin:** nixtla-bigquery-forecaster
**Version:** Demo
**Status:** Implemented
**Last Updated:** 2025-12-12

---

## Overview

HTTP Cloud Function that reads time series data from BigQuery, runs Nixtla statsforecast models, and optionally writes forecasts back to BigQuery.

---

## Goals

1. Demonstrate Nixtla statsforecast on BigQuery data
2. Provide serverless forecasting via HTTP API
3. Show integration with public BigQuery datasets
4. Enable GitHub Actions automated deployment

## Non-Goals

- Production-ready security
- Multi-region deployment
- Cost optimization
- Real-time streaming forecasts

---

## Functional Requirements

### FR-1: Data Reading
- Read time series from any BigQuery table
- Support grouping by dimension column
- Support WHERE clause filtering
- Support row limiting

### FR-2: Forecasting
- Run AutoETS and AutoTheta models
- Support configurable forecast horizon
- Optional TimeGPT integration (requires API key)
- Return forecasts as JSON

### FR-3: Data Writing
- Optionally write forecasts to BigQuery
- Replace or append modes
- Auto-create output table schema

### FR-4: Deployment
- Deploy via GitHub Actions
- Workload Identity Federation (keyless auth)
- Cloud Functions Gen2 runtime

---

## Non-Functional Requirements

### NFR-1: Performance
- Handle 100K+ rows input data
- Forecast latency <30 seconds for typical workloads
- Memory: 512MB-1GB Cloud Functions

### NFR-2: Dependencies
- Python 3.12 runtime
- statsforecast 2.0.3
- google-cloud-bigquery
- functions-framework

---

## API Specification

### Endpoint

```
POST https://<REGION>-<PROJECT>.cloudfunctions.net/nixtla-bigquery-forecaster
Content-Type: application/json
```

### Request Body

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
    "include_timegpt": false,
    "output_dataset": "forecast_results",
    "output_table": "forecasts",
    "limit": 1000,
    "source_project": "bigquery-public-data"
}
```

### Response

```json
{
    "status": "success",
    "metadata": {
        "source_table": "bigquery-public-data.chicago_taxi_trips.taxi_trips",
        "rows_read": 210,
        "unique_series": 7,
        "horizon": 7,
        "models_used": ["AutoETS", "AutoTheta"],
        "forecast_points_generated": 49
    },
    "forecasts": [
        {
            "unique_id": "Cash",
            "ds": "2023-02-01",
            "AutoETS": 69918.06,
            "AutoTheta": 56865.52
        }
    ],
    "output_table": "your-project.forecast_results.forecasts"
}
```

---

## User Stories

### US-1: Data Analyst
> "As a data analyst, I want to forecast BigQuery time series via API so I don't need Python setup."

**Acceptance:** POST request returns forecasts in <30 seconds.

### US-2: Nixtla Sales
> "As a Nixtla rep, I want to demo BigQuery integration using public data."

**Acceptance:** Demo uses Chicago taxi public dataset, no customer data needed.

---

## Scope

### In Scope
- HTTP API for forecasting
- BigQuery read/write
- AutoETS, AutoTheta models
- GitHub Actions deployment
- Public dataset demo

### Out of Scope
- Authentication/authorization
- Multi-region deployment
- Cost optimization
- Monitoring/alerting
- Production SLA
