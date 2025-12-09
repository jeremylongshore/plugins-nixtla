# TimeGPT Lab Environment Setup

**Purpose**: Configure local development environment for TimeGPT API experimentation and workflow development.

**Last Updated**: 2025-12-08

## Prerequisites

- **Python**: 3.9+ (recommended: 3.10 or 3.11)
- **Git**: For cloning and version control
- **API Access**: Valid Nixtla TimeGPT API key (obtain from [Nixtla dashboard](https://dashboard.nixtla.io/))

## Installation Steps

### 1. Python Environment

We recommend using a virtual environment to isolate TimeGPT lab dependencies:

```bash
# From repository root
cd 002-workspaces/timegpt-lab

# Create virtual environment
python3 -m venv .venv-timegpt

# Activate (Linux/Mac)
source .venv-timegpt/bin/activate

# Activate (Windows)
.venv-timegpt\Scripts\activate
```

### 2. Install TimeGPT Dependencies

TimeGPT lab requires the Nixtla SDK and supporting libraries:

```bash
# Install core TimeGPT dependencies
pip install nixtla>=0.5.0 utilsforecast pandas>=1.5.0

# Optional: Install additional forecasting libraries for comparison
pip install statsforecast mlforecast
```

**Note**: If the repository root has a `pyproject.toml` or `requirements.txt` that already includes these dependencies, you can install from there instead:

```bash
# From repository root
pip install -e .
```

### 3. Set Environment Variables

TimeGPT requires an API key. **Never commit this key to git**.

#### Option A: Local Shell Export (Session-Only)

```bash
export NIXTLA_TIMEGPT_API_KEY="your_api_key_here"
export NIXTLA_ENV="dev"  # Optional: dev, demo, prod
```

Add to your `~/.bashrc` or `~/.zshrc` for persistence across sessions.

#### Option B: Local .env File (Recommended for Development)

1. Copy the example file:

```bash
cp .env.example .env
```

2. Edit `.env` with your actual API key:

```dotenv
NIXTLA_TIMEGPT_API_KEY=your_actual_api_key_here
NIXTLA_ENV=dev
```

3. Load the `.env` file before running scripts:

```bash
# Using python-dotenv
pip install python-dotenv

# In your scripts:
from dotenv import load_dotenv
load_dotenv()
```

**Important**: `.env` is gitignored and will NOT be committed.

### 4. Verify Installation

Run the environment validation script:

```bash
python scripts/validate_env.py
```

Expected output on success:

```
✓ Python 3.10.x (supported)
✓ NIXTLA_TIMEGPT_API_KEY environment variable present
✓ nixtla package installed (version 0.5.x)
✓ utilsforecast package installed
✓ pandas package installed

Environment validation: PASSED
```

If validation fails, review error messages and ensure all steps above were completed.

## Common Issues

### ImportError: No module named 'nixtla'

**Solution**: Install dependencies:

```bash
pip install nixtla utilsforecast pandas
```

### Environment variable NIXTLA_TIMEGPT_API_KEY not set

**Solution**: Set the environment variable using one of the methods above. Verify with:

```bash
echo $NIXTLA_TIMEGPT_API_KEY  # Should print your key (or first few chars)
```

### Python version < 3.9

**Solution**: Upgrade Python. TimeGPT requires Python 3.9+.

```bash
python --version  # Check current version
```

## Next Steps

Once your environment is validated:

1. **Explore sample scripts**: `scripts/` directory contains TimeGPT workflows
2. **Run smoke tests**: `python scripts/timegpt_smoke_placeholder.py` (when implemented)
3. **Experiment with data**: Use `data/` for sample datasets
4. **Generate reports**: Results will be saved to `reports/`

## Security Reminders

- **Never commit** `.env` or any file containing `NIXTLA_TIMEGPT_API_KEY`
- **Never share** API keys in logs, screenshots, or documentation
- **Rotate keys** if accidentally exposed
- **Use read-only keys** for experimentation when available

## References

- Nixtla TimeGPT Documentation: https://docs.nixtla.io/
- Nixtla SDK (nixtla package): https://github.com/Nixtla/nixtla
- Repository standards: `{baseDir}/002-workspaces/.directory-standards.md`

---

**Maintained by**: TimeGPT Lab Team
**Contact**: jeremy@intentsolutions.io
