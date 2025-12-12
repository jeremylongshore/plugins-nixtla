# Baseline Lab - Business Case

**Plugin:** nixtla-baseline-lab
**Category:** Internal Efficiency
**Status:** Implemented (v0.8.0)
**Last Updated:** 2025-12-12

---

## Problem Statement

Time-series forecasting practitioners need a standardized way to establish baseline model performance before investing in more complex solutions. Currently, running baseline benchmarks requires:

- Manual setup of statsforecast models
- Custom code to load M4 competition data
- Ad-hoc metric calculation (sMAPE, MASE)
- No standardized comparison framework

## Solution

A Claude Code plugin that runs statistical baseline models (AutoETS, AutoTheta, SeasonalNaive) on M4 benchmark data with standardized metric reporting.

---

## Target Users

1. **Nixtla Team**: Validate statsforecast performance on standard benchmarks
2. **Data Scientists**: Establish baselines before evaluating TimeGPT
3. **ML Engineers**: Compare model accuracy using industry-standard metrics

---

## Value Proposition

| Without Plugin | With Plugin |
|---------------|-------------|
| Hours to set up baseline tests | 30-second smoke test |
| Manual metric calculation | Automated sMAPE/MASE |
| No reproducibility | Standardized test harness |
| Custom code per benchmark | Single slash command |

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Smoke test pass rate | 100% | 100% |
| Time to run baseline | <90 seconds | ~30 seconds |
| M4 datasets supported | 4 (Daily, Hourly, Monthly, Weekly) | 4 |

---

## Competitive Landscape

No direct competitors exist for this specific use case. Alternatives:
- Manual statsforecast scripts (time-consuming)
- M4 competition code (not integrated with Claude Code)

---

## Recommendation

**Status: IMPLEMENTED** - Plugin is working and tested. Primary use is internal validation and demos.
