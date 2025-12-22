# Universal Validator (Template)

Use this template to create a multi-phase “he-man” validator skill: subagent phases for narrative + reconciliation, plus a deterministic runner that generates an evidence bundle for CI-grade gates.

## What It Produces

- `reports/<project>/<timestamp>/summary.json` (machine-readable)
- `reports/<project>/<timestamp>/report.md` (human-readable)
- `reports/<project>/<timestamp>/checks/*.log` (ground truth)

## How To Use

1. Copy `skill-package/` into your repo’s skills directory.
2. Replace the default `profiles/default.json` checks with your org’s validators and tests.
3. Keep Phase 4 as the ground-truth reconciliation gate (scripts/logs win over narrative).

## Reference Implementation (Nixtla)

See: `003-skills/.claude/skills/nixtla-universal-validator/`

