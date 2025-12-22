# ARD — Universal Validator Skill (Template)

## Architecture

Two-layer design:

1) **Subagent workflow** (phases + strict JSON contracts) for human analysis and reconciliation.  
2) **Deterministic runner** (profile-driven) for ground-truth execution and evidence capture.

## Evidence Bundle Contract

```
reports/<project>/<timestamp>/
├── summary.json
├── report.md
├── state.json
└── checks/
    └── <check>.log
```

## Profile Contract (JSON)

- phases: ordered list
- checks: `name`, `command[]`, `cwd`, optional `when`, optional `timeout_sec`, `severity`

## Retry & Resume

- `state.json` checkpoints completed checks
- `--resume` skips completed checks
- `--max-retries N` retries failing checks

