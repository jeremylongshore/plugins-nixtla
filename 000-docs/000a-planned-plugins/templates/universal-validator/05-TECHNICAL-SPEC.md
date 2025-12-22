# Universal Validator - Technical Spec

**Plugin:** universal-validator  
**Version:** 0.1.0  
**Status:** Planned (Template / Reusable)  
**Last Updated:** 2025-12-22  

---

## Commands

- `validate`: runs the deterministic suite with a selected profile and writes evidence bundles.

---

## Deterministic Runner Requirements

- No interactive prompts.
- Deterministic outputs (stable JSON fields).
- Always write evidence bundle files even on failure.
- Support:
  - `--profile`, `--list-profiles`
  - `--phase-start`, `--phase-end`
  - `--run-tests`, `--fail-on-warn`
  - `--resume`, `--max-retries`

---

## Profile Schema (JSON)

Minimum:

```json
{
  "name": "default",
  "phases": [
    {
      "name": "structural",
      "checks": [
        {
          "name": "example.check",
          "command": ["bash", "script.sh"],
          "cwd": "{repo_root}",
          "severity": "error"
        }
      ]
    }
  ]
}
```

---

## Evidence Bundle Validation

Ship a deterministic validator that checks:

- `summary.json` exists and has `status` + non-empty `checks[]`
- `report.md` exists and is non-empty
- `checks/` exists

---

## Security

- Default profiles should not require network.
- Prefer scoped shell execution (e.g., `python:*`, `bash:*`) and avoid unscoped command execution in skills.

