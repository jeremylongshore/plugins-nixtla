# Baseline Result and Metric Contract

## CSV schema

The Baseline Lab writes one row per evaluated series/model pair:

| Column | Meaning | Validation |
| --- | --- | --- |
| `series_id` | Series identifier | non-empty string |
| `model` | Executed model name | non-empty string |
| `sMAPE` | Symmetric mean absolute percentage error | finite number from 0 through 200 |
| `MASE` | Mean absolute scaled error | finite, non-negative number |

The current runtime supports `SeasonalNaive`, `AutoETS`, and `AutoTheta`, but a
run can intentionally select a subset. Treat unknown names as reported model
identifiers; do not silently relabel them.

Reject duplicate `(series_id, model)` pairs because they would overweight that
pair in aggregates. Report missing model/series pairs as coverage gaps.

## sMAPE in this repository

`nixtla_baseline_mcp.py` computes:

```text
100 * mean(abs(actual - forecast) / ((abs(actual) + abs(forecast)) / 2))
```

The denominator has a small zero guard. CSV values are therefore percentage
points, not proportions. Lower values indicate lower symmetric percentage error
for the evaluated observations. There is no dataset-independent threshold that
makes a forecast "good" or production-ready.

## MASE in this repository

The runtime divides test forecast MAE by an in-sample naive error scale derived
from the training series and configured `season_length`. When the training
series is too short for that seasonal lag, the implementation falls back to a
one-step difference scale.

Consequences:

- MASE below 1 means test MAE is below the run's in-sample naive scale.
- MASE above 1 means it is above that scale.
- The meaning depends on the selected seasonal period and fallback behavior.
- A held-out SeasonalNaive forecast does not necessarily have MASE exactly 1.
- `1 - MASE` is not a universal percentage improvement claim.

## Comparison discipline

Compare models only when they use the same series, split, horizon, and metric
configuration. Report both aggregate central tendency and per-series coverage.
Mean, median, standard deviation, and win count answer different questions; no
single statistic proves general dominance.

Treat a tie as a tie. Avoid arbitrary tie-breaking by model name or CSV order.
If two runs differ in dataset, horizon, sample, frequency, or seasonal period,
describe them separately unless the user explicitly requests a qualified
cross-run comparison.

## Provenance files

When present beside the CSV, use:

- `run_manifest.json` for resolved parameters and dataset scope;
- `compat_info.json` for package/runtime versions;
- `summary_*.txt` as a derived human-readable summary;
- `benchmark_report_*.md` as another derived view.

The CSV and manifest outrank narrative summaries when values disagree. The
community plugin is not an official Nixtla benchmark certification.
