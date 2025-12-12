# Baseline Lab - User Journey

**Plugin:** nixtla-baseline-lab
**Last Updated:** 2025-12-12

---

## Quick Start Journey

### Step 1: Setup Environment

```bash
cd 005-plugins/nixtla-baseline-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

### Step 2: Run Smoke Test

```bash
python tests/run_baseline_m4_smoke.py
```

**Expected Output:**
```
Running baseline smoke test...
Loading M4 Daily data (5 series, h=7)...
Running AutoETS, AutoTheta, SeasonalNaive...
Calculating sMAPE and MASE...
GOLDEN TASK PASSED
```

### Step 3: Review Results

Results saved to:
```
nixtla_baseline_m4_test/
├── results_M4_Daily_h7.csv    # Per-series metrics
└── summary_M4_Daily_h7.txt    # Averaged results
```

---

## Claude Code Journey

### Using Slash Command

In Claude Code:

```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

Claude will:
1. Load M4 Daily data (first 5 series)
2. Run AutoETS, AutoTheta, SeasonalNaive with h=7
3. Report sMAPE and MASE metrics
4. Interpret results

### Interpreting Results

Example output:

| Model | sMAPE | MASE |
|-------|-------|------|
| AutoETS | 0.77% | 0.422 |
| AutoTheta | 0.85% | 0.454 |
| SeasonalNaive | 1.49% | 0.898 |

**Interpretation:**
- sMAPE < 2% = excellent accuracy
- MASE < 1.0 = beats naive baseline
- AutoETS best performer on this subset

---

## Using Your Own Data

### CSV Format Required

```csv
unique_id,ds,y
store_001,2024-01-01,100
store_001,2024-01-02,105
store_002,2024-01-01,200
store_002,2024-01-02,210
```

- `unique_id`: Series identifier
- `ds`: Timestamp (date or datetime)
- `y`: Value to forecast

### Running Custom Data

```bash
python scripts/nixtla_baseline_mcp.py --data your_file.csv --horizon 7
```

---

## Error Scenarios

### "Module not found"

```bash
pip install -r scripts/requirements.txt
```

### "Data file not found"

```bash
ls data/m4/  # Check M4 files exist
```

### Smoke Test Fails

```bash
# Check Python version (3.10+ required)
python3 --version

# Reinstall dependencies
pip install --force-reinstall -r scripts/requirements.txt
```

---

## Tips

1. **Start small**: Use `m4_daily_small` preset (5 series) for quick validation
2. **Check metrics**: sMAPE is percentage-based, MASE is scale-independent
3. **Compare models**: AutoETS usually beats SeasonalNaive baseline
4. **Save results**: Each run creates dated results files
