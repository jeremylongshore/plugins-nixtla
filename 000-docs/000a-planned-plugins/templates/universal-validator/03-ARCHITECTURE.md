# Universal Validator - Architecture

**Plugin:** universal-validator  
**Version:** 0.1.0  
**Status:** Planned (Template / Reusable)  
**Last Updated:** 2025-12-22  

---

## High-Level Design

Two-layer system:

1) **Deterministic Runner** (the “engine”): runs commands, captures logs, writes `summary.json`.  
2) **Orchestration Layer** (the “workflow”): phases that interpret results and produce remediation.

---

## Planned Plugin Structure

```
005-plugins/universal-validator/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── validate.md
├── scripts/
│   ├── run_validator_suite.py
│   ├── validate_scaffold.py
│   └── profiles/
│       ├── default.json
│       ├── skills-only.json
│       ├── plugins-only.json
│       └── enterprise.json
└── README.md
```

Optional (if bundling a skill inside the plugin):

```
skills/universal-validator/SKILL.md
```

---

## Evidence Bundle Contract

```
reports/<project>/<timestamp>/
├── summary.json
├── report.md
├── state.json
└── checks/
    └── <check>.log
```

---

## Check Execution Model

- Checks run in phase order.
- Each check has a severity (`info|warn|error`) and optional condition (`when`).
- Failures still produce complete artifacts; exit code indicates pass/fail.

