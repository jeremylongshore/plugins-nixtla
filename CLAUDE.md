# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Private agentic engineering workspace for Nixtla time series forecasting. Built on Bob's Brain architecture (Vertex AI Agent Engine), this project wraps Nixtla's stack (TimeGPT, StatsForecast, MLForecast, NeuralForecast) with "junior engineer" agents that automate repetitive workflows.

**Status**: Experimental private collaboration between Intent Solutions and Nixtla.

## High-Level Architecture

The system follows an **orchestrator + specialist agents** pattern:

```
User → Orchestrator Agent → Specialist Agents → Nixtla Tools/GitHub
```

**Planned Specialist Agents**:
- **Baseline Builder** - Auto-generate forecasts with StatsForecast/MLForecast/NeuralForecast
- **Backtest QA** - Run backtests on benchmark datasets, compare models
- **TimeGPT Runner** - Manage TimeGPT experiments with different configs
- **CI Triage** - Parse CI failures, propose fixes
- **Doc Sync** - Detect drift between code and documentation
- **Anomaly Monitor** - Detect anomalies using TimeGPT methods

**Implemented Components**:
- `plugins/nixtla-search-to-slack/` - Working content discovery and curation plugin
- `claude-code-plugins-plus/` - Plugin marketplace with 200+ Claude Code plugins

## Commands

### Development Setup
```bash
# Set up development environment
./scripts/setup-dev-environment.sh

# Validate plugin structure
./scripts/validate-all-plugins.sh
./scripts/validate-marketplace.sh

# Run tests
pytest
```

### Search-to-Slack Plugin
```bash
cd plugins/nixtla-search-to-slack

# Install dependencies
pip install -r requirements.txt

# Run content digest
python -m nixtla_search_to_slack --topic nixtla-core

# List available topics
python -m nixtla_search_to_slack --list-topics

# Dry run (no Slack posting)
python -m nixtla_search_to_slack --dry-run --topic nixtla-core
```

### Testing
```bash
# Run all tests
pytest

# Run specific plugin tests
pytest plugins/nixtla-search-to-slack/tests/

# Run with coverage
pytest --cov=src
```

## Project Structure

```
nixtla/
├── plugins/
│   └── nixtla-search-to-slack/     # ✅ Working plugin
│       ├── src/nixtla_search_to_slack/
│       │   ├── main.py             # Entry point, digest workflow
│       │   ├── search_orchestrator.py
│       │   ├── content_aggregator.py
│       │   ├── ai_curator.py
│       │   └── slack_publisher.py
│       ├── config/                  # YAML configs for topics/sources
│       └── tests/
├── claude-code-plugins-plus/        # Plugin marketplace (200+ plugins)
├── 000-docs/                        # Technical documentation
├── scripts/                         # Automation scripts
└── docs/                            # MkDocs site
```

## Search-to-Slack Architecture

The only implemented plugin follows a 4-phase pipeline:

1. **Search** (`search_orchestrator.py`) - Query multiple sources (SerpAPI, GitHub)
2. **Aggregate** (`content_aggregator.py`) - Deduplicate and normalize results
3. **Curate** (`ai_curator.py`) - AI scoring and summary generation
4. **Publish** (`slack_publisher.py`) - Format and post to Slack

**Required Environment Variables**:
```bash
SLACK_BOT_TOKEN=xoxb-...
SERP_API_KEY=...
GITHUB_TOKEN=ghp_...
# Plus one LLM provider:
OPENAI_API_KEY=... OR ANTHROPIC_API_KEY=... OR GOOGLE_API_KEY=...
```

## Nixtla Integration Patterns

Reference patterns for Nixtla API usage (not yet in agents):

```python
# TimeGPT
from nixtla import NixtlaClient
client = NixtlaClient(api_key='YOUR_API_KEY')
forecast = client.forecast(df=data, h=24, freq='H', level=[80, 90, 95])

# StatsForecast
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS
sf = StatsForecast(models=[AutoARIMA(season_length=12)], freq='M')
sf.fit(df)
forecasts = sf.predict(h=12)

# MLForecast
from mlforecast import MLForecast
mlf = MLForecast(models=[RandomForestRegressor()], freq='D', lags=[1,7,14])
mlf.fit(df)
predictions = mlf.predict(h=30)
```

## Document Organization

Documentation in `000-docs/` follows format: `NNN-CC-ABCD-description.md`
- **001-PP-PROD** - Product requirements
- **002-AA-AUDT** - Audits and analysis
- **003-PP-PLAN** - Planning documents
- **004-AT-ARCH** - Architecture docs

## Key Dependencies

**Search-to-Slack Plugin**:
- `slack-sdk` - Slack API integration
- `requests` - HTTP client
- `pyyaml` - Configuration loading
- `python-dotenv` - Environment management
- One LLM: `google-generativeai`, `groq`, `openai`, or `anthropic`

## Reference Architecture

This project adapts patterns from Bob's Brain (https://github.com/jeremylongshore/bobs-brain):
- Vertex AI Agent Engine for orchestration
- A2A protocol for agent communication
- Golden tasks for validation
- CI-only deployments with guardrails