# Phase 2 Procedure: Structural Validation (Schemas + Scaffold)

## Goal

Run deterministic schema/scaffold validators and produce an evidence-backed report.

## Steps

1. Run the deterministic suite with a structural profile:

```bash
python {baseDir}/scripts/run_validator_suite.py \
  --target <target> \
  --project <project> \
  --out <reports_base> \
  --profile default \
  --phase-end structural
```

2. Confirm artifacts exist under `{session_dir}`:
   - `summary.json`
   - `checks/*.log`

3. Write the report:
   - Link to `summary.json`
   - List failed checks (if any) and point to the log files
   - If a check failed, extract the exact error lines (last ~30 lines is usually enough)

## Output Checklist

- [ ] Report written to `{session_dir}/02-structural.md`
- [ ] JSON includes `suite_summary_path` and `status`

