# Universal Validator - User Journey

**Plugin:** universal-validator  
**Version:** 0.1.0  
**Status:** Planned (Template / Reusable)  
**Last Updated:** 2025-12-22  

---

## Primary Flow (PR Validation)

1. Developer edits skills/plugins.
2. Developer runs `validate` with a target and profile.
3. Plugin writes an evidence bundle.
4. If failed:
   - developer reads `report.md` and failing `checks/*.log`
   - fixes issues
   - re-runs with `--resume` (fast)

---

## Example Commands

Validate repo:

```bash
validate --target . --profile default --project pr-1234
```

Strict enterprise run:

```bash
validate --target . --profile enterprise --project pr-1234 --run-tests --fail-on-warn
```

Resume after fixing:

```bash
validate --target . --profile enterprise --project pr-1234 --resume
```

