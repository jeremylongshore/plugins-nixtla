# Phase 4 Procedure: Verify & Reconcile (Ground Truth)

## Goal

Treat `summary.json` + check logs as ground truth. Reconcile any narrative claims from phases 1–3 against the deterministic outputs.

## Steps

1. Load `summary.json` and compute:
   - overall pass/fail
   - failed checks
   - durations

2. For each failed check:
   - open the corresponding `checks/<name>.log`
   - extract the concrete error(s)
   - record what the next action should be (fix code vs install dependency vs adjust profile)

3. Reconciliation rules:
   - **Confirmed**: narrative matches the summary/logs
   - **Revised**: narrative differs from logs (correct it)
   - **Unverified**: narrative claims something not grounded in artifacts (mark unverified)

4. Write the verification report:
   - include a “Verified Status” section (pass/fail)
   - include a table mapping check → exit code → log path → outcome

## Output Checklist

- [ ] Report written to `{session_dir}/04-verify.md`
- [ ] JSON includes `verification_results` and `confidence_level`

