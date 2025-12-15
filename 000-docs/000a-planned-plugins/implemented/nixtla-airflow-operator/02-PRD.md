# Airflow Operator - Product Requirements Document

**Plugin:** nixtla-airflow-operator
**Version:** 0.1.0
**Status:** Specified
**Last Updated:** 2025-12-12

---

## Overview

Custom Apache Airflow operators for TimeGPT and StatsForecast integration. Enables data engineering teams to embed Nixtla forecasting directly into production data pipelines with proper monitoring, retry logic, and observability.

---

## Problem Statement

Enterprise data platform integration gap:
> "Data engineering teams run everything through Airflow. Without a native operator, they're writing custom Python operators that lack production-grade error handling, retry logic, and monitoring."

This plugin provides first-class Airflow integration for enterprise data platforms.

---

## Goals

1. Provide native Airflow operators for TimeGPT and StatsForecast
2. Include production-grade retry logic and error handling
3. Support connection management through Airflow connections
4. Enable monitoring via Airflow task metrics
5. Integrate with existing data warehouse operators (BigQuery, Snowflake, Redshift)

## Non-Goals

- Replace custom ML pipeline orchestration
- Support non-Airflow orchestrators (Dagster, Prefect)
- Handle model training/fine-tuning
- Provide GUI-based DAG building

---

## Target Users

| User | Need |
|------|------|
| Data engineers | Integrate forecasting into existing DAGs |
| Platform teams | Standardize forecasting across organization |
| MLOps engineers | Production-grade forecasting pipelines |
| DataOps teams | Scheduling and monitoring forecasts |

---

## Functional Requirements

### FR-1: TimeGPT Operator
- `TimeGPTForecastOperator` - Generate forecasts via API
- Support all TimeGPT parameters (horizon, freq, level)
- Handle API rate limiting and retries
- Return forecasts to XCom for downstream tasks

### FR-2: StatsForecast Operator
- `StatsForecastOperator` - Run local statistical models
- Support model selection (AutoARIMA, AutoETS, etc.)
- Handle large datasets with chunking
- Support parallel processing configuration

### FR-3: Connection Management
- Custom Airflow connection type for Nixtla
- Secure API key storage
- Support multiple environments (dev, staging, prod)

### FR-4: Data Source Integration
- `NixtlaBigQueryOperator` - Read from BigQuery, forecast, write back
- `NixtlaSnowflakeOperator` - Snowflake integration
- `NixtlaS3Operator` - S3 input/output support

### FR-5: Monitoring & Observability
- Task duration metrics
- Forecast count tracking
- API cost estimation per run
- Alert on accuracy degradation

---

## Non-Functional Requirements

### NFR-1: Compatibility
- Apache Airflow 2.6+
- Python 3.10+
- Support Composer, MWAA, Astronomer

### NFR-2: Performance
- Batch API calls for efficiency
- Configurable parallelism
- Memory-efficient for large datasets

### NFR-3: Reliability
- Exponential backoff retry logic
- Circuit breaker for API failures
- Graceful degradation options

---

## User Stories

### US-1: Daily Demand Forecasting DAG
> "As a data engineer, I want to add forecasting to my daily retail DAG so I can generate demand forecasts alongside inventory updates."

**Acceptance:**
- Drop-in operator for existing DAGs
- Configurable via Airflow variables
- Output to BigQuery/Snowflake

### US-2: Multi-Tenant Forecasting
> "As a platform engineer, I want to run forecasts for 100+ tenants in a single DAG so I can scale without managing individual pipelines."

**Acceptance:**
- Support dynamic task mapping
- Per-tenant configuration
- Aggregate cost tracking

### US-3: Monitoring Integration
> "As an MLOps engineer, I want forecasting metrics in Datadog/Prometheus so I can monitor pipeline health alongside other ML systems."

**Acceptance:**
- Export standard metrics
- Support custom metric labels
- Alert on anomalies

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Installation success rate | 99%+ |
| Operator failure rate | < 0.1% |
| Time to first successful DAG | < 30 minutes |
| Enterprise adoption (Airflow users) | 20% of TimeGPT customers |

---

## Scope

### In Scope
- TimeGPT forecast operator
- StatsForecast operator
- BigQuery/Snowflake/S3 data operators
- Airflow connection management
- Basic monitoring metrics

### Out of Scope
- Dagster/Prefect integrations
- Custom model training operators
- Airflow UI plugins
- GUI-based DAG building

---

## API Keys Required

```bash
# Airflow connection (conn_id: nixtla_default)
# Connection type: nixtla
# Host: api.nixtla.io
# Password: nixak-...          # API key

# Optional environment variables
NIXTLA_API_KEY=nixak-...       # Fallback if connection not set
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  AIRFLOW DAG                                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  extract_data >> TimeGPTForecastOperator >> load     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OPERATORS (airflow-provider-nixtla)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - TimeGPTForecastOperator                           │  │
│  │  - StatsForecastOperator                             │  │
│  │  - NixtlaBigQueryOperator                            │  │
│  │  - NixtlaSnowflakeOperator                           │  │
│  │  - NixtlaS3Operator                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  HOOKS (Connection Management)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - NixtlaHook (API client)                           │  │
│  │  - Connection type: nixtla                           │  │
│  │  - Secure credential storage                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation

```bash
pip install airflow-provider-nixtla

# Or with extras
pip install airflow-provider-nixtla[bigquery,snowflake]
```

---

## References

- **Full Specification:** `000-docs/000b-archive-001-096/012-AT-ARCH-plugin-04-nixtla-airflow-operator.md`
- **Category:** Business Growth
- **Priority:** Tier 1 (Enterprise Data Platform)
