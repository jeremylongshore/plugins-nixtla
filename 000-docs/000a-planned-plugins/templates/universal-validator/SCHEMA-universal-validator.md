# SCHEMA - universal-validator

This schema defines the minimum contract for the Universal Validator plugin’s outputs and core components.

## Required Plugin Components

- `.claude-plugin/plugin.json`
- `commands/validate.md`
- `scripts/run_validator_suite.py`
- `scripts/profiles/default.json`

## Required Evidence Bundle Files

```
reports/<project>/<timestamp>/
├── summary.json
├── report.md
└── checks/
    └── <check>.log
```

## summary.json Fields (Minimum)

- `status`: `complete|failed`
- `timestamp`
- `target`
- `profile`: `{ name, path }`
- `checks[]`: list containing `{ name, phase, severity, exit_code, log_path }`

