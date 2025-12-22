---
name: nixtla-baseline-setup
description: Install Nixtla dependencies and prepare environment for baseline forecasting
---

# Nixtla Baseline Lab – Environment Setup

This command automates the setup of Nixtla OSS (Open Source Software) dependencies required to run baseline forecasting models.

## What This Command Does

When the user runs `/nixtla-baseline-setup`, you should:

1. **Check prerequisites**: Verify Python 3 and pip are available
2. **Run the setup script**: Execute `setup_nixtla_env.sh` to install dependencies
3. **Verify installations**: Confirm that `statsforecast` and `datasetsforecast` can be imported
4. **Report status**: Tell the user whether setup succeeded and what to do next

## Step-by-Step Workflow

### Step 1: Confirm Working Directory

Ensure you're at the repository root. If not already there, navigate to it:

```bash
cd /home/jeremy/000-projects/nixtla
```

### Step 2: Navigate to Plugin Directory

Change to the plugin directory:

```bash
cd plugins/nixtla-baseline-lab
```

### Step 3: Verify Setup Script Exists

Check that the setup script is present and executable:

```bash
ls -la scripts/setup_nixtla_env.sh
```

If the file exists but is not executable, make it executable:

```bash
chmod +x scripts/setup_nixtla_env.sh
```

### Step 4: Ask User About Environment Preference

Before running the setup, ask the user:

**"Would you like to install Nixtla dependencies into your current Python environment, or create a dedicated virtualenv?"**

Provide options:
- **Option A**: Current environment (faster, no isolation)
- **Option B**: Dedicated virtualenv (isolated, recommended for clean testing)

### Step 5: Run Setup Script

Based on the user's choice:

**Option A (Current environment)**:
```bash
./scripts/setup_nixtla_env.sh
```

**Option B (Virtualenv)**:
```bash
./scripts/setup_nixtla_env.sh --venv
```

The script will:
- Check for Python 3 and pip
- Install dependencies from `scripts/requirements.txt`:
  - `statsforecast` – Classical forecasting methods
  - `datasetsforecast` – M4 benchmark datasets
  - `pandas` and `numpy` – Data processing
- Print version information
- Report success or failure

### Step 6: Verify Nixtla OSS Imports

After the setup script completes successfully, run a quick import check:

```bash
python3 -c "import statsforecast, datasetsforecast; print('OK: Nixtla OSS imports successful')"
```

Expected output:
```
OK: Nixtla OSS imports successful
```

If this fails, troubleshoot using the section below.

### Step 7: Report Success

If all steps pass, tell the user:

**"✅ Nixtla Baseline Lab is ready!"**

Then provide next steps:
- "You can now run `/nixtla-baseline-m4 horizon=7 series_limit=5` to generate your first baseline forecast."
- "After running baselines, ask: 'Which baseline model performed best overall in the last run?'"

## What Gets Installed

The setup script installs Nixtla's open-source forecasting libraries:

- **statsforecast** (≥1.5.0) – Classical statistical forecasting methods:
  - SeasonalNaive
  - AutoETS (exponential smoothing state space)
  - AutoTheta (Theta method with optimization)

- **datasetsforecast** (≥0.0.8) – Public benchmark datasets:
  - M4 Competition datasets (Daily, Monthly, Quarterly, Yearly)
  - Standard evaluation utilities

- **pandas** (≥2.0.0) – Data manipulation and analysis

- **numpy** (≥1.24.0) – Numerical computing

All libraries are publicly available via PyPI and do not require API keys or authentication.

## Troubleshooting

### Python Not Found

**Error**: `python3: command not found`

**Solution**:
- **Ubuntu/Debian**: `sudo apt-get install python3 python3-pip`
- **macOS**: `brew install python3`
- **Windows**: Download from https://www.python.org/downloads/

After installing, verify with:
```bash
python3 --version
```

### pip Not Found

**Error**: `pip: command not found`

**Solution**:
- **Ubuntu/Debian**: `sudo apt-get install python3-pip`
- **macOS**: `python3 -m ensurepip`
- **Check existing pip**: `python3 -m pip --version`

### Package Installation Fails

**Error**: `Could not install packages due to an EnvironmentError`

**Possible causes and solutions**:

1. **Corporate firewall or proxy**:
   - Try: `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r scripts/requirements.txt`
   - Or configure proxy: `export HTTP_PROXY=http://proxy.example.com:8080`

2. **Insufficient permissions**:
   - Use virtualenv option: `./scripts/setup_nixtla_env.sh --venv`
   - Or install with `--user` flag: `pip install --user -r scripts/requirements.txt`

3. **Outdated pip**:
   - Upgrade pip first: `python3 -m pip install --upgrade pip`

4. **Python version too old**:
   - Verify Python 3.8+: `python3 --version`
   - Upgrade Python if necessary

### Import Errors After Installation

**Error**: `ModuleNotFoundError: No module named 'statsforecast'`

**Solution**:
- Verify installation: `python3 -m pip show statsforecast`
- If not found, manually install: `python3 -m pip install statsforecast`
- Check you're using the correct Python: `which python3`

### Long Download Times

**Issue**: M4 dataset download takes several minutes on first run

**Expected behavior**:
- The M4 Daily dataset (~50MB) downloads automatically on first use
- This is normal and only happens once
- Subsequent runs use cached data from `plugins/nixtla-baseline-lab/data/`

### Disk Space Concerns

**Requirements**:
- Python packages: ~200-300 MB
- M4 datasets (cached): ~50-100 MB
- Generated results: < 10 MB per run

If disk space is limited, clean up old results:
```bash
rm -rf plugins/nixtla-baseline-lab/nixtla_baseline_m4/
```

## Environment Isolation

If you used the `--venv` option, the virtualenv is created at:
```
plugins/nixtla-baseline-lab/.venv-nixtla-baseline/
```

**To activate it manually** (for debugging or manual runs):
```bash
cd plugins/nixtla-baseline-lab
source .venv-nixtla-baseline/bin/activate
```

**To deactivate**:
```bash
deactivate
```

The MCP server will automatically use this virtualenv if it exists.

## Notes for Claude Code

- **Be transparent**: Show the user what commands you're running and why
- **Handle errors gracefully**: If the setup script fails, read the error output and provide specific guidance
- **Don't assume success**: Always verify imports before declaring success
- **Respect user choice**: Let them choose between current environment vs virtualenv

## Documentation

For complete technical details, see:
- Architecture: `000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`
- Planning: `000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`
- Phase 5 AAR: `000-docs/019-AA-AACR-phase-05-setup-and-validation.md`
