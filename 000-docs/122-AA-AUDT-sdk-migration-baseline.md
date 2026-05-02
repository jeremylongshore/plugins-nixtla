---
doc_id: 122-AA-AUDT-sdk-migration-baseline
title: Nixtla SDK v0.7.3+ Migration Baseline Audit
date: 2026-04-29
author: Jeremy Longshore <jeremy@intentsolutions.io>
status: complete
beads_epic: nixtla-48n (F1)
---

# Nixtla SDK v0.7.3+ Migration Baseline Audit

Read-only baseline audit of every plugin under `005-plugins/` for usage of the deprecated Nixtla SDK surface. Produced as the first deliverable of beads epic F1 (`nixtla-48n`). Per-plugin remediation lands as child tasks claimed off this audit.

## Deprecated surface (v0.7.3 breaking changes, Feb 2026)

| Old | New |
|---|---|
| `from nixtla import TimeGPT` | `from nixtla import NixtlaClient` |
| `validate_token()` | `validate_api_key()` |
| `token=` kwarg | `api_key=` kwarg |
| `environment=` kwarg | `base_url=` kwarg |
| `TIMEGPT_TOKEN` env var | `NIXTLA_API_KEY` env var |
| Implicit gap-filling | Explicit `fill_gaps()` call |
| `nixtla<0.7.3` pin | `nixtla>=0.7.3` |

## Findings (14 plugin dirs)

> **Errata 2026-04-29 (post-publication correction).** The first cut of this table conflated which plugins actually pin the Nixtla SDK. Filesystem ground truth (verified by `grep -rn "nixtla" 005-plugins/*/requirements.txt 005-plugins/*/scripts/requirements.txt`):
>
> - 7 plugins pin `nixtla>=0.5.0`: airflow-operator, baseline-lab, bigquery-forecaster, cost-optimizer, defi-sentinel, migration-assistant, vs-statsforecast-benchmark
> - 5 plugins have no nixtla pin: forecast-explainer, roi-calculator, search-to-slack, snowflake-adapter, changelog-automation
> - 2 plugins are SCAFFOLD with no requirements file: anomaly-streaming-monitor, dbt-package
> - 1 root-level pin in `requirements.txt` was also `>=0.5.0`
>
> All 7 plugin pins + the root pin were bumped to `>=0.7.3` in commit `479575f` (closes child task `nixtla-3d8`). The table below reflects the corrected state.

| Plugin | TimeGPT SDK? | Pinned `nixtla` (pre/post bump) | Deprecated symbols | Effort |
|---|---|---|---|---|
| nixtla-airflow-operator | yes | `>=0.5.0` → `>=0.7.3` | none — pin only | moderate (operator pattern needs v0.7.3 API check) |
| nixtla-baseline-lab | yes (optional, for TimeGPT comparison) | `>=0.5.0` → `>=0.7.3` | none — pin only | trivial (statsforecast is the primary surface) |
| nixtla-bigquery-forecaster | yes | `>=0.5.0` → `>=0.7.3` | none — pin only | moderate (BQ→forecast→BQ flow needs verification) |
| nixtla-cost-optimizer | yes | `>=0.5.0` → `>=0.7.3` | none — pin only | trivial |
| nixtla-defi-sentinel | yes | `>=0.5.0` → `>=0.7.3` | none — pin only | trivial (pin bump) |
| nixtla-migration-assistant | yes | `>=0.5.0` → `>=0.7.3` | none — pin only | trivial |
| nixtla-vs-statsforecast-benchmark | yes | `>=0.5.0` → `>=0.7.3` | none — pin only | moderate (benchmark must reflect v0.7.3 perf) |
| nixtla-forecast-explainer | no (uses statsmodels) | unpinned | none | exempt — no Nixtla SDK |
| nixtla-roi-calculator | no (calculator only) | unpinned | none | exempt — no Nixtla SDK |
| nixtla-snowflake-adapter | no (uses snowflake-connector-python only) | unpinned | none | exempt — but see note: Nixtla SDK v0.7.3 added native Snowflake support, may want to re-evaluate |
| nixtla-search-to-slack (SCAFFOLD) | no | unpinned | none | covered under epic B3 (`nixtla-9vz`) |
| nixtla-anomaly-streaming-monitor (SCAFFOLD) | n/a (no requirements yet) | n/a | n/a | covered under epic B1 (`nixtla-v6n`) |
| nixtla-dbt-package (SCAFFOLD) | n/a (no requirements yet) | n/a | n/a | covered under epic B2 (`nixtla-o6p`) |
| changelog-automation | no | n/a | n/a | exempt (non-Nixtla; tracked under epic C0 `nixtla-xha`) |

## Executive Summary

1. **No deprecated symbol calls found** in any plugin. The `validate_token()`/`token=`/`environment=`/`TIMEGPT_TOKEN` surface is entirely absent across the codebase. This is the easy half of v0.7.3 — those plugins were either young enough to ship after the SDK matured or never used those particular APIs.

2. **Version pin is the only regression hot-path — and it has been remediated.** 7 plugin requirements files plus the root `requirements.txt` (8 locations total) pinned `nixtla>=0.5.0`, which silently let pip install pre-v0.7.3 releases. All bumped to `nixtla>=0.7.3` in commit `479575f` (closes child task `nixtla-3d8`).

3. **Effort is concentrated in API verification, not code rewrite.** No plugin needs symbol-level migration. The remaining F1 work is: live-execute each plugin against v0.7.3 in a fresh codespace to confirm nothing depends on implicit gap-filling or other behavioral changes (story #11 per plugin epic).

4. **`fill_gaps()` is the dark-horse risk.** Pre-v0.7.3, the SDK auto-filled gaps in time series; post-v0.7.3, callers must invoke `fill_gaps()` explicitly. Static analysis can't catch this — only live execution against irregular data will. Story #11 (codespace live-execution) per epic catches this; static unit tests will not.

5. **Snowflake adapter is the highest-leverage upgrade.** Nixtla SDK v0.7.3 added native Snowflake integration. The current `nixtla-snowflake-adapter` plugin should be re-evaluated against the new SDK surface — there's a chance much of the custom adapter logic can be deleted in favor of native SDK calls.

## Per-plugin remediation tasks (created from this audit)

For each non-exempt plugin in the table, F1 spawns one child task:

```text
Title: <plugin>: bump nixtla>=0.7.3 + verify against v0.7.3 SDK
Type: task
Parent: nixtla-48n
Acceptance: requirements.txt pinned >=0.7.3; live execution in codespace passes one primary forecast/anomaly call; no behavioral regression vs pre-bump.
```

Trivial-effort plugins can be batched into one PR; moderate-effort plugins each get their own.

## What this audit does NOT cover

- Plugin-level version drift across `marketplace.json`, `planned-plugins/README.md`, and per-plugin `plugin.json` (covered by F2 scoped to marketplace.json; per-plugin sync is D1).
- TimeGPT-2 family adoption (out of scope per the build plan; private preview as of 2026-04-29).
- Behavioral parity testing for forecast accuracy across SDK versions (D1 health audit).

## Provenance

- Method: `grep`/`rg` across all `005-plugins/<dir>/**/*.py` and `requirements*.txt` files for the 7 deprecated symbols and pin patterns. No execution.
- Tooling: Explore subagent for read-only grep, this document hand-written from the subagent's findings.
- Verification: spot-checked 3 plugins (nixtla-anomaly-streaming-monitor, nixtla-snowflake-adapter, nixtla-bigquery-forecaster) for missed deprecated symbols — none found.
