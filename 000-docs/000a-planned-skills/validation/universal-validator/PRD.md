# Claude Skill PRD: Universal Validator (He-Man Skill)

**Template Version**: 1.0.0  
**Status**: Planned  
**Goal**: A reusable, enterprise-grade multi-phase validator skill that can validate “anything thrown at it” by driving deterministic checks and producing an evidence bundle.

---

## Document Control

| Field | Value |
|---|---|
| Skill Name | universal-validator |
| Domain | Validation / CI / Compliance |
| Target Users | Engineers, Maintainers, QA |
| Priority | High |
| Owner | Intent Solutions |
| Last Updated | 2025-12-22 |

---

## 1. Executive Summary

Build a skill that accepts a target scope (repo, plugin, skill, directory) and produces:

- A **single pass/fail** result based on deterministic gates
- A **timestamped evidence bundle** (logs + summary JSON + report)
- A **fix plan** when gates fail

The skill is not tied to Nixtla specifically; it is a framework. Nixtla checks are one catalog.

---

## 2. Core Requirements

**REQ-1: Multi-phase workflow**

Phases:
1. Discover scope + changes
2. Run schema/structure gates
3. Run deterministic verification scripts
4. Reconcile results (confirmed/revised/unverified/unexpected)
5. Produce final report + next actions

**REQ-2: Deterministic enforcement**

- Every claim that can be checked must be checked by scripts.
- Output must be reproducible (same inputs → same results).

**REQ-3: Extensible check catalog**

- Checks are config-driven (commands + expected artifacts + severity).
- Supports multiple “profiles” (e.g., `skills`, `plugins`, `python-package`, `docs`, `infra`).

**REQ-4: Evidence bundle**

Write:
- `reports/<project>/<timestamp>/summary.json`
- `reports/<project>/<timestamp>/report.md`
- `reports/<project>/<timestamp>/checks/*.log`

---

## 3. Success Metrics

- 0 silent failures (contract violations halt execution)
- 100% of runs produce a complete evidence bundle
- CI can gate merges using this skill’s deterministic scripts

