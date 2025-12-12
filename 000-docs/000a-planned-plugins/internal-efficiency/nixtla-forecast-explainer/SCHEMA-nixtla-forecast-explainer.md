# Schema: nixtla-forecast-explainer

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Planned (Internal Efficiency)

---

## Directory Tree (Planned)

```
nixtla-forecast-explainer/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   ├── nixtla-explain.md          # Slash command: Generate explanation
│   └── nixtla-decompose.md        # Slash command: Time series decomposition
├── scripts/
│   ├── explainer_mcp.py           # MCP server (5 tools exposed)
│   ├── decomposition.py           # STL decomposition engine
│   ├── driver_identifier.py       # Trend/seasonal driver analysis
│   ├── narrative_generator.py     # Plain-English narrative
│   ├── report_generator.py        # PDF/HTML/PPTX export
│   └── requirements.txt           # Python dependencies
├── templates/
│   ├── executive_summary.html     # Board-ready template
│   ├── technical_analysis.html    # Data science template
│   └── compliance_report.html     # SOX/Basel III template
├── skills/
│   └── nixtla-explain-analyst/
│       └── SKILL.md               # AI skill for interpretation
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (Planned plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-forecast-explainer | Required |
| description | Post-hoc explainability for TimeGPT forecasts... | Required |
| version | 0.1.0 | Required |
| author.name | Intent Solutions | Required |

---

## MCP Tools (5 planned)

| Tool Name | Purpose |
|-----------|---------|
| decompose_forecast | STL decomposition (trend/seasonal/residual) |
| identify_drivers | Calculate contribution percentages |
| generate_narrative | Plain-English explanation |
| generate_report | PDF/HTML/PPTX export |
| assess_risk_factors | Flag high uncertainty periods |

---

## Slash Commands (2 planned)

| Command | Purpose |
|---------|---------|
| /nixtla-explain | Generate full explanation report |
| /nixtla-decompose | Time series decomposition only |

---

## Decomposition Components

| Component | Description |
|-----------|-------------|
| Trend | Long-term directional movement |
| Seasonal | Repeating patterns (daily/weekly/yearly) |
| Residual | Unexplained variation |

---

## Driver Identification

| Driver | Calculation |
|--------|-------------|
| Trend contribution | % of forecast from trend |
| Seasonal contribution | % from recurring patterns |
| Recent momentum | Deviation from 90-day average |
| External factors | Exogenous variable impact |

---

## Report Formats

| Format | Use Case |
|--------|----------|
| HTML Interactive | Dashboard embedding |
| PDF Executive | Board presentations |
| PowerPoint | Stakeholder meetings |
| Markdown | Technical documentation |

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

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Explanation generation | <30 seconds |
| Report generation | <60 seconds |
| Audit pass rate | 100% |
| User satisfaction (enterprise) | 4.5+/5.0 |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Business analysts, non-technical users
- **What:** Generate plain-English explanations of forecast results
- **When:** Communicate forecasts to business teams
- **Target Goal:** Generate explanation readable by non-technical user
- **Production:** false (planned-internal-efficiency)
