# Nixtla Airflow Operator

Real Airflow tooling for production TimeGPT forecasting pipelines. Generates DAGs targeting BigQuery / Snowflake / Postgres / S3, validates them via AST + (when available) DagBag, produces real Airflow Connection JSON for 5 source types, and emits pytest test modules that exercise the DAG structure.

**Version**: 1.0.0 · **Status**: Working · **API key needed**: For runtime, `NIXTLA_API_KEY` (Airflow tasks call `NixtlaClient`)

---

## 30-second pitch

Most Nixtla customers running production forecasts need an Airflow pipeline. This plugin produces a real one — extract from your warehouse, run TimeGPT, write back — with retry logic + email alerts + per-source connection config + a pytest module that asserts the DAG loads, has the expected tasks, and has no orphans.

---

## Quick start

```bash
cd 005-plugins/nixtla-airflow-operator
pip install -r scripts/requirements.txt

# In Claude Code:
# 1. "Generate an Airflow DAG named retail_forecast for BigQuery, daily, horizon 14."
# 2. "Validate that DAG file."
# 3. "Configure an Airflow connection for nixtla with my API key."
# 4. "Generate the pytest module for retail_forecast."
```

---

## MCP tools

| Tool | What it does |
|---|---|
| `generate_dag` | Real Python DAG file: `extract_data → run_forecast → load_results`, default_args + retries + email alerts, BigQuery/Snowflake/Postgres/S3 sources |
| `validate_dag` | Syntax check + AST extraction (task IDs, DAG id, duplicates) + optional DagBag load (when airflow installed) + lint for hardcoded credentials / missing schedule / missing default_args |
| `configure_connection` | Real Airflow Connection JSON for **nixtla**, **bigquery**, **snowflake**, **postgres**, **s3** + the `airflow connections add` CLI command |
| `generate_tests` | Real pytest module that loads the DAG via DagBag and asserts: import errors empty, DAG present, expected task IDs, no orphan tasks |

---

## Connection types supported

`configure_connection` produces real Airflow Connection JSON for:

| Source | Required config | Notes |
|---|---|---|
| `nixtla` | `api_key` | HTTP connection, password = api_key |
| `bigquery` | `project_id` (+ optional `key_path`) | google_cloud_platform conn_type |
| `snowflake` | `account`, `user`, `password`, `warehouse`, `database`, `schema` | host = `<account>.snowflakecomputing.com` |
| `postgres` | `host`, `port`, `user`, `password`, `database` | postgres conn_type |
| `s3` | `aws_access_key_id`, `aws_secret_access_key` (+ optional `region_name`) | aws conn_type, defaults region us-east-1 |

Returns the JSON + the exact `airflow connections add <conn_id> --conn-json '<json>'` CLI command.

---

## Validator catches

`validate_dag` catches these in addition to syntax:

- **Duplicate `task_id`** — common copy-paste bug; flagged as error
- **Hardcoded credentials** — `password=`, `api_key=`, `secret=`, AWS access key IDs (`AKIA...`); flagged as warning unless they reference `Variable.get` or `var.value`
- **Missing `schedule_interval` / `schedule`** — warning
- **Missing `default_args`** — warning (no retries / email config)
- **DagBag import errors** (when airflow is installed in the environment) — error

---

## Tests

```bash
cd 005-plugins/nixtla-airflow-operator
PYTHONPATH=scripts pytest tests/ --cov=airflow_mcp -v
```

25 tests covering DAG generation template substitution, validate_dag (valid/syntax-error/dupes/hardcoded creds/missing default_args/missing file), all 5 connection types with required-field validation, generate_tests with task ID extraction + default fallback, and async MCP dispatch.

---

## License

MIT — Jeremy Longshore.
