# Nixtla Baseline Lab – Quick Review Checklist

**For:** Max Mergenthaler (Nixtla CEO)
**Purpose:** Test the working plugin in 10 minutes
**Status:** Production-ready (v0.8.0)

---

This is a self-contained workspace that runs Nixtla's statsforecast baselines locally inside Claude Code, with optional TimeGPT comparison if you choose to enable it.

---

## 0. Prerequisites

- Claude Code installed and able to use local plugins
- Python 3.10+ on your machine
- Git installed

---

## 1. Clone the repo

```bash
git clone https://github.com/jeremylongshore/claude-code-plugins-nixtla.git
cd claude-code-plugins-nixtla
```

---

## 2. Open in Claude Code and install the plugin

1. Open this folder (`claude-code-plugins-nixtla`) in Claude Code
2. Add the repo as a local marketplace source (pointing to the `.claude-plugin/marketplace.json` in the root)
3. Install the plugin:
   - **Plugin name:** Nixtla Baseline Lab
   - This will register:
     - Commands like `/nixtla-baseline-m4` and `/nixtla-baseline-setup`
     - The MCP server that runs Nixtla's statsforecast models

---

## 3. One-time Python environment setup

**Option A - Terminal:**
```bash
cd plugins/nixtla-baseline-lab
./scripts/setup_nixtla_env.sh --venv
```

**Option B - Inside Claude Code:**
```
/nixtla-baseline-setup
```

Either way, this step creates a local virtualenv and installs:
- `statsforecast`
- `datasetsforecast`
- `nixtla` (TimeGPT SDK, only used if you opt in)
- pandas, numpy, matplotlib, etc.

---

## 4. Run the offline statsforecast demo (safe baseline)

**In Claude Code:**
```
/nixtla-baseline-m4 demo_preset=m4_daily_small
```

This will:
- Load a small M4 Daily subset via datasetsforecast
- Run Nixtla's statsforecast models:
  - SeasonalNaive
  - AutoETS
  - AutoTheta
- Compute sMAPE and MASE
- Write outputs under the plugin directory:
  - `nixtla_baseline_m4_test/results_M4_Daily_h7.csv`
  - `nixtla_baseline_m4_test/summary_M4_Daily_h7.txt`
  - A benchmark/report Markdown file
  - A small "repro bundle" (compat info + manifest)

**Then ask Claude:**
```
Which statsforecast model performed best in that run, and why?
```

Claude will read the metrics and explain the results.

**Note:** This entire flow is offline statsforecast-only (no TimeGPT calls unless you explicitly enable them).

---

## 5. Optional: Tiny TimeGPT showdown (manual, opt-in)

If you want to see a small TimeGPT comparison:

1. Set your TimeGPT key in the environment:
   ```bash
   export NIXTLA_TIMEGPT_API_KEY="your-key-here"
   ```

2. In Claude Code, run a small showdown:
   ```
   /nixtla-baseline-m4 demo_preset=m4_daily_small include_timegpt=true timegpt_max_series=2
   ```

This will:
- Re-run the baseline on a tiny subset
- Call TimeGPT for at most 2 series
- Produce an additional "showdown" text file in the output directory comparing baselines vs TimeGPT

**If the key is not set**, the plugin just skips TimeGPT and stays fully offline.

---

## 6. What Else Is In This Repo

### Working Plugin (Production)
- **Nixtla Baseline Lab** (`plugins/nixtla-baseline-lab/`)
  - v0.8.0, fully tested
  - Golden task harness passes
  - 65%+ test coverage

### Claude Skills Pack (8 Skills, 95%+ Compliant)
- **Location:** `skills-pack/.claude/skills/`
- **Skills:**
  - `nixtla-timegpt-lab` (Mode skill - transforms Claude into Nixtla expert)
  - `nixtla-experiment-architect` (Scaffold experiments)
  - `nixtla-schema-mapper` (Map data to Nixtla formats)
  - `nixtla-timegpt-finetune-lab` (Fine-tuning guidance)
  - `nixtla-prod-pipeline-generator` (Production pipelines)
  - `nixtla-usage-optimizer` (Cost optimization)
  - `nixtla-skills-bootstrap` (Install/update skills)
  - `nixtla-skills-index` (List skills)
- **Compliance:** 95%+ ([Audit Report](000-docs/085-QA-AUDT-claude-skills-compliance-audit.md))

### Plugin Specifications (9 Complete, Ready to Build)
- **Location:** `000-docs/050-060-AT-ARCH-plugin-*.md`
- **Categories:**
  - Internal efficiency (3 plugins): Cost Optimizer, Migration Assistant, Forecast Explainer
  - Business growth (6 plugins): VS StatsForecast Benchmark, ROI Calculator, Airflow Operator, dbt Package, Snowflake Adapter, Anomaly Streaming Monitor
- **Status:** Fully specified, awaiting prioritization

### Technical Exploration (Just Added)
- **DeFi Sentinel Concept** (`000-docs/plugins/nixtla-defi-sentinel/`)
  - 6 documents exploring how TimeGPT could detect DeFi exploits
  - Inspired by Anthropic's SCONE-bench research
  - Reference implementation (not a product proposal)
  - Shows TimeGPT application in blockchain anomaly detection

---

## 7. Scope / Expectations

This repo is an experimental, community-built integration around Nixtla's OSS stack.

**It is meant to:**
- Show how Claude Code can drive statsforecast baselines and TimeGPT in a reproducible way
- Produce artifacts (metrics, reports, repro bundles) that make it easy to discuss or file issues against Nixtla repos
- Demonstrate plugin/skill patterns for the Nixtla ecosystem
- Explore high-value use cases for TimeGPT API

**It is NOT:**
- An official Nixtla product
- Production-ready for customer deployments
- Supported with SLAs or guarantees

---

## 8. Questions to Consider

After reviewing the repo, here are some questions you might have opinions on:

1. **Working Plugin:** Does Baseline Lab demonstrate enough value to justify further plugin investment?

2. **Skills Pack:** Would Nixtla benefit from officially supporting these 8 Claude Skills?

3. **Plugin Roadmap:** Of the 9 specified plugins, which 3 deliver the most value?
   - Internal efficiency vs business growth focus?
   - Quick wins vs strategic long-term plays?

4. **DeFi Sentinel:** Is blockchain/DeFi security monitoring an interesting application of TimeGPT?
   - Worth exploring further?
   - Potential enterprise customers in this space?

---

## Contact

**Prepared by:** Intent Solutions (Jeremy Longshore)
- Email: jeremy@intentsolutions.io
- Phone: 251.213.1115

**For:** Nixtla (Max Mergenthaler)
- Email: max@nixtla.io

**Repository:** https://github.com/jeremylongshore/claude-code-plugins-nixtla

---

**Last Updated:** 2025-12-02
**Version:** 1.0
