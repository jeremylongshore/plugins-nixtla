# Universal Verification Pipeline (5-Phase) — Template

This template defines a **repeatable, enterprise-grade workflow pattern** for building skills that produce **verifiable outputs** (data, metrics, contracts) instead of “vibe-based” recommendations.

## The Pattern (Why It Scales)

- **Agents produce claims** per phase (human-readable report + structured JSON summary).
- **Scripts verify claims deterministically** (schema checks, integrity checks, backtests, JSON-schema validation).
- **The orchestrator (SKILL.md) gates progress**: if a phase’s JSON is invalid or a verification script fails → the run stops.

Use this for Nixtla forecasting, but also for any company workflow where **inputs → transformations → evaluation → deployable contract** must be provably correct.

## What’s Included

- `PRD.md`: product requirements for a 5-phase verified pipeline skill.
- `ARD.md`: architecture + phase contracts + artifact definitions.
- `skill-package/`: a copy-paste starter layout for a real skill implementation:
  - `SKILL.md` orchestrator template
  - `agents/` phase prompts (strict JSON contracts)
  - `references/` procedure docs (the “real expertise”)
  - `scripts/` deterministic validators/backtest harness
  - `reports/_samples/` example outputs

## How to Instantiate

1. Copy `skill-package/` into one of:
   - `.claude/skills/<skill-name>/` (local)
   - `003-skills/.claude/skills/<skill-name>/` (shipped skill pack)
   - `005-plugins/<plugin>/skills/<skill-name>/` (plugin-shipped skill)
2. Rename placeholders (`<skill-name>`, `project`, `dataset`, etc.).
3. Implement scripts for your domain (Phase 2 + Phase 4 are mandatory for enterprise-grade).
4. Run strict validation:
   - `python 004-scripts/validate_skills_v2.py --fail-on-warn`
   - `bash 004-scripts/validate-all-plugins.sh .` (if plugin-scoped)

## Recommended Naming

- Generic: `verification-pipeline`, `data-contract-verifier`, `workflow-verification`
- Nixtla: `nixtla-forecast-verification`, `nixtla-canonical-series`

