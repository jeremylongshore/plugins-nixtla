# Test Harness Applications for Nixtla

**How to apply the multi-phase validation pattern to nixtla's time-series forecasting workflows**

---

## Overview

Nixtla builds time-series forecasting libraries (TimeGPT, StatsForecast, MLForecast, NeuralForecast, HierarchicalForecast). The test harness pattern applies perfectly to:

1. **Release Validation** - Verify no regressions before shipping
2. **Benchmark Regression Detection** - Ensure performance doesn't degrade
3. **Documentation Sync** - Keep docs aligned with code reality

Each application follows the same 5-phase pattern with **Phase 4 running actual verification scripts** (pytest, benchmarks, doc tests).

---

## Application 1: Release Validation Workflow ⭐ RECOMMENDED

### Problem Statement

Before releasing nixtla v1.8.0, you need confidence that:
- No tests broke
- No performance regressions
- Breaking changes are documented
- Migration path is clear

**Current approach:** Manual testing, hoping nothing broke.

**Test harness approach:** 5-phase automated validation with empirical verification.

### 5-Phase Workflow

```
Phase 1: Change Analysis
├─ Read: git diff v1.7.0..v1.8.0, CHANGELOG.md, modified files
├─ Output: List of changed APIs, functions, dependencies
└─ JSON: {changed_files: [...], changed_apis: [...], breaking_changes: [...]}

Phase 2: Test Impact Prediction
├─ For each change, predict which tests might fail
├─ Example: "Modified forecast() signature → test_forecast_* tests affected"
└─ JSON: {test_predictions: [{change: "...", affected_tests: [...], reason: "..."}]}

Phase 3: Risk Assessment
├─ Categorize changes: breaking vs non-breaking
├─ Estimate: User impact, migration complexity, rollback difficulty
└─ JSON: {high_risk: [...], medium_risk: [...], low_risk: [...], go_no_go: "pending"}

Phase 4: VERIFICATION ★ THE CRITICAL PHASE
├─ RUN ACTUAL TEST SUITE: pytest tests/ --cov --json-report
├─ Compare: Manual predictions (Phase 2) vs Actual test results
├─ Script: scripts/analyze_test_results.sh
├─ Output comparison:
│  ├─ Confirmed: test_forecast_basic FAILED (predicted ✓)
│  ├─ Revised: test_anomaly_detection PASSED (predicted fail ✗)
│  └─ Unexpected: test_hierarchical_reconciliation FAILED (not predicted ⚠️)
└─ JSON: {
     tests_run: 145,
     tests_passed: 142,
     tests_failed: 3,
     predictions_confirmed: [...],
     predictions_revised: [...],
     unexpected_failures: [...],
     revised_risk_score: "medium"
   }

Phase 5: Go/No-Go Recommendation
├─ Synthesize: Confirmed safe changes + risky changes
├─ Output: Release notes, migration guide, rollback plan
└─ JSON: {
     recommendation: "go" | "no-go",
     blockers: [...],
     release_notes: "...",
     migration_steps: [...]
   }
```

### Verification Script (Phase 4)

**Location:** `scripts/analyze_test_results.sh`

```bash
#!/bin/bash
# Nixtla Release Validation Script

REPO_PATH="$1"
OUTPUT_PATH="$2"

cd "$REPO_PATH"

# Run full test suite
pytest tests/ \
  --cov \
  --json-report \
  --json-report-file="$OUTPUT_PATH/pytest-results.json" \
  -v

# Parse results
TOTAL=$(jq '.summary.total' "$OUTPUT_PATH/pytest-results.json")
PASSED=$(jq '.summary.passed' "$OUTPUT_PATH/pytest-results.json")
FAILED=$(jq '.summary.failed' "$OUTPUT_PATH/pytest-results.json")
COVERAGE=$(coverage json -o "$OUTPUT_PATH/coverage.json" && jq '.totals.percent_covered' "$OUTPUT_PATH/coverage.json")

# Extract failed test names
FAILED_TESTS=$(jq -r '.tests[] | select(.outcome == "failed") | .nodeid' "$OUTPUT_PATH/pytest-results.json" | jq -R . | jq -s .)

# Output structured JSON
cat > "$OUTPUT_PATH/verification_report.json" <<EOF
{
  "metadata": {
    "script": "analyze_test_results.sh",
    "timestamp": "$(date -Iseconds)",
    "repo": "$REPO_PATH"
  },
  "results": {
    "tests_run": $TOTAL,
    "tests_passed": $PASSED,
    "tests_failed": $FAILED,
    "coverage_pct": $COVERAGE,
    "failed_tests": $FAILED_TESTS
  }
}
EOF

echo "Verification complete: $OUTPUT_PATH/verification_report.json"
exit 0
```

### How to Use

```bash
cd /home/jeremy/000-projects/nixtla/002-workspaces/test-harness-lab/

# Create nixtla-specific skill
mkdir -p skills/nixtla-release-validation/{agents,references,scripts,reports}

# Copy and adapt reference implementation
# Update Phase 4 to use scripts/analyze_test_results.sh

# Test with last release
git checkout v1.7.0
# Run Phase 1-5 workflow
# Compare predictions vs actual results
```

**Expected outcome:**
- Automated pre-release validation
- Clear go/no-go decision with evidence
- Audit trail of what was tested and why
- Confidence: "Script confirmed safe to release"

---

## Application 2: Benchmark Regression Detection

### Problem Statement

Did this code change slow down forecasting? Need to know before merging PR.

### 5-Phase Workflow

```
Phase 1: Baseline Identification
├─ Identify benchmark targets (M4, M5, custom datasets)
├─ Read: benchmarks/baseline.json (previous run results)
└─ JSON: {baseline_benchmarks: [...], performance_thresholds: {...}}

Phase 2: Performance Prediction
├─ Analyze code changes (git diff)
├─ Predict: "Optimized FFT → expect 10-15% faster on M4 Daily"
└─ JSON: {performance_predictions: [{benchmark: "...", expected_change: "..."}]}

Phase 3: Risk Scoring
├─ Categorize: Critical benchmarks (M4, M5) vs Nice-to-have
├─ Threshold: >5% regression = high risk, >10% = blocker
└─ JSON: {critical_benchmarks: [...], regression_thresholds: {...}}

Phase 4: VERIFICATION ★
├─ RUN ACTUAL BENCHMARKS: python benchmarks/run_all.py
├─ Compare: Baseline vs Current performance
├─ Script: scripts/analyze_benchmark_results.sh
├─ Output comparison:
│  ├─ M4 Daily: Predicted +12%, Actual +14% ✓ (within tolerance)
│  ├─ M4 Hourly: Predicted no change, Actual -8% ✗ (unexpected regression)
│  └─ M5 Weekly: Predicted +5%, Actual +3% ✓ (close enough)
└─ JSON: {
     benchmarks_run: 15,
     regressions_detected: 1,
     predictions_confirmed: 12,
     predictions_revised: 3,
     blocker_regressions: ["M4_Hourly: -8%"]
   }

Phase 5: Performance Report
├─ Synthesize: Safe changes + regressions
├─ Output: Performance summary, investigation leads
└─ JSON: {
     recommendation: "investigate" | "approve",
     regressions_to_fix: [...],
     performance_summary: "..."
   }
```

### Verification Script (Phase 4)

```bash
#!/bin/bash
# scripts/analyze_benchmark_results.sh

BASELINE_FILE="$1"  # benchmarks/baseline.json
CURRENT_RUN="$2"    # benchmarks/current_run.json
OUTPUT="$3"

# Compare results
python3 << 'PYEOF'
import json
import sys

with open(sys.argv[1]) as f:
    baseline = json.load(f)
with open(sys.argv[2]) as f:
    current = json.load(f)

regressions = []
improvements = []

for bench_name, baseline_time in baseline.items():
    current_time = current.get(bench_name)
    if not current_time:
        continue

    pct_change = ((current_time - baseline_time) / baseline_time) * 100

    if pct_change > 5:  # >5% slower = regression
        regressions.append({
            "benchmark": bench_name,
            "baseline_time": baseline_time,
            "current_time": current_time,
            "pct_change": pct_change
        })
    elif pct_change < -5:  # >5% faster = improvement
        improvements.append({
            "benchmark": bench_name,
            "pct_change": pct_change
        })

with open(sys.argv[3], 'w') as f:
    json.dump({
        "regressions": regressions,
        "improvements": improvements,
        "benchmarks_compared": len(baseline)
    }, f, indent=2)
PYEOF "$BASELINE_FILE" "$CURRENT_RUN" "$OUTPUT/comparison.json"
```

---

## Application 3: Documentation Sync Validation

### Problem Statement

Docstring examples drift from code reality. Need to verify all examples actually run.

### 5-Phase Workflow

```
Phase 1: API Surface Scan
├─ Scan code for public APIs with docstrings
├─ Extract: Function signatures, parameter types, return types
└─ JSON: {public_apis: [...], docstring_count: N}

Phase 2: Documentation Extraction
├─ Extract code examples from docstrings
├─ Parse: ```python blocks in docstrings
└─ JSON: {examples_found: [...], examples_count: N}

Phase 3: Gap Analysis
├─ Compare: Documented APIs vs Actual APIs
├─ Identify: Missing docs, deprecated functions still documented
└─ JSON: {missing_docs: [...], stale_docs: [...]}

Phase 4: VERIFICATION ★
├─ RUN DOC EXAMPLES: Extract and execute each example
├─ Script: scripts/verify_docstring_examples.sh
├─ Output:
│  ├─ forecast() example: PASSED ✓
│  ├─ cross_validation() example: FAILED (DeprecationWarning) ⚠️
│  └─ anomaly_detection() example: ERROR (module not found) ✗
└─ JSON: {
     examples_tested: 47,
     examples_passed: 44,
     examples_failed: 2,
     examples_error: 1,
     failures: [...]
   }

Phase 5: Documentation Update Plan
├─ Synthesize: Working examples + broken examples
├─ Output: List of docs to update, examples to fix
└─ JSON: {
     docs_to_update: [...],
     examples_to_fix: [...],
     priority: "high" | "medium" | "low"
   }
```

---

## Common Patterns Across All Applications

### Phase 1: Always Establish Baseline
- Scan files, count metrics, identify scope
- Output: Concrete numbers (N tables, M tests, X benchmarks)

### Phase 2: Make Predictions (LLM Analysis)
- Analyze patterns, make educated guesses
- Output: Structured predictions with reasoning

### Phase 3: Assess Risk/Impact
- Categorize by severity (high/medium/low)
- Output: Prioritized list with impact estimates

### Phase 4: EMPIRICAL VERIFICATION (The Key)
- **Always run actual tools:** pytest, benchmarks, linters, etc.
- **Always compare:** Manual predictions vs Script results
- **Always output:** Confirmed, Revised, Unexpected findings
- **Script characteristics:** Deterministic, fast (<5 min), structured JSON output

### Phase 5: Synthesize Validated Findings
- Build on confirmed conclusions only
- Flag revised items for investigation
- Output: Actionable recommendations with evidence

---

## Building Your Own Nixtla Workflow

**Template:**
1. Pick your domain (release, benchmarks, docs, etc.)
2. Design 5 phases (use patterns above)
3. **Focus on Phase 4 script** - this is what makes it real
4. Write reference docs (step-by-step procedures)
5. Create agents with strict JSON contracts
6. Test end-to-end with real nixtla data
7. Deploy to `../../003-skills/.claude/skills/` when ready

**Time investment:**
- Simple 3-phase: 2 hours
- Standard 5-phase: Half day
- Complex 7-phase: 1 day

**ROI:**
- Automated validation (save hours per release)
- Empirical confidence (no more "hoping it works")
- Audit trail (can review past decisions)
- Reusable pattern (build once, use everywhere)

---

## Next Steps

**Option 1: Start with Release Validation**
1. Copy `reference-implementation/` → `skills/nixtla-release-validation/`
2. Adapt Phase 4 to use `scripts/analyze_test_results.sh`
3. Test with last nixtla release (v1.6.0 → v1.7.0)
4. Deploy when validated

**Option 2: Start with Benchmarks**
1. Adapt for `scripts/analyze_benchmark_results.sh`
2. Use nixtla's existing benchmark infrastructure
3. Test with M4/M5 datasets

**Option 3: Build Custom Workflow**
1. Follow `guides/GUIDE-02-BUILDING-YOUR-OWN.md`
2. Design your own 5-phase workflow
3. Implement verification script (Phase 4)

---

**Key Takeaway:** The test harness pattern turns "LLM analyzed my code" into "LLM + script verified my code with evidence." That's the difference between a chatbot and a production system.

---

*Concrete applications of test harness pattern for nixtla time-series workflows*
