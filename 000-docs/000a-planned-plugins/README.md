# Plugins Documentation Directory

This directory contains documentation for both **implemented** and **planned** Claude Code plugins.

## Directory Structure

```
000a-planned-plugins/
├── implemented/              # Documentation for 13 working plugins
│   ├── nixtla-baseline-lab/
│   ├── nixtla-bigquery-forecaster/
│   ├── nixtla-search-to-slack/
│   ├── nixtla-airflow-operator/
│   ├── nixtla-anomaly-streaming-monitor/
│   ├── nixtla-dbt-package/
│   ├── nixtla-roi-calculator/
│   ├── nixtla-snowflake-adapter/
│   ├── nixtla-vs-statsforecast-benchmark/
│   ├── nixtla-cost-optimizer/
│   ├── nixtla-forecast-explainer/
│   ├── nixtla-migration-assistant/
│   └── nixtla-defi-sentinel/
└── external-revenue/         # Planned: 6 revenue-generating plugins
    ├── nixtla-support-deflector/
    ├── nixtla-docs-qa-generator/
    ├── nixtla-sales-demo-builder/
    ├── nixtla-forecast-workflow-templates/
    ├── nixtla-embedded-forecast-widget/
    └── nixtla-forecast-audit-report/
└── templates/                # Reusable plugin blueprints
    └── universal-validator/
```

---

## Summary

| Category | Count | Status |
|----------|-------|--------|
| **Implemented Plugins (PRD-tracked)** | 13 | Live in `005-plugins/`; the 14th (`changelog-automation`) is tracked separately under epic C0 — see note below |
| **Planned Plugins** | 6 | PRDs complete, awaiting build |
| **Templates** | 1 | Reusable blueprints |
| **Total** | 20 | (13 PRD-tracked + 1 separately-tracked + 6 planned) |

---

## Implemented Plugins (13 + 1 separate)

All implemented plugins have working code in `/005-plugins/` with full documentation. A 14th plugin, **changelog-automation**, exists in `005-plugins/` and has its own documentation at `000a-planned-plugins/changelog-automation/`. It is tracked separately because its PRD reports 0% complete despite a partial implementation on disk — that drift is reconciled by beads epic `C0` (`nixtla-xha`).

For the canonical disk-state inventory of all 14 plugins with status labels (WORKING/PARTIAL/SCAFFOLD), see `005-plugins/README.md`.

### Original Core (3)
| Plugin | Status | Description |
|--------|--------|-------------|
| **nixtla-baseline-lab** | v0.8.0 | M4 benchmark harness for statsforecast |
| **nixtla-bigquery-forecaster** | Demo | TimeGPT forecasting on BigQuery data |
| **nixtla-search-to-slack** | v0.1.0 | Search results → Slack notifications |

### Business Growth (6)
| Plugin | Status | Description |
|--------|--------|-------------|
| **nixtla-airflow-operator** | v0.1.0 | Custom Airflow operator for TimeGPT |
| **nixtla-anomaly-streaming-monitor** | v0.1.0 | Real-time anomaly detection (Kafka/Kinesis) |
| **nixtla-dbt-package** | v0.1.0 | dbt macros for SQL-first forecasting |
| **nixtla-roi-calculator** | v0.1.0 | Cost/benefit calculator for TimeGPT |
| **nixtla-snowflake-adapter** | v0.1.0 | Native Snowflake integration |
| **nixtla-vs-statsforecast-benchmark** | v0.1.0 | TimeGPT vs open source comparison |

### Internal Efficiency (3)
| Plugin | Status | Description |
|--------|--------|-------------|
| **nixtla-cost-optimizer** | v0.1.0 | API cost analysis and optimization |
| **nixtla-forecast-explainer** | v0.1.0 | Plain-language forecast explanations |
| **nixtla-migration-assistant** | v0.1.0 | Migration from pandas/scikit-learn |

### Vertical (1)
| Plugin | Status | Description |
|--------|--------|-------------|
| **nixtla-defi-sentinel** | v0.1.0 | DeFi protocol monitoring |

---

## Planned Plugins (6) - External Revenue

Six strategic plugins designed to generate direct revenue and unlock enterprise deals.

### Internal Efficiency (to be built)
| Plugin | Effort | Revenue Impact |
|--------|--------|----------------|
| **nixtla-support-deflector** | 4-6 weeks | $15-25K/mo in recovered productivity |
| **nixtla-docs-qa-generator** | 3-4 weeks | Reduced churn, faster releases |
| **nixtla-sales-demo-builder** | 3 weeks | Direct sales acceleration |

### External Revenue (to be built)
| Plugin | Effort | Revenue Impact |
|--------|--------|----------------|
| **nixtla-forecast-workflow-templates** | 6 weeks | $50-100K ARR (template sales + API) |
| **nixtla-embedded-forecast-widget** | 10-12 weeks | $200-500K ARR by Y2 |
| **nixtla-forecast-audit-report** | 8 weeks | $100-200K ARR (enterprise deals) |

---

## Planned Plugin Details

### 1. nixtla-support-deflector
**Category:** Internal Efficiency | **Effort:** 4-6 weeks

AI-powered support ticket triage using RAG over Nixtla documentation. Auto-drafts responses, detects patterns, and surfaces product insights.

- **Impact:** 50% faster response time, 30% auto-resolution rate
- **Revenue:** Indirect (engineering productivity recovery)

### 2. nixtla-docs-qa-generator
**Category:** Internal Efficiency | **Effort:** 3-4 weeks

Monitors SDK changes, generates documentation updates, and validates code examples. Prevents docs/code drift.

- **Impact:** 80% reduction in "docs wrong" tickets
- **Revenue:** Indirect (reduced churn, trust)

### 3. nixtla-sales-demo-builder
**Category:** Internal Efficiency | **Effort:** 3 weeks

Generates industry-specific demo notebooks in minutes. Retail, energy, finance, healthcare verticals with public datasets and talking points.

- **Impact:** Demo prep: 4 hours → 15 minutes
- **Revenue:** Direct (accelerates enterprise deals)

### 4. nixtla-forecast-workflow-templates
**Category:** External Revenue | **Effort:** 6 weeks

Marketplace of pre-built forecasting workflow templates ($99-499 each). Includes data connectors, scheduling, and output integrations.

- **Impact:** 3x API consumption for template users
- **Revenue:** $50-100K ARR (Y1)

### 5. nixtla-embedded-forecast-widget
**Category:** External Revenue | **Effort:** 10-12 weeks

White-label React component for SaaS companies to embed forecasting. Drop-in integration, usage-based pricing.

- **Impact:** Partner distribution multiplies reach
- **Revenue:** $200-500K ARR (Y2)

### 6. nixtla-forecast-audit-report
**Category:** External Revenue | **Effort:** 8 weeks

Automated compliance documentation (SOX, FDA, Basel III, IFRS 9). Essential for regulated industries.

- **Impact:** Unlocks blocked enterprise deals
- **Revenue:** $100-200K ARR + premium pricing justification

---

## Prioritization Matrix

| Plugin | Category | Effort | Revenue (Y1) | Priority |
|--------|----------|--------|--------------|----------|
| Sales Demo Builder | Internal | 3 weeks | Indirect | **High** |
| Workflow Templates | Revenue | 6 weeks | $50-100K | **High** |
| Audit Report | Revenue | 8 weeks | $100-200K | **High** |
| Support Deflector | Internal | 4-6 weeks | Indirect | Medium |
| Docs QA Generator | Internal | 3-4 weeks | Indirect | Medium |
| Embedded Widget | Revenue | 10-12 weeks | $200-500K | Medium |

---

## Plugin Specification Structure

Each plugin directory contains 6 standardized documents:

```
plugin-name/
├── 01-BUSINESS-CASE.md      # Value proposition, ROI
├── 02-PRD.md                # Product requirements
├── 03-ARCHITECTURE.md       # System design
├── 04-USER-JOURNEY.md       # User workflows
├── 05-TECHNICAL-SPEC.md     # API specifications
└── 06-STATUS.md             # Current status
```

---

## Related Documentation

- **Live Plugin Code**: `/005-plugins/`
- **Skills Pack**: `003-skills/.claude/skills/`
- **Repository Guide**: `/CLAUDE.md`

---

**Last Updated**: 2025-12-15
**Version**: 2.0.0 (Reorganized: 13 implemented + 6 planned)
**Maintained By**: Intent Solutions × Nixtla
