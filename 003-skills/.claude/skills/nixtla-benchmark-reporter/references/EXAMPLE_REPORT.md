# Example Benchmark Report (Excerpt)

**Generated:** 2025-12-21
**Dataset:** M4 Daily (h=14)
**Primary metric:** sMAPE

## Executive Summary

- **Winner:** AutoTheta (mean sMAPE: 12.3%)
- **Runner-up:** AutoETS (mean sMAPE: 13.5%)
- **Baseline:** SeasonalNaive (mean sMAPE: 15.2%)

## Model Comparison (sMAPE)

| Model | Mean | Median | Std Dev | Wins |
|------|------:|------:|------:|-----:|
| AutoTheta | 12.3% | 11.8% | 4.2% | 32/50 |
| AutoETS | 13.5% | 12.9% | 5.1% | 18/50 |
| SeasonalNaive | 15.2% | 14.5% | 6.3% | 0/50 |

## Recommendations

- Use **AutoTheta** as the default baseline for this dataset.
- Investigate failure cases where all models exceed **30% sMAPE**.
