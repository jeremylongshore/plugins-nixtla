---
name: nixtla-benchmark-reporter
description: Generate comprehensive markdown benchmark reports from forecast accuracy metrics with model comparisons, statistical analysis, and regression detection. Use when analyzing baseline performance, comparing forecast models, or validating model quality. Trigger with 'generate benchmark report', 'analyze forecast metrics', or 'create performance summary'.
allowed-tools: "Read,Write,Glob,Bash(python:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Benchmark Reporter

## Purpose

Generate production-ready benchmark reports from forecasting accuracy metrics, enabling systematic model comparison and regression detection for Nixtla forecasting workflows.

## Overview

This skill transforms raw forecast metrics (sMAPE, MASE, MAE, RMSE) into actionable insights. It:
- Parses benchmark results CSV files from statsforecast/TimeGPT experiments
- Calculates summary statistics (mean, median, std dev, percentiles)
- Generates model comparison tables with winners highlighted
- Creates regression detection reports comparing current vs. baseline results
- Produces GitHub issue templates for performance degradations
- Generates markdown reports with embedded charts and recommendations

**Key Benefits**:
- Automates tedious manual benchmarking analysis (2-3 hours → 2 minutes)
- Provides consistent reporting format across all forecasting experiments
- Detects performance regressions automatically
- Generates shareable, version-controlled markdown reports

## Prerequisites

- Benchmark results CSV files with metrics per series and model
- CSV format: columns `series_id`, `model`, `sMAPE`, `MASE` (minimum)
- Optional: Baseline results CSV for regression comparison
- Python 3.8+ with pandas, numpy installed

**Expected CSV Structure**:
```csv
series_id,model,sMAPE,MASE,MAE,RMSE
D1,SeasonalNaive,15.23,1.05,12.5,18.3
D1,AutoETS,13.45,0.92,10.2,15.1
D1,AutoTheta,12.34,0.87,9.8,14.5
D2,SeasonalNaive,18.67,1.23,15.1,22.4
...
```

## Instructions

### Step 1: Parse Benchmark Results

The script automatically:
1. Reads benchmark CSV file(s)
2. Validates CSV structure (required columns present)
3. Extracts unique models and series
4. Groups metrics by model

**Usage**:
```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results /path/to/benchmark_results.csv \
    --output /path/to/report.md
```

### Step 2: Calculate Summary Statistics

For each model, calculates:
- **Mean**: Average metric across all series
- **Median**: Middle value (less sensitive to outliers)
- **Std Dev**: Measure of consistency
- **Min/Max**: Best and worst performance
- **Percentiles**: 25th, 50th, 75th, 95th percentiles
- **Win Rate**: Percentage of series where model performed best

### Step 3: Generate Comparison Table

Creates markdown table comparing all models:

```markdown
## Model Comparison (sMAPE)

| Model | Mean | Median | Std Dev | Min | Max | Wins |
|-------|------|--------|---------|-----|-----|------|
| AutoTheta | 12.3% | 11.8% | 4.2% | 5.1% | 28.9% | 32/50 (64%) |
| AutoETS | 13.5% | 12.9% | 5.1% | 6.2% | 31.2% | 18/50 (36%) |
| SeasonalNaive | 15.2% | 14.5% | 6.3% | 7.8% | 35.4% | 0/50 (0%) |
```

### Step 4: Identify Winner and Recommendations

Determines overall best model based on:
1. **Primary metric**: Lowest mean sMAPE/MASE
2. **Consistency**: Lowest standard deviation
3. **Win rate**: Most series won

Generates recommendations:
- Production baseline model selection
- When to use alternatives (e.g., AutoETS for seasonal data)
- Failure case analysis (series where all models struggle)

### Step 5: Regression Detection (Optional)

If baseline results provided, compares current vs. baseline:

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results current_results.csv \
    --baseline baseline_results.csv \
    --output regression_report.md \
    --threshold 5.0  # Alert if sMAPE degrades >5%
```

**Regression Report Includes**:
- Models with performance degradation
- Severity of regression (% change)
- Affected series
- GitHub issue template for regressions

### Step 6: Customize Report Format

Supports multiple output formats:

**Standard Report** (default):
```bash
python {baseDir}/scripts/generate_benchmark_report.py --results metrics.csv
```

**Executive Summary** (1-page):
```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results metrics.csv \
    --format executive \
    --output summary.md
```

**GitHub Issue Template**:
```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results metrics.csv \
    --format github \
    --output .github/ISSUE_TEMPLATE/regression.md
```

## Output

The script generates:

**Standard Report** (`report.md`):
1. Executive Summary (1-2 paragraphs)
2. Model Comparison Table (all metrics)
3. Statistical Analysis (means, std devs, percentiles)
4. Winner Declaration with justification
5. Per-Series Breakdown (optional)
6. Recommendations for production use
7. Failure Case Analysis (series with sMAPE > 30%)

**Regression Report** (if baseline provided):
1. Regression Summary (models degraded)
2. Severity Analysis (% change per model)
3. Affected Series List
4. GitHub Issue Template

**GitHub Issue Template**:
```markdown
---
title: "Performance Regression Detected: {model_name}"
labels: ["regression", "performance"]
assignees: ["team-lead"]
---

## Regression Summary
Model: {model_name}
Metric: sMAPE degraded by {X}%
Baseline: {baseline_value}%
Current: {current_value}%

## Affected Series
- {series_1}: {baseline}% → {current}% ({delta}%)
- {series_2}: {baseline}% → {current}% ({delta}%)
...

## Acceptance Criteria
- [ ] Investigate root cause
- [ ] Restore performance to within 2% of baseline
- [ ] Add regression test to CI/CD
```

## Error Handling

**Missing Metrics File**:
```
Error: Benchmark results not found at /path/to/results.csv
Solution: Verify path and ensure CSV file exists
```

**Invalid CSV Structure**:
```
Error: Required columns missing: series_id, model, sMAPE
Solution: Ensure CSV has minimum required columns
```

**Empty Results**:
```
Warning: No metrics found in CSV file
Solution: Verify CSV has data rows (not just headers)
```

**Regression Threshold Exceeded**:
```
🚨 REGRESSION DETECTED: AutoTheta sMAPE degraded by 12.5%
  Baseline: 12.3%
  Current: 13.8%
  Threshold: 5.0%
Solution: Review recent model changes, check data quality
```

## Examples

### Example 1: Generate Standard Benchmark Report

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results nixtla_baseline_m4/results_M4_Daily_h14.csv \
    --output reports/m4_daily_baseline.md \
    --verbose
```

**Output**:
```
✓ Loaded 150 results (50 series × 3 models)
✓ Calculated summary statistics
✓ Identified winner: AutoTheta (mean sMAPE: 12.3%)
✓ Generated report: reports/m4_daily_baseline.md (1,245 words)
```

### Example 2: Detect Regressions vs. Baseline

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results current_run/results.csv \
    --baseline baseline/v1.0_results.csv \
    --output regression_report.md \
    --threshold 3.0
```

**Output**:
```
⚠️  REGRESSION DETECTED in 2/3 models:
  - AutoETS: sMAPE 13.5% → 14.8% (+9.6%)
  - AutoTheta: sMAPE 12.3% → 12.7% (+3.3%)
✓ Generated regression report with GitHub issue template
```

### Example 3: Generate Executive Summary

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results quarterly_benchmark.csv \
    --format executive \
    --output Q1_summary.md
```

**Output**:
```markdown
# Q1 2025 Forecast Baseline Report

**Winner**: AutoTheta with 12.3% sMAPE (vs. 13.5% AutoETS, 15.2% Naive)

**Key Findings**:
- AutoTheta won 64% of series (32/50)
- Most consistent performance (std dev 4.2%)
- Recommended for production baseline

**Action Items**:
- Deploy AutoTheta as default model
- Use AutoETS for highly seasonal data (criteria: seasonal_strength > 0.8)
- Investigate 3 failure cases (sMAPE > 30%)
```

### Example 4: Custom Metric Focus

```bash
python {baseDir}/scripts/generate_benchmark_report.py \
    --results results.csv \
    --primary-metric MASE \
    --output mase_focused_report.md
```

## Best Practices

1. **Version Control Reports**: Commit generated reports to track performance over time
2. **Automate in CI/CD**: Generate reports automatically on every benchmark run
3. **Set Regression Thresholds**: Use `--threshold` to catch regressions early (recommend 3-5%)
4. **Include Timestamps**: Reports automatically include generation date/time
5. **Document Assumptions**: Reports include metadata about benchmark setup
6. **Share with Stakeholders**: Markdown reports render nicely on GitHub/GitLab
7. **Archive Baselines**: Keep historical baseline CSVs for regression comparison

## Resources

- **Script**: `{baseDir}/scripts/generate_benchmark_report.py`
- **Template**: `{baseDir}/assets/templates/report_template.md`
- **Example Report**: `{baseDir}/references/EXAMPLE_REPORT.md`
- **M4 Benchmark**: https://github.com/Mcompetitions/M4-methods
- **Forecast Metrics**: https://otexts.com/fpp3/accuracy.html
