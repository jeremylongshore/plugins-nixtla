# Claude Skill ARD: Universal Validator (He-Man Skill)

**Template Version**: 1.0.0  
**Status**: Planned  
**Pattern**: 5-phase subagent orchestration + deterministic verification

---

## 1. Architecture Overview

The skill is an orchestrator and a harness:

- Orchestrator: runs phases, validates strict JSON handoffs
- Harness scripts: run deterministic checks and produce machine outputs
- Evidence bundle: all outputs are saved under project/timestamp

## 2. Directory Layout (target implementation)

```
<skill>/
├── SKILL.md
├── agents/
│   ├── phase-1-discovery.md
│   ├── phase-2-gates.md
│   ├── phase-3-verification.md
│   ├── phase-4-reconciliation.md
│   └── phase-5-synthesis.md
├── references/
│   ├── checks-catalog.md
│   ├── report-template.md
│   └── policies.md
├── scripts/
│   ├── run_validator_suite.py
│   └── profiles/
│       ├── skills.json
│       ├── plugins.json
│       └── repo.json
└── reports/
    └── _samples/
```

## 3. Deterministic Checks (examples)

- Skills schema/content gate: `python 004-scripts/validate_skills_v2.py --fail-on-warn`
- Plugin structure gate: `bash 004-scripts/validate-all-plugins.sh <target>`
- Repo unit tests: `pytest`

## 4. Recovery + Restartability

- Each phase writes its report and returns JSON.
- The orchestrator can restart from the last successful phase using saved JSON checkpoints.

## 5. CI Integration

- PR: run strict gates + a small test subset
- Main: run full tests + publish evidence bundle artifacts

