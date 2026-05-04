# Nixtla Plugin Suite – Getting Started Guide

**For:** Max Mergenthaler (Nixtla CEO)
**Version:** 1.3.0 | **Updated:** 2025-12-06
**What's Live:** 3 working plugins, 8 production skills, 8 prediction market skills (documented)

---

## Prerequisites

- Python 3.10+
- Claude Code installed
- Git

---

## Section 1: Working Plugins

### 1.1 Baseline Lab (Benchmarking)

Runs statsforecast baselines on M4 data. Fully offline, no API costs.

```bash
# Clone and setup
git clone https://github.com/jeremylongshore/plugins-nixtla.git
cd plugins-nixtla/plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Run in Claude Code
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

**Output:** Metrics CSV, summary report, reproducibility bundle (~90 seconds)

---

### 1.2 BigQuery Forecaster (Cloud Integration)

Runs statsforecast on BigQuery data via Cloud Functions.

```bash
cd plugins/nixtla-bigquery-forecaster
source .venv/bin/activate
python test_local.py
```

**Use case:** Forecasting on large datasets without moving data out of BigQuery.

---

### 1.3 Search-to-Slack (Content Automation)

Automated web search → AI summary → Slack posting.

```bash
cd plugins/nixtla-search-to-slack
pip install -r requirements.txt
cp .env.example .env  # Add API keys
pytest tests/
```

**Use case:** Monitor web for Nixtla mentions, auto-curate content.

---

## Section 2: Claude Skills Pack (8 Skills)

AI skills that activate automatically when Claude detects forecasting context.

### Quick Install

```bash
pip install -e packages/nixtla-claude-skills-installer
cd /path/to/your/project
nixtla-skills init
```

### Skills Available

| Skill | What It Does |
|-------|--------------|
| `nixtla-timegpt-lab` | Transforms Claude into Nixtla forecasting expert |
| `nixtla-experiment-architect` | Scaffolds complete forecasting experiments |
| `nixtla-schema-mapper` | Maps data to Nixtla format (unique_id, ds, y) |
| `nixtla-timegpt-finetune-lab` | Guides TimeGPT fine-tuning |
| `nixtla-prod-pipeline-generator` | Generates production pipelines |
| `nixtla-usage-optimizer` | Audits usage, suggests cost savings |
| `nixtla-skills-bootstrap` | Installs/updates skills |
| `nixtla-skills-index` | Lists available skills |

**Compliance:** 95%+ Anthropic standard

---

## Section 3: Prediction Markets Vertical (NEW in v1.3.0)

8 documented skills for analyzing Polymarket/Kalshi prediction markets with TimeGPT.

### Skills Documented (PRDs De-Hyped for Technical Review)

| Skill | Purpose |
|-------|---------|
| `nixtla-polymarket-analyst` | Fetch odds → TimeGPT forecast → Cross-platform analysis |
| `nixtla-arbitrage-detector` | Detect cross-platform pricing discrepancies |
| `nixtla-batch-forecaster` | Batch forecast multiple contracts |
| `nixtla-contract-schema-mapper` | Transform prediction market data to Nixtla format |
| `nixtla-event-impact-modeler` | Model event impacts on market odds |
| `nixtla-forecast-validator` | Validate forecast accuracy with backtesting |
| `nixtla-liquidity-forecaster` | Forecast orderbook depth and spreads |
| `nixtla-model-selector` | Select best model (TimeGPT vs StatsForecast) |

**Status:** All PRDs reviewed and de-hyped. Analysis-only tools, not trading bots. No profit guarantees.

**Location:** `000-docs/planned-skills/prediction-markets/*/PRD.md`

---

## Section 4: Optional TimeGPT Comparison

Add TimeGPT to any baseline run (requires API key):

```bash
export NIXTLA_TIMEGPT_API_KEY="your-key"

# In Claude Code
/nixtla-baseline-m4 demo_preset=m4_daily_small include_timegpt=true timegpt_max_series=2
```

---

## Quick Reference

| What | Where | Status |
|------|-------|--------|
| Baseline Lab plugin | `plugins/nixtla-baseline-lab/` | Production |
| BigQuery plugin | `plugins/nixtla-bigquery-forecaster/` | Working demo |
| Search-to-Slack | `plugins/nixtla-search-to-slack/` | MVP |
| Skills Pack | `skills-pack/.claude/skills/` | Production (8 skills) |
| Prediction Markets | `000-docs/planned-skills/prediction-markets/` | Documented (8 PRDs) |
| Skills installer | `packages/nixtla-claude-skills-installer/` | Production |

---

## Contact

**Jeremy Longshore** | Intent Solutions
jeremy@intentsolutions.io | 251.213.1115

---

**Repository:** https://github.com/jeremylongshore/plugins-nixtla
