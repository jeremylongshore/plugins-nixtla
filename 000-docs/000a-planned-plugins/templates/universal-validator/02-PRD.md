# Universal Validator - Product Requirements Document

**Plugin:** universal-validator  
**Version:** 0.1.0  
**Status:** Planned (Template / Reusable)  
**Last Updated:** 2025-12-22  

---

## Overview

A plugin that provides a **universal validation command** with:

- profile-driven deterministic checks
- phase-based orchestration (discover → structural → behavioral → verify → synthesize)
- evidence bundles suitable for CI artifacts and compliance reports

---

## Goals

1. Run structural gates first (schema/scaffold/manifest validation).
2. Run optional behavioral checks (tests) only when needed.
3. Produce an evidence bundle per run under `reports/<project>/<timestamp>/`.
4. Support profiles (default, skills-only, plugins-only, enterprise).
5. Provide deterministic “he-man completeness” validation for the validator itself.

---

## Non-Goals

- Replace repository-specific validators (the plugin executes and standardizes them).
- Make network calls by default (validation should be offline-first).

---

## Functional Requirements

### FR-1: Single Entry Command
- Provide a command (e.g., `validate`) that accepts:
  - `--target`
  - `--profile`
  - `--run-tests` flag
  - `--fail-on-warn` flag
  - `--resume` and `--max-retries`

### FR-2: Evidence Bundle Contract
- Always write:
  - `summary.json` (machine-readable)
  - `report.md` (human-readable)
  - `checks/*.log` (ground truth)
  - `state.json` (checkpoint/resume)

### FR-3: Profiles (Check Catalog)
- Profiles define phases and checks:
  - `name`, `command[]`, `cwd`, optional `when`, optional `timeout_sec`, `severity`
- Profiles can be added without code changes.

### FR-4: Phase 4 Ground Truth Reconciliation
- The “verify” phase treats logs/summary as authoritative.
- Narrative output must reconcile to evidence (confirmed/revised/unverified).

### FR-5: Self-Validation (He-Man Status)
- A scaffold validator must ensure the plugin ships:
  - commands
  - deterministic runner
  - profile catalog
  - phase procedures/templates (if included)

---

## Acceptance Criteria

- Running the plugin produces an evidence bundle even when checks fail.
- Profiles can be listed and executed deterministically.
- The plugin can validate itself (scaffold + evidence bundle checks).

