# dbt Package - Product Requirements Document

**Plugin:** nixtla-dbt-package
**Version:** 0.1.0
**Status:** Specified
**Last Updated:** 2025-12-12

---

## Overview

A dbt package that enables SQL-first time series forecasting using TimeGPT and StatsForecast. Analytics engineers can add forecasting to their data models without leaving the dbt workflow, using familiar SQL patterns.

---

## Problem Statement

Analytics engineering gap:
> "Our analytics engineers live in dbt. They don't want to write Python or call APIs. They want forecasting to be just another SQL transformation."

This plugin brings forecasting to the analytics engineering market.

---

## Goals

1. Provide dbt macros for TimeGPT and StatsForecast forecasting
2. Enable forecasting through SQL-only interfaces
3. Support BigQuery, Snowflake, Databricks, and Redshift
4. Integrate with dbt Cloud CI/CD workflows
5. Generate forecast models as dbt models

## Non-Goals

- Replace Python-based ML pipelines
- Support real-time streaming forecasts
- Handle complex feature engineering
- Provide model training capabilities

---

## Target Users

| User | Need |
|------|------|
| Analytics engineers | SQL-based forecasting |
| Data teams | Forecasting in existing dbt workflow |
| BI developers | Forecasts in Looker/Tableau |
| Data analysts | Self-service forecasting |

---

## Functional Requirements

### FR-1: dbt Macros
- `nixtla_forecast()` - Generate forecasts from SQL query
- `nixtla_anomaly_detect()` - Detect anomalies in time series
- `nixtla_cross_validation()` - Run backtesting
- `statsforecast_local()` - Run StatsForecast locally

### FR-2: Data Warehouse Support
- BigQuery: Native UDF integration
- Snowflake: External function support
- Databricks: UDF via Python
- Redshift: Lambda integration

### FR-3: dbt Model Generation
- Generate incremental forecast models
- Support model materialization options
- Handle forecast refresh scheduling
- Manage historical forecast versioning

### FR-4: Configuration
- YAML-based model configuration
- Per-model frequency and horizon settings
- API key management via dbt profiles
- Environment-specific settings

---

## Non-Functional Requirements

### NFR-1: Performance
- Batch processing for efficiency
- Incremental updates only forecast new data
- Caching for repeated queries

### NFR-2: Compatibility
- dbt 1.4+
- dbt Cloud support
- All major adapters (BigQuery, Snowflake, Databricks, Redshift)

### NFR-3: Developer Experience
- Familiar dbt patterns
- Clear error messages
- Comprehensive documentation
- Example models included

---

## User Stories

### US-1: SQL-Based Demand Forecasting
> "As an analytics engineer, I want to add demand forecasts to my dbt project so I can include them in our Looker dashboards without writing Python."

**Acceptance:**
- Add `dbt_nixtla` package to packages.yml
- Write SQL using `nixtla_forecast()` macro
- Run `dbt run` to generate forecasts
- Query forecasts in Looker

### US-2: dbt Cloud CI/CD
> "As a data platform lead, I want forecasts to run in our dbt Cloud CI/CD pipeline so we have version-controlled, tested forecasting."

**Acceptance:**
- Configure in dbt_project.yml
- Run in dbt Cloud jobs
- Test forecasts with dbt tests
- Alert on forecast failures

### US-3: Self-Service Analytics
> "As a business analyst, I want to create ad-hoc forecasts in SQL so I can answer business questions without waiting for data science."

**Acceptance:**
- Write SQL with forecast macros
- Preview results in dbt Cloud IDE
- Share forecast models with team

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Package installation rate | 500+ dbt projects |
| Time to first forecast | < 15 minutes |
| dbt Cloud job success rate | 99%+ |
| User satisfaction (NPS) | 50+ |

---

## Scope

### In Scope
- dbt macros for forecasting
- BigQuery, Snowflake, Databricks, Redshift support
- dbt Cloud integration
- Basic documentation and examples

### Out of Scope
- Custom model training
- Real-time streaming
- Non-dbt SQL interfaces
- GUI-based configuration

---

## API Keys Required

```yaml
# In profiles.yml or environment variables
vars:
  nixtla_api_key: "{{ env_var('NIXTLA_API_KEY') }}"
```

```bash
# Environment variable
NIXTLA_API_KEY=nixak-...
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  DBT PROJECT                                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  models/                                              │  │
│  │    staging/                                           │  │
│  │      stg_sales.sql                                   │  │
│  │    forecasts/                                         │  │
│  │      fct_sales_forecast.sql  -- Uses nixtla_forecast │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  DBT_NIXTLA PACKAGE                                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  macros/                                              │  │
│  │    nixtla_forecast.sql                               │  │
│  │    nixtla_anomaly_detect.sql                         │  │
│  │    nixtla_cross_validation.sql                       │  │
│  │    statsforecast_local.sql                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA WAREHOUSE                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ BigQuery     │  │ Snowflake    │  │ Databricks   │      │
│  │ UDF          │  │ Ext Function │  │ Python UDF   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation

```yaml
# packages.yml
packages:
  - package: nixtla/dbt_nixtla
    version: [">=0.1.0", "<1.0.0"]
```

```bash
dbt deps
```

---

## Example Usage

```sql
-- models/forecasts/fct_sales_forecast.sql

{{ config(materialized='table') }}

with historical_sales as (
    select * from {{ ref('stg_sales') }}
)

{{ nixtla_forecast(
    source_table='historical_sales',
    timestamp_col='sale_date',
    value_col='revenue',
    group_by_col='product_id',
    horizon=30,
    freq='D'
) }}
```

---

## References

- **Full Specification:** `000-docs/000b-archive-001-096/013-AT-ARCH-plugin-05-nixtla-dbt-package.md`
- **Category:** Business Growth
- **Priority:** Tier 1 (Analytics Engineering Market)
