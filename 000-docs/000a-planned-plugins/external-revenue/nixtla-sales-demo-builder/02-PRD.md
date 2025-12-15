# Sales Demo Builder - Product Requirements Document

**Plugin:** nixtla-sales-demo-builder
**Version:** 0.1.0
**Status:** Planned
**Last Updated:** 2025-12-15

---

## Overview

A plugin that generates industry-specific demo notebooks in minutes. Input a prospect's vertical (retail, energy, finance, healthcare), and the plugin produces a Jupyter notebook with relevant public datasets, compelling visualizations, and talking points.

---

## Problem Statement

Sales cycles for enterprise forecasting deals are long because prospects need to see TimeGPT work on data relevant to their industry. Generic demos don't resonate. Creating custom demos takes engineering time away from product work.

---

## Goals

1. Pre-built demo structures for retail (M5), energy (load forecasting), finance (stock/crypto), healthcare (patient volume)
2. Curated public datasets mapped to verticals, ready to download
3. Input prospect name, use case, and data characteristics to personalize notebook
4. Generate markdown cells with sales narrative tailored to vertical
5. Side-by-side TimeGPT vs Prophet vs ARIMA comparison to prove value

## Non-Goals

- Handle prospect's actual data (privacy/security concerns)
- Replace sales team judgment
- Generate pricing proposals

---

## Target Users

| User | Need |
|------|------|
| Sales representatives | Quick, compelling demos |
| Solutions engineers | Technical proof-of-value |
| Account executives | Industry-specific pitches |
| Pre-sales team | Standardized demo quality |

---

## Functional Requirements

### FR-1: Vertical Templates
- Retail demand planning (M5 dataset)
- Energy load forecasting (public utility data)
- Finance (Yahoo Finance, crypto APIs)
- Healthcare (patient volume, CDC data)
- Supply chain (shipping/logistics)

### FR-2: Public Dataset Library
- Curated datasets per vertical
- JSON manifest with download URLs, schemas
- Pre-validated data quality
- License information included

### FR-3: Dynamic Customization
- Input: prospect name, company, use case
- Personalize notebook title and narrative
- Adapt data selection to prospect's industry segment
- Include company logo placeholder

### FR-4: Talking Points Generation
- Sales narrative in markdown cells
- Key value propositions per vertical
- Objection handling guidance
- Call-to-action cells

### FR-5: Comparison Mode
- TimeGPT vs Prophet vs ARIMA
- Accuracy metrics (MAPE, RMSE, MAE)
- Training time comparison
- Ease-of-use comparison

### FR-6: MCP Server Tools
Expose 5 tools to Claude Code:
1. `list_verticals` - Get available industry templates
2. `generate_demo` - Create customized notebook
3. `list_datasets` - Browse available public datasets
4. `add_comparison` - Add model comparison section
5. `export_notebook` - Export to .ipynb or HTML

---

## Non-Functional Requirements

### NFR-1: Performance
- Notebook generation: <30 seconds
- Dataset download: <60 seconds for typical size
- HTML export: <10 seconds

### NFR-2: Dependencies
- Python 3.10+
- Jupyter/nbformat for notebook generation
- pandas, matplotlib for visualizations
- nixtla, statsforecast for forecasting

### NFR-3: Quality
- All generated notebooks must execute without errors
- Visualizations render correctly
- Narrative is grammatically correct

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Demo prep time | 4 hours → 15 minutes |
| Sales cycle reduction | 20% |
| Win rate increase | 10% |
| Demo satisfaction score | 9/10 |

---

## Template Examples

### Retail Demand Planning
- Dataset: M5 Competition data (Walmart)
- Use case: SKU-level demand forecasting
- Narrative: "Reduce stockouts by 30%, cut overstock by 25%"
- Comparison: TimeGPT vs Walmart's baseline models

### Energy Load Forecasting
- Dataset: Public utility load data
- Use case: Grid demand prediction
- Narrative: "Optimize generation scheduling, reduce peak costs"
- Comparison: TimeGPT vs traditional ARIMA

### Financial Forecasting
- Dataset: Yahoo Finance stock data
- Use case: Revenue/price prediction
- Narrative: "Improve forecast accuracy for planning"
- Comparison: TimeGPT vs Prophet

### Healthcare Capacity
- Dataset: CDC patient volume data
- Use case: Hospital capacity planning
- Narrative: "Right-size staffing, reduce wait times"
- Comparison: TimeGPT vs simple baselines

---

## Scope

### In Scope
- 5 industry verticals
- Public datasets only
- Jupyter notebook generation
- Model comparison
- Sales narrative

### Out of Scope
- Prospect's proprietary data
- Pricing/quoting
- Contract generation
- CRM integration

---

## Technical Approach

- **Notebook Templates**: Jinja2 templates for each vertical with placeholder variables
- **Dataset Registry**: JSON manifest of public datasets with vertical tags, download URLs, schema info
- **Claude Skill**: Generate custom narrative sections and adapt code to prospect specifics
- **MCP Tool**: Single command to generate complete notebook: `/nixtla-demo --vertical=retail --prospect="Acme Corp"`

---

## Estimated Effort

3 weeks for core template system + 3 verticals. Additional 1 week per vertical.

---

## Revenue Impact

Direct. Accelerates sales pipeline, improves conversion. Each enterprise deal worth $50K-500K ARR.
