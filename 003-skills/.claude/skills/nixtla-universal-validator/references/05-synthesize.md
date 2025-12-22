# Phase 5 Procedure: Synthesize & Remediate

## Goal

Produce a final action plan that is directly traceable to verified evidence.

## Steps

1. Start from `summary.json`:
   - If status is `complete`, produce a short “all green” summary and list the checks run.
   - If status is `failed`, list failures in priority order (schema/scaffold before tests).

2. For each failure:
   - specify the exact file(s) involved
   - specify the re-run command(s)
   - specify the expected green condition

3. Write the final report:
   - “What failed”
   - “How to fix”
   - “How to re-run”
   - “Acceptance criteria”

## Output Checklist

- [ ] Report written to `{session_dir}/05-final.md`
- [ ] JSON includes `top_fixes` and `rerun_commands`

