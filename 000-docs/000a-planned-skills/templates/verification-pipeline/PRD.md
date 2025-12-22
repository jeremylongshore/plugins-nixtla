# Claude Skill PRD: Universal Verification Pipeline (5-Phase)

**Template Version**: 1.0.0  
**Based On**: Lee Han Chung Claude Skills deep dive + Intent Solutions standards  
**Status**: Template (copy and customize)

---

## Document Control

| Field | Value |
|---|---|
| Skill Name | `<org>-verification-pipeline` |
| Domain | `<org> / <product> / <vertical>` |
| Target Users | Engineers, Data Scientists, Analysts |
| Priority | High |
| Status | Planned |
| Owner | `<team>` |
| Last Updated | YYYY-MM-DD |

---

## 1. Executive Summary

Build a skill that takes **raw inputs + a contract**, and produces **verified artifacts**:

- Verified canonical datasets (schema + integrity)
- Verified evaluation results (backtests/benchmarks)
- Verified deployable contract bundle (schemas + examples + run commands)

This enables manufacturing plugins/skills at scale by enforcing correctness at boundaries.

---

## 2. Problem Statement

### Current State

- Workflows rely on LLM “interpretation” without deterministic validation.
- Data issues and contract drift are discovered late (or in production).
- Teams can’t trust outputs across multiple projects/clients.

### Desired State

- Every run produces a traceable, replayable evidence bundle.
- The LLM can propose, but scripts decide pass/fail.
- CI can gate merges on contract + evaluation correctness.

---

## 3. Goals / Non-Goals

### Goals

- Enforce strict **input schema** + **integrity** checks (Phase 1–2).
- Enforce strict **evaluation/backtest verification** (Phase 4).
- Produce a **deployable handoff bundle** (Phase 5).
- Support multiple scenarios by swapping reference procedures + scripts.

### Non-Goals

- Becoming a full MLOps platform.
- Replacing modeling libraries; this orchestrates them.

---

## 4. Functional Requirements

**REQ-1: Sessionized runs**
- Create a run directory: `reports/<project>/<timestamp>/`
- Write phase reports + machine-readable outputs there

**REQ-2: Canonical mapping**
- Map raw input → canonical dataset contract (domain-specific)
- Output: `canonical_dataset.*` + mapping table + report

**REQ-3: Data quality audit**
- Deterministic checks: duplicates, monotonic timestamps, missingness, feasibility, leakage
- Output: quality report + `quality.json`

**REQ-4: Model/evaluation plan + verification**
- Define evaluation config (backtest strategy, metrics, seeds)
- Run deterministic evaluation producing:
  - `metrics.json`
  - `predictions.*`

**REQ-5: Deployable contract**
- Validate request/response examples against JSON schema (or equivalent)
- Produce “handoff bundle”: schema + examples + run commands + constraints

---

## 5. Success Metrics

- 100% of runs produce a complete evidence bundle
- 0 merges when schema/contract validation fails (CI gate)
- >90% reduction in “late discovery” data issues (measured by incidents)

