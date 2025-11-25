# Nixtla Baseline Lab – Claude Code Plugin

## What This Is

**Nixtla Baseline Lab** is a Claude Code plugin that runs Nixtla-style baseline time series forecasting models on public benchmark datasets (M4) directly inside your editor conversations.

This plugin demonstrates how to:
- Execute baseline forecasting workflows (SeasonalNaive, AutoETS, AutoTheta)
- Analyze model performance with AI-powered interpretation
- Generate reproducible benchmark results
- Integrate Nixtla's open-source forecasting stack into development workflows

## Who This Is For

This is an **internal Proof of Concept (PoC)** developed through collaboration between:
- **Nixtla** - Time series forecasting platform and research team
- **Intent Solutions** - AI/ML engineering and agent architecture

The plugin serves as a reference implementation for integrating Nixtla workflows into Claude Code, with patterns designed to scale to production agent systems.

## Data & Libraries

### Nixtla Open-Source Tools

This plugin uses Nixtla's open-source forecasting libraries:

- **`statsforecast`** - Classical statistical forecasting methods
  - SeasonalNaive (baseline benchmark)
  - AutoETS (exponential smoothing state space)
  - AutoTheta (Theta method with optimization)

- **`datasetsforecast`** - Benchmark time series datasets
  - M4 Competition datasets (Daily, Monthly, Quarterly, Yearly)
  - Standard evaluation utilities

### Public Benchmark Data Only

**Important**: This PoC uses **public benchmark datasets only**:
- M4 Daily dataset (starting point)
- No Nixtla customer data
- No production TimeGPT infrastructure
- No proprietary or sensitive time series

Future phases may integrate TimeGPT API for comparative analysis, but initial development focuses on reproducible open-source workflows.

## Plugin Components

This plugin demonstrates all major Claude Code plugin capabilities:

- **Commands** - `/nixtla-baseline-m4` slash command for running baseline models
- **Agents** - `nixtla-baseline-analyst` subagent for expert result interpretation
- **Skills** - `NixtlaBaselineReview` model-invoked capability for metric analysis
- **MCP Tools** - Local MCP server exposing `run_baselines` forecasting tool

## Documentation

For complete technical details, see the canonical 6767 documentation:

- **Architecture**: [`000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md`](../../000-docs/6767-OD-ARCH-nixtla-claude-plugin-poc-baseline-lab.md)
  - Plugin structure and component design
  - Code examples for all components
  - Data flow and integration patterns
  - Testing and debugging workflows

- **Planning**: [`000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md`](../../000-docs/6767-PP-PLAN-nixtla-claude-plugin-poc-baseline-lab.md)
  - Goals, non-goals, and scope
  - Phase-by-phase implementation plan
  - Success metrics and validation strategy
  - Future extension roadmap

## Installation

### From the Dev Marketplace

From the repository root:

```bash
# Start Claude Code
claude

# In Claude Code, add the local marketplace:
/plugin marketplace add ./

# Install the plugin:
/plugin install nixtla-baseline-lab@nixtla-dev-marketplace
```

### Install Python Dependencies

The MCP server requires Nixtla's open-source libraries:

```bash
cd plugins/nixtla-baseline-lab/scripts
pip install -r requirements.txt
```

This installs:
- `statsforecast` - Classical forecasting methods
- `datasetsforecast` - M4 benchmark datasets
- `pandas` and `numpy` - Data processing

## Quick Smoke Test

Test the plugin with a minimal baseline run:

1. **Install the plugin** (see Installation above)

2. **Install Python dependencies** (if not already done)

3. **Run a small baseline experiment** in Claude Code:
   ```
   /nixtla-baseline-m4 horizon=7 series_limit=5
   ```

   This will:
   - Load 5 series from M4 Daily dataset
   - Run SeasonalNaive, AutoETS, AutoTheta models
   - Forecast 7 days ahead
   - Write results to `nixtla_baseline_m4/` directory

4. **Analyze the results** by asking Claude:
   ```
   Which baseline model performed best in that run?
   ```

   Claude will use the `NixtlaBaselineReview` skill to interpret the metrics and provide analysis.

**Expected Runtime**: 30-60 seconds for 5 series

**Expected Output Files**:
- `nixtla_baseline_m4/results_M4_Daily_h7.csv` - Full metrics table
- `nixtla_baseline_m4/summary_M4_Daily_h7.txt` - Human-readable summary

## Status

**Current Phase**: Phase 4 - Testing, Skills wiring, dev marketplace

**Capabilities**:
- ✅ Run baseline forecasts on M4 Daily benchmark
- ✅ Calculate sMAPE and MASE metrics
- ✅ AI-powered result interpretation via Skills
- ✅ Strategic analysis via analyst agent
- ✅ Local dev marketplace for easy installation

## License

MIT License - see repository root LICENSE file.

## Contact

- **Technical Lead**: Jeremy Longshore (jeremy@intentsolutions.io)
- **Nixtla Collaboration**: Max Mergenthaler (max@nixtla.io)
- **Repository**: https://github.com/jeremylongshore/claude-code-plugins-nixtla

---

**Version**: 0.2.0 (Phase 4)
**Last Updated**: 2025-11-24
