# Nixtla Baseline Lab Plugin

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║              🔬 NIXTLA BASELINE LAB PLUGIN                   ║
║         Statistical Forecasting & M4 Benchmarking            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## Plugin Structure

```
🔬 nixtla-baseline-lab/
│
├── 📖 README.md
│
├── 🤖 agents/
│   └── 📝 nixtla-baseline-analyst.md
│
├── ⚡ commands/
│   ├── 📋 nixtla-baseline-m4.md
│   └── 📋 nixtla-baseline-setup.md
│
├── 💾 data/
│   └── 📊 m4/
│       ├── M4-Daily.csv
│       ├── M4-Hourly.csv
│       ├── M4-Monthly.csv
│       └── M4-Weekly.csv
│
├── 🔧 scripts/
│   ├── 🐍 nixtla_baseline_mcp.py ⭐ (MCP Server)
│   ├── 🐍 timegpt_client.py
│   ├── 📦 requirements.txt
│   └── 🛠️  setup_nixtla_env.sh
│
├── 🎯 skills/
│   └── 📚 nixtla-baseline-review/
│       ├── 📄 SKILL.md
│       └── 📁 resources/
│
└── 🧪 tests/
    ├── 📂 csv_test/
    ├── 📂 custom/
    ├── 📊 data/
    ├── 🏆 golden_tasks/
    ├── 📂 m4_test/
    └── 🐍 run_baseline_m4_smoke.py ✨
```

---

## What It Does

**Nixtla Baseline Lab** is a statistical forecasting benchmark plugin that compares multiple baseline models against M4 competition datasets. It provides a rapid testing environment for evaluating forecast accuracy using industry-standard metrics (sMAPE, MASE).

**Who It Helps**:
- 📊 Data scientists evaluating forecasting models
- 🔬 Researchers comparing baseline performance
- 🏢 Teams needing quick forecasting benchmarks
- 🎯 Developers testing time-series implementations

**Key Value**: Run comprehensive model comparisons in 90 seconds with offline datasets - no API keys required.

---

## Branch-by-Branch Description

### 🤖 agents/

**Purpose**: AI agent definitions for Claude Code

**Contents**:
- `nixtla-baseline-analyst.md` - Agent that assists with baseline model analysis and interpretation

**What it does**: Provides intelligent assistance when analyzing forecasting results, suggesting which models performed best and why.

---

### ⚡ commands/

**Purpose**: Slash commands for quick plugin actions

**Contents**:
- `nixtla-baseline-m4.md` - Slash command to run M4 benchmarking
- `nixtla-baseline-setup.md` - Slash command to set up the environment

**What it does**: Enables users to type `/nixtla-baseline-m4` in Claude Code to instantly run benchmarks without writing code.

---

### 💾 data/m4/

**Purpose**: M4 Competition benchmark datasets

**Contents**:
- `M4-Daily.csv` - 4,227 daily time series
- `M4-Hourly.csv` - 414 hourly time series
- `M4-Monthly.csv` - 48,000 monthly time series
- `M4-Weekly.csv` - 359 weekly time series

**What it does**: Provides real-world time-series data from the M4 forecasting competition for testing. These are industry-standard benchmarks used globally.

**Size**: ~50MB of historical time-series data across multiple frequencies.

---

### 🔧 scripts/

**Purpose**: Core plugin functionality and utilities

#### `nixtla_baseline_mcp.py` ⭐ (MCP Server)

**What it does**:
- Model Context Protocol server that exposes forecasting tools to Claude Code
- Runs StatsForecast models (AutoETS, AutoTheta, SeasonalNaive, etc.)
- Generates benchmark reports
- Calculates accuracy metrics (sMAPE, MASE)

**Key Functions**:
- `run_baselines()` - Execute forecasting models on datasets
- `get_nixtla_compatibility_info()` - Check installed library versions
- `generate_benchmark_report()` - Create markdown reports from results
- `generate_github_issue_draft()` - Template for bug reports

**MCP Integration**: Communicates with Claude via stdio for real-time forecasting.

#### `timegpt_client.py`

**What it does**:
- Client wrapper for TimeGPT API calls
- Handles API authentication
- Formats requests/responses

**When to use**: When comparing baseline models against TimeGPT (requires API key).

#### `setup_nixtla_env.sh`

**What it does**:
- Automated environment setup script
- Installs Python dependencies
- Creates virtual environment
- Validates installation

**Usage**: Run once during initial plugin setup.

---

### 🎯 skills/nixtla-baseline-review/

**Purpose**: Claude Code skill for reviewing baseline results

**What it does**:
- Automatically activates when Claude sees forecasting results
- Provides expert analysis of metrics
- Suggests model improvements
- Identifies data quality issues

**Triggers**: Activates when user says "review these baseline results" or similar phrases.

---

### 🧪 tests/

**Purpose**: Comprehensive test suite for validation

#### `golden_tasks/`
**What it does**: Production smoke tests that must pass before release. Tests the entire workflow end-to-end.

#### `run_baseline_m4_smoke.py` ✨
**What it does**:
- 90-second smoke test
- Runs 3 baseline models on M4 Daily subset
- Validates metrics are within expected ranges
- Offline test (no API required)

**Exit codes**:
- 0 = All tests passed
- 1 = Tests failed

#### Other test directories:
- `csv_test/` - Custom CSV file testing
- `custom/` - User-defined test scenarios
- `m4_test/` - Full M4 dataset tests
- `data/` - Test fixtures and sample data

---

## Terminal How-To Guide

### Initial Setup

```bash
# Navigate to plugin directory
cd /home/jeremy/000-projects/nixtla/005-plugins/nixtla-baseline-lab

# Run automated setup (installs dependencies)
./scripts/setup_nixtla_env.sh --venv

# Activate virtual environment
source .venv-nixtla-baseline/bin/activate

# Verify installation
pip list | grep -E "statsforecast|mlforecast|nixtla"
```

**Expected output**: statsforecast, mlforecast, and nixtla packages installed.

---

### Running Quick Smoke Test

```bash
# From plugin root directory
python tests/run_baseline_m4_smoke.py

# With verbose output
python tests/run_baseline_m4_smoke.py --verbose

# Save results to file
python tests/run_baseline_m4_smoke.py > results.txt
```

**Expected time**: ~90 seconds
**Expected output**:
```
✓ AutoETS model completed
✓ AutoTheta model completed
✓ SeasonalNaive model completed
All tests passed! (sMAPE: 12.3%, MASE: 0.89)
```

---

### Running M4 Benchmarking via Slash Command

```bash
# Inside Claude Code CLI
/nixtla-baseline-m4 demo_preset=m4_daily_small

# Run with specific frequency
/nixtla-baseline-m4 frequency=monthly horizon=12

# Run with custom models
/nixtla-baseline-m4 models=AutoETS,AutoTheta,AutoARIMA
```

**What happens**:
1. Loads M4 dataset
2. Runs specified models
3. Calculates sMAPE and MASE
4. Generates markdown report
5. Shows top-performing model

---

### Using MCP Server Directly

```bash
# Start MCP server (usually automatic via Claude Code)
python scripts/nixtla_baseline_mcp.py

# The server exposes these tools:
# - run_baselines
# - get_nixtla_compatibility_info
# - generate_benchmark_report
# - generate_github_issue_draft
```

**Note**: Claude Code automatically manages the MCP server lifecycle. Manual startup is rarely needed.

---

### Testing Custom Data

```bash
# Prepare your CSV with columns: unique_id, ds, y
# Example:
# unique_id,ds,y
# store_001,2024-01-01,100
# store_001,2024-01-02,105
# ...

# Copy to test data directory
cp my_data.csv tests/csv_test/

# Run test
cd tests/csv_test
python ../../scripts/nixtla_baseline_mcp.py --data my_data.csv --horizon 7
```

---

### Checking Compatibility

```bash
# Check installed Nixtla libraries
python -c "from scripts.nixtla_baseline_mcp import get_nixtla_compatibility_info; print(get_nixtla_compatibility_info())"

# Expected output:
# {
#   "statsforecast": "1.6.0",
#   "mlforecast": "0.10.0",
#   "nixtla": "0.5.1",
#   "python": "3.10.12"
# }
```

---

### Generating Reports

```bash
# After running benchmarks, results are in metrics.csv
# Generate markdown report:
python scripts/nixtla_baseline_mcp.py generate-report \
  --metrics results/metrics.csv \
  --output report.md

# View report
cat report.md
# or
less report.md
```

---

### Troubleshooting

#### Error: "Module 'statsforecast' not found"

```bash
# Solution: Install requirements
pip install -r scripts/requirements.txt
```

#### Error: "Data file not found"

```bash
# Solution: Verify M4 data exists
ls -lh data/m4/

# If missing, download from M4 competition
# Or use custom data in tests/csv_test/
```

#### Error: "MCP server not responding"

```bash
# Solution: Restart Claude Code CLI
# The MCP server auto-starts when Claude Code launches
```

---

## Performance Benchmarks

| Dataset | Records | Models | Runtime | Memory |
|---------|---------|--------|---------|--------|
| M4 Daily (small) | 100 series | 3 models | ~90s | <2GB |
| M4 Daily (full) | 4,227 series | 3 models | ~15min | ~4GB |
| M4 Monthly (full) | 48,000 series | 3 models | ~45min | ~8GB |

---

## Common Use Cases

### Use Case 1: Quick Model Comparison

```bash
# I need to compare baseline models on my data
cd 005-plugins/nixtla-baseline-lab
python scripts/nixtla_baseline_mcp.py --data my_sales.csv --horizon 30
```

**Result**: sMAPE and MASE for AutoETS, AutoTheta, SeasonalNaive in ~2 minutes.

---

### Use Case 2: M4 Competition Benchmarking

```bash
# I want to see how models perform on industry-standard data
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**Result**: Official M4 benchmark scores for comparison with published research.

---

### Use Case 3: CI/CD Integration

```bash
# Run in GitHub Actions or CI pipeline
python tests/run_baseline_m4_smoke.py
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
  echo "Baseline tests failed!"
  exit 1
fi
```

**Result**: Automated testing before deployment.

---

## Key Metrics Explained

### sMAPE (Symmetric Mean Absolute Percentage Error)
- **Range**: 0% to 200%
- **Lower is better**
- **Interpretation**:
  - <10% = Excellent
  - 10-20% = Good
  - 20-50% = Acceptable
  - >50% = Poor

### MASE (Mean Absolute Scaled Error)
- **Range**: 0 to ∞
- **Lower is better**
- **Interpretation**:
  - <1.0 = Better than naive forecast
  - 1.0 = Equal to naive forecast
  - >1.0 = Worse than naive forecast

---

## Integration with Other Plugins

**Works with**:
- `nixtla-bigquery-forecaster` - Compare baseline models vs cloud forecasts
- `nixtla-search-to-slack` - Share benchmark results with team
- `nixtla-timegpt-lab` - Compare statistical baselines vs TimeGPT

---

## Support & Resources

- **Plugin README**: `005-plugins/nixtla-baseline-lab/README.md`
- **Test Data**: `005-plugins/nixtla-baseline-lab/data/m4/`
- **Example Scripts**: `005-plugins/nixtla-baseline-lab/tests/`

---

**Version**: 1.7.0
**Status**: ✅ Production Ready
**Last Updated**: 2025-12-09
