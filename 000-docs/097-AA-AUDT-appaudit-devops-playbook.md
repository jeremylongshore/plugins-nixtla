# 097-AA-AUDT-appaudit-devops-playbook.md

**Document Type**: DevOps Operations Playbook
**Version**: 1.0.0
**Created**: 2025-12-08T23:45:00Z
**Status**: PRODUCTION-READY
**Target Audience**: Incoming DevOps Engineer

---

# Nixtla Claude Code Plugins - DevOps Operations Playbook

## Executive Summary

**What This Repository Is**:
A business showcase demonstrating Claude Code plugins and AI skills for Nixtla's time-series forecasting ecosystem. This repository contains 3 working plugins, 21 Claude Skills, and comprehensive automation infrastructure for quality assurance and deployment.

**Business Context**:
This is experimental/prototype work for business development collaboration between Nixtla (time series forecasting platform) and Intent Solutions (AI/ML engineering). It demonstrates how to integrate Nixtla forecasting workflows into Claude Code IDE conversations.

**What You Need to Operate**:
- GitHub Actions CI/CD (9 workflows)
- Python 3.9-3.12 environments
- Optional: GCP credentials for BigQuery plugin, Nixtla TimeGPT API key

**Total Repository Size**: ~1.9 GB (including archives and test data)

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Repository Structure](#repository-structure)
3. [Core Components](#core-components)
4. [CI/CD Pipeline Reference](#cicd-pipeline-reference)
5. [Environment Configuration](#environment-configuration)
6. [Operational Runbooks](#operational-runbooks)
7. [Monitoring & Health Checks](#monitoring--health-checks)
8. [Security Considerations](#security-considerations)
9. [Cost Management](#cost-management)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Backup & Recovery](#backup--recovery)
12. [Quick Reference Card](#quick-reference-card)

---

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NIXTLA CLAUDE CODE PLUGINS                           │
│                            Version 1.6.0                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │   PLUGINS (3)    │    │   SKILLS (21)    │    │   WORKSPACES (6) │      │
│  │   005-plugins/   │    │   003-skills/    │    │   002-workspaces/│      │
│  ├──────────────────┤    ├──────────────────┤    ├──────────────────┤      │
│  │ baseline-lab     │    │ experiment-arch  │    │ timegpt-lab      │      │
│  │ bigquery-fcst    │    │ schema-mapper    │    │ statsforecast-lab│      │
│  │ search-to-slack  │    │ timegpt-lab      │    │ mlforecast-lab   │      │
│  └────────┬─────────┘    │ + 18 more        │    │ + 3 more         │      │
│           │              └────────┬─────────┘    └────────┬─────────┘      │
│           │                       │                       │                 │
│           └───────────────────────┴───────────────────────┘                 │
│                                   │                                         │
│                    ┌──────────────▼──────────────┐                          │
│                    │       VALIDATION LAYER      │                          │
│                    │   scripts/validate_skills.py│                          │
│                    │   (v2.3.0 ENGINEERING-COMPLETE)                        │
│                    └──────────────┬──────────────┘                          │
│                                   │                                         │
│           ┌───────────────────────┼───────────────────────┐                 │
│           │                       │                       │                 │
│  ┌────────▼────────┐    ┌────────▼────────┐    ┌────────▼────────┐         │
│  │   CI/CD (9)     │    │   DOCS (100+)   │    │   TESTS         │         │
│  │ .github/        │    │  000-docs/      │    │  007-tests/     │         │
│  │ workflows/      │    │  Doc-Filing v3  │    │  pytest suite   │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Request (Claude Code IDE)
        │
        ▼
┌───────────────────┐
│  Claude Code CLI  │
└─────────┬─────────┘
          │ Activates skill based on context
          ▼
┌───────────────────┐
│   SKILL.md        │ ← Read-only prompts that transform Claude behavior
│   (21 skills)     │
└─────────┬─────────┘
          │ May invoke MCP tools
          ▼
┌───────────────────┐
│   MCP Server      │ ← nixtla_baseline_mcp.py
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
│   Libraries       │
└─────────┬─────────┘
          │
          ▼
     Results (CSV, Markdown reports)
```

---

## Repository Structure

### Top-Level Directory Map

```
/home/jeremy/000-projects/nixtla/
│
├── .claude/                    # Claude Code configuration
│   ├── settings.json           # Hooks, marketplace, readAfterCompact
│   ├── hooks/post-compact.sh   # Post-compaction automation
│   └── skills/                 # Root-level skills (2)
│
├── .github/                    # GitHub automation
│   ├── workflows/              # 9 CI/CD workflows
│   └── ISSUE_TEMPLATE/         # 4 issue templates
│
├── 000-docs/                   # Documentation hub (100+ files)
│   ├── skills-schema/          # Standards v2.3.0
│   ├── planned-skills/         # Future skill specifications
│   ├── planned-plugins/        # Future plugin specifications
│   ├── global/                 # Cross-cutting docs
│   └── NNN-CC-ABCD-*.md        # Doc-Filing v3.0 format
│
├── 002-workspaces/             # Development labs (6)
│   ├── timegpt-lab/            # TimeGPT experiments
│   ├── statsforecast-lab/      # StatsForecast experiments
│   ├── mlforecast-lab/         # MLForecast experiments
│   ├── neuralforecast-lab/     # NeuralForecast experiments
│   ├── hierarchicalforecast-lab/
│   └── demo-project/           # Example patterns
│
├── 003-skills/                 # Production skills pack (8 skills)
│   └── .claude/skills/nixtla-*/
│
├── 005-plugins/                # Working plugins (3)
│   ├── nixtla-baseline-lab/    # MAIN SHOWCASE
│   ├── nixtla-bigquery-forecaster/
│   └── nixtla-search-to-slack/
│
├── 006-packages/               # Installable packages
│   └── nixtla-claude-skills-installer/
│
├── 007-tests/                  # Integration tests
│
├── 010-archive/                # Historical backups
│
├── scripts/                    # Repository-level automation
│   ├── validate_skills.py      # CRITICAL: v2.3.0 validator
│   └── *.sh, *.py              # Utility scripts
│
├── CLAUDE.md                   # AI assistant instructions
├── VERSION                     # 1.6.0
├── pyproject.toml              # Python project configuration
├── requirements.txt            # Core dependencies
└── requirements-dev.txt        # Development dependencies
```

### Critical Files Reference

| File | Purpose | When to Check |
|------|---------|---------------|
| `VERSION` | Current version (1.6.0) | Before releases |
| `scripts/validate_skills.py` | Skills compliance validator | Before merging skill changes |
| `000-docs/skills-schema/SKILLS-STANDARD-COMPLETE.md` | Canonical skill standard v2.3.0 | When authoring skills |
| `.github/workflows/ci.yml` | Main CI pipeline | On CI failures |
| `pyproject.toml` | Python config, tool settings | Dependency changes |
| `.claude/settings.json` | Claude Code hooks/settings | Post-compact issues |

---

## Core Components

### 1. Plugins (005-plugins/)

#### nixtla-baseline-lab (MAIN SHOWCASE)

**Status**: Working
**Purpose**: M4 benchmark baseline forecasting in Claude Code
**Python**: 3.10+

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
1. `run_baselines` - Execute forecasting models
2. `get_nixtla_compatibility_info` - Library version info
3. `generate_benchmark_report` - Markdown report generation
4. `generate_github_issue_draft` - GitHub issue template

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

#### nixtla-bigquery-forecaster

**Status**: Working
**Purpose**: BigQuery integration with Cloud Functions
**Python**: 3.12

**Key Files**:
- Cloud Functions source code
- GCP deployment configuration
- BigQuery schema definitions

#### nixtla-search-to-slack

**Status**: MVP
**Purpose**: Web/GitHub search with Slack notifications

**Key Files**:
- `src/nixtla_search_to_slack/` - Main implementation
- `config/sources.yaml` - Search source configuration
- `config/topics.yaml` - Topic configuration
- Test suite: 6 test modules

### 2. Skills (003-skills/ + .claude/skills/)

**Total Active Skills**: 21
**Validation**: 100% compliant with v2.3.0 standard

**Skill Categories**:

| Category | Count | Examples |
|----------|-------|----------|
| Core Forecasting | 5 | anomaly-detector, cross-validator |
| Prediction Markets | 10 | polymarket-analyst, arbitrage-detector |
| Live/Lab | 6 | timegpt-lab, experiment-architect |

**Directory Structure Per Skill**:
```
skill-name/
├── SKILL.md              # Required: Skill definition
├── assets/               # Templates, examples
│   └── templates/
├── references/           # Progressive disclosure docs
└── scripts/              # Implementation code
```

**Validation Command**:
```bash
python scripts/validate_skills.py
# Expected: ✅ All SKILL.md files passed validation!
```

### 3. Workspaces (002-workspaces/)

Development labs for experimenting with Nixtla libraries:

| Workspace | Library | Purpose |
|-----------|---------|---------|
| timegpt-lab | nixtla (TimeGPT API) | API experiments |
| statsforecast-lab | statsforecast | Classical methods |
| mlforecast-lab | mlforecast | ML-based forecasting |
| neuralforecast-lab | neuralforecast | Deep learning |
| hierarchicalforecast-lab | hierarchicalforecast | Hierarchical reconciliation |
| demo-project | All | Usage patterns |

**Standard Lab Structure**:
```
workspace-lab/
├── data/           # Test datasets
├── docs/           # Lab documentation
├── experiments/    # Experiment configs
├── reports/        # Output reports
├── scripts/        # Utility scripts
└── skills/         # Embedded skills
```

---

## CI/CD Pipeline Reference

### Workflow Matrix

| Workflow | Trigger | Runtime | Cost Tier | Purpose |
|----------|---------|---------|-----------|---------|
| `ci.yml` | push, PR | ~2-15 min | TIER 1/2 | Main CI: lint, test, validate |
| `skills-validation.yml` | push, PR | ~1 min | TIER 1 | Skill compliance check |
| `nixtla-baseline-lab-ci.yml` | push, PR | Variable | TIER 2 | Plugin smoke tests |
| `skills-installer-ci.yml` | push, PR | Variable | TIER 2 | Package tests |
| `plugin-validator.yml` | PR | Variable | TIER 2 | Schema validation |
| `deploy-bigquery-forecaster.yml` | manual | N/A | TIER 3 | Cloud Functions deploy |
| `gemini-pr-review.yml` | PR | ~2 min | TIER 2 | AI code review |
| `gemini-daily-audit.yml` | cron 6am | ~5 min | TIER 3 | Nightly audit |
| `timegpt-real-smoke.yml` | manual | Variable | TIER 3 | Live API tests |

### CI Cost Optimization Strategy

**Problem**: macOS = 10x multiplier, Windows = 2x multiplier on free minutes

**Solution**: Tiered approach

```
TIER 1 (Every push):     Linux + Python 3.11 only (~2 min)
TIER 2 (PRs to main):    Full OS matrix (~15 min)
TIER 3 (Weekly/Manual):  Comprehensive audits
```

**Savings**: ~90% reduction in workflow minutes

### CI Pipeline Diagram

```
Push to main/develop
        │
        ▼
┌───────────────────────┐
│  TIER 1 (~2 min)      │
│  ├─ lint-and-format   │  ← black, isort, flake8
│  ├─ test-primary      │  ← pytest (Python 3.11)
│  └─ validate-plugins  │  ← JSON validation
└───────────┬───────────┘
            │
            ▼
     all-checks-passed
            │
            ▼
      ✅ Merge Ready

PR to main
    │
    ▼
┌───────────────────────┐
│  TIER 2 (~15 min)     │
│  ├─ test-matrix       │  ← All Python versions
│  │  ├─ Linux 3.9      │     All OS platforms
│  │  ├─ Linux 3.10     │
│  │  ├─ Linux 3.12     │
│  │  ├─ Windows 3.11   │
│  │  └─ macOS 3.11     │
│  └─ security-scan     │  ← Trivy, secrets check
└───────────────────────┘
```

### Key CI Files

**Main CI** (`.github/workflows/ci.yml`):
```yaml
# Cost-optimized triggers
on:
  push:
    branches: [main, develop]
    paths:
      - '**.py'
      - '**.js'
      - '**.ts'
      - 'requirements*.txt'
      - 'pyproject.toml'
      - '.github/workflows/ci.yml'
```

**Skills Validation** (`.github/workflows/skills-validation.yml`):
```yaml
# Runs validate_skills.py
- run: pip install pyyaml
- run: python scripts/validate_skills.py
```

---

## Environment Configuration

### Required Environment Variables

| Variable | Required | Purpose | Example |
|----------|----------|---------|---------|
| `NIXTLA_TIMEGPT_API_KEY` | Optional | TimeGPT API access | `nixak-...` |
| `PROJECT_ID` | Optional | GCP project ID | `my-gcp-project` |
| `LOCATION` | Optional | GCP region | `us-central1` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Optional | GCP service account | `/path/to/key.json` |

### Python Environment Setup

**Repository Root**:
```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Verify
python --version  # 3.9+
pytest --version  # 7.4+
```

**Plugin-Specific (nixtla-baseline-lab)**:
```bash
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt
```

### Dependencies Reference

**Core** (`requirements.txt`):
```
nixtla>=0.5.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
pydantic>=2.0.0
python-dotenv>=1.0.0
click>=8.1.0
```

**Development** (`requirements-dev.txt`):
```
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.4.0
isort>=5.12.0
pre-commit>=3.3.0
```

**Plugin-Specific** (`005-plugins/nixtla-baseline-lab/scripts/requirements.txt`):
```
statsforecast>=1.5.0
datasetsforecast>=0.0.8
utilsforecast>=0.0.15
```

---

## Operational Runbooks

### Runbook 1: Daily Health Check

**Frequency**: Daily (or after deployments)
**Duration**: ~5 minutes

```bash
#!/bin/bash
# Daily Health Check Script

echo "=== Nixtla Repository Health Check ==="
echo "Date: $(date)"
echo ""

# 1. Check Python environment
echo "1. Python Environment:"
python --version
pip list | grep -E "nixtla|statsforecast|pandas"
echo ""

# 2. Run linting
echo "2. Code Quality:"
black --check . 2>&1 | tail -3
isort --check-only . 2>&1 | tail -3
echo ""

# 3. Run tests
echo "3. Test Suite:"
pytest --co -q 2>&1 | tail -5
echo ""

# 4. Validate skills
echo "4. Skills Validation:"
python scripts/validate_skills.py 2>&1 | tail -5
echo ""

# 5. Check git status
echo "5. Git Status:"
git status --short
echo ""

echo "=== Health Check Complete ==="
```

### Runbook 2: Plugin Smoke Test

**Purpose**: Verify plugin functionality after changes
**Duration**: ~2 minutes

```bash
#!/bin/bash
# Plugin Smoke Test

cd 005-plugins/nixtla-baseline-lab

# Activate environment
source .venv-nixtla-baseline/bin/activate 2>/dev/null || {
    echo "Creating virtual environment..."
    ./scripts/setup_nixtla_env.sh --venv
    source .venv-nixtla-baseline/bin/activate
}

# Run golden task
echo "Running baseline smoke test (90 seconds)..."
python tests/run_baseline_m4_smoke.py

# Check results
if [ $? -eq 0 ]; then
    echo "✅ Smoke test PASSED"
else
    echo "❌ Smoke test FAILED"
    exit 1
fi
```

### Runbook 3: Release Process

**Purpose**: Create a new release
**Duration**: ~15 minutes

```bash
#!/bin/bash
# Release Process

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh 1.7.0"
    exit 1
fi

echo "=== Starting Release v$VERSION ==="

# 1. Update VERSION file
echo "$VERSION" > VERSION
echo "✓ Updated VERSION to $VERSION"

# 2. Run full validation
echo "Running validation..."
black --check .
isort --check-only .
pytest -v
python scripts/validate_skills.py

if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Fix issues before releasing."
    exit 1
fi

# 3. Update CHANGELOG
echo ""
echo "ACTION REQUIRED: Update CHANGELOG.md with:"
echo "  - Version: $VERSION"
echo "  - Date: $(date +%Y-%m-%d)"
echo "  - Changes since last release"
echo ""
read -p "Press Enter when CHANGELOG is updated..."

# 4. Commit changes
git add VERSION CHANGELOG.md
git commit -m "chore: release v$VERSION"

# 5. Create tag
git tag -a "v$VERSION" -m "Release v$VERSION"

echo ""
echo "=== Release v$VERSION Prepared ==="
echo ""
echo "Next steps:"
echo "  1. Review: git log -1 && git show v$VERSION"
echo "  2. Push: git push origin main && git push origin v$VERSION"
echo "  3. Create GitHub Release with notes from CHANGELOG"
```

### Runbook 4: Skill Authoring

**Purpose**: Create a new compliant skill
**Duration**: ~10 minutes

```bash
#!/bin/bash
# New Skill Creation

SKILL_NAME=$1
if [ -z "$SKILL_NAME" ]; then
    echo "Usage: ./new-skill.sh nixtla-my-skill"
    exit 1
fi

BASE_DIR="003-skills/.claude/skills/$SKILL_NAME"

# Create directory structure
mkdir -p "$BASE_DIR"/{assets/templates,references,scripts}
touch "$BASE_DIR/assets/.gitkeep"

# Create SKILL.md template
cat > "$BASE_DIR/SKILL.md" << 'EOF'
---
name: SKILL_NAME_PLACEHOLDER
description: Third-person description (max 1024 chars). Analyzes X and provides Y. Use when Z.
allowed-tools: "Read,Glob,Grep"
version: "1.0.0"
license: "MIT"
---

# Skill Name

Brief overview of what this skill does.

## Overview

Detailed explanation of capabilities.

## Prerequisites

What the user needs before using this skill.

## Instructions

Step-by-step guidance for the skill.

## Error Handling

Common errors and solutions.

## Examples

Usage examples with expected outputs.

## Resources

Internal and external references.
EOF

# Replace placeholder
sed -i "s/SKILL_NAME_PLACEHOLDER/$SKILL_NAME/g" "$BASE_DIR/SKILL.md"

echo "✓ Created skill at: $BASE_DIR"
echo ""
echo "Next steps:"
echo "  1. Edit $BASE_DIR/SKILL.md"
echo "  2. Validate: python scripts/validate_skills.py"
echo "  3. Test the skill in Claude Code"
```

---

## Monitoring & Health Checks

### Health Check Matrix

| Component | Check | Command | Expected |
|-----------|-------|---------|----------|
| Python | Version | `python --version` | 3.9+ |
| Dependencies | Installed | `pip list \| grep nixtla` | nixtla>=0.5.0 |
| Linting | Black | `black --check .` | Exit 0 |
| Linting | isort | `isort --check-only .` | Exit 0 |
| Tests | pytest | `pytest -v` | All pass |
| Skills | Validator | `python scripts/validate_skills.py` | All pass |
| Git | Status | `git status --short` | Clean |

### Automated Health Checks

**GitHub Actions Status**: Check `.github/workflows/ci.yml` status badges in README

**Local Check Script**:
```bash
# Quick health check
make health  # If Makefile exists

# Or manually
python scripts/validate_skills.py && pytest -v --tb=short
```

### Alerting

Currently manual - check CI status on GitHub Actions dashboard.

**Future Enhancement**: Add Slack notifications for CI failures via GitHub Actions.

---

## Security Considerations

### Secrets Management

**Never Commit**:
- `.env` files with real credentials
- API keys (NIXTLA_TIMEGPT_API_KEY)
- GCP service account keys
- Any file matching `*secret*`, `*credential*`, `*key*.json`

**GitHub Secrets** (for CI/CD):
- `GCP_WORKLOAD_IDENTITY_PROVIDER` - WIF provider
- `GCP_SERVICE_ACCOUNT` - Service account email
- `NIXTLA_TIMEGPT_API_KEY` - For live tests

### Security Scanning

**Trivy Scan** (runs on PRs):
```yaml
# .github/workflows/ci.yml
- name: Run Trivy security scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    severity: 'CRITICAL,HIGH'
```

**Manual Secrets Check**:
```bash
# Check for hardcoded secrets
grep -r --include="*.py" --include="*.js" \
  -E "(api_key|secret|password|token)\s*=\s*['\"][^'\"]+['\"]" \
  --exclude-dir=venv --exclude-dir=.git .
```

### Access Control

- Repository: Private (Intent Solutions org)
- CI/CD: GitHub Actions with OIDC to GCP (no long-lived keys)
- GCP: Workload Identity Federation for keyless auth

---

## Cost Management

### GitHub Actions Minutes

**Free Tier**: 2,000 minutes/month (private repos)

**Current Usage** (estimated):
- TIER 1 jobs: ~2 min each
- TIER 2 jobs: ~15 min each
- macOS: 10x multiplier
- Windows: 2x multiplier

**Cost Optimization Implemented**:
1. Tiered CI (90% savings)
2. Path filters (skip docs-only changes)
3. Reduced OS matrix (macOS only on PRs)
4. Caching (pip packages)

### GCP Costs (if using BigQuery plugin)

| Service | Usage | Estimated Cost |
|---------|-------|----------------|
| Cloud Functions | Minimal | Free tier |
| BigQuery | Query bytes | ~$5/TB |
| Cloud Storage | Minimal | ~$0.02/GB/month |

### TimeGPT API Costs

- Per-call pricing varies by plan
- Smoke tests use minimal data
- Batch forecasting can increase costs
- Monitor usage at https://dashboard.nixtla.io/

---

## Troubleshooting Guide

### Common Issues

#### Issue 1: Skills Validation Fails

**Symptom**: `❌ ERROR: 'description' must use third person`

**Cause**: Description contains first-person pronouns ("I", "We", "You")

**Solution**:
```bash
# Check the specific skill
cat 003-skills/.claude/skills/nixtla-my-skill/SKILL.md | head -10

# Fix: Use third-person ("This skill...", "Analyzes...", "Guides...")
```

#### Issue 2: CI Fails on Black Check

**Symptom**: `black --check --diff .` exits non-zero

**Solution**:
```bash
# Auto-fix formatting
black .

# Commit and push
git add -A && git commit -m "style: format with black"
```

#### Issue 3: MCP Server Not Starting

**Symptom**: Plugin commands fail with connection errors

**Solution**:
```bash
# Check Python environment
cd 005-plugins/nixtla-baseline-lab
source .venv-nixtla-baseline/bin/activate

# Test MCP server directly
python scripts/nixtla_baseline_mcp.py --help

# Check dependencies
pip install -r scripts/requirements.txt
```

#### Issue 4: Tests Timeout on Baseline Smoke

**Symptom**: `run_baseline_m4_smoke.py` takes >90 seconds

**Cause**: Missing M4 data cache or slow network

**Solution**:
```bash
# Pre-download M4 data
cd 005-plugins/nixtla-baseline-lab
python -c "from datasetsforecast.m4 import M4; M4.load('data/m4', 'Daily')"
```

#### Issue 5: Post-Compact Hook Not Running

**Symptom**: Claude Code doesn't read standards after compaction

**Solution**:
```bash
# Check hook is executable
chmod +x .claude/hooks/post-compact.sh

# Verify settings.json
cat .claude/settings.json | jq '.hooks'
```

### Error Reference Table

| Error Code | Location | Cause | Fix |
|------------|----------|-------|-----|
| E1001 | validate_skills.py | Missing 'name' | Add name to frontmatter |
| E1002 | validate_skills.py | Missing 'description' | Add description field |
| E1003 | validate_skills.py | Missing 'allowed-tools' | Add allowed-tools field |
| E1004 | validate_skills.py | Description >1024 chars | Shorten description |
| E1005 | validate_skills.py | Body >5000 words | Move content to references/ |
| W1001 | validate_skills.py | Missing 'version' | Add version field |
| W1002 | validate_skills.py | Missing 'license' | Add license field |

---

## Backup & Recovery

### Git-Based Recovery

**Revert to Previous Version**:
```bash
# View recent commits
git log --oneline -20

# Revert to specific commit
git checkout <commit-hash> -- <file>

# Or reset entire branch (destructive!)
git reset --hard <commit-hash>
```

### Archive Directory

Historical backups stored in `010-archive/`:
```
010-archive/
├── backups-20251108/
│   ├── skill-structure-cleanup-20251108-073936/
│   └── skills-migration-20251108-070147/
└── [Historical versions]
```

### Recovery Runbook

```bash
#!/bin/bash
# Recovery from archive

BACKUP_DATE=$1
COMPONENT=$2

if [ -z "$BACKUP_DATE" ] || [ -z "$COMPONENT" ]; then
    echo "Usage: ./recover.sh 20251108 skills-pack"
    exit 1
fi

ARCHIVE_DIR="010-archive/backups-$BACKUP_DATE"

if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "Archive not found: $ARCHIVE_DIR"
    ls 010-archive/
    exit 1
fi

echo "Available backups:"
ls "$ARCHIVE_DIR/"

echo ""
echo "To restore, use:"
echo "  cp -r $ARCHIVE_DIR/$COMPONENT/* <destination>/"
```

---

## Quick Reference Card

### Daily Commands

```bash
# Health check
python scripts/validate_skills.py && pytest -v --tb=short

# Format code
black . && isort .

# Run plugin smoke test
cd 005-plugins/nixtla-baseline-lab && python tests/run_baseline_m4_smoke.py

# View CI status
gh run list --workflow=ci.yml --limit=5
```

### Git Workflow

```bash
# Feature branch
git checkout -b feature/my-feature
# ... make changes ...
black . && isort .
git add -A
git commit -m "feat: description of change"
git push -u origin feature/my-feature
# Create PR via GitHub UI
```

### Key File Locations

| What | Where |
|------|-------|
| Version | `VERSION` |
| Main CI | `.github/workflows/ci.yml` |
| Skills Validator | `scripts/validate_skills.py` |
| Skills Standard | `000-docs/skills-schema/SKILLS-STANDARD-COMPLETE.md` |
| Plugin Smoke Test | `005-plugins/nixtla-baseline-lab/tests/run_baseline_m4_smoke.py` |
| Changelog | `CHANGELOG.md` |
| Claude Instructions | `CLAUDE.md` |

### Emergency Contacts

- **Repository Owner**: Jeremy Longshore (Intent Solutions)
- **Nixtla Contact**: [TBD based on collaboration]
- **GitHub Issues**: https://github.com/intent-solutions-io/plugins-nixtla/issues

---

## Appendix A: Validation Rules Reference

### Skills Validator v2.3.0 Rules

| Rule | Constraint | Level |
|------|------------|-------|
| name | Required, lowercase, 1-64 chars, no "anthropic"/"claude" | ERROR |
| description | Required, max 1024 chars, third-person | ERROR |
| allowed-tools | Required, CSV string | ERROR |
| body | Max 5000 words | ERROR |
| paths | No hardcoded /home/, /Users/ | ERROR |
| total budget | All descriptions < 15,000 chars combined | ERROR |
| version | Recommended, semantic | WARN |
| license | Recommended | WARN |
| when_to_use | Deprecated | WARN |

### Sources of Truth (by Authority)

1. **Anthropic Platform Docs** (platform.claude.com) - Official spec
2. **Lee Han Chung** (Oct 2025) - Implementation guide
3. **Official Blog** (claude.com/blog) - Product guidance
4. **Engineering Blog** (anthropic.com/engineering) - Architecture

---

## Appendix B: Directory Standards

### Doc-Filing v3.0

Format: `NNN-CC-ABCD-description.md`

| Code | Category |
|------|----------|
| PP | Planning |
| AT | Architecture |
| AA | Audits/AAR |
| OD | Overview |
| DR | Reference |
| QA | Quality |
| UC | User Content |
| MC | Miscellaneous |

### Skill Directory Structure

```
skill-name/
├── SKILL.md              # Required
├── assets/               # Optional
│   ├── templates/
│   └── .gitkeep
├── references/           # Optional (progressive disclosure)
└── scripts/              # Optional (implementation code)
```

---

**Document End**

*Generated: 2025-12-08T23:45:00Z*
*Playbook Version: 1.0.0*
*Repository Version: 1.6.0*
