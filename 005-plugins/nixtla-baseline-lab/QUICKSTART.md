# Quickstart

```bash
# Setup (one-time)
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt

# Run smoke test (~30 seconds)
python tests/run_baseline_m4_smoke.py
```

**Expected output:** `GOLDEN TASK PASSED`

## What It Does

Runs 3 forecasting models (AutoETS, AutoTheta, SeasonalNaive) on M4 benchmark data and outputs:
- `nixtla_baseline_m4_test/results_M4_Daily_h7.csv` - Per-series metrics
- `nixtla_baseline_m4_test/summary_M4_Daily_h7.txt` - Averaged results

## Metrics

| Model | sMAPE | MASE |
|-------|-------|------|
| AutoETS | 0.77% | 0.422 |
| AutoTheta | 0.85% | 0.454 |
| SeasonalNaive | 1.49% | 0.898 |

## Requirements

- Python 3.10+
- No API keys needed (uses open-source statsforecast)
