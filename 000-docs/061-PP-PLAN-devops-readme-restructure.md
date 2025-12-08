# DevOps README Restructure Plan

**Document ID**: 061-PP-PLAN-devops-readme-restructure
**Created**: 2025-12-08
**Status**: APPROVED FOR IMPLEMENTATION

---

## Problem Statement

A DevOps engineer landing in this repo for the first time cannot answer these questions within 30 seconds:
1. What does each folder DO?
2. Where do I run commands from?
3. What env vars do I need?
4. How do I verify the system works?
5. Where's the CI/CD?

The current README focuses on **plugin installation** but not **operational understanding**.

---

## Target Audience

**Primary**: DevOps engineer assigned to this repo for the first time
**Secondary**: New contributor, SRE, or infrastructure team member

---

## Design Principles

1. **30-Second Rule**: Answer "what is this?" in 30 seconds
2. **Visual Navigation**: Directory tree with PURPOSE annotations
3. **Copy-Paste Ready**: Every command is complete, tested, runnable
4. **Health Check First**: Show how to verify the system BEFORE explaining details
5. **Env Var Bible**: Single source of truth for all environment variables
6. **No Scrolling for Essentials**: Critical info above the fold

---

## Proposed README Structure

```markdown
# Nixtla Plugin Showcase

[1-line what] | [Status badge] | [Version badge]

## 🎯 TL;DR (30 seconds)

- **What**: Claude Code plugins for time-series forecasting
- **Status**: Experimental showcase (not production)
- **Stack**: Python 3.10+ | statsforecast | TimeGPT

## 🏃 Health Check (Run First)

[3 commands to verify repo is operational]

## 📁 Directory Map

[Visual tree with PURPOSE of each folder]

## 🔑 Environment Variables

[Table of ALL env vars with required/optional]

## ⚡ Quick Commands

[Day 1 commands for DevOps]

## 🔧 CI/CD Reference

[What runs, where, when]

## 📚 Deep Dive Docs

[Links to detailed docs]

## 🆘 Troubleshooting

[Common problems, fast solutions]
```

---

## Section Details

### Section 1: TL;DR (30 seconds)

**Purpose**: Answer "what is this repo?" immediately

```markdown
## 🎯 TL;DR

| Question | Answer |
|----------|--------|
| **What** | Claude Code plugins + AI skills for time-series forecasting |
| **Who** | Business showcase for Nixtla CEO |
| **Status** | Experimental (3 plugins, 21 skills) |
| **Stack** | Python 3.10+, statsforecast, TimeGPT API |
| **Entry Point** | `plugins/nixtla-baseline-lab/` |
```

### Section 2: Health Check (Run First)

**Purpose**: Verify repo works BEFORE reading docs

```markdown
## 🏃 Health Check (Run First)

```bash
# 1. Dependencies OK?
python3 --version  # Need 3.10+

# 2. Tests pass?
pytest -v --tb=short 2>/dev/null || echo "Run: pip install -e . && pip install pytest"

# 3. Baseline lab works? (90 sec, offline)
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv 2>/dev/null || echo "Setup required"
source .venv-nixtla-baseline/bin/activate 2>/dev/null
python tests/run_baseline_m4_smoke.py
```

✅ All pass? You're ready.
❌ Something failed? See [Troubleshooting](#troubleshooting)
```

### Section 3: Directory Map

**Purpose**: Visual navigation with PURPOSE annotations

```markdown
## 📁 Directory Map

```
nixtla/
├── 000-docs/              # 📖 ALL documentation (Doc-Filing v3.0)
│   ├── global/            #    Executive summaries, DevOps guide
│   └── planned-skills/    #    Generated skill specs (21 skills)
│
├── plugins/               # 🔌 WORKING PLUGINS (start here)
│   ├── nixtla-baseline-lab/      # ⭐ Main showcase - M4 benchmarks
│   ├── nixtla-bigquery-forecaster/  # BigQuery integration
│   └── nixtla-search-to-slack/      # Slack notifications
│
├── skills-pack/           # 🧠 Claude Skills (AI behavior mods)
│   └── .claude/skills/    #    8 production skills
│
├── packages/              # 📦 Installable packages
│   └── nixtla-claude-skills-installer/  # CLI: nixtla-skills
│
├── scripts/               # 🛠️ Repo-level automation
├── tests/                 # 🧪 Integration tests
├── .github/workflows/     # 🔄 CI/CD pipelines
│
├── CLAUDE.md              # 🤖 AI assistant instructions
├── README.md              # 👈 You are here
└── VERSION                # 📌 Current: 1.4.1
```

**Entry Points by Role**:
| Role | Start Here |
|------|------------|
| DevOps | `000-docs/global/003-GUIDE-devops-*.md` |
| Developer | `plugins/nixtla-baseline-lab/` |
| Stakeholder | `000-docs/global/000-EXECUTIVE-SUMMARY.md` |
```

### Section 4: Environment Variables

**Purpose**: Single source of truth for all env vars

```markdown
## 🔑 Environment Variables

| Variable | Required | Purpose | Where Used |
|----------|----------|---------|------------|
| `NIXTLA_TIMEGPT_API_KEY` | For TimeGPT | Nixtla API access | All TimeGPT skills |
| `PYTHONPATH` | No | Module resolution | Tests |
| `PROJECT_ID` | For GCP | Google Cloud project | BigQuery plugin |
| `LOCATION` | For GCP | GCP region | BigQuery plugin |

**Quick Setup**:
```bash
# Minimal (baseline lab only - no API needed)
# Nothing required! Baseline lab uses statsforecast (offline)

# Full setup (TimeGPT features)
export NIXTLA_TIMEGPT_API_KEY='your-key-here'
```
```

### Section 5: Quick Commands

**Purpose**: Day 1 commands for DevOps

```markdown
## ⚡ Quick Commands

### First Time Setup
```bash
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla
pip install -e .
pip install -r requirements-dev.txt
```

### Run Tests
```bash
pytest -v                    # All tests
pytest plugins/ -v           # Plugin tests only
pytest --cov=plugins -v      # With coverage
```

### Lint & Format
```bash
black --check .              # Check formatting
black .                      # Fix formatting
isort --check-only .         # Check imports
flake8 .                     # Lint
```

### Build & Deploy
```bash
# No deployment - this is a showcase repo
# See CI/CD section for automated checks
```
```

### Section 6: CI/CD Reference

**Purpose**: What runs, where, when

```markdown
## 🔄 CI/CD Reference

| Workflow | Trigger | What It Does |
|----------|---------|--------------|
| `ci.yml` | PR, push | Lint, format, test |
| `nixtla-baseline-lab-ci.yml` | PR, push | Plugin-specific tests |
| `skills-installer-ci.yml` | PR, push | Skills installer tests |

**Files**: `.github/workflows/`

**Required to Merge**: All checks must pass
```

### Section 7: Deep Dive Docs

**Purpose**: Links to detailed docs (not inline)

```markdown
## 📚 Documentation

| Doc | Audience | Location |
|-----|----------|----------|
| DevOps Operations Guide | DevOps/SRE | `000-docs/global/003-GUIDE-devops-*.md` |
| Executive Summary | Stakeholders | `000-docs/global/000-EXECUTIVE-SUMMARY.md` |
| Plugin Implementation | Developers | `000-docs/6767-f-OD-GUIDE-*.md` |
| Skill Standard | Skill authors | `000-docs/6767-m-DR-STND-*.md` |

**Doc-Filing System**: All docs use `NNN-CC-ABCD-description.md` naming
- `PP` = Planning, `AT` = Architecture, `AA` = Audits, `OD` = Overview
```

### Section 8: Troubleshooting

**Purpose**: Common problems, fast solutions

```markdown
## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | `pip install -e . && pip install -r requirements-dev.txt` |
| Tests fail with import error | `export PYTHONPATH=$PWD` |
| Permission denied on script | `chmod +x scripts/*.sh` |
| Plugin not found | Restart Claude Code after install |
| Smoke test timeout | Network issue or first run (downloads M4 data) |

**Still stuck?** Open an issue or email jeremy@intentsolutions.io
```

---

## Implementation Checklist

- [ ] Backup current README.md
- [ ] Create new README.md with above structure
- [ ] Test all commands in Health Check section
- [ ] Verify all links work
- [ ] Get stakeholder sign-off

---

## Success Criteria

A new DevOps engineer should be able to:
1. ✅ Understand repo purpose in 30 seconds
2. ✅ Run health check in 2 minutes
3. ✅ Find any file by purpose using directory map
4. ✅ Know all required env vars
5. ✅ Run tests and lint checks
6. ✅ Find detailed docs without searching

---

**Document Created**: 2025-12-08
**Status**: Ready for implementation
