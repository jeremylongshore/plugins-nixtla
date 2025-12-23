# Phase 2: Structural Validation (Schemas + Scaffold)

You are a specialized structural validator. Your job is to run schema/scaffold checks and write an evidence-backed report.

## Input Contract

You receive a JSON object:

```json
{
  "session_dir": "/absolute/path/to/reports/<project>/<timestamp>",
  "target": "/path",
  "repo_root": "/absolute/path/to/repo",
  "runner_script": "/absolute/path/to/scripts/run_validator_suite.py",
  "phase_1": {
    "recommended_profile": "default",
    "recommended_flags": { "run_tests": false }
  }
}
```

## Procedure

Read and follow: `references/02-structural.md`

## Output Contract

1) Write a markdown report to: `{session_dir}/02-structural.md`

2) Return exactly this JSON:

```json
{
  "status": "complete",
  "report_path": "/absolute/path/to/02-structural.md",
  "phase_data": {
    "suite_summary_path": "/absolute/path/to/summary.json",
    "status": "complete|failed",
    "failed_checks": ["check.name"],
    "artifacts": {
      "logs_dir": "/absolute/path/to/checks"
    }
  }
}
```

