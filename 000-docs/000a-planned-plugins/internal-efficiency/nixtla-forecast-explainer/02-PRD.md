# Forecast Explainer - Product Requirements Document

**Plugin:** nixtla-forecast-explainer
**Version:** 0.1.0
**Status:** Specified
**Last Updated:** 2025-12-12

---

## Overview

Post-hoc explainability tool that transforms TimeGPT's "black box" forecasts into transparent, stakeholder-friendly narratives with visual decomposition, feature attribution, confidence bounds, and plain-English explanations. Makes forecasts auditable and boardroom-ready.

---

## Problem Statement

Enterprise blocker:
> "Risk committees and compliance teams reject foundation models as 'black boxes'. We lose enterprise deals because TimeGPT can't explain *why* it predicted X."

This plugin makes TimeGPT forecasts auditable, defensible, and boardroom-ready.

---

## Goals

1. Decompose forecasts into trend, seasonal, and residual components
2. Generate plain-English narratives explaining forecast drivers
3. Visualize confidence intervals and uncertainty
4. Create executive-ready PDF reports
5. Support compliance requirements (SOX, Basel III)

## Non-Goals

- Replace statistical model interpretability (SHAP on traditional models)
- Provide real-time explanation during inference
- Modify TimeGPT's forecasting behavior
- Generate legally binding forecast statements

---

## Target Users

| User | Need |
|------|------|
| Finance teams | Auditable forecasts for budgets |
| Risk managers | Explainability for compliance (SOX, Basel III) |
| Executives | Plain-English forecast summaries |
| Data scientists | Debug forecast behavior |

---

## Functional Requirements

### FR-1: Forecast Decomposition
- Decompose time series into trend, seasonal, residual
- Use STL decomposition or similar methods
- Handle multiple seasonality (daily, weekly, yearly)
- Visualize components separately

### FR-2: Driver Identification
- Identify key forecast drivers (trend, momentum, seasonality)
- Calculate contribution percentages for each driver
- Compare recent values to historical patterns
- Highlight unusual patterns or anomalies

### FR-3: Narrative Generation
- Generate plain-English summaries of forecasts
- Optional LLM enhancement (OpenAI/Anthropic/Google)
- Template-based fallback for offline use
- Customizable narrative styles (executive, technical)

### FR-4: Visual Report Generation
- Interactive charts with decomposition
- Confidence interval visualization
- Driver contribution bar charts
- Export to HTML, PDF, PowerPoint

### FR-5: Risk Factor Analysis
- Identify forecast risk factors
- Flag high uncertainty periods
- Detect extrapolation beyond historical range
- Warn on data quality issues

---

## Non-Functional Requirements

### NFR-1: Performance
- Explanation generation: < 30 seconds
- No additional API calls to TimeGPT required
- Works offline with StatsForecast models

### NFR-2: Accuracy
- Decomposition mathematically reproducible
- Clear documentation of methodology
- Confidence intervals properly calibrated

### NFR-3: Compliance
- Audit trail for all explanations
- Version tracking for reports
- No sensitive data in output files

---

## User Stories

### US-1: CFO Budget Justification
> "As a CFO, I want an explainable Q4 revenue forecast so I can justify budget decisions to the Board of Directors with visual evidence."

**Acceptance:**
- Run `/nixtla-explain revenue.csv --horizon 90`
- Get HTML report with decomposition charts
- See plain-English driver summary
- Export PDF for board presentation

### US-2: Compliance Audit
> "As a risk manager, I want model documentation for Basel III compliance so I can demonstrate forecast methodology to regulators."

**Acceptance:**
- Generate compliance-ready report
- Include backtesting results
- Show prediction interval coverage
- Document all assumptions

### US-3: Data Scientist Debugging
> "As a data scientist, I want to understand why TimeGPT predicted a 30% spike so I can validate if it's realistic."

**Acceptance:**
- Run `/nixtla-decompose data.csv`
- See seasonal pattern analysis
- Identify historical patterns matching prediction
- Confirm or refute forecast reasonableness

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Explanation generation time | < 30 seconds |
| Report generation success rate | 99%+ |
| User satisfaction (enterprise) | 4.5+/5.0 |
| Compliance audit pass rate | 100% |

---

## Scope

### In Scope
- Time series decomposition
- Plain-English narrative generation
- HTML/PDF/PowerPoint reports
- Confidence interval visualization
- Risk factor identification

### Out of Scope
- SHAP values for TimeGPT (model internals unavailable)
- Real-time explanation API
- Custom model interpretability
- Legal forecast disclaimers

---

## API Keys Required

```bash
# Required
NIXTLA_API_KEY=nixak-...          # For TimeGPT forecasts

# Optional (enhanced narratives)
OPENAI_API_KEY=sk-...             # LLM-powered explanations
ANTHROPIC_API_KEY=sk-ant-...      # Alternative LLM
GOOGLE_API_KEY=...                # Gemini LLM
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TIMEGPT FORECAST (Black Box)                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  forecasts = client.forecast(df, h=12)                │  │
│  │  Returns: [1250, 1340, 1420, ...]                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  FORECAST EXPLAINER (Glass Box)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Phase 1: Decomposition                               │  │
│  │  - Trend, Seasonal, Residual components               │  │
│  │                                                        │  │
│  │  Phase 2: Driver Identification                       │  │
│  │  - Historical patterns, Recent momentum               │  │
│  │                                                        │  │
│  │  Phase 3: Narrative Generation                        │  │
│  │  - Plain-English summary, Risk factors                │  │
│  │                                                        │  │
│  │  Phase 4: Visual Report                               │  │
│  │  - Charts, PDF export, PowerPoint slides              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT (Explained Forecast)                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  "Revenue is predicted to grow 12% in Q4 2025        │  │
│  │   driven by:                                          │  │
│  │   - Strong historical Q4 seasonality (+8%)           │  │
│  │   - Recent upward trend (+4%)                        │  │
│  │   - 90% confidence: $1.2M - $1.5M"                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Example Output

```
Executive Summary:

"Q4 revenue is forecasted at $2.15M, representing a 15.2% increase
 over Q3 2025. This growth is driven by three key factors:

 1. Seasonal Q4 Pattern (+8.7%): Historical data shows consistent
    Q4 revenue increases averaging 8-10% over the past 5 years.

 2. Recent Momentum (+4.2%): The last 30 days show accelerating
    growth 4.2% above the 90-day average.

 3. Product Mix Shift (+2.3%): Higher-margin products now represent
    35% of sales vs 28% last year.

 With 95% confidence, Q4 revenue will fall between $1.98M and $2.31M.

 Risk Factors:
 - Supply chain delays could reduce fulfillment capacity
 - Forecast extends 12% beyond historical maximum"
```

---

## References

- **Full Specification:** `000-docs/000b-archive-001-096/017-AT-ARCH-plugin-09-nixtla-forecast-explainer.md`
- **Category:** Internal Efficiency
- **Priority:** Tier 1 (Enterprise Conversion)
