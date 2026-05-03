# Nixtla Plugin Showcase

Production-grade Claude Code plugins and AI skills for time-series forecasting with Nixtla — `statsforecast`, `mlforecast`, `neuralforecast`, and TimeGPT.

**Version**: 1.9.0 · **Status**: Public showcase · **Flagship plugins**: 3 · **Skills**: 30 · **Experimental tier**: 11 plugins

> **What this is.** A curated reference implementation showing what production-grade time-series forecasting looks like inside Claude Code. Three flagship plugins demonstrate the patterns; thirty skills carry the forecasting expertise; an experimental tier shows where the work goes next. See [`000-docs/130-AA-VISN-strategic-vision-v2-flagship-curation.md`](000-docs/130-AA-VISN-strategic-vision-v2-flagship-curation.md) for the strategy and the four-tier structure.

---

## TL;DR (30 seconds)

| Question | Answer |
|----------|--------|
| **What** | Three flagship Claude Code plugins + 30 forecasting skills |
| **Why** | Showcase Nixtla's stack inside the AI-augmented developer workflow |
| **Who** | Time-series practitioners, data engineers, Nixtla customers and prospects |
| **Stack** | Python 3.10+, statsforecast, mlforecast, neuralforecast, TimeGPT API |
| **Try first** | [`005-plugins/nixtla-baseline-lab/`](005-plugins/nixtla-baseline-lab/) — runs offline in 90 seconds, no API key |

---

## The flagship — three plugins, ready to install

```
.claude-plugin/marketplace.json  ← the curated set
```

| Plugin | What it does | API key | Status |
|--------|--------------|--------|--------|
| [`nixtla-baseline-lab`](005-plugins/nixtla-baseline-lab/) | Run statsforecast baselines on M4 (or your CSV) inside a Claude conversation | None | Working |
| [`nixtla-bigquery-forecaster`](005-plugins/nixtla-bigquery-forecaster/) | Pull from BigQuery, forecast with AutoETS / AutoTheta, write results back, all from chat | GCP creds | Working |
| [`nixtla-search-to-slack`](005-plugins/nixtla-search-to-slack/) | Discover and curate forecasting content from web + GitHub, post AI-summarized digests to Slack | Slack + (SerpAPI or Claude WebSearch) | Working |

> The flagship is hardened to the v2.0 acceptance gate: install loads cleanly on a fresh clone, per-plugin CI gates merge, ≥80% test coverage, security-reviewed, screencast linked, deploy guide for self-hosting. See the strategic vision doc for the full ten-gate criterion.

### Quickstart — Baseline Lab

Five-minute install with zero API keys:

```bash
git clone https://github.com/jeremylongshore/plugins-nixtla.git
cd plugins-nixtla/005-plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
source .venv-nixtla-baseline/bin/activate
pip install -r scripts/requirements.txt

# In Claude Code:
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

Runs in ~90 seconds, fully offline, zero API cost. First-time download fetches ~30 MB of M4 data.

### What's in the marketplace

```bash
# Install any of the Trinity directly via the marketplace manifest
claude plugin install github:jeremylongshore/plugins-nixtla/005-plugins/nixtla-baseline-lab
claude plugin install github:jeremylongshore/plugins-nixtla/005-plugins/nixtla-bigquery-forecaster
claude plugin install github:jeremylongshore/plugins-nixtla/005-plugins/nixtla-search-to-slack
```

---

## The skills — 30 production skills

Skills are Claude behavior modifications (`SKILL.md` + scripts/templates) that auto-activate on relevant context. The repo ships 30 of them across two domains:

| Domain | Count | Examples |
|---|---|---|
| **Forecasting / time-series** | 19 | `nixtla-anomaly-detector`, `nixtla-batch-forecaster`, `nixtla-correlation-mapper`, `nixtla-cross-validator`, `nixtla-event-impact-modeler`, `nixtla-exogenous-integrator`, `nixtla-forecast-validator`, `nixtla-model-selector`, `nixtla-timegpt-finetune-lab`, `nixtla-uncertainty-quantifier` |
| **Engineering / infra** | 11 | `nixtla-mcp-server-builder`, `nixtla-plugin-scaffolder`, `nixtla-prd-to-code`, `nixtla-test-generator`, `nixtla-universal-validator`, `nixtla-prod-pipeline-generator` |

```bash
# Install all 30 into your own project
pip install -e 006-packages/nixtla-claude-skills-installer
cd /path/to/your/project
nixtla-skills init
```

Spec for the skill format we use: [`000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md`](000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md).

---

## Experimental tier — 11 plugins, not for public install

The repo also contains 11 in-progress plugin directories at various stages of maturity. **They are not in the marketplace and are not recommended for production use.** They live here as transparency about ongoing work and as a starting point for community contributors.

The full list and disposition (deferred / archived / removed-from-roadmap) is in [`130-AA-VISN`](000-docs/130-AA-VISN-strategic-vision-v2-flagship-curation.md) §"Tier 4". The short version: each plugin's README will carry an experimental banner; none are listed in `.claude-plugin/marketplace.json`.

---

## Roadmap — where this goes next

Three plugins in the v3.0 expansion, each with a complete PRD already written:

| Next-up plugin | Effort | Drives |
|---|---|---|
| `nixtla-sales-demo-builder` | 3 wk | Industry-specific TimeGPT demo notebooks generated in minutes |
| `nixtla-forecast-workflow-templates` | 6 wk | Drop-in production workflows (demand planning, revenue, capacity); $50–100K ARR opportunity |
| `nixtla-forecast-audit-report` | 8 wk | Compliance-grade audit reports (SOX, FDA, Basel III); unlocks regulated verticals |

PRDs live in `000-docs/000a-planned-plugins/external-revenue/`. Each lands as its own minor release on the v2.x line.

---

## Health check (run first)

```bash
# 1. Python version
python3 --version              # need 3.10+ (Nixtla SDK >=0.7.3 requires it)

# 2. Clone + install
git clone https://github.com/jeremylongshore/plugins-nixtla.git
cd plugins-nixtla
pip install -e . && pip install -r requirements-dev.txt

# 3. Tests pass?
pytest -v --tb=short -m "not integration"

# 4. Skills validate?
python 004-scripts/validate_skills_v2.py
```

All four green? Ready to work. Any failures? See [Troubleshooting](#troubleshooting).

---

## Repository map

```
plugins-nixtla/
├── 000-docs/                         # All documentation, NNN-CC-CODE-slug.md filing
│   ├── 130-AA-VISN-...               # ← strategic vision (start here)
│   ├── 122-AA-AUDT-...               # SDK migration baseline audit
│   ├── 000a-skills-schema/           # Master skills standard
│   └── 000a-planned-plugins/         # PRDs for v3.0 expansion plugins
├── 003-skills/.claude/skills/        # 30 production skills
├── 005-plugins/                      # Plugin implementations
│   ├── nixtla-baseline-lab/          #   FLAGSHIP — M4 baselines, offline-capable
│   ├── nixtla-bigquery-forecaster/   #   FLAGSHIP — GCP / BigQuery
│   ├── nixtla-search-to-slack/       #   FLAGSHIP — content curation → Slack
│   └── ...                           #   11 experimental plugins (banner in each)
├── 006-packages/                     # Installable packages
│   └── nixtla-claude-skills-installer/   # CLI: `nixtla-skills init`
├── 004-scripts/                      # Validators, generators
├── tests/                            # Repo-level pytest suite
├── .github/workflows/                # CI/CD
├── .claude-plugin/marketplace.json   # The flagship 3-plugin marketplace
├── CHANGELOG.md                      # Release history
└── VERSION                           # 1.9.0
```

---

## Environment

| Variable | When you need it | What it's for |
|---|---|---|
| `NIXTLA_TIMEGPT_API_KEY` | TimeGPT-based skills/plugins only | Nixtla TimeGPT API access |
| `PROJECT_ID` | `nixtla-bigquery-forecaster` only | Your GCP project |
| `LOCATION` | `nixtla-bigquery-forecaster` only | GCP region (default: `us-central1`) |
| `SLACK_BOT_TOKEN`, `SERPAPI_KEY` | `nixtla-search-to-slack` only | See plugin's setup guide |

Baseline lab needs no keys. Just `statsforecast` and ~30 MB of M4 data.

---

## Quick commands

```bash
# Tests
pytest -v                                # all
pytest -m "not integration"              # skip network/GCP/API tests
pytest --cov=005-plugins -v              # with coverage

# Validation
python 004-scripts/validate_skills_v2.py --fail-on-warn
bash 004-scripts/validate-all-plugins.sh .

# Format
black --check . && isort --check-only . && flake8 .
black . && isort .                       # fix

# Skills installer (in another project)
pip install -e 006-packages/nixtla-claude-skills-installer
nixtla-skills init                       # install all skills
nixtla-skills update                     # update to latest
```

---

## CI/CD

| Workflow | Trigger | Required to merge? |
|---|---|---|
| `ci.yml` | every push + PR | Yes (lint, format, test) |
| `skills-validation.yml` | PR | Yes (skills schema strict) |
| `plugin-validator.yml` | PR | No (per-plugin schema check) |
| `nixtla-baseline-lab-ci.yml` | PR touching the lab | No |
| `gemini-pr-review.yml` | PR | No (AI review) |

Workflows live in [`.github/workflows/`](.github/workflows/).

---

## Documentation

| Document | Audience |
|---|---|
| [Strategic Vision v2.0](000-docs/130-AA-VISN-strategic-vision-v2-flagship-curation.md) | Anyone deciding what to build next |
| [Skills Standard](000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md) | Skill authors |
| [SDK Migration Baseline](000-docs/122-AA-AUDT-sdk-migration-baseline.md) | Anyone touching plugin requirements files |
| [Planned-Plugins Index](000-docs/000a-planned-plugins/README.md) | Roadmap readers |
| Per-plugin READMEs | Plugin users |

Doc filing format: `NNN-CC-CODE-description.md` — see [`002-command-bible/DOCUMENT-FILING-STANDARD-v3.0.md`](https://github.com/jeremylongshore/...) (lives outside this repo, in the personal command-bible).

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: statsforecast` | `cd 005-plugins/<plugin> && pip install -r scripts/requirements.txt` |
| `ModuleNotFoundError` (general) | `pip install -e . && pip install -r requirements-dev.txt` |
| Tests fail with import error | `export PYTHONPATH=$PWD` (or activate the venv) |
| `Could not find a version that satisfies the requirement nixtla>=0.7.3` | Python 3.10+ required (Nixtla 0.7.3 dropped 3.9). `python3 --version` to verify. |
| Smoke test timeout | First baseline-lab run downloads ~30 MB of M4 data; ~30–60 s the first time, instant after |
| Plugin not found after install | Restart Claude Code |
| `NIXTLA_TIMEGPT_API_KEY not set` | Only TimeGPT skills need it. Baseline lab is offline. |

Still stuck? Open an issue at https://github.com/jeremylongshore/plugins-nixtla/issues, or email jeremy@intentsolutions.io.

---

## Contributing

1. Fork `https://github.com/jeremylongshore/plugins-nixtla`
2. Branch: `git checkout -b feat/<short-description>`
3. Make changes; add or update tests
4. `pytest && black . && isort .` locally
5. Open PR against `main`

Two non-negotiables for any plugin contribution:

- **Tier discipline.** New plugin ideas default to Tier 4 (experimental). Promotion to a higher tier requires reconciliation against the [strategic vision](000-docs/130-AA-VISN-strategic-vision-v2-flagship-curation.md).
- **Test the change.** Repo-level CI must pass; if you touch a flagship plugin, that plugin's CI must pass too.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full details.

---

## Sponsorship & contact

This work is open-source under MIT, supported by:

- [GitHub Sponsors → @jeremylongshore](https://github.com/sponsors/jeremylongshore)
- [Buy Me a Coffee → @jeremylongshore](https://www.buymeacoffee.com/jeremylongshore)

Commercial engagements (custom plugins, integrations, advisory): [jeremy@intentsolutions.io](mailto:jeremy@intentsolutions.io)

---

## Prototypes & research

Beyond the flagship plugins, the repo carries two research artifacts kept for transparency about ongoing exploration:

### ERCOT grid forecasting

48-hour electricity load forecasting for the Texas (ERCOT) grid with interactive map visualization. Result: SeasonalNaive wins at **4.28% MAPE** on the 48 h holdout.

```bash
cd 002-workspaces/energy-grid-prototype
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python ercot_grid_forecast.py
```

Research write-up: [`000-docs/121-AA-REPT-energy-grid-forecasting-opportunity-research.md`](000-docs/121-AA-REPT-energy-grid-forecasting-opportunity-research.md).

### Test harness lab

5-phase validated workflow pattern for evaluating release readiness — used internally as the precursor to the `nixtla-release-validation` skill. Reference docs in [`002-workspaces/test-harness-lab/`](002-workspaces/test-harness-lab/).

---

## License

[MIT](LICENSE) — copyright Jeremy Longshore.
