# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Business showcase for Nixtla CEO** demonstrating Claude Code plugins and AI skills for time-series forecasting.

| Attribute | Value |
|-----------|-------|
| **Version** | 1.9.0 (source: `VERSION`) |
| **Status** | 13 plugins at v1.0 marketplace tier (or v1.0-poc); 6 Phase 4/5 plugins scaffolded as v0.1.0-wip |
| **Stack** | Python 3.10+ (Nixtla SDK >=0.7.3 dropped 3.9), statsforecast, TimeGPT API, pytest, black, isort |
| **Skills** | 30 (in `003-skills/.claude/skills/`) |
| **Plugins** | 19 (in `005-plugins/`) — 13 at v1.0 / v1.0-poc + 6 at v0.1.0-wip with honest WIP labeling |

## Quick Start (5 Minutes)

```bash
# 1. Setup environment
./004-scripts/setup-dev-environment.sh      # Creates venv + .env
# OR manually:
python3 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt

# 2. Activate
source venv/bin/activate

# 3. Run tests
pytest -v --tb=short -m "not integration"

# 4. Validate skills
python 004-scripts/validate_skills_v2.py
```

**All pass?** Ready to work. **Failures?** See Troubleshooting section.

## Directory Structure

```
000-docs/           # ALL documentation (AAR system, specs, standards)
001-htmlcov/        # Test coverage reports
002-workspaces/     # Demo projects (notably test-harness-lab/)
003-skills/         # Claude Skills (.claude/skills/nixtla-*/)
004-scripts/        # Automation (validators, generators)
005-plugins/        # Plugin implementations
006-packages/       # Installable packages (skills-installer)
007-tests/          # E2E/integration tests (run explicitly)
009-temp-data/      # Generated/temporary data
010-archive/        # Archived content
tests/              # pytest suite (DEFAULT target)
```

**Key locations**:
- Skills: `003-skills/.claude/skills/nixtla-*/SKILL.md`
- Plugins: `005-plugins/nixtla-*/`
- Master skill standard: `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md`

## Commands Reference

### Testing

```bash
# All tests
pytest -v

# With coverage (outputs to 001-htmlcov/)
pytest --cov=005-plugins --cov-report=term -v

# By marker (see pytest.ini)
pytest -m "unit"                # Unit tests only
pytest -m "not integration"     # Skip integration
pytest -m "not slow"            # Skip slow tests
pytest -m "not cloud"           # Skip cloud-dependent
pytest -m "not api"             # Skip external API calls

# Single test
pytest tests/skills/test_all_skills.py::test_l4_quality -v

# Pattern match
pytest -k "test_baseline" -v
```

### Validation

```bash
# Skills validation (strict mode)
python 004-scripts/validate_skills_v2.py --fail-on-warn

# Plugin validation
bash 004-scripts/validate-all-plugins.sh .

# Universal validator (evidence bundle)
python 003-skills/.claude/skills/nixtla-universal-validator/scripts/run_validator_suite.py \
  --target . --project pr-1234 --out reports/pr-1234 --profile default
```

### Formatting

```bash
# Check
black --check . && isort --check-only . && flake8 .

# Fix
black . && isort .
```

### Plugin Development (Baseline Lab)

```bash
cd 005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# Smoke test (90 sec, offline)
python tests/run_baseline_m4_smoke.py

# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

### Skills Installer

```bash
pip install -e 006-packages/nixtla-claude-skills-installer
cd /path/to/your/project
nixtla-skills init      # Install all skills
nixtla-skills update    # Update to latest
```

## Architecture

### Three-Layer System

1. **Claude Skills** (`003-skills/.claude/skills/nixtla-*/`)
   - AI prompts that transform Claude's behavior
   - Auto-activate on relevant context
   - Each has: `SKILL.md` + optional `scripts/`, `assets/templates/`

2. **Plugins** (`005-plugins/*/`)
   - Independently-shipped apps. Each plugin owns its own `plugin.json`,
     MCP server, tests, and per-plugin GitHub Actions workflow.
   - Granularity: one plugin per job (NOT a monolith). Pre-PoC v1.0:
     baseline-lab, search-to-slack, snowflake-adapter, bigquery-forecaster,
     dbt-package, plus 7 Phase 1 plugins (roi-calculator, forecast-explainer,
     vs-statsforecast-benchmark, cost-optimizer, migration-assistant,
     airflow-operator, changelog-automation).
   - PoC pattern (v1.0-poc): defi-sentinel, anomaly-streaming-monitor.
   - WIP scaffolds (v0.1.0-wip): sales-demo-builder, forecast-workflow-templates,
     forecast-audit-report, support-deflector, docs-qa-generator,
     embedded-forecast-widget.

3. **Slash Commands** (`005-plugins/*/commands/*.md`)
   - User-invoked commands like `/nixtla-baseline-m4`

### MCP Server Pattern

The baseline lab MCP server (`005-plugins/nixtla-baseline-lab/scripts/nixtla_baseline_mcp.py`) exposes:
- `run_baselines` - Run statsforecast models on M4/custom data
- `get_nixtla_compatibility_info` - Library version info
- `generate_benchmark_report` - Markdown report from metrics CSV
- `generate_github_issue_draft` - GitHub issue template

Most MCP servers are Python (using the `mcp` package). One exception: streaming-monitor's MCP server is TypeScript (`@modelcontextprotocol/sdk`) because its production target is `kafkajs` / `aws-sdk`.

### Honest Labeling Pattern (load-bearing)

Plugin posture is encoded in three layers — version suffix, tool description prefix, response disclaimer field. Each tier has dedicated tests verifying the labeling integrity.

| Tier | Version | Tool desc prefix | Response field | Example |
|---|---|---|---|---|
| Production v1.0 | `1.0.0` | none | none | baseline-lab, snowflake-adapter, bigquery-forecaster |
| Proof of Concept | `1.0.0-poc` | `[PoC]` | `_disclaimer` (PoC notice) | defi-sentinel, anomaly-streaming-monitor |
| Work In Progress | `0.1.0-wip` | `[WIP]` | `_disclaimer` (WIP notice) | sales-demo-builder, support-deflector, etc. |

**Why this matters**: a future Claude / contributor / user looking at the plugin needs to know its fidelity at a glance. Renaming a `0.1.0-wip` plugin to `1.0.0` without implementing the production gap = silent regression. The labeling tests block that.

**Test pattern** (each plugin's `tests/test_{poc,wip}_labeling.py`):
- Plugin manifest version contains the suffix
- README has the banner / Origin section / What's-real-vs-roadmap matrix
- Every tool description starts with the prefix
- Every `call_tool()` response contains the `_disclaimer` field

### Production Hardening Patterns

When taking a plugin from demo → production (Epic 2.4 `bigquery-forecaster` is the canonical reference):

- **`src/sql_validation.py`**: identifier validators (`validate_identifier`, `validate_project_id`) for SQL-injection mitigation. BigQuery doesn't support parameterized identifiers; the only safe path is regex allow-list.
- **`src/retry.py`**: `@retry_on_transient` decorator with exponential backoff + jitter. Catches `google.api_core.exceptions` `{ServiceUnavailable, TooManyRequests, InternalServerError, GatewayTimeout, DeadlineExceeded}`. Default 5 attempts, 1s→30s.
- **Lazy `src/__init__.py`**: PEP 562 `__getattr__` so light modules (validators, retry) load without statsforecast / google-cloud-bigquery installed. Lets CI run validator/security tests without the heavy deps.
- **`DEPLOY.md`**: per-plugin deployment guide covering GCP service accounts, Cloud Run Jobs, Secret Manager, observability, troubleshooting, cost notes.

### plugin.json Canonical Fields (Anthropic spec — validator allow-list)

The validator's `PLUGIN_JSON_FIELDS` accepts: `name` (required), `version`, `description`, `author` (object with `name`), `homepage`, `repository`, `license`, `keywords`, `commands`, `agents`, `skills`, `hooks`, `mcpServers`, `outputStyles`, `lspServers`. Anything else = ERROR (e.g., `displayName` is rejected; `tags` and `compatibility` belong only in SKILL.md frontmatter, not plugin.json).

## Skills Standard (Summary)

**Full spec**: `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md`
**Canonical validator**: `~/000-projects/claude-code-plugins/scripts/validate-skills-schema.py` (Plugin Validator v7.0 / schema 3.3.1)
**Vendored copy** at `004-scripts/validate_skills_v2.py` is for in-repo CI only — the canonical validator is the source of truth.

### Required Frontmatter (IS 8-field marketplace tier — all required, ERROR if missing)

```yaml
name: nixtla-<short-name>
description: |
  [Capabilities]. [Features].
  Use when [scenarios].
  Trigger with "phrase 1", "phrase 2".
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash(python:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: "MIT"
tags:
  - forecasting
  - time-series
compatibility: Claude Code 1.0+; Python 3.10+; statsforecast 1.7+.
```

### L4 Quality Requirements (100% mandatory)

- Action verb in description (analyze, detect, forecast, generate, validate, etc.)
- "Use when" phrase present
- "Trigger with" phrase present
- 100-300 character description length
- Domain keyword (timegpt, forecast, time series, nixtla, statsforecast)

### Validation

```bash
python 004-scripts/validate_skills_v2.py --verbose
```

## Environment Variables

Create `.env` in repo root (use `./004-scripts/setup-dev-environment.sh`):

```bash
# Optional - TimeGPT features only
NIXTLA_TIMEGPT_API_KEY=your-key

# Optional - GCP features only
PROJECT_ID=your-gcp-project
LOCATION=us-central1
```

**Note**: Baseline lab works fully offline with zero API keys.

## Nixtla Integration Patterns

```python
# StatsForecast (open source, no API key)
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive
sf = StatsForecast(models=[AutoETS(), AutoTheta()], freq='D')
forecasts = sf.forecast(df=df_train, h=14)

# TimeGPT (requires NIXTLA_TIMEGPT_API_KEY)
from nixtla import NixtlaClient
client = NixtlaClient(api_key='...')
forecast = client.forecast(df=data, h=24, freq='H')
```

## Development Workflow

### Commit Messages

Follow Conventional Commits: `<type>(<scope>): <description>`

**Types**: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `style`, `perf`
**Scopes**: `skills`, `plugins`, `scripts`, `docs`, `ci`, `tests`, `packages`

```bash
feat(skills): add nixtla-timegpt-lab skill
fix(baseline-lab): correct M4 data loading bug
docs(readme): update installation instructions
```

### Code Style

- **Indentation**: 4 spaces (see `.editorconfig`)
- **Line length**: ≤100 characters (Black/Flake8)
- **Naming**: plugin folders `kebab-case`, Python `snake_case`

### Pre-PR Checklist

```bash
python 004-scripts/validate_skills_v2.py --fail-on-warn
bash 004-scripts/validate-all-plugins.sh .
pytest -v -m "not integration"
black --check . && isort --check-only . && flake8 .
```

## Documentation Standards

### Doc-Filing System

All docs in `000-docs/` use naming: `NNN-AA-CODE-descriptive-slug.md`

- `NNN` = 3-digit sequence (never renumber)
- `AA-CODE` = Type (REPT, AACR, STAT, PRD, ADR, AUDT)

### AAR Required Sections

1. Title with doc ID
2. Date/time (CST)
3. Executive Summary
4. Scope
5. Changes Made
6. Risks/Unknowns
7. Next Actions

## CI/CD Workflows

Every plugin has a per-plugin workflow at `.github/workflows/{name}-ci.yml`. The pattern (replicated 19×):

```yaml
jobs:
  unit-tests:    # pytest -o addopts="" (overrides repo-root coverage flags)
  validator-gate: # clones jeremylongshore/claude-code-plugins, runs Plugin Validator v7.0 marketplace tier
```

**Why `-o addopts=""`**: the repo-root `pytest.ini` injects `--cov` flags requiring pytest-cov. Per-plugin jobs install only `pytest` to keep CI fast — the override neutralizes the inifile injection.

**Cross-cutting workflows** (in `.github/workflows/`):

| Workflow | Purpose |
|---|---|
| `ci.yml` | Main repo-wide validation (lint + repo-level tests) |
| `skills-validation.yml` | Vendored skills validator |
| `plugin-validator.yml` | Per-plugin matrix validation via canonical validator |
| `gemini-daily-audit.yml` | Daily audit run |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: statsforecast` | `pip install -r scripts/requirements.txt` (in plugin dir) |
| `ModuleNotFoundError` (general) | `pip install -e . && pip install -r requirements-dev.txt` |
| Tests fail with import error | `export PYTHONPATH=$PWD` or activate venv |
| Permission denied on script | `chmod +x scripts/*.sh` |
| Plugin not found after install | Restart Claude Code |
| Smoke test timeout | First run downloads M4 data (~30MB) |
| `NIXTLA_TIMEGPT_API_KEY not set` | Only needed for TimeGPT, not baseline lab |
| Validation failures | `python 004-scripts/validate_skills_v2.py --verbose` |
| Virtual environment issues | Delete `venv/`, re-run setup script |

## Post-Compact Context Restoration

**After context compaction, read these files:**

1. `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md` - Skills schema
2. Last two AAR docs in `000-docs/` (highest numbered `*-AA-*.md` files)

## Version & Release

**Current**: 1.9.0 (source of truth: `VERSION`)

Use `/release` (Universal Release Engineering skill) for the full ceremony — it handles version-consistency checks, CHANGELOG generation, README sync, security scan, branch-protection bypass/restore, gist update, and AAR generation.

Manual release steps if `/release` is unavailable:
1. Update `VERSION` file
2. Update `CHANGELOG.md`
3. Create release AAR in `000-docs/`
4. Tag: `git tag -a v1.X.Y -m "Release v1.X.Y"`
5. Push: `git push origin v1.X.Y`

### Marketplace.json discipline

`.claude-plugin/marketplace.json` deliberately lists only WORKING-only plugins (per CHANGELOG v1.9.0). Per-plugin expansion to all 19 plugins is deferred to the D1 health audit. Don't expand it without re-reading that CHANGELOG entry.

### Public gist

`.gist-id` at repo root holds the canonical Project Landing gist ID (`dcdd7d8a9a262ec1f556fcb60b7af4f9`). `/gist-auditor` uses it to scope audits; `/release` Phase 7.5 uses it to keep the gist in sync with HEAD.


## Testing baseline (2026-05-01 — Intent Solutions Testing SOP)

This repo participates in the **Intent Solutions Testing SOP** per `~/.claude/CLAUDE.md` § "Intent Solutions Testing SOP" and the VPS-as-the-home program (`OPS-5nm`, Priority 6).

**Installed**: `@intentsolutions/audit-harness v0.1.0` vendored at `.audit-harness/` with wrapper at `scripts/audit-harness`.

**Commands**: `scripts/audit-harness {verify, init, list, escape-scan --staged}`.

**Next step**: run `/audit-tests` to produce `TEST_AUDIT.md`. See `000-docs/677-OD-SOPS-audit-harness-baseline-2026-05-01.md`.

**Upgrade**: `AUDIT_HARNESS_VERSION=vX.Y.Z curl -sSL https://raw.githubusercontent.com/jeremylongshore/audit-harness/main/install.sh | bash`. Or run `/sync-testing-harness` from any session.
