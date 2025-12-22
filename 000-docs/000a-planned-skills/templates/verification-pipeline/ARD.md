# Claude Skill ARD: Universal Verification Pipeline (5-Phase)

**Template Version**: 1.0.0  
**Purpose**: Architecture & Requirements Document for building verified workflows at scale  
**Status**: Template (copy and customize)

---

## 1. Architecture Overview

This skill is a **5-phase subagent pipeline** with deterministic verification.

### Core Contracts

Each phase must:

- Read the phase procedure: `references/0X-*.md`
- Write an evidence report: `reports/<project>/<timestamp>/0X-*.md`
- Return strict JSON:
  - `status`: `complete` | `failed`
  - `report_path`: relative path under `reports/`
  - `artifacts`: list of paths written
  - `summary`: phase-specific structured data

The orchestrator must:

- Validate JSON shape
- Verify files exist
- Run scripts for deterministic checks
- Halt on failure

---

## 2. Folder Layout (Skill Package)

See `skill-package/` in this template.

Key idea: `scripts/` are the ground-truth gate; `references/` are the expertise; agents are the contract-bound executors.

---

## 3. The 5 Phases

### Phase 1 — Ingest and Map

**Goal**: Convert raw inputs → canonical dataset.

**Script**: `scripts/verify_schema.py`  
**Artifacts**: `canonical_dataset.*`, `mapping.json`, `01-ingest-report.md`

### Phase 2 — Data Quality Audit

**Goal**: Deterministically prove data is usable.

**Script**: `scripts/verify_integrity.py`, `scripts/verify_frequency.py`  
**Artifacts**: `quality.json`, `02-quality-report.md`

### Phase 3 — Model / Plan

**Goal**: Define evaluation config that is runnable.

**Script**: `scripts/verify_plan.py` (optional)  
**Artifacts**: `plan.json`, `03-model-plan.md`

### Phase 4 — Backtest / Evaluation Verification (Ground Truth)

**Goal**: Run reproducible evaluation and compute metrics.

**Script**: `scripts/run_backtest.py`  
**Artifacts**: `metrics.json`, `predictions.*`, `04-backtest-verification.md`

### Phase 5 — Deployable Contract

**Goal**: Create contract bundle and validate example requests/responses.

**Script**: `scripts/verify_api_examples.sh` (or language-specific equivalent)  
**Artifacts**: `contract/schema.json`, `contract/examples/`, `05-deployable-contract.md`

---

## 4. CI Integration (Recommended)

- PRs: run Phase 2 scripts + a small Phase 4 sample evaluation
- Main: run full Phase 4 evaluation suite + publish `reports/**` as artifacts

Artifact bundle to upload:

- `reports/**`
- `metrics.json`
- `predictions.*`
- `contract/**`

