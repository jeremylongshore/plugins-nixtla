# Phase 3 Procedure: Behavioral Validation (Tests)

## Goal

Run tests deterministically and record failures with enough detail to reproduce.

## Steps

1. Run the suite including tests:

```bash
python {baseDir}/scripts/run_validator_suite.py \
  --target <target> \
  --project <project> \
  --out <reports_base> \
  --profile default \
  --run-tests \
  --phase-start behavioral
```

2. If tests fail:
   - Identify the failing test node ids
   - Capture command, exit code, and log path

3. Write the report:
   - Summarize what passed/failed
   - Include the minimal reproduction command(s)

## Output Checklist

- [ ] Report written to `{session_dir}/03-behavioral.md`
- [ ] JSON includes `suite_summary_path` and `failed_checks`

