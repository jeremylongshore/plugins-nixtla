# StatsForecast Lab

Classical statistical baselines (Naive, SeasonalNaive, AutoETS, AutoARIMA) for M4/M5 benchmarking and model comparisons. This workspace is the home base for StatsForecast engineers to design, validate, and refine baseline forecasting workflows using Nixtla's open-source StatsForecast library.

**Current Status**: Phase 07 complete - baseline M4 daily experiments operational.

## Purpose

The StatsForecast lab provides a local, cost-free environment for:
- **Baseline evaluation**: Run classical statistical models (Naive, SeasonalNaive, AutoETS) on daily time series
- **Metric validation**: Compute sMAPE, MAE, and other forecasting metrics
- **Workflow prototyping**: Design and test baseline comparison workflows before promoting to production plugins
- **TimeGPT comparison**: Generate baseline benchmarks for comparison against TimeGPT results

**Key Difference from TimeGPT Lab**: StatsForecast is 100% local (no API keys, no network calls, no costs). Ideal for rapid experimentation and baseline model development.

## Structure

- **skills/** - StatsForecast Claude Skills (baseline forecasters, benchmark runners)
- **scripts/** - M4/M5 benchmark runners, model comparison utilities, evaluation harnesses
- **data/** - M4/M5 datasets, custom benchmark datasets, baseline experiment data
- **reports/** - Benchmark results, model performance comparisons, sMAPE/MAE analysis
- **docs/** - Baselines documentation, benchmark setup guides, evaluation best practices

## Quick Start

### 1. Environment Setup

**Python Version**: 3.10+ recommended

**Create virtual environment**:
```bash
cd 002-workspaces/statsforecast-lab
python3 -m venv .venv-statsforecast
source .venv-statsforecast/bin/activate  # Linux/Mac
# or
.venv-statsforecast\Scripts\activate  # Windows
```

**Install dependencies**:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install statsforecast>=1.7.0 utilsforecast pandas numpy
```

### 2. Run Baseline Models

The baseline runner script (`scripts/run_statsforecast_baseline.py`) runs three classical models (Naive, SeasonalNaive, AutoETS) on the sample M4-style daily dataset:

```bash
# From statsforecast-lab/ directory
python scripts/run_statsforecast_baseline.py
```

**Expected Output**:
```
============================================================
StatsForecast Baseline Runner
============================================================

Step 1: Loading dataset...
✓ Dataset loaded: 3 series, 279 rows

Step 2: Running baseline models...
============================================================
Running Baseline Models
============================================================
Horizon: 14 days
Models: Naive, SeasonalNaive(7), AutoETS

  Series series_1: 76 train, 14 test
    Naive: sMAPE=X.XX%, MAE=X.XXXX
    SeasonalNaive: sMAPE=X.XX%, MAE=X.XXXX
    AutoETS: sMAPE=X.XX%, MAE=X.XXXX
  ...

✓ Baseline models completed: 9 total results

Step 3: Generating reports...
✓ CSV report: reports/statsforecast_baseline_results.csv
✓ Markdown summary: reports/statsforecast_baseline_summary.md

============================================================
✓ StatsForecast Baseline Run: COMPLETE
============================================================
```

### 3. Review Results

**CSV Report** (`reports/statsforecast_baseline_results.csv`):
- Per-series, per-model metrics
- Columns: `unique_id`, `model`, `horizon`, `smape`, `mae`
- Use for detailed analysis or further processing

**Markdown Summary** (`reports/statsforecast_baseline_summary.md`):
- Human-readable summary
- Executive summary (2-3 sentences)
- Results by model (tables)
- Comparative analysis (best model by metric)

## Dataset

**Sample Dataset**: `data/statsforecast_baseline_sample.csv`

- **Format**: M4-style with columns `unique_id`, `ds`, `y`
- **Series**: 3 time series (`series_1`, `series_2`, `series_3`)
- **Length**: 90 days per series (2024-01-01 to 2024-03-31)
- **Characteristics**:
  - `series_1`: Upward trend
  - `series_2`: Slight upward trend with small noise
  - `series_3`: Upward trend

**Forecast Horizon**: 14 days (last 14 points used as holdout for evaluation)

## Models

The baseline runner implements three classical statistical models from StatsForecast:

1. **Naive**: Simple last-value forecast (baseline)
2. **SeasonalNaive**: Seasonal last-value with 7-day period (weekly seasonality for daily data)
3. **AutoETS**: Automated Exponential Smoothing State Space model with 7-day seasonality

## Metrics

Two forecasting accuracy metrics are computed:

1. **sMAPE (Symmetric Mean Absolute Percentage Error)**:
   - Range: 0-200% (lower is better)
   - Formula: `100 * mean(|y_true - y_pred| / ((|y_true| + |y_pred|) / 2))`
   - Symmetric: treats over/under-prediction equally
   - Handles zeros better than MAPE

2. **MAE (Mean Absolute Error)**:
   - Range: 0 to infinity (lower is better)
   - Formula: `mean(|y_true - y_pred|)`
   - Absolute error metric (same units as data)

## Example Future Flows

1. **Run M4/M5 benchmarks** with full suite of StatsForecast models
2. **Compare baselines** (AutoETS vs AutoARIMA vs SeasonalNaive) on domain-specific data
3. **Prototype new baseline models** before integrating into `nixtla-baseline-lab` plugin
4. **Validate benchmark harness** for StatsForecast CI smoke tests
5. **Generate benchmark reports** for Nixtla CEO/stakeholders
6. **TimeGPT vs StatsForecast comparison**: Run identical experiments in both labs and compare results
7. **CI integration**: Add dry-run mode for CI validation (similar to TimeGPT lab Phase 06)

## Cross-Lab Comparison

Generate baseline metrics for comparison against TimeGPT experiments:

```bash
# 1. Run StatsForecast baselines (this lab)
cd 002-workspaces/statsforecast-lab
python scripts/run_statsforecast_baseline.py

# 2. Ensure TimeGPT experiments exist
cd ../timegpt-lab
export NIXTLA_TIMEGPT_API_KEY='your_key_here'
python scripts/run_experiment.py  # If not already run

# 3. Generate comparison report
cd /home/jeremy/000-projects/nixtla
python 004-scripts/compare_timegpt_vs_statsforecast.py
```

**Outputs**:
- CSV: `004-scripts/compare_outputs/timegpt_vs_statsforecast_metrics.csv`
- Report: `000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md`

The aggregator compares metrics (sMAPE, MAE) across both labs and generates CEO-friendly summary reports. StatsForecast results are optional - if not run, aggregator generates TimeGPT-only report with PENDING status.

## Next Steps

After validating the baseline workflow:

1. **Compare with TimeGPT**: Run equivalent experiments in `timegpt-lab/` and compare metrics
2. **Add more models**: Extend to AutoARIMA, AutoCES, AutoTheta
3. **Custom datasets**: Add domain-specific daily datasets to `data/`
4. **CI dry-run**: Implement dry-run mode for CI integration (no models fit, synthetic metrics)
5. **Promote to plugin**: Integrate validated workflows into `005-plugins/nixtla-baseline-lab/`

## Promotion Path

When a StatsForecast workflow is stable and validated:
- **Skills**: Promote to `003-skills/.claude/skills/nixtla-statsforecast-*`
- **Scripts**: Integrate into `005-plugins/nixtla-baseline-lab/scripts/`
- **Reports**: Archive to `000-docs/` with AA-REPT or AA-STAT type codes

## Troubleshooting

### ImportError: No module named 'statsforecast'

**Solution**: Install statsforecast
```bash
pip install statsforecast utilsforecast
```

### Dataset Not Found

**Solution**: Ensure you're running from the statsforecast-lab directory:
```bash
cd 002-workspaces/statsforecast-lab
python scripts/run_statsforecast_baseline.py
```

### Model Fitting Errors

**Cause**: Insufficient data or incompatible data format
**Solution**: Ensure dataset has > 14 points per series and matches M4 schema (`unique_id`, `ds`, `y`)

---

**Lab Status**: ✅ Operational (Phase 07)
**Last Updated**: 2025-12-08
**Contact**: jeremy@intentsolutions.io
