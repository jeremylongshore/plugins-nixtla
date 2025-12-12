# BigQuery Forecaster - Business Case

**Plugin:** nixtla-bigquery-forecaster
**Category:** Business Growth
**Status:** Implemented (Demo)
**Last Updated:** 2025-12-12

---

## Problem Statement

Organizations with time series data in BigQuery face friction when applying Nixtla forecasting models:

- Manual data export from BigQuery to Python
- Custom code to run statsforecast models
- No serverless deployment option
- No integration with existing data pipelines

## Solution

A Cloud Functions-based forecaster that reads time series data from BigQuery, runs statsforecast models, and optionally writes results back to BigQuery.

---

## Target Users

1. **Data Engineers**: Need serverless forecasting integrated with BigQuery pipelines
2. **Analytics Teams**: Want SQL-accessible forecasts without Python expertise
3. **Nixtla Sales**: Demo showing enterprise BigQuery integration

---

## Value Proposition

| Without Plugin | With Plugin |
|---------------|-------------|
| Manual data export | Direct BigQuery read |
| Custom Python scripts | HTTP API call |
| Local execution | Serverless Cloud Functions |
| No scalability | Auto-scaling |

---

## Demo Use Case

Uses **public** Chicago taxi dataset (bigquery-public-data.chicago_taxi_trips):

- 200M+ rows available
- No customer data required
- Demonstrates real-world scale
- Zero setup for demo

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Deploy time | <5 minutes | ~3 minutes (GitHub Actions) |
| Forecast latency | <30 seconds | ~10-15 seconds |
| Max series tested | 100+ | 100+ verified |

---

## Limitations

This is a **demo/prototype**, NOT production-ready:

- No authentication beyond Cloud Functions default
- No rate limiting
- No monitoring/alerting
- Single region deployment
- Cost optimization not implemented

---

## Competitive Landscape

| Alternative | Limitation |
|-------------|------------|
| BigQuery ML | Limited model selection |
| Vertex AI Forecasting | Complex setup, higher cost |
| Custom Cloud Run | More maintenance |
| **This Plugin** | Showcase integration |

---

## Recommendation

**Status: DEMO** - Working prototype that demonstrates Nixtla + BigQuery integration. Suitable for demos and proof-of-concept. Not designed for production workloads.
