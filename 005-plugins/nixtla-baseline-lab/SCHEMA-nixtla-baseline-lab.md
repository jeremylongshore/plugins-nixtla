# Schema: nixtla-baseline-lab

**Generated:** 2025-12-12
**Plugin Version:** 1.5.0
**Status:** Production (Live)

---

## Directory Tree

```
nixtla-baseline-lab/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── agents/
│   └── nixtla-baseline-analyst.md # Agent definition for baseline analysis
├── commands/
│   ├── nixtla-baseline-m4.md      # Slash command: Run M4 benchmark
│   └── nixtla-baseline-setup.md   # Slash command: Environment setup
├── data/
│   └── m4/datasets/               # M4 benchmark test data (6 files)
├── scripts/
│   ├── nixtla_baseline_mcp.py     # MCP server (4 tools exposed)
│   ├── requirements.txt           # Python dependencies
│   ├── setup_nixtla_env.sh        # Environment setup script
│   └── timegpt_client.py          # TimeGPT API client wrapper
├── skills/
│   └── nixtla-baseline-review/
│       ├── SKILL.md               # Skill definition
│       └── resources/             # Supporting docs (3 files)
├── tests/
│   ├── golden_tasks/              # CI test definitions
│   └── run_baseline_m4_smoke.py   # Smoke test runner
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-baseline-lab | Required |
| description | Run Nixtla-style baseline forecasting models... | Required |
| version | 1.5.0 | Required |
| author.name | Jeremy Longshore | Required |
| homepage | https://github.com/jeremylongshore/plugins-nixtla | Optional |
| repository | https://github.com/jeremylongshore/plugins-nixtla | Optional |
| license | MIT | Optional |

---

## MCP Tools (4 exposed)

| Tool Name | Purpose |
|-----------|---------|
| run_baselines | Run statsforecast models on M4/custom data |
| get_nixtla_compatibility_info | Library version information |
| generate_benchmark_report | Markdown report from metrics CSV |
| generate_github_issue_draft | GitHub issue template with reproducibility |

---

## Slash Commands (2)

| Command | Purpose |
|---------|---------|
| /nixtla-baseline-m4 | Run baseline models on M4 benchmark dataset |
| /nixtla-baseline-setup | Set up Python environment and dependencies |

---

## Skills (1)

| Skill | Purpose |
|-------|---------|
| nixtla-baseline-review | Analyze baseline forecasting results (sMAPE/MASE) |

---

## Agents (1)

| Agent | Purpose |
|-------|---------|
| nixtla-baseline-analyst | Autonomous baseline model analysis |

---

## Key Files

| File | Lines | Purpose |
|------|-------|---------|
| scripts/nixtla_baseline_mcp.py | ~600 | MCP server exposing 4 forecasting tools |
| scripts/timegpt_client.py | ~200 | TimeGPT API client wrapper |
| tests/run_baseline_m4_smoke.py | ~300 | Golden task smoke test (90 sec) |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Data scientists, ML practitioners
- **What:** Run statistical forecasting baseline models (AutoETS, AutoTheta, SeasonalNaive)
- **When:** Model benchmarking, baseline comparison, forecast accuracy validation
- **Target Goal:** sMAPE < 5% on M4 Daily; smoke test < 90 seconds
- **Production:** true
