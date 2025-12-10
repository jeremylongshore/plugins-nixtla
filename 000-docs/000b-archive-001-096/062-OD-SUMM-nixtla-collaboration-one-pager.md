# Nixtla x Intent Solutions: Claude Code Integration

**One-Pager for Stakeholder Review**
**Date**: 2025-12-08
**Version**: 1.6.0
**Status**: Experimental Showcase

---

## Executive Summary

This collaboration demonstrates how **Claude Code plugins and AI skills** can accelerate time-series forecasting workflows using Nixtla's open-source libraries (statsforecast, TimeGPT).

**What We Built**: 3 working plugins + 21 AI skills that make Claude an expert forecasting assistant.

---

## What's Inside

### Plugins (3 Working)

| Plugin | What It Does | Why It Matters | API Key |
|--------|--------------|----------------|---------|
| **Baseline Lab** | Runs statsforecast models (AutoETS, AutoTheta, SeasonalNaive) on M4 benchmark data | Proves Claude can execute forecasting workflows with reproducible results | No |
| **BigQuery Forecaster** | Forecasts BigQuery data via Cloud Functions | Shows enterprise integration (GCP + Nixtla + Claude) | Yes |
| **Search-to-Slack** | Finds Nixtla content across web/GitHub, posts AI summaries to Slack | Automates content curation for forecasting practitioners | Yes |

### AI Skills (21 Generated)

Skills transform Claude into a forecasting expert. When activated, Claude gains specialized knowledge and workflows.

#### Core Forecasting (5 skills)

| Skill | Purpose |
|-------|---------|
| `nixtla-anomaly-detector` | Detect outliers, level shifts, trend breaks in time series |
| `nixtla-exogenous-integrator` | Add external variables (weather, holidays) to forecasts |
| `nixtla-uncertainty-quantifier` | Generate prediction intervals and confidence bands |
| `nixtla-cross-validator` | Backtest models with time series cross-validation |
| `nixtla-timegpt2-migrator` | Migrate existing forecasts to TimeGPT 2 |

#### Prediction Markets (10 skills)

| Skill | Purpose |
|-------|---------|
| `nixtla-polymarket-analyst` | Analyze and forecast Polymarket contract prices |
| `nixtla-arbitrage-detector` | Find pricing inefficiencies across prediction markets |
| `nixtla-contract-schema-mapper` | Transform market data into Nixtla format |
| `nixtla-batch-forecaster` | Run forecasts on multiple contracts simultaneously |
| `nixtla-event-impact-modeler` | Model how events affect prediction market prices |
| `nixtla-forecast-validator` | Validate forecast quality against market outcomes |
| `nixtla-model-selector` | Choose optimal model based on data characteristics |
| `nixtla-liquidity-forecaster` | Predict market liquidity and trading volume |
| `nixtla-correlation-mapper` | Find correlations between related contracts |
| `nixtla-market-risk-analyzer` | Assess portfolio risk across prediction markets |

#### Live/Retroactive (6 skills)

| Skill | Purpose |
|-------|---------|
| `nixtla-timegpt-lab` | Interactive forecasting with TimeGPT/StatsForecast |
| `nixtla-experiment-architect` | Design and structure forecasting experiments |
| `nixtla-schema-mapper` | Convert data to Nixtla format (unique_id, ds, y) |
| `nixtla-timegpt-finetune-lab` | Fine-tune TimeGPT on custom datasets |
| `nixtla-prod-pipeline-generator` | Generate Airflow/Prefect production pipelines |
| `nixtla-usage-optimizer` | Audit and optimize TimeGPT API costs |

---

## How It Works

### User Experience

```
User: "Forecast next 14 days of sales using AutoETS"

Claude (with nixtla-timegpt-lab skill):
1. Reads user's data file
2. Validates schema (unique_id, ds, y)
3. Generates Python code using statsforecast
4. Executes forecast
5. Returns predictions + visualization
```

### Technical Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Claude Code                        │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Skills    │  │   Plugins   │  │  Commands   │ │
│  │ (21 total)  │  │ (3 working) │  │ /nixtla-*   │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │        │
│         ▼                ▼                ▼        │
│  ┌─────────────────────────────────────────────┐   │
│  │              MCP Server Layer               │   │
│  │   (Model Context Protocol - tool access)    │   │
│  └──────────────────────┬──────────────────────┘   │
└─────────────────────────┼───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                  Nixtla Stack                        │
├─────────────────────────────────────────────────────┤
│  statsforecast    │  TimeGPT API  │  datasetsforecast│
│  (open source)    │  (cloud API)  │  (benchmarks)    │
└─────────────────────────────────────────────────────┘
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Plugins Working | 3 |
| Skills Generated | 21 |
| Test Coverage | 100% |
| CI/CD Workflows | 7 |
| Baseline Lab Runtime | ~90 seconds |
| API Key Required | Only for TimeGPT features |

---

## Value Proposition

### For Nixtla

1. **Showcases Nixtla ecosystem** - statsforecast, TimeGPT, mlforecast integration
2. **New distribution channel** - Claude Code has growing developer adoption
3. **Reduces time-to-value** - Users get forecasting capabilities without setup
4. **Community engagement** - Open-source skills can be community-extended

### For Users

1. **Zero setup** - Baseline lab works offline, no API key
2. **Expert guidance** - Skills teach best practices as they execute
3. **Production patterns** - Generated code follows Nixtla conventions
4. **Cost optimization** - usage-optimizer skill audits API spending

---

## What's Next

### Phase 1 (Current): Showcase
- Demonstrate value with working plugins
- Validate skill patterns with 21 generated skills
- Prove CI/CD and quality gates

### Phase 2 (Planned): Integration
- TimeGPT API integration in baseline lab
- Comparative analysis (statsforecast vs TimeGPT)
- User feedback collection

### Phase 3 (Future): Production
- Plugin marketplace listing
- Enterprise features (SSO, audit logs)
- Custom skill development service

---

## Try It Yourself

### Quick Start (90 seconds, offline)

```bash
# Clone
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla

# Setup baseline lab
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Run smoke test
python tests/run_baseline_m4_smoke.py
```

### In Claude Code

```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

---

## Contact

**Jeremy Longshore**
Intent Solutions
jeremy@intentsolutions.io

**Repository**: github.com/intent-solutions-io/plugins-nixtla

---

*This is experimental/prototype work for business development. Not production-ready.*
