#!/usr/bin/env bash
#
# Nixtla Review – Optional TimeGPT Showdown Demo
#
# This script runs a small TimeGPT comparison on 3 series.
# REQUIRES: NIXTLA_TIMEGPT_API_KEY environment variable
# COST WARNING: Makes actual TimeGPT API calls (limited to 3 series)
#

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_DIR="$REPO_ROOT/plugins/nixtla-baseline-lab"

echo "=========================================="
echo "Nixtla Review – TimeGPT Showdown Demo"
echo "=========================================="
echo ""

# Check for API key
if [[ -z "${NIXTLA_TIMEGPT_API_KEY:-}" ]]; then
    echo "NIXTLA_TIMEGPT_API_KEY is not set."
    echo ""
    echo "The TimeGPT showdown is OPTIONAL and requires a valid API key."
    echo "Offline statsforecast baselines are available without any keys."
    echo ""
    echo "To run this demo:"
    echo "  1. Get a TimeGPT API key from https://dashboard.nixtla.io/"
    echo "  2. Set the environment variable:"
    echo "     export NIXTLA_TIMEGPT_API_KEY=\"your-api-key-here\""
    echo "  3. Run this script again"
    echo ""
    echo "Skipping TimeGPT showdown (not an error)."
    exit 0
fi

echo "API Key: Found (${#NIXTLA_TIMEGPT_API_KEY} characters)"
echo "Repository: $(basename "$REPO_ROOT")"
echo "Plugin: nixtla-baseline-lab"
echo "Mode: TimeGPT showdown (limited to 3 series)"
echo ""
echo "COST WARNING:"
echo "  - This demo makes REAL TimeGPT API calls"
echo "  - Limited to 3 series to minimize cost"
echo "  - Check your Nixtla dashboard for current pricing"
echo "  - Press Ctrl+C now to abort, or wait 5 seconds to continue..."
echo ""

sleep 5

# Check if plugin directory exists
if [[ ! -d "$PLUGIN_DIR" ]]; then
    echo "ERROR: Plugin directory not found: $PLUGIN_DIR"
    exit 1
fi

cd "$PLUGIN_DIR"

# Activate virtualenv if it exists
if [[ -d ".venv-nixtla-baseline" ]]; then
    echo "Activating virtualenv..."
    source .venv-nixtla-baseline/bin/activate
fi

# Check dependencies
echo "Checking dependencies..."
python3 -c "import statsforecast" 2>/dev/null || {
    echo "ERROR: statsforecast not installed"
    exit 1
}

python3 -c "import nixtla" 2>/dev/null || {
    echo "WARNING: nixtla SDK not installed"
    echo "Installing nixtla SDK..."
    pip install nixtla
}

echo ""
echo "Running TimeGPT showdown demo..."
echo "  - Baseline models: SeasonalNaive, AutoETS, AutoTheta"
echo "  - TimeGPT comparison: 3 series (cost-controlled)"
echo "  - Dataset: M4 Daily sample"
echo "  - Horizon: 7 days"
echo ""

# Run test mode with TimeGPT enabled
python3 scripts/nixtla_baseline_mcp.py test --include-timegpt

echo ""
echo "=========================================="
echo "TimeGPT showdown demo complete!"
echo "=========================================="
echo ""
echo "Results available in: $PLUGIN_DIR/nixtla_baseline_m4_test/"
echo ""
echo "Files generated:"
echo "  - results_M4_Daily_h7.csv       (baseline metrics)"
echo "  - summary_M4_Daily_h7.txt       (baseline summary)"
echo "  - benchmark_report_M4_Daily_h7.md (benchmark report)"
echo "  - timegpt_showdown_M4_Daily_h7.txt (TimeGPT vs baselines comparison)"
echo "  - run_manifest.json             (includes TimeGPT config)"
echo "  - compat_info.json              (library versions)"
echo ""
echo "Next steps:"
echo "  1. Review TimeGPT comparison: cat nixtla_baseline_m4_test/timegpt_showdown_M4_Daily_h7.txt"
echo "  2. Check if TimeGPT beat the baselines"
echo "  3. Remember: Results on 3 series are indicative, not conclusive"
echo ""
echo "DISCLAIMER:"
echo "  - Small sample size (3 series) = indicative results only"
echo "  - Official TimeGPT behavior: https://docs.nixtla.io/"
echo "  - Cost and pricing: https://dashboard.nixtla.io/"
echo ""
