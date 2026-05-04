# dbt_nixtla v1.0.0

Native dbt package for TimeGPT forecasting + anomaly detection across data warehouses.

**Posture**: BigQuery is the **canonical** implementation. Snowflake and Databricks adapters ship as **honest PoCs** — the underlying integrations (Nixtla Snowflake Native App, registered Databricks Python UDF) are external dependencies the package does not own.

## Installation

Add to your `packages.yml`:

```yaml
packages:
  - package: nixtla/dbt_nixtla
    version: [">=1.0.0", "<2.0.0"]
```

Then run:

```bash
dbt deps
```

## Configuration

Add to your `dbt_project.yml`:

```yaml
vars:
  nixtla_api_key: "{{ env_var('NIXTLA_API_KEY') }}"
  default_horizon: 14
  default_freq: 'D'
  confidence_levels: [80, 90, 95]
```

## Macros

### nixtla_forecast

Generate forecasts from time series data:

```sql
{{ nixtla_forecast(
    source_table='my_data',
    timestamp_col='ds',
    value_col='y',
    group_by_col='unique_id',
    horizon=30,
    freq='D'
) }}
```

### nixtla_anomaly_detect

Detect anomalies in time series:

```sql
{{ nixtla_anomaly_detect(
    source_table='my_data',
    timestamp_col='ds',
    value_col='y',
    level=95
) }}
```

## Supported Warehouses (v1.0 honest matrix)

| Warehouse | Status | Integration | Notes |
|-----------|--------|-------------|-------|
| BigQuery | **Canonical** | BQML `ML.FORECAST` | Production-ready. Set `var('nixtla_bq_model')` to your trained BQML model name; the macro emits the standard `ML.FORECAST` SELECT against it. |
| Snowflake | **PoC** | Nixtla Snowflake Native App | Macro emits `CALL NIXTLA.FORECAST(...)`. Requires the Nixtla Native App installed in your Snowflake account (currently a private Nixtla deployment — contact Nixtla for access). |
| Databricks | **PoC** | External Python UDF | Macro calls `nixtla_forecast_udf(...)` which you must register yourself (Nixtla SDK + spark UDF wrapper). No registration helper bundled in this package. |
| Redshift | Not supported | — | Roadmap item; would need a Lambda invocation pattern. Macro raises a compiler error if you target Redshift. |

**Why this matters**: the BigQuery adapter is buildable and runs end-to-end with public BQML credentials. The Snowflake / Databricks adapters compile to syntactically valid SQL but require infrastructure outside this package. Treat them as templates, not turnkey integrations.

## Example Model

See `models/examples/fct_sales_forecast.sql` for a complete example.

## License

MIT
