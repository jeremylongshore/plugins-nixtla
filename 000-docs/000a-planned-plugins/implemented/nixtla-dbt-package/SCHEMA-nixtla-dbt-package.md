# Schema: nixtla-dbt-package

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Planned (Business Growth)

---

## Directory Tree (Planned)

```
dbt_nixtla/                        # dbt Hub package name
├── dbt_project.yml                # dbt project definition
├── macros/
│   ├── nixtla_forecast.sql        # {{ nixtla_forecast() }} macro
│   ├── nixtla_anomaly_detect.sql  # {{ nixtla_anomaly_detect() }} macro
│   ├── nixtla_cross_validation.sql# {{ nixtla_cross_validation() }} macro
│   └── statsforecast_local.sql    # {{ statsforecast_local() }} macro
├── models/
│   └── examples/
│       ├── fct_sales_forecast.sql # Example forecast model
│       └── schema.yml             # Model documentation
├── adapters/
│   ├── bigquery/                  # BigQuery UDF integration
│   ├── snowflake/                 # Snowflake external function
│   ├── databricks/                # Databricks Python UDF
│   └── redshift/                  # Redshift Lambda integration
├── tests/
│   └── test_macros.sql
├── integration_tests/
│   └── test_forecast_model.sql
└── README.md                      # Full documentation
```

---

## dbt Hub Package

```yaml
# packages.yml
packages:
  - package: nixtla/dbt_nixtla
    version: [">=0.1.0", "<1.0.0"]
```

---

## Macros (4 planned)

| Macro | Purpose |
|-------|---------|
| nixtla_forecast() | Generate forecasts from SQL query |
| nixtla_anomaly_detect() | Detect anomalies in time series |
| nixtla_cross_validation() | Run backtesting |
| statsforecast_local() | Run StatsForecast locally |

---

## Data Warehouse Support

| Warehouse | Integration Type | Status |
|-----------|-----------------|--------|
| BigQuery | Native UDF | Phase 1 |
| Snowflake | External function | Phase 1 |
| Databricks | Python UDF | Phase 1 |
| Redshift | Lambda integration | Phase 2 |

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

## Configuration

```yaml
# dbt_project.yml
vars:
  nixtla_api_key: "{{ env_var('NIXTLA_API_KEY') }}"
  default_horizon: 14
  default_freq: 'D'
  confidence_levels: [80, 90, 95]
```

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Package installation | <15 minutes |
| dbt Cloud job success | 99%+ |
| NPS score | 50+ |
| Adoption | 500+ dbt projects |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Analytics engineers, data teams
- **What:** Native dbt integration for TimeGPT forecasting
- **When:** Generate forecasts as part of dbt jobs
- **Target Goal:** dbt run completes with forecast table materialized
- **Production:** false (planned-business-growth)
