# ROI Calculator - Product Requirements Document

**Plugin:** nixtla-roi-calculator
**Version:** 0.1.0
**Status:** Specified
**Last Updated:** 2025-12-12

---

## Overview

Enterprise ROI calculator that quantifies TimeGPT value vs. building in-house forecasting infrastructure. Generates comprehensive financial analysis with build-vs-buy scenarios, executive summaries, and Salesforce-ready ROI documentation.

---

## Problem Statement

Sales cycle friction:
> "Enterprise buyers need 3-6 months to evaluate build vs. buy decisions. By the time they decide, the champion has moved on or budget is gone."

This plugin provides instant ROI quantification to accelerate enterprise sales cycles.

---

## Goals

1. Quantify TimeGPT ROI vs. build-in-house (5-year TCO analysis)
2. Generate executive-ready PDF ROI reports
3. Provide Salesforce-ready documentation for sales teams
4. Compare against common alternatives (Prophet, in-house ML teams)
5. Calculate break-even point and payback period

## Non-Goals

- Replace detailed vendor evaluation processes
- Provide binding financial commitments
- Handle non-forecasting cost comparisons
- Generate legal procurement documents

---

## Target Users

| User | Need |
|------|------|
| Enterprise sales | Accelerate deal closure with quantified ROI |
| VP Data Science | Justify API budget to CFO |
| Finance teams | Build vs. buy analysis for procurement |
| Solution architects | Technical cost comparison |

---

## Functional Requirements

### FR-1: Cost Input Collection
- Collect current infrastructure costs (compute, storage, personnel)
- Capture forecasting volume (series count, frequency, horizon)
- Gather team composition (data scientists, ML engineers)
- Record existing tool costs (licenses, cloud services)

### FR-2: ROI Calculation Engine
- Calculate 5-year TCO for build-in-house scenario
- Calculate 5-year TCO for TimeGPT API scenario
- Include hidden costs (maintenance, upgrades, hiring)
- Factor in opportunity cost of delayed time-to-value
- Generate sensitivity analysis for key assumptions

### FR-3: Report Generation
- Executive summary (1-page PDF)
- Detailed financial analysis (multi-page PDF)
- Salesforce-ready opportunity documentation
- PowerPoint slides for stakeholder presentations

### FR-4: Comparison Scenarios
- TimeGPT vs. Prophet (open source)
- TimeGPT vs. in-house ML team
- TimeGPT vs. existing vendor
- Hybrid scenarios (StatsForecast + TimeGPT)

### FR-5: MCP Server Tools
Expose 4 tools to Claude Code:
1. `calculate_roi` - Run ROI calculation with inputs
2. `generate_report` - Create PDF/PowerPoint report
3. `compare_scenarios` - Compare multiple approaches
4. `export_salesforce` - Export to Salesforce format

---

## Non-Functional Requirements

### NFR-1: Performance
- ROI calculation: < 5 seconds
- Report generation: < 30 seconds
- No external API dependencies (offline capable)

### NFR-2: Accuracy
- Use industry-standard cost benchmarks
- Clearly document all assumptions
- Provide sensitivity analysis for key variables

### NFR-3: Security
- No sensitive financial data stored
- Reports generated locally
- No data transmitted to third parties

---

## User Stories

### US-1: Sales Deal Acceleration
> "As an enterprise sales rep, I want to generate an ROI report during the first call so I can differentiate from competitors still doing manual proposals."

**Acceptance:**
- Run `/nixtla-roi` with basic inputs
- Generate executive summary in < 1 minute
- Email-ready PDF with company branding option

### US-2: Budget Justification
> "As a VP of Data Science, I want to show my CFO the 5-year TCO comparison so I can get budget approval without a 6-month evaluation."

**Acceptance:**
- Detailed financial breakdown
- Clear assumptions documented
- Sensitivity analysis showing best/worst case

### US-3: Procurement Support
> "As a procurement manager, I want standardized vendor comparison documentation so I can satisfy our evaluation requirements."

**Acceptance:**
- Side-by-side cost comparison table
- Risk assessment for each option
- Implementation timeline estimates

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Time to generate ROI report | < 2 minutes |
| Sales cycle reduction | 30-50% |
| Report accuracy (vs manual analysis) | 95%+ |
| User satisfaction (sales teams) | 4.5+/5.0 |

---

## Scope

### In Scope
- TimeGPT API cost modeling
- Build-in-house cost estimation
- Open source alternative comparison
- PDF/PowerPoint report generation
- Salesforce integration export

### Out of Scope
- Real-time pricing updates from Nixtla
- Integration with customer financial systems
- Binding cost commitments
- Legal contract generation

---

## API Keys Required

```bash
# Required
NIXTLA_API_KEY=nixak-...          # For pricing tier lookup

# Optional (enhanced reports)
OPENAI_API_KEY=sk-...             # AI-generated executive summaries
COMPANY_LOGO_PATH=/path/to/logo   # Custom branding
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  USER INTERFACE                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ /nixtla-roi  │  │ Agent Skill  │  │  MCP Server     │  │
│  │              │  │ (Auto-invoke)│  │  (4 tools)      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  CORE LOGIC (Python)                                        │
│  - Cost modeling engine                                     │
│  - Scenario comparison                                      │
│  - Report generation (ReportLab/python-pptx)               │
│  - Salesforce export                                        │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │  Cost       │  │  Industry   │  │  Report          │   │
│  │  Models     │  │  Benchmarks │  │  Templates       │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## References

- **Full Specification:** `000-docs/000b-archive-001-096/011-AT-ARCH-plugin-03-nixtla-roi-calculator.md`
- **Category:** Business Growth
- **Priority:** Tier 1 (Enterprise Conversion)
