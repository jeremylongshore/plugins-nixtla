# 109-AA-AUDT-appaudit-devops-playbook.md

**Document Type**: DevOps Operations Playbook (v2.0)
**Version**: 1.8.1
**Created**: 2025-12-21T20:00:00-06:00 (CST)
**Status**: PRODUCTION-READY
**Target Audience**: Incoming DevOps Engineer, AI Agents
**Supersedes**: 097-AA-AUDT-appaudit-devops-playbook.md (v1.6.0)

---

# Nixtla Claude Code Plugins - DevOps Operations Playbook v2.0

## Executive Summary

### What This Repository Is

**Business showcase demonstrating Claude Code plugins and AI skills for Nixtla's time-series forecasting ecosystem.**

| Metric | Value |
|--------|-------|
| **Version** | 1.8.1 |
| **Production Skills** | 23 (100% L4 quality) |
| **Working Plugins** | 3 |
| **Planned Plugins** | 11 (with full PRDs) |
| **CI/CD Workflows** | 9 |
| **Workspaces** | 7 (development labs) |
| **Documentation** | 100+ files (Doc-Filing v4.0) |

### Operational Status Matrix

| Component | Status | Health | Last Verified |
|-----------|--------|--------|---------------|
| nixtla-baseline-lab | WORKING | GREEN | 2025-12-21 |
| nixtla-bigquery-forecaster | WORKING | GREEN | 2025-12-21 |
| nixtla-search-to-slack | MVP | YELLOW | 2025-12-10 |
| Skills Pack (23) | PRODUCTION | GREEN | 2025-12-21 |
| Skills Installer | WORKING | GREEN | 2025-12-21 |
| CI/CD Pipeline | OPERATIONAL | GREEN | 2025-12-21 |

### Technology Stack

| Layer | Technology |
|-------|------------|
| **Languages** | Python 3.9-3.12, Bash, TypeScript |
| **Forecasting** | statsforecast, TimeGPT API, MLForecast, NeuralForecast |
| **AI/ML** | Nixtla SDK, Claude Code MCP Protocol |
| **Testing** | pytest, pytest-cov, GitHub Actions |
| **Quality** | black, isort, flake8, mypy |
| **Cloud** | GCP (BigQuery, Cloud Functions), Firebase |
| **Automation** | GitHub Actions (9 workflows) |

---

## Table of Contents

1. [Repository Architecture](#repository-architecture)
2. [Directory Structure](#directory-structure)
3. [Core Components Deep Dive](#core-components-deep-dive)
4. [Skills Inventory (23)](#skills-inventory-23)
5. [CI/CD Pipeline Reference](#cicd-pipeline-reference)
6. [Environment Configuration](#environment-configuration)
7. [Operational Runbooks](#operational-runbooks)
8. [Monitoring & Health Checks](#monitoring--health-checks)
9. [Security Considerations](#security-considerations)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Development Workflow](#development-workflow)
12. [Quick Reference Card](#quick-reference-card)
13. [Recommendations Roadmap](#recommendations-roadmap)

---

## Repository Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        NIXTLA CLAUDE CODE PLUGINS                                │
│                            Version 1.8.1                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐         │
│  │   PLUGINS (3+11)  │   │   SKILLS (23)     │   │   WORKSPACES (7)  │         │
│  │   005-plugins/    │   │   003-skills/     │   │   002-workspaces/ │         │
│  ├───────────────────┤   ├───────────────────┤   ├───────────────────┤         │
│  │ ✅ baseline-lab   │   │ 8 core skills     │   │ timegpt-lab       │         │
│  │ ✅ bigquery-fcst  │   │ 5 core-forecast   │   │ statsforecast-lab │         │
│  │ ✅ search-to-slack│   │ 10 prediction-mkt │   │ mlforecast-lab    │         │
│  │ 📋 11 planned     │   │                   │   │ neuralforecast-lab│         │
│  └─────────┬─────────┘   └────────┬──────────┘   │ hierarchical-lab  │         │
│            │                      │              │ demo-project      │         │
│            │                      │              │ test-harness-lab  │         │
│            │                      │              └─────────┬─────────┘         │
│            └──────────────────────┴────────────────────────┘                   │
│                                   │                                             │
│                    ┌──────────────▼──────────────┐                              │
│                    │       VALIDATION LAYER      │                              │
│                    │   004-scripts/validate_*.py │                              │
│                    │   (SKILLS-STANDARD v2.3.0)  │                              │
│                    └──────────────┬──────────────┘                              │
│                                   │                                             │
│           ┌───────────────────────┼───────────────────────┐                     │
│           │                       │                       │                     │
│  ┌────────▼────────┐    ┌────────▼────────┐    ┌────────▼────────┐             │
│  │   CI/CD (9)     │    │   DOCS (100+)   │    │   TESTS         │             │
│  │ .github/        │    │  000-docs/      │    │  tests/         │             │
│  │ workflows/      │    │  Doc-Filing v4  │    │  007-tests/     │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Request (Claude Code IDE)
        │
        ▼
┌───────────────────┐
│  Claude Code CLI  │
└─────────┬─────────┘
          │ Auto-activates skill based on context
          ▼
┌───────────────────┐
│   SKILL.md        │ ← Read-only prompts that transform Claude behavior
│   (23 skills)     │   All at 100% L4 quality
└─────────┬─────────┘
          │ May invoke MCP tools
          ▼
┌───────────────────┐
│   MCP Server      │ ← nixtla_baseline_mcp.py (baseline-lab)
│   (4 tools)       │
│   - run_baselines │
│   - get_compat    │
│   - gen_report    │
│   - gen_gh_issue  │
└─────────┬─────────┘
          │ Executes forecasting
          ▼
┌───────────────────┐
│   Nixtla OSS      │ ← statsforecast, datasetsforecast
│   Libraries       │   OR TimeGPT API (requires API key)
└─────────┬─────────┘
          │
          ▼
     Results (CSV, Markdown reports)
```

---

## Directory Structure

### Post-Cleanup Root Layout (v1.8.1)

The root directory follows a **numbered prefix convention** for clean organization:

```
/home/jeremy/000-projects/nixtla/
│
├── 000-docs/                   # Documentation hub (100+ files)
│   ├── 000a-skills-schema/     # SKILLS-STANDARD v2.3.0
│   ├── planned-plugins/        # 11 plugin PRDs (6 docs each)
│   ├── planned-skills/         # Future skill specifications
│   ├── plugin-reference/       # Plugin API documentation
│   ├── AGENTS.md               # Agent configuration
│   ├── CODE_OF_CONDUCT.md      # Community standards (master)
│   ├── CONTRIBUTING.md         # Contribution guidelines (master)
│   ├── SECURITY.md             # Security policy (master)
│   ├── FOR-MAX-QUICKSTART.md   # Nixtla CEO quickstart
│   ├── GEMINI.md               # Gemini integration docs
│   └── NNN-AA-CODE-*.md        # Doc-Filing v4.0 format
│
├── 001-htmlcov/                # Test coverage artifacts
│   ├── index.html              # Coverage HTML report
│   ├── coverage.xml            # Coverage XML (CI)
│   └── .coverage               # Coverage data
│
├── 002-workspaces/             # Development labs (7)
│   ├── timegpt-lab/            # TimeGPT experiments
│   ├── statsforecast-lab/      # StatsForecast experiments
│   ├── mlforecast-lab/         # MLForecast experiments
│   ├── neuralforecast-lab/     # NeuralForecast experiments
│   ├── hierarchicalforecast-lab/
│   ├── demo-project/           # Example patterns
│   └── test-harness-lab/       # Learning lab (multi-phase patterns)
│
├── 003-skills/                 # Production skills (23)
│   └── .claude/skills/nixtla-*/
│
├── 004-scripts/                # Automation scripts
│   ├── configs/                # Configuration files
│   │   ├── nixtla-playground-config.env
│   │   └── timegpt2_config.yaml
│   ├── emailer/                # Email utility
│   ├── validate_skills.py      # Skills validator
│   ├── add_scripts_to_skills.py
│   └── overnight_skill_generator.py
│
├── 005-plugins/                # Plugin implementations (3 working, 11 planned)
│   ├── nixtla-baseline-lab/    # MAIN SHOWCASE ✅
│   ├── nixtla-bigquery-forecaster/ # Cloud Functions ✅
│   ├── nixtla-search-to-slack/ # MVP ✅
│   └── [11 planned plugins]/   # See planned-plugins/
│
├── 006-packages/               # Installable packages
│   └── nixtla-claude-skills-installer/
│
├── 007-tests/                  # Additional test utilities
│
├── 009-temp-data/              # Generated temporary data
│   ├── compliance-report.json
│   ├── plugins_inventory.csv
│   └── skills_inventory.csv
│
├── 010-archive/                # Historical backups
│
├── tests/                      # Main pytest test suite
│   ├── skills/                 # Skills test framework
│   ├── test_basic.py
│   └── conftest.py
│
├── .claude/                    # Claude Code configuration
│   ├── settings.json           # Hooks, marketplace config
│   └── hooks/                  # Post-compact automation
│
├── .github/                    # GitHub automation
│   ├── workflows/              # 9 CI/CD workflows
│   └── ISSUE_TEMPLATE/         # Issue templates
│
├── CHANGELOG.md                # Version history
├── CLAUDE.md                   # AI assistant instructions
├── CODE_OF_CONDUCT.md          # → symlink to 000-docs/
├── CONTRIBUTING.md             # → symlink to 000-docs/
├── LICENSE                     # MIT License
├── README.md                   # Project overview
├── SECURITY.md                 # → symlink to 000-docs/
├── VERSION                     # 1.8.1
├── pyproject.toml              # Python project config
├── pytest.ini                  # pytest configuration
├── requirements.txt            # Core dependencies
└── requirements-dev.txt        # Dev dependencies
```

### Directory Purpose Matrix

| Directory | Purpose | Key Files | Owner |
|-----------|---------|-----------|-------|
| **000-docs/** | All documentation | Doc-Filing v4.0 files | DevOps/PM |
| **001-htmlcov/** | Coverage artifacts | index.html, coverage.xml | CI/CD |
| **002-workspaces/** | Development labs | README.md, experiments | Developers |
| **003-skills/** | Production skills | SKILL.md files | AI/PM |
| **004-scripts/** | Automation | validate_skills.py | DevOps |
| **005-plugins/** | Plugin code | MCP servers, tests | Developers |
| **006-packages/** | Pip packages | setup.py, core.py | DevOps |
| **007-tests/** | Extra tests | Integration tests | QA |
| **009-temp-data/** | Generated data | CSVs, JSONs | Automated |
| **010-archive/** | Backups | Historical files | DevOps |

---

## Core Components Deep Dive

### 1. Plugins (005-plugins/)

#### nixtla-baseline-lab (MAIN SHOWCASE) ✅

**Status**: WORKING
**Purpose**: M4 benchmark baseline forecasting in Claude Code
**Python**: 3.10+
**MCP Tools**: 4

```
005-plugins/nixtla-baseline-lab/
├── commands/
│   ├── nixtla-baseline-m4.md      # /nixtla-baseline-m4 slash command
│   └── nixtla-baseline-setup.md   # /nixtla-baseline-setup command
├── agents/
│   └── nixtla-baseline-analyst.md # AI analyst subagent
├── scripts/
│   ├── nixtla_baseline_mcp.py     # MCP server (4 tools)
│   ├── timegpt_client.py          # TimeGPT API client
│   ├── setup_nixtla_env.sh        # Environment setup
│   └── requirements.txt           # Plugin-specific deps
├── skills/
│   └── nixtla-baseline-review/    # Embedded skill
├── data/m4/                       # M4 benchmark data
└── tests/
    └── run_baseline_m4_smoke.py   # Golden task (90 sec, offline)
```

**MCP Tools Exposed**:

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `run_baselines` | Execute forecasting models | df, freq, horizon | CSV metrics |
| `get_nixtla_compatibility_info` | Library version info | None | JSON |
| `generate_benchmark_report` | Markdown report | metrics CSV | Markdown |
| `generate_github_issue_draft` | GitHub issue template | experiment info | Markdown |

**Key Commands**:
```bash
# Setup environment
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate

# Run smoke test (90 seconds, offline)
python tests/run_baseline_m4_smoke.py

# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

#### nixtla-bigquery-forecaster ✅

**Status**: WORKING
**Purpose**: BigQuery integration with Cloud Functions
**Python**: 3.12
**Deployment**: GCP Cloud Functions

**Key Components**:
- Cloud Functions source code (Node.js/Python)
- BigQuery schema definitions
- GCP deployment configuration
- CI/CD via `.github/workflows/deploy-bigquery-forecaster.yml`

**Environment Requirements**:
- GCP Project with BigQuery enabled
- Cloud Functions deployment permissions
- Service account with BigQuery read/write

#### nixtla-search-to-slack ✅

**Status**: MVP
**Purpose**: Web/GitHub search with Slack notifications
**Test Coverage**: 6 test modules

```
005-plugins/nixtla-search-to-slack/
├── src/nixtla_search_to_slack/   # Main implementation
├── config/
│   ├── sources.yaml              # Search source config
│   └── topics.yaml               # Topic configuration
└── tests/                        # 6 test modules
```

#### Planned Plugins (11)

All planned plugins have complete PRD documentation in `000-docs/planned-plugins/`:

| Plugin | Status | PRD Complete | Revenue Model |
|--------|--------|--------------|---------------|
| nixtla-airflow-operator | PLANNED | ✅ | Enterprise |
| nixtla-anomaly-streaming-monitor | PLANNED | ✅ | SaaS |
| nixtla-cost-optimizer | PLANNED | ✅ | Enterprise |
| nixtla-dbt-package | PLANNED | ✅ | Open Source |
| nixtla-defi-sentinel | PLANNED | ✅ | SaaS |
| nixtla-forecast-explainer | PLANNED | ✅ | Enterprise |
| nixtla-migration-assistant | PLANNED | ✅ | Enterprise |
| nixtla-roi-calculator | PLANNED | ✅ | Lead Gen |
| nixtla-snowflake-adapter | PLANNED | ✅ | Enterprise |
| nixtla-vs-statsforecast-benchmark | PLANNED | ✅ | Marketing |

Each plugin has 6 standardized docs:
1. 01-BUSINESS-CASE.md
2. 02-PRD.md
3. 03-ARCHITECTURE.md
4. 04-USER-JOURNEY.md
5. 05-TECHNICAL-SPEC.md
6. 06-STATUS.md

### 2. Skills Installer (006-packages/)

**Location**: `006-packages/nixtla-claude-skills-installer/`
**Purpose**: Install all 23 skills to any project
**Distribution**: PyPI (planned), local pip install

```bash
# Install the installer
pip install -e 006-packages/nixtla-claude-skills-installer

# Install skills to your project
cd /path/to/your/project
nixtla-skills init    # Install all 23 skills
nixtla-skills update  # Update to latest
nixtla-skills list    # List installed skills
```

### 3. Workspaces (002-workspaces/)

Development labs for Nixtla library experimentation:

| Workspace | Library | Status | Key Files |
|-----------|---------|--------|-----------|
| timegpt-lab | TimeGPT API | ACTIVE | notebooks, examples |
| statsforecast-lab | statsforecast | ACTIVE | tutorials |
| mlforecast-lab | mlforecast | STUB | README only |
| neuralforecast-lab | neuralforecast | STUB | README only |
| hierarchicalforecast-lab | hierarchicalforecast | STUB | README only |
| demo-project | All | ACTIVE | Demo patterns |
| test-harness-lab | Multi-phase validation | NEW | 4 guides, 60 pages |

**test-harness-lab** (NEW in 1.8.x):
- Comprehensive learning lab for multi-phase validated workflows
- Teaches "Phase 4 pattern" (deterministic validation of LLM conclusions)
- 4 comprehensive guides (~60 pages total)
- See: `002-workspaces/test-harness-lab/docs/QUICK-START.md`

---

## Skills Inventory (23)

**Total**: 23 production skills
**Quality**: 100% L4 (all pass quality scoring)
**Standard**: SKILLS-STANDARD v2.3.0

### Skills by Category

#### Core Skills (8)

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| nixtla-experiment-architect | Design forecasting experiments | "design experiment", "plan forecast" |
| nixtla-schema-mapper | Map data to Nixtla schemas | "schema mapping", "data structure" |
| nixtla-timegpt-lab | TimeGPT experimentation | "TimeGPT lab", "API experiment" |
| nixtla-timegpt-finetune-lab | Fine-tuning TimeGPT | "fine-tune", "custom model" |
| nixtla-usage-optimizer | Optimize API usage | "reduce costs", "optimize calls" |
| nixtla-prod-pipeline-generator | Production pipeline code | "production pipeline", "deploy" |
| nixtla-skills-bootstrap | Create new skills | "new skill", "bootstrap skill" |
| nixtla-skills-index | Skills discovery | "list skills", "find skill" |

#### Core Forecasting (5)

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| nixtla-anomaly-detector | Detect time series anomalies | "anomaly detection", "outliers" |
| nixtla-cross-validator | Time series cross-validation | "cross-validate", "validate model" |
| nixtla-exogenous-integrator | Add external variables | "exogenous", "external factors" |
| nixtla-timegpt2-migrator | Migrate to TimeGPT-2 | "upgrade TimeGPT", "migrate v2" |
| nixtla-uncertainty-quantifier | Confidence intervals | "uncertainty", "prediction intervals" |

#### Prediction Markets (10)

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| nixtla-polymarket-analyst | Polymarket analysis | "Polymarket", "prediction market" |
| nixtla-market-risk-analyzer | Market risk assessment | "market risk", "volatility" |
| nixtla-contract-schema-mapper | Contract data mapping | "contract schema", "market data" |
| nixtla-correlation-mapper | Cross-market correlations | "correlations", "market relationships" |
| nixtla-arbitrage-detector | Arbitrage opportunities | "arbitrage", "price discrepancy" |
| nixtla-event-impact-modeler | Event impact modeling | "event impact", "news effect" |
| nixtla-liquidity-forecaster | Liquidity predictions | "liquidity", "market depth" |
| nixtla-batch-forecaster | Batch market forecasting | "batch forecast", "bulk predictions" |
| nixtla-forecast-validator | Forecast validation | "validate forecast", "accuracy check" |
| nixtla-model-selector | Model selection | "best model", "model comparison" |

### Skill Quality Scoring (L4)

All skills must achieve **100/100** on L4 quality checks:

| Criteria | Weight | Requirement |
|----------|--------|-------------|
| **Action verbs** | 20% | Contains: analyze, detect, forecast, transform, generate, validate, compare, optimize |
| **"Use when"** | 25% | Must include "Use when" phrase |
| **"Trigger with"** | 25% | Must include "Trigger with" phrase |
| **Length** | 15% | Description 100-300 characters |
| **Domain keywords** | 15% | Contains: timegpt, forecast, time series, nixtla, statsforecast |

**Validation Command**:
```bash
python 004-scripts/validate_skills.py
# Expected: ✅ All SKILL.md files passed validation!

# Detailed test
python tests/skills/test_all_skills.py
```

---

## CI/CD Pipeline Reference

### Workflow Inventory (9)

| Workflow | Trigger | Purpose | Status |
|----------|---------|---------|--------|
| `ci.yml` | push, PR | Main validation pipeline | REQUIRED |
| `skills-validation.yml` | push, PR | Skills compliance check | REQUIRED |
| `nixtla-baseline-lab-ci.yml` | push | Baseline lab tests | ACTIVE |
| `skills-installer-ci.yml` | push | Skills installer tests | ACTIVE |
| `plugin-validator.yml` | push | Plugin schema validation | ACTIVE |
| `deploy-bigquery-forecaster.yml` | manual, push | BigQuery deployment | ACTIVE |
| `gemini-code-assist-trigger.yml` | PR | Gemini review trigger | ACTIVE |
| `gemini-daily-audit.yml` | cron | Daily automated audit | ACTIVE |
| `timegpt-real-smoke.yml` | manual | TimeGPT API smoke test | MANUAL |

### Main CI Pipeline (ci.yml)

```yaml
# Runs on every push and PR
jobs:
  lint:
    - black --check .
    - isort --check-only .
    - flake8 . --select=E9,F63,F7,F82

  test:
    matrix:
      python-version: [3.9, 3.10, 3.11, 3.12]
    steps:
      - pytest --cov=005-plugins -v
```

### Required Checks Before Merge

1. **CI Pipeline** (`ci.yml`) - Lint + Test
2. **Skills Validation** (`skills-validation.yml`) - SKILL.md compliance
3. **PR Review** - At least 1 approval (if enabled)

### Manual Workflows

```bash
# Trigger TimeGPT smoke test
gh workflow run timegpt-real-smoke.yml

# Trigger BigQuery deployment
gh workflow run deploy-bigquery-forecaster.yml
```

---

## Environment Configuration

### Required Environment Variables

| Variable | Purpose | Required By | How to Set |
|----------|---------|-------------|------------|
| `NIXTLA_TIMEGPT_API_KEY` | TimeGPT API access | timegpt-lab, baseline-lab | `.env` or export |
| `GOOGLE_APPLICATION_CREDENTIALS` | GCP service account | bigquery-forecaster | JSON file path |
| `SLACK_WEBHOOK_URL` | Slack notifications | search-to-slack | `.env` |
| `BEADS_DIR` | Beads database isolation | All (optional) | export |

### Python Environment Setup

```bash
# Repository root (for testing)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Baseline lab plugin
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
```

### Local Development Config

Create `.env` in repository root:
```bash
# TimeGPT (optional, for API tests)
NIXTLA_TIMEGPT_API_KEY=your_api_key_here

# GCP (optional, for BigQuery plugin)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Beads (optional, for task tracking)
BEADS_DIR=/custom/path/to/.beads
```

---

## Operational Runbooks

### Runbook 1: New Release

```bash
# 1. Verify all tests pass
pytest -v
python 004-scripts/validate_skills.py

# 2. Update version
echo "1.9.0" > VERSION

# 3. Update CHANGELOG.md
vim CHANGELOG.md  # Add release notes

# 4. Create release AAR
# Follow Doc-Filing v4.0 convention:
# NNN-AA-AAR-release-v1.9.0.md

# 5. Commit and tag
git add -A
git commit -m "release: v1.9.0"
git tag -a v1.9.0 -m "Release v1.9.0"
git push origin main --tags
```

### Runbook 2: Add New Skill

```bash
# 1. Create skill directory
mkdir -p 003-skills/.claude/skills/nixtla-new-skill/{scripts,assets/templates,references}

# 2. Create SKILL.md following standard
# See: 000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md

# 3. Validate
python 004-scripts/validate_skills.py

# 4. Test L4 quality
python tests/skills/test_all_skills.py --skill nixtla-new-skill

# 5. Commit
git add 003-skills/.claude/skills/nixtla-new-skill/
git commit -m "feat(skills): add nixtla-new-skill"
```

### Runbook 3: Plugin Development

```bash
# 1. Create plugin structure
mkdir -p 005-plugins/nixtla-new-plugin/{commands,agents,scripts,skills,tests}

# 2. Create required files
touch 005-plugins/nixtla-new-plugin/README.md
touch 005-plugins/nixtla-new-plugin/scripts/requirements.txt

# 3. Create PRD docs in 000-docs/planned-plugins/nixtla-new-plugin/
# 6 required docs: 01-BUSINESS-CASE.md through 06-STATUS.md

# 4. Add to 005-plugins/README.md

# 5. Commit
git add 005-plugins/nixtla-new-plugin/
git commit -m "feat(plugins): scaffold nixtla-new-plugin"
```

### Runbook 4: CI/CD Failure Triage

```bash
# 1. Check which workflow failed
gh run list --limit 5

# 2. View logs
gh run view <run-id> --log-failed

# 3. Common fixes:
# - Lint failure: black . && isort .
# - Test failure: pytest -v tests/test_failing.py -x
# - Skills validation: python 004-scripts/validate_skills.py

# 4. Re-run after fix
git push  # Triggers new CI run
```

---

## Monitoring & Health Checks

### Daily Health Check Script

```bash
#!/bin/bash
# Run as: ./scripts/daily_health_check.sh

echo "=== Nixtla Health Check ==="
echo "Version: $(cat VERSION)"
echo ""

# 1. Lint check
echo "Lint check..."
black --check . 2>/dev/null && echo "✅ Black" || echo "❌ Black"
isort --check-only . 2>/dev/null && echo "✅ isort" || echo "❌ isort"

# 2. Tests
echo "Tests..."
pytest tests/test_basic.py -v --tb=no 2>/dev/null && echo "✅ Basic tests" || echo "❌ Basic tests"

# 3. Skills validation
echo "Skills validation..."
python 004-scripts/validate_skills.py 2>/dev/null && echo "✅ Skills" || echo "❌ Skills"

# 4. Git status
echo ""
echo "Git Status:"
git status --short
```

### Metrics to Monitor

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| Test pass rate | CI/CD | < 100% |
| Skills L4 score | validate_skills.py | < 100% |
| Coverage | pytest-cov | < 50% |
| Lint errors | black/isort | > 0 |
| Open issues | GitHub | > 20 |
| CI failure rate | GitHub Actions | > 10%/week |

### Log Locations

| Component | Log Location |
|-----------|--------------|
| GitHub Actions | github.com/repo/actions |
| pytest output | stdout + 001-htmlcov/ |
| MCP server | stdout (when running) |
| Cloud Functions | GCP Console > Cloud Functions > Logs |

---

## Security Considerations

### Secrets Management

| Secret | Location | Rotation |
|--------|----------|----------|
| NIXTLA_TIMEGPT_API_KEY | GitHub Secrets / .env | Annually |
| GCP Service Account | JSON file (gitignored) | Annually |
| SLACK_WEBHOOK_URL | .env | On compromise |

### Security Checklist

- [ ] No secrets in committed code
- [ ] `.env` files are gitignored
- [ ] Service account has minimal permissions
- [ ] Dependencies regularly updated
- [ ] SECURITY.md provides vulnerability reporting

### Gitignored Security Files

```gitignore
# In .gitignore
.env
*.json  # GCP credentials (selective)
004-scripts/emailer/.env
009-temp-data/
```

---

## Troubleshooting Guide

### Common Issues

#### Issue 1: Skills Validation Fails

**Symptom**: `python 004-scripts/validate_skills.py` reports errors

**Causes & Fixes**:
```bash
# Check specific skill
python tests/skills/test_all_skills.py --skill nixtla-failing-skill

# Common fixes:
# 1. Description too long/short (100-300 chars required)
# 2. Missing "Use when" or "Trigger with" phrases
# 3. Missing action verb (analyze, detect, forecast, etc.)
# 4. Missing domain keyword (timegpt, forecast, nixtla, etc.)
```

#### Issue 2: pytest Coverage Path Wrong

**Symptom**: Coverage writes to wrong directory

**Fix**: Check pytest.ini
```ini
# In pytest.ini
--cov-report=html:001-htmlcov
--cov-report=xml:001-htmlcov/coverage.xml
```

#### Issue 3: MCP Server Won't Start

**Symptom**: Claude Code can't connect to MCP tools

**Fix**:
```bash
cd 005-plugins/nixtla-baseline-lab
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Test directly
python scripts/nixtla_baseline_mcp.py
```

#### Issue 4: Beads Database Conflicts

**Symptom**: `bd` commands fail or show wrong project

**Fix**:
```bash
# Isolate Beads database
export BEADS_DIR=$(pwd)/.beads
bd ready
```

### Debug Commands

```bash
# Full diagnostic
python -c "import sys; print(sys.version)"
pip list | grep nixtla
cat VERSION
git status
git log --oneline -5
```

---

## Development Workflow

### Daily Workflow

```bash
# Start of session
cd /home/jeremy/000-projects/nixtla
bd ready

# Create task
bd create "Implement feature X" -p 1 --description "Details here"

# Work on feature
bd update <id> --status in_progress
# ... make changes ...
pytest -v
python 004-scripts/validate_skills.py

# Complete
bd close <id> --reason "Done"

# End of session
bd sync
git add -A
git commit -m "feat: implement feature X"
git push
```

### Branch Strategy

```
main                    # Production-ready
├── feature/xxx         # New features
├── fix/xxx            # Bug fixes
├── docs/xxx           # Documentation
└── chore/xxx          # Maintenance
```

### Commit Message Convention

```
type(scope): subject

Types: feat, fix, docs, style, refactor, test, chore
Scope: plugins, skills, docs, ci, scripts

Examples:
feat(skills): add nixtla-new-skill
fix(plugins): resolve MCP connection issue
docs(000-docs): update AAR template
```

---

## Quick Reference Card

### Essential Commands

```bash
# Testing
pytest -v                                    # All tests
pytest tests/test_basic.py -v               # Specific test
pytest --cov=005-plugins -v                 # With coverage

# Skills
python 004-scripts/validate_skills.py       # Validate all skills
python tests/skills/test_all_skills.py      # L1/L2/L4 tests

# Formatting
black .                                      # Format Python
isort .                                      # Sort imports

# Beads
bd ready                                     # Start session
bd create "Task" -p 1                        # Create task
bd update <id> --status in_progress          # Update status
bd close <id> --reason "Done"                # Close task
bd sync                                      # Sync to git

# Git
git status                                   # Check status
git add -A && git commit -m "msg"           # Commit
git push                                     # Push
```

### Key Paths

| Resource | Path |
|----------|------|
| CLAUDE.md | `/home/jeremy/000-projects/nixtla/CLAUDE.md` |
| Skills Standard | `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md` |
| All Skills | `003-skills/.claude/skills/nixtla-*/` |
| Main Plugin | `005-plugins/nixtla-baseline-lab/` |
| CI Workflows | `.github/workflows/` |
| Coverage | `001-htmlcov/` |

### Version Info

| Component | Version | File |
|-----------|---------|------|
| Repository | 1.8.1 | VERSION |
| Skills Standard | 2.3.0 | 000-docs/000a-skills-schema/ |
| Python | 3.9-3.12 | pyproject.toml |
| pyproject | 0.7.0 | pyproject.toml |

---

## Recommendations Roadmap

### Week 1 - Immediate Actions

- [ ] Review all 9 CI/CD workflows for current status
- [ ] Run full test suite and fix any failures
- [ ] Update any stale documentation
- [ ] Verify all 23 skills pass L4 quality

### Month 1 - Short-term Improvements

- [ ] Add pre-commit hooks for automated formatting
- [ ] Create automated skill quality dashboard
- [ ] Implement daily health check cron job
- [ ] Document any manual processes

### Quarter 1 - Strategic Initiatives

- [ ] Evaluate moving planned plugins to development
- [ ] Create skills installer PyPI package
- [ ] Implement monitoring/alerting for CI failures
- [ ] Expand test coverage to 80%+
- [ ] Create onboarding documentation for new developers

---

## Footer

**intent solutions io — confidential IP**
**Contact**: jeremy@intentsolutions.io
**Repository**: nixtla (plugins-nixtla)
**Document**: 109-AA-AUDT-appaudit-devops-playbook.md
**Version**: 1.8.1
**Last Updated**: 2025-12-21
**Supersedes**: 097-AA-AUDT-appaudit-devops-playbook.md (v1.6.0)
