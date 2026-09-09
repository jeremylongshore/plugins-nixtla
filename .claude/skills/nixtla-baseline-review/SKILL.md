---
name: nixtla-baseline-review
description: |
  Analyze real sMAPE and MASE results produced by the community Nixtla Baseline
  Lab, compare models, and surface fragile series without inventing benchmarks.
  Use when reviewing StatsForecast output; trigger with "baseline review",
  "interpret sMAPE/MASE", or "compare AutoETS and AutoTheta".
allowed-tools: 'Read, Glob, Bash(python3:*)'
version: 1.1.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
compatibility: 'Claude Code with Python 3.10+; reads results_*.csv output from the community-built nixtla-baseline-lab plugin. No API key is required to review existing files.'
tags: [nixtla, statsforecast, forecasting, smape, mase, model-evaluation]
argument-hint: '[results CSV or output directory] [metric or question]'
model: inherit
---

# Nixtla Baseline Review

## Overview

Review one concrete Baseline Lab result set. Rank models from observed metrics,
show both aggregate and per-series evidence, and keep benchmark conclusions
inside the dataset, horizon, and series sample that produced them.

## Prerequisites

- Provide a `results_*.csv` path or a directory containing one.
- Require columns `series_id`, `model`, `sMAPE`, and `MASE`.
- Treat this repository as a community integration, not an official Nixtla
  product or an independent reproduction of an entire benchmark.

## Instructions

1. Resolve the input with `Glob`. If several result files match, list their
   paths and modification context and ask the user to choose; never silently
   combine separate runs or pick a filename as "latest" without confirmation.
2. Use `Read` to inspect the header, representative rows, sibling summary, and
   `run_manifest.json` or `compat_info.json` when present. Record the dataset,
   horizon, series count, models, frequency, and seasonal period that are
   actually supported by those artifacts.
3. Run the bundled analyzer:

   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/analyze_results.py path/to/results.csv
   ```

4. Check the analyzer receipt for rejected rows, duplicate series/model pairs,
   ties, model coverage, and non-finite values. Stop on schema or numeric
   failures instead of averaging partial data.
5. Rank models by the metric the user requested; otherwise lead with mean and
   median sMAPE, then report MASE and win counts as supporting evidence. Do not
   turn a small mean difference into a categorical claim.
6. Inspect series where models disagree or all reported errors are high. State
   patterns as hypotheses unless timestamps, seasonality, or covariates in the
   source data actually support them.
7. Give a bounded recommendation for the observed evaluation only. Require
   out-of-sample validation, cost/latency checks, and operational review before
   calling any model production-ready.

## Metric guardrails

- Lower sMAPE and MASE are better, but neither has a universal "good" threshold.
- Interpret MASE against the scaling denominator and seasonal period used by
  the run. A model's MASE below 1 indicates lower test MAE than that in-sample
  naive scale; it does not prove a fixed percentage improvement in every case.
- Do not claim a SeasonalNaive forecast must have MASE exactly 1 on held-out
  data. See [the result and metric contract](references/metric-contract.md).

## Validation

- Cite the exact CSV and any manifest/summary used.
- Reconcile reported row count with series count multiplied by model coverage.
- Show ties and missing model/series combinations rather than hiding them.
- Preserve units: Baseline Lab writes sMAPE as percentage points.
- Never fabricate TimeGPT, benchmark, or production-performance results.

## Output

Return scope and provenance, data-quality receipt, per-model mean/median/std-dev
sMAPE, mean/median MASE, series win counts and ties, failure cases, a scoped
recommendation, uncertainties, and reproducible next steps.

## Error Handling

- **No result file:** explain the expected filename/schema and point to the
  Baseline Lab run workflow; do not manufacture sample metrics.
- **Several result files:** ask the user to select or explicitly approve a
  comparison across runs.
- **Invalid or duplicate rows:** report exact row numbers and stop aggregation.
- **Missing run metadata:** analyze the CSV but label dataset/horizon/frequency
  unknown unless the filename or sibling artifacts establish them.
- **TimeGPT requested without results:** state that no comparison is available;
  never infer hosted-model performance from StatsForecast rows.

## Examples

Use prompts that name the evidence and comparison boundary:

```text
Review nixtla_baseline_m4/results_M4_Daily_h7.csv. Rank by median sMAPE,
show ties and missing coverage, and keep conclusions limited to this run.
```

```text
Compare AutoETS and AutoTheta using both sMAPE and MASE. Identify series where
the metrics disagree and do not use generic accuracy labels.
```

## Resources

- [Result schema and metric guardrails](references/metric-contract.md)
- Analyzer: `scripts/analyze_results.py`
- Runtime source: `005-plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py`
