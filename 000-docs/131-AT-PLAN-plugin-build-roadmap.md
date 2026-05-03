# 131-AT-PLAN — Plugin Build Roadmap

| | |
|---|---|
| **Status** | Proposed — awaiting principal approval before bead creation |
| **Date** | 2026-05-03 (CST) |
| **Source of truth** | `000-docs/000a-planned-plugins/README.md` (researched demand; v2.0.0 dated 2025-12-15) |
| **Maintained by** | Intent Solutions × Nixtla |

---

## Intent

Anchor every bead-tracked engineering effort in the repo to the planned-plugins README's research. Every plugin gets exactly one epic; every epic decomposes into sequenced child beads with concrete acceptance criteria. This document is the build queue. When a plugin epic is closed, the plugin is a real working product a Nixtla customer can install and use.

This plan is read-only research until approved. **No beads are created from this plan until principal greenlights the epic structure.** Once approved, epics + child beads land in one batch (not editorial-by-editorial).

---

## Canonical validators (source of truth)

Every plugin epic's acceptance gate references these. Local `004-scripts/validate_skills_v2.py` is **not authoritative** — it's a vendored copy that drifts. The canonical validators live in the `claude-code-plugins` repo.

| Validator | Path | What it checks |
|---|---|---|
| **Claude Code Plugin Validator v7.0** (schema 3.3.1) | `~/000-projects/claude-code-plugins/scripts/validate-skills-schema.py` | SKILL.md frontmatter against the IS enterprise 8-field set (`name, description, allowed-tools, version, author, license, compatibility, tags`); two tiers (`standard` mirrors Anthropic spec, `marketplace` enforces IS strict); `--deep` adds 10-dimension analysis with badges + Elo. |
| **SkillMD validator (slash command)** | `/validate-skillmd` | Same engine wrapped as a Claude Code skill. Default = standard tier; `--marketplace` flag = strict tier; `--deep` = full evaluation. |
| **Bulk remediator** | `~/000-projects/claude-code-plugins/scripts/batch-remediate.py` | Applies migrations (e.g., deprecated `compatible-with` CSV → free-text `compatibility`) when the validator surfaces them. |
| **Schema spec** | `~/000-projects/claude-code-plugins/000-docs/6767-b-SPEC-DR-STND-claude-skills-standard.md` | The master spec the validator enforces. |
| **Schema changelog** | `~/000-projects/claude-code-plugins/000-docs/SCHEMA_CHANGELOG.md` | Non-negotiables and version history. **Read before touching the validator.** |

Every plugin epic must have a child bead that runs these against every SKILL.md the plugin ships, plus marketplace tier on the plugin's manifest entries. **Validator gates are not optional.**

For each plugin's `plugin.json` manifest itself (separate from skills), the same validator runs in marketplace tier — it understands plugin-level metadata too.

---

## Standard child-bead templates

Two templates depending on starting state.

### Template A — Fix existing claimed-implemented plugin (currently stub-quality)

```
1. <plugin>: implement stub: <tool name> #1
2. <plugin>: implement stub: <tool name> #2
   ... (one bead per stubbed tool)
N. <plugin>: pytest unit tests, coverage ≥ 80%
N+1. <plugin>: per-plugin CI workflow (paths + pytest + black + validator gate)
N+2. <plugin>: README quickstart + usage examples + troubleshooting
N+3. <plugin>: claude plugin install smoke verification
N+4. <plugin>: VALIDATOR GATE — run claude-code-plugins v7.0 validator (marketplace tier)
                against every SKILL.md the plugin ships AND against plugin.json
                manifest. Must pass with zero errors. Run via:
                `python ~/000-projects/claude-code-plugins/scripts/validate-skills-schema.py
                --tier marketplace --target 005-plugins/<plugin>/`
                or via the `/validate-skillmd --marketplace` slash command per skill.
N+5. <plugin>: version bump + plugin.json sync (and marketplace entry if applicable)
```

Effort: typically 1–3 days per epic depending on stub count.

### Template B — Greenfield from PRD

```
1. <plugin>: read PRD + write build spec into bead description
2. <plugin>: scaffold plugin.json, .mcp.json, directory structure (using
             the IS enterprise 8-field set so the validator passes from
             day one — name, description, allowed-tools, version, author,
             license, compatibility, tags)
3. <plugin>: MCP server skeleton with declared tool registration
4. <plugin>: implement core tool: <name> #1
5. <plugin>: implement core tool: <name> #2
   ... (one bead per declared tool from PRD)
M. <plugin>: auxiliary helpers (templates, dataset bundles, integrations)
M+1. <plugin>: pytest unit tests
M+2. <plugin>: pytest integration tests (where external infra exists)
M+3. <plugin>: per-plugin CI workflow with validator gate baked in
M+4. <plugin>: README + setup guide + quickstart
M+5. <plugin>: claude plugin install smoke verification
M+6. <plugin>: VALIDATOR GATE — claude-code-plugins v7.0 marketplace tier on
               every SKILL.md + plugin.json. Zero errors required.
M+7. <plugin>: v1.0 release artifact (tag + GitHub release notes)
```

Effort: matches the PRD's estimate (3–12 weeks per plugin).

### Template C — Already-working plugin polish

```
1. <plugin>: pytest migration (if homegrown smoke runner exists)
2. <plugin>: per-plugin CI gate (with validator step)
3. <plugin>: README freshening
4. <plugin>: smoke verification
5. <plugin>: VALIDATOR GATE — claude-code-plugins v7.0 marketplace tier
              passes on every SKILL.md + plugin.json
6. <plugin>: version bump to 1.0
```

Effort: 1–2 days per epic.

### Template D — Honest PoC labeling

```
1. <plugin>: PROOF OF CONCEPT banner in README + module docstring
2. <plugin>: stub returns include explicit PoC disclaimer
3. <plugin>: origin / motivation section in README
4. <plugin>: VALIDATOR GATE — claude-code-plugins v7.0 marketplace tier
              still passes on the plugin manifest + any SKILL.md (PoC plugins
              must still meet the schema even if their tools return PoC text)
```

Effort: half-day per epic.

---

## Build sequence

Five phases. Earlier phases unblock later ones (CI pattern from Phase 1 reused in Phase 2; shared infra patterns reused throughout).

| Phase | Theme | Plugins | Total effort |
|---|---|---|---|
| **1** | Stop deceiving customers — fix existing stubs | 7 plugins (Tier-1 fix) | ~2–3 weeks |
| **2** | Polish already-working plugins to v1.0 | 4 plugins (Tier-2 polish) | ~1 week |
| **3** | Honest PoC labeling | 2 plugins (defi-sentinel, streaming-monitor) | ~1 day |
| **4** | High-priority greenfield from PRDs | 3 plugins (sales-demo-builder, workflow-templates, audit-report) | 17 weeks per PRDs |
| **5** | Medium-priority greenfield | 3 plugins (support-deflector, docs-qa-generator, embedded-widget) | 17–22 weeks per PRDs |

Phase 1 first because: a Nixtla customer who installs `nixtla-roi-calculator` today and runs `generate_report` gets a placeholder string back. That is worse than the plugin not existing. Every day Phase 1 is delayed is a day customers can be misled.

Phase 4 high-priority greenfield is anchored on the planned-plugins README's stated High priorities — Sales Demo Builder, Workflow Templates, Audit Report — in that order (smallest effort first, validating the build template).

---

## Phase 1 — Fix existing stubs (Tier 1)

Seven epics. All Template A. Listed easiest → hardest by stub count and infra complexity.

### Epic 1.1 — `nixtla-roi-calculator` v1.0

**Current**: 4 tools, 1 real (`calculate_roi` — TCO math works), 3 stubs returning placeholder strings.

**Child beads**:
1. Implement `generate_report` — real PDF via reportlab, sections: title page, exec summary (3yr ROI, payback, NPV), cost breakdown table, FTE savings, recommendations.
2. Implement `compare_scenarios` — run `calculate_roi` on each scenario, return ranked comparison + sensitivity analysis.
3. Implement `export_salesforce` — POST to SF REST API using `NIXTLA_SF_INSTANCE_URL` + `NIXTLA_SF_ACCESS_TOKEN` env vars; if absent, return shaped JSON payload that *would* be sent (testable without live SF).
4. Pytest tests covering all 4 tools (≥80% coverage on `roi_calculator_mcp.py`).
5. Per-plugin CI workflow (`.github/workflows/nixtla-roi-calculator-ci.yml`).
6. README quickstart + env-var matrix + troubleshooting.
7. `claude plugin install` smoke verification (transcript captured in close-reason).
8. Version bump 0.1.0 → 1.0.0; sync `plugin.json` (URL fixes already done in PR #11 pattern).

**DoD**: Nixtla customer runs `calculate_roi` → gets numeric result; runs `generate_report` → gets real PDF; runs `compare_scenarios` → gets ranked comparison; runs `export_salesforce` → either creates real SF Opportunity or gets the configurability message.

**Effort**: ~2 days.

### Epic 1.2 — `nixtla-forecast-explainer` v1.0

**Current**: 5 tools, 2 real (narrative templating + risk assessment), 2 stubs, 1 partial (decompose_forecast is passthrough).

**Child beads**:
1. Implement `decompose_forecast` — real STL via `statsmodels.tsa.seasonal.STL`. Return trend/seasonal/residual + Hyndman strength metrics.
2. Implement `identify_drivers` — Pearson correlation analysis with optional lag (1–7 periods) using scipy.stats.
3. Implement `generate_report` — real markdown composition combining decompose + drivers + risk + narrative outputs.
4. Pytest tests with synthetic seasonality + known drivers (verifiable expected outputs).
5. Per-plugin CI workflow.
6. README quickstart with example STL output.
7. Smoke verification.
8. Version bump 0.1.0 → 1.0.0.

**Effort**: ~2 days.

### Epic 1.3 — `nixtla-vs-statsforecast-benchmark` v1.0

**Current**: 4 tools, 1 real (CSV loader), 2 stubs, 1 partial.

**Child beads**:
1. Implement `run_benchmark` — real `StatsForecast([AutoETS, AutoTheta, SeasonalNaive])` runs + optional `NixtlaClient` (when `NIXTLA_API_KEY` set). Compute sMAPE/MASE/MAE/RMSE on holdout split. Return per-engine metrics + wall time + winner.
2. Implement `get_recommendations` — rule-based recommendations from benchmark dict (TimeGPT-skipped path, accuracy-vs-speed tradeoffs).
3. Implement `generate_report` — markdown report with metrics table, wall-time comparison, winner verdict, recommendations.
4. Pytest tests with M4 sample data fixtures (deterministic).
5. Per-plugin CI workflow.
6. README quickstart.
7. Smoke verification.
8. Version bump 0.1.0 → 1.0.0.

**Effort**: ~2–3 days.

### Epic 1.4 — `nixtla-cost-optimizer` v1.0

**Current**: 5 tools, 2 real (`analyze_usage`, `simulate_batching`), 3 stubs.

**Child beads**:
1. Implement `recommend_optimizations` — heuristic engine that consumes `analyze_usage` output and returns ranked recommendations with savings estimates + implementation steps.
2. Implement `generate_hybrid_strategy` — rules engine producing routing decision tree (TimeGPT vs statsforecast) as code snippet + JSON config.
3. Implement `export_report` — multi-format output (markdown/json/csv).
4. Pytest tests.
5. Per-plugin CI workflow.
6. README + cost-model worked example.
7. Smoke verification.
8. Version bump 0.1.0 → 1.0.0.

**Effort**: ~2 days.

### Epic 1.5 — `nixtla-migration-assistant` v1.0

**Current**: 5 tools, 2 real (`analyze_code` AST parsing, `generate_code` template subst), 3 stubs.

**Child beads**:
1. Implement `transform_data` — Prophet/statsmodels/sklearn → Nixtla schema. Validate `ds`/`y`/`unique_id` columns; configurable NaN strategy.
2. Implement `compare_accuracy` — fit source model + Nixtla model on same data, compare sMAPE/MAE on holdout. Optional deps imported via try/except.
3. Implement `generate_plan` — phased migration plan derived from `analyze_code` output (line counts → phase sizing).
4. Pytest tests.
5. Per-plugin CI workflow.
6. README with worked Prophet→Nixtla migration example.
7. Smoke verification.
8. Version bump 0.1.0 → 1.0.0.

**Effort**: ~3 days (most complex Phase 1 epic — multiple optional deps, real model fits).

### Epic 1.6 — `nixtla-airflow-operator` v1.0

**Current**: 4 tools, 1 real (`generate_dag` produces real DAG Python code), 3 stubs.

**Child beads**:
1. Implement `validate_dag` — `compile()` syntax check + optional `airflow.models.dagbag.DagBag` load + AST-based dependency cycle check + lint (deprecated patterns, hardcoded creds).
2. Implement `configure_connection` — return Airflow Connection JSON for `nixtla|bigquery|snowflake|postgres|s3` + `airflow connections add` CLI command.
3. Implement `generate_tests` — produce a real pytest module (DAG load test, structure tests, per-task stubs).
4. Pytest tests for the validator/connection/test-generator themselves.
5. Per-plugin CI workflow.
6. README + worked DAG example.
7. Smoke verification.
8. Version bump 0.1.0 → 1.0.0.

**Effort**: ~2–3 days.

### Epic 1.7 — `changelog-automation` v1.0

**Current**: 3 tools, 1 real (`get_changelog_config`), 2 partials with explicit "Week 1/2 TODO" markers.

**Child beads**:
1. Implement `fetch_changelog_data` (Week 2 TODO) — `gh` CLI subprocess for GitHub PRs/issues + `git log` parsing + optional Slack via the **CCS repo's canonical patterns** (`~/000-projects/claude-code-slack-channel/`, per principal direction).
2. Implement `validate_frontmatter` (Week 1 TODO) — `jsonschema.Draft7Validator` against a defined CHANGELOG schema (version, date, type, categories, audience, breaking_changes).
3. Pytest tests (mock gh + git subprocess calls).
4. Per-plugin CI workflow.
5. README quickstart.
6. Smoke verification.
7. Version bump (current is "drift" per planned-plugins README) → 1.0.0.

**Effort**: ~2 days.

---

## Phase 2 — Polish already-working plugins (Tier 2)

Four epics. All Template C.

### Epic 2.1 — `nixtla-baseline-lab` 1.5.0 → 1.0 hardening

**Current**: A− per audit. Real working: 5 MCP tools, 1925-line server, 3 documented skills, golden-task smoke harness. Gaps: homegrown smoke runner (not pytest), no per-plugin CI gate, no committed golden output CSVs/plots.

**Child beads**:
1. Migrate `tests/run_baseline_m4_smoke.py` → pytest (preserve golden_tasks/baseline_m4_smoke.yaml semantics).
2. Per-plugin CI workflow (PR #11 already fixed the path filter; this adds the pytest gate).
3. Commit golden output CSVs + reference plots to `examples/`.
4. README freshening (any drift since v1.5.0).
5. Smoke verification.

**Effort**: ~1–2 days.

### Epic 2.2 — `nixtla-search-to-slack` v0.2 → v1.0

**Current**: 1.5K LOC across 7 modules, 5 pytest suites at 70–85% coverage, 24K SETUP_GUIDE, real Slack/SerpAPI/AI integration.

**Child beads**:
1. Verify `claude plugin install` loads cleanly on fresh clone.
2. Wire 3 declared skills as Claude-Code-discoverable skills.
3. **Use `~/000-projects/claude-code-slack-channel/` (CCS repo) patterns for any Slack code refactors** (per principal direction — don't reinvent).
4. Optional: Claude WebSearch fallback to drop SerpAPI cost dependency.
5. Real Slack-bot smoke test (private workspace, transcript captured).
6. Per-plugin CI gate (verify ≥80% coverage threshold).
7. Version bump 0.2.0 → 1.0.0.

**Effort**: ~1 day.

### Epic 2.3 — `nixtla-snowflake-adapter` v0.1 → v1.0

**Current**: 4/4 tools real (`generate_forecast_sql`, `validate_setup`, `generate_anomaly_sql`, `export_looker_view`). Per audit, this is fully working.

**Child beads**:
1. Real integration tests against a Snowflake test account (CI uses GH-secrets-stored creds).
2. Per-plugin CI workflow.
3. README quickstart + worked example with seed schema.
4. Smoke verification.
5. Version bump 0.1.0 → 1.0.0.

**Effort**: ~1–2 days. Blocker: requires Snowflake test account access.

### Epic 2.4 — `nixtla-bigquery-forecaster` demo → production

**Current**: 543 LOC, real GCP integration via Workload Identity Federation. Audit gaps: SQL injection vector in column-name f-strings, no retry/backoff, no caching, no enterprise auth/deploy guide.

**Child beads**:
1. Parameterize all column names in `bigquery_connector.py` `read_timeseries()` (security fix).
2. Add `google.api_core.retry` with exponential backoff for BQ quota errors.
3. Add timeout to blocking `job.result()` calls.
4. Optional response cache layer (Redis or local).
5. Surface BQ query cost estimate (DRY_RUN) in response.
6. Terraform/gcloud "deploy to your own GCP project" guide.
7. Pytest unit tests with BQ mocks (offline-runnable in CI).
8. Per-plugin CI gate (separate gate for live integration tests requiring GCP creds).
9. Version bump 0.1.0 → 1.0.0.

**Effort**: ~3 days.

---

## Phase 3 — Honest PoC labeling

Two epics. Template D.

### Epic 3.1 — `nixtla-defi-sentinel` honest PoC

**Current**: 6/6 mock returns. Per principal: built in response to a real DeFi exploit as anomaly-detection demonstration; intentionally PoC, not production.

**Child beads**:
1. PROOF OF CONCEPT banner in README. Origin section explaining the exploit motivation.
2. Module docstring + each stub return labeled with explicit `[PoC]` disclaimer + production-gap notes.
3. `plugin.json` description updated to reflect PoC status.

**Effort**: half-day. Do NOT implement live integrations.

### Epic 3.2 — `nixtla-anomaly-streaming-monitor` PoC

**Current**: 10 files, all 6 MCP tools return mocks, no Kafka/Kinesis consumer code. Pure scaffold.

**Disposition** (principal-decided 2026-05-03): **keep as PoC with honest labeling**, same treatment as `nixtla-defi-sentinel`. Do not drop.

**Child beads**:
1. PROOF OF CONCEPT banner in README. Production-gap matrix (what's mocked vs what would need to land — Kafka/Kinesis consumers, alert delivery to PagerDuty/Slack/Email, real anomaly detection on streamed data).
2. Module docstring + each of the 6 stub returns labeled with explicit `[PoC]` disclaimer + `_disclaimer` field in dict shapes (don't change response schemas — keep the API surface developable-against).
3. `plugin.json` description updated to reflect PoC status.
4. Origin section in README — what the plugin demonstrates and why it exists.

**Effort**: half-day. Do NOT implement live integrations.

---

## Phase 4 — High-priority greenfield (planned-plugins README "High")

Three epics. Template B. Sequenced by ascending PRD effort to validate the greenfield template before larger builds.

### Epic 4.1 — `nixtla-sales-demo-builder` v1.0 (3 weeks per PRD)

**Source PRD**: `000-docs/000a-planned-plugins/external-revenue/nixtla-sales-demo-builder/`

**Goal**: Generate industry-specific demo notebooks (retail, energy, finance, healthcare) for Nixtla's sales team. Demo prep: 4 hours → 15 minutes.

**Child beads** (high-level — refine on epic claim):
1. Read 6-doc PRD set, write build spec into bead description.
2. Scaffold `plugin.json`, `.mcp.json`, directory structure.
3. MCP server skeleton with declared tools (e.g., `generate_demo`, `list_verticals`, `render_notebook`, `export_pptx`).
4. Implement `generate_demo` core (vertical templates + dataset binding).
5. Implement vertical-specific templates: retail (M5), energy (ERCOT-style), finance (Yahoo Finance), healthcare (CDC).
6. Implement `render_notebook` (jupyter `nbformat`).
7. Implement `export_pptx` (python-pptx).
8. Public dataset integration helpers.
9. Pytest tests with notebook-execution validation.
10. Per-plugin CI workflow.
11. README + setup guide.
12. Smoke verification.
13. v1.0 release artifact.

**Effort**: 3 weeks per PRD.

### Epic 4.2 — `nixtla-forecast-workflow-templates` v1.0 (6 weeks per PRD)

**Source PRD**: `000-docs/000a-planned-plugins/external-revenue/nixtla-forecast-workflow-templates/`

**Goal**: Marketplace of pre-built workflow templates ($99–499 each). Direct revenue + 3× API consumption.

**Child beads** (refine on epic claim — likely 12–18 child beads given marketplace + runtime + scheduler scope).

**Effort**: 6 weeks per PRD.

### Epic 4.3 — `nixtla-forecast-audit-report` v1.0 (8 weeks per PRD)

**Source PRD**: `000-docs/000a-planned-plugins/external-revenue/nixtla-forecast-audit-report/`

**Goal**: Compliance documentation (SOX, FDA, Basel III, IFRS 9). Unlocks regulated-industry deals.

**Child beads** (refine on epic claim — likely 14–20 child beads given multi-framework template work).

**Effort**: 8 weeks per PRD.

---

## Phase 5 — Medium-priority greenfield

Three epics. Template B.

### Epic 5.1 — `nixtla-support-deflector` v1.0 (4–6 weeks)

**Source PRD**: `000-docs/000a-planned-plugins/external-revenue/nixtla-support-deflector/`

**Goal**: AI-powered ticket triage with RAG over Nixtla docs. 50% faster response, 30% auto-resolution.

### Epic 5.2 — `nixtla-docs-qa-generator` v1.0 (3–4 weeks)

**Source PRD**: `000-docs/000a-planned-plugins/external-revenue/nixtla-docs-qa-generator/`

**Goal**: Monitor SDK changes, generate doc updates, validate code examples. 80% reduction in "docs wrong" tickets.

### Epic 5.3 — `nixtla-embedded-forecast-widget` v1.0 (10–12 weeks, Y2 flagship)

**Source PRD**: `000-docs/000a-planned-plugins/external-revenue/nixtla-embedded-forecast-widget/`

**Goal**: White-label React component for SaaS embedding. $200–500K Y2 ARR per PRD.

---

## Phase 0 — `nixtla-dbt-package` BigQuery-canonical (parallel-runnable; not blocking Phase 1)

Listed separately because it's neither stub-fix nor greenfield — it's a partially-scaffolded SQL package.

**Current**: `dbt_project.yml` configured, 2 dispatcher macros, 4 EMPTY adapter directories, 1 example model, no tests, no `packages.yml`, no seed data.

**Child beads**:
1. Implement BigQuery adapter macros: `nixtla_forecast_bigquery.sql` (BQML `ML.FORECAST`) + `nixtla_anomaly_detect_bigquery.sql` (`ML.DETECT_ANOMALIES`).
2. Snowflake / Databricks adapter directories: PoC stubs with clear "requires Nixtla Native App" comment + `exceptions.raise_compiler_error`.
3. Redshift directory: drop or keep PoC (Redshift not on Nixtla supported list per their docs).
4. `packages.yml` with project metadata.
5. Seed data: `data/seed_sales.csv` with seasonal pattern (~50–100 rows).
6. Integration test: `integration_tests/test_bigquery_adapter.sql` asserting non-null forecast output on seed data.
7. README updated: BigQuery is canonical, Snowflake/Databricks are PoC awaiting Native App.
8. Version bump 0.1.0 → 1.0.0.

**Effort**: ~2–3 days.

---

## Out of scope (intentionally excluded)

- The `templates/universal-validator/` directory is reusable infrastructure, not a customer plugin. No epic.
- The `nixtla-snowflake-adapter` PRD-folder reorg under planned-plugins. The plugin works; doc reshuffling is busywork.
- New skill creation. The 30 skills in `003-skills/.claude/skills/` already cover the forecasting domain. New skills only get created if a child bead specifically requires one (and at that point the skill-creator skill is invoked).
- Strategic / vision documents. This document is the plan; no parallel ADR.

---

## Total scope summary

| Tier | Plugins | Epics | Aggregate effort |
|---|---|---|---|
| Phase 1 (fix existing stubs) | 7 | 7 | ~2–3 weeks |
| Phase 2 (polish working) | 4 | 4 | ~1 week |
| Phase 3 (PoC labeling) | 2 | 2 | ~1 day |
| Phase 0 (dbt-package) | 1 | 1 | ~2–3 days |
| Phase 4 (High planned) | 3 | 3 | 17 weeks |
| Phase 5 (Medium planned) | 3 | 3 | 17–22 weeks |
| **Total** | **20** | **20** | **~6 months** |

The 20 plugins match the planned-plugins README's count exactly (13 implemented + 1 separately-tracked + 6 planned = 20).

---

## Approval and execution

If approved as-is:

1. Create the 20 epics in beads (one `bd create --type=epic` per plugin).
2. Create child beads for **Phase 1.1 only** initially (~8 children for `nixtla-roi-calculator`). Decompose subsequent epics on claim.
3. Branch off main: `feat/<plugin>-v1` per epic. Single PR per epic.
4. Merge order = phase order (Phase 1 → 2 → 3 → 4 → 5).

If revisions wanted: mark them on this doc; I update before bead creation.

This document lives at `000-docs/131-AT-PLAN-plugin-build-roadmap.md` and is the canonical reference for every plugin epic until v1.0 ships across all 20.
