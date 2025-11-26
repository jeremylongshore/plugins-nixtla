#!/usr/bin/env bash
#
# Nixtla Review – Offline Baseline Demo
#
# This script runs the Nixtla Baseline Lab plugin in offline statsforecast-only mode.
# No API keys required. No network calls. Pure reproducible baseline experiment.
#

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_DIR="$REPO_ROOT/plugins/nixtla-baseline-lab"

echo "=========================================="
echo "Nixtla Review – Offline Baseline Demo"
echo "=========================================="
echo ""
echo "Repository: $(basename "$REPO_ROOT")"
echo "Plugin: nixtla-baseline-lab"
echo "Mode: Offline statsforecast-only (no TimeGPT)"
echo ""

# Check if plugin directory exists
if [[ ! -d "$PLUGIN_DIR" ]]; then
    echo "ERROR: Plugin directory not found: $PLUGIN_DIR"
    exit 1
fi

cd "$PLUGIN_DIR"

# Check if virtualenv exists, create if needed
if [[ ! -d ".venv-nixtla-baseline" ]]; then
    echo "Setting up virtualenv..."
    if [[ -x "./scripts/setup_nixtla_env.sh" ]]; then
        ./scripts/setup_nixtla_env.sh --venv
    else
        echo "WARNING: setup script not found, attempting to continue..."
    fi
fi

# Activate virtualenv if it exists
if [[ -d ".venv-nixtla-baseline" ]]; then
    echo "Activating virtualenv..."
    source .venv-nixtla-baseline/bin/activate
fi

# Check Python dependencies
echo "Checking dependencies..."
python3 -c "import statsforecast" 2>/dev/null || {
    echo "ERROR: statsforecast not installed. Run: pip install -r scripts/requirements.txt"
    exit 1
}

echo ""
echo "Running offline baseline demo..."
echo "  - Models: SeasonalNaive, AutoETS, AutoTheta"
echo "  - Dataset: M4 Daily (5 series sample)"
echo "  - Horizon: 7 days"
echo "  - Metrics: sMAPE, MASE"
echo ""

# Run test mode (offline only)
python3 scripts/nixtla_baseline_mcp.py test

echo ""
echo "=========================================="
echo "Offline baseline demo complete!"
echo "=========================================="
echo ""
echo "Results available in: $PLUGIN_DIR/nixtla_baseline_m4_test/"
echo ""
echo "Files generated:"
echo "  - results_M4_Daily_h7.csv       (per-series, per-model metrics)"
echo "  - summary_M4_Daily_h7.txt       (human-readable summary)"
echo "  - benchmark_report_M4_Daily_h7.md (Markdown benchmark report)"
echo "  - run_manifest.json             (reproducibility config)"
echo "  - compat_info.json              (library versions)"
echo ""
echo "Next steps:"
echo "  1. Review the summary: cat nixtla_baseline_m4_test/summary_M4_Daily_h7.txt"
echo "  2. Check metrics CSV: cat nixtla_baseline_m4_test/results_M4_Daily_h7.csv"
echo "  3. View benchmark: cat nixtla_baseline_m4_test/benchmark_report_M4_Daily_h7.md"
echo ""
echo "For TimeGPT comparison (optional): scripts/run_nixtla_review_timegpt.sh"
echo ""
