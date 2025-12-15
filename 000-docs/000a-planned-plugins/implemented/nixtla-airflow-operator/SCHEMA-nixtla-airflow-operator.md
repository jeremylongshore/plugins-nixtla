# Schema: nixtla-airflow-operator

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Planned (Business Growth)

---

## Directory Tree (Planned)

```
airflow-provider-nixtla/          # PyPI package name
├── airflow_provider_nixtla/
│   ├── __init__.py
│   ├── operators/
│   │   ├── __init__.py
│   │   ├── timegpt.py            # TimeGPTForecastOperator
│   │   ├── statsforecast.py      # StatsForecastOperator
│   │   ├── bigquery.py           # NixtlaBigQueryOperator
│   │   ├── snowflake.py          # NixtlaSnowflakeOperator
│   │   └── s3.py                 # NixtlaS3Operator
│   ├── hooks/
│   │   ├── __init__.py
│   │   └── nixtla.py             # NixtlaHook (connection management)
│   └── sensors/
│       └── __init__.py
├── tests/
│   ├── operators/
│   └── hooks/
├── setup.py                       # Package setup
├── pyproject.toml                 # Modern Python packaging
└── README.md                      # Full documentation
```

---

## Operators (5 planned)

| Operator | Purpose |
|----------|---------|
| TimeGPTForecastOperator | Generate forecasts via TimeGPT API |
| StatsForecastOperator | Run local statistical models |
| NixtlaBigQueryOperator | BigQuery read/forecast/write |
| NixtlaSnowflakeOperator | Snowflake integration |
| NixtlaS3Operator | S3 input/output support |

---

## Hooks (1 planned)

| Hook | Purpose |
|------|---------|
| NixtlaHook | Connection management, API client |

---

## Connection Type

```python
# Airflow connection configuration
conn_id: nixtla_default
conn_type: nixtla
host: api.nixtla.io
password: nixak-...  # API key
```

---

## Supported Platforms

| Platform | Status |
|----------|--------|
| Apache Airflow 2.6+ | Full support |
| Google Cloud Composer | Full support |
| AWS MWAA | Full support |
| Astronomer | Full support |

---

## Example DAG

```python
from airflow_provider_nixtla.operators import TimeGPTForecastOperator

forecast_task = TimeGPTForecastOperator(
    task_id='generate_forecast',
    nixtla_conn_id='nixtla_default',
    data='{{ ti.xcom_pull("extract_data") }}',
    horizon=14,
    freq='D',
    level=[90, 95]
)
```

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Installation success | 99%+ |
| Operator failure rate | <0.1% |
| Time to first DAG | <30 minutes |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Data engineers managing Airflow DAGs
- **What:** Enable TimeGPT/StatsForecast execution within Apache Airflow
- **When:** Schedule forecasting jobs in data pipelines
- **Target Goal:** Execute forecast task in Airflow DAG successfully
- **Production:** false (planned-business-growth)
