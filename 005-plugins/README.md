# 005-plugins/ — Plugin Index

Claude Code plugins for time-series forecasting with Nixtla. Each plugin is an independent module with its own `.claude-plugin/plugin.json` manifest, scripts, and (where applicable) MCP server.

## Status legend

| Symbol | Meaning |
|---|---|
| WORKING | Loads, tests pass, primary commands run end-to-end. Listed in `.claude-plugin/marketplace.json`. |
| PARTIAL | Real implementation present; missing tests, polish, or live-execution proof. Not yet in marketplace. |
| SCAFFOLD | Manifest + skeleton only. Build epics in `bd` track these (`B1`, `B2`, `B3`). |

## Inventory (14 plugins)

### WORKING (1)

| Plugin | Version | Description |
|---|---|---|
| [nixtla-baseline-lab](nixtla-baseline-lab/) | 1.5.0 | M4 benchmark harness running statsforecast (AutoETS, AutoTheta, SeasonalNaive). Offline-capable, no API key required. Entry point for new contributors. |

### PARTIAL (10)

Real code, missing tests/polish/live-exec. Reconciliation tracked in beads epic `C0` (`nixtla-xha`).

| Plugin | Version | Description |
|---|---|---|
| [nixtla-bigquery-forecaster](nixtla-bigquery-forecaster/) | 0.1.0 | Pull from BigQuery, forecast with statsforecast, write results back. |
| [nixtla-airflow-operator](nixtla-airflow-operator/) | 0.1.0 | Custom Airflow operator wrapping TimeGPT. |
| [nixtla-snowflake-adapter](nixtla-snowflake-adapter/) | 0.1.0 | Native Snowflake integration; SDK v0.7.3 makes parts of this redundant — see `122-AA-AUDT-sdk-migration-baseline.md`. |
| [nixtla-roi-calculator](nixtla-roi-calculator/) | 0.1.0 | Cost/benefit calculator for adopting TimeGPT. |
| [nixtla-migration-assistant](nixtla-migration-assistant/) | 0.1.0 | Helper for migrating from pandas/scikit-learn forecasting to Nixtla. |
| [nixtla-vs-statsforecast-benchmark](nixtla-vs-statsforecast-benchmark/) | 0.1.0 | Side-by-side benchmark of TimeGPT vs open-source statsforecast. |
| [nixtla-cost-optimizer](nixtla-cost-optimizer/) | 0.1.0 | API-call cost analysis and optimization recommendations. |
| [nixtla-defi-sentinel](nixtla-defi-sentinel/) | 0.1.0 | DeFi protocol monitoring with anomaly detection. |
| [nixtla-forecast-explainer](nixtla-forecast-explainer/) | 0.1.0 | Plain-language explanations of forecast outputs. |
| [changelog-automation](changelog-automation/) | drift | Internal automation; PRD says 0% but partial impl exists. Reconciliation tracked in beads `C0`. |

### SCAFFOLD (3)

Manifest only or manifest + tests only. Build to WORKING tracked in beads epics `B1`/`B2`/`B3`.

| Plugin | Beads epic | Note |
|---|---|---|
| [nixtla-anomaly-streaming-monitor](nixtla-anomaly-streaming-monitor/) | `nixtla-v6n` | Real-time Kafka/Kinesis anomaly detection (planned). |
| [nixtla-dbt-package](nixtla-dbt-package/) | `nixtla-o6p` | dbt macros for SQL-first forecasting (planned). |
| [nixtla-search-to-slack](nixtla-search-to-slack/) | `nixtla-9vz` | Search → Slack digest (tests present, no commands/scripts). |

## SDK compatibility

All TimeGPT-using plugins should target **Nixtla SDK v0.7.3+** (Feb 2026 breaking changes: `NixtlaClient` class, `api_key=`, canonical env var `NIXTLA_API_KEY`, explicit `fill_gaps()`). See `000-docs/122-AA-AUDT-sdk-migration-baseline.md` for the audit and per-plugin remediation plan (beads epic `F1` / `nixtla-48n`).

> **Env var status (as of v1.9.0).** The canonical post-v0.7.3 environment variable is `NIXTLA_API_KEY`. Repo plugins currently use a mix of `NIXTLA_TIMEGPT_API_KEY` (Intent Solutions legacy variant) and `TIMEGPT_API_KEY` (legacy upstream Nixtla variant). Standardizing on `NIXTLA_API_KEY` is part of each plugin's F1 codespace live-execution gate — do not propagate the legacy variants in new code.

`nixtla-baseline-lab` keeps `nixtla` as an *optional* dep for the TimeGPT comparison path; the primary surface (statsforecast) does not need the SDK.

## Planned plugins (not yet on disk)

Six revenue-generating plugins have full PRDs in `000-docs/000a-planned-plugins/external-revenue/` but no code yet. Each has its own beads epic (`A1`–`A6`). See `000-docs/000a-planned-plugins/README.md` for the catalog.

## Developing a new plugin

1. Read `000-docs/6767-f-OD-GUIDE-enterprise-plugin-implementation.md` (implementation standard).
2. Use `nixtla-baseline-lab` as the reference structure.
3. Pin `nixtla>=0.7.3` (or use `statsforecast` only for offline-capable plugins).
4. Add to `.claude-plugin/marketplace.json` only after live-execution proof in a fresh codespace (per the per-plugin epic's gate-13).
