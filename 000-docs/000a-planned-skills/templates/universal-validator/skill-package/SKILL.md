---
name: org-universal-validator
description: "Validate skills and plugins with deterministic evidence bundles and strict schema gates. Use when auditing changes or enforcing compliance. Trigger with 'run validation' or 'audit validators'."
allowed-tools: "Read,Write,Glob,Grep,Bash(python:*),Bash(bash:*),Bash(pytest:*)"
version: "0.1.0"
author: "Your Team <team@example.com>"
license: MIT
---

# Universal Validator

## Purpose

Produce deterministic, reviewable validation evidence (reports + JSON + logs) for a repo, plugin, or skill.

## Overview

- Phase prompts live in `{baseDir}/agents/`
- Procedures live in `{baseDir}/references/`
- Deterministic runner + profiles live in `{baseDir}/scripts/`

## Prerequisites

- Python 3.11+
- Your repo validators and tests installed

## Instructions

1. Choose a target (repo/plugin/skill).
2. Run the deterministic suite with a profile:

```bash
python {baseDir}/scripts/run_validator_suite.py \
  --target . \
  --project example \
  --out reports/example \
  --profile default
```

3. Optionally run tests:

```bash
python {baseDir}/scripts/run_validator_suite.py \
  --target . \
  --project example \
  --out reports/example \
  --profile default \
  --run-tests
```

## Output

- `reports/<project>/<timestamp>/summary.json`
- `reports/<project>/<timestamp>/report.md`
- `reports/<project>/<timestamp>/checks/*.log`

## Error Handling

- If schema checks fail, fix structure before running tests.
- Treat logs as ground truth; update narratives to match evidence.

## Examples

```bash
python {baseDir}/scripts/run_validator_suite.py --target . --project pr-1234 --out reports/pr-1234 --profile default
```

## Resources

- Agents: `{baseDir}/agents/`
- Procedures: `{baseDir}/references/`
- Scripts: `{baseDir}/scripts/`

