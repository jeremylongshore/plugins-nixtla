# Schema: nixtla-roi-calculator

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Planned (Business Growth)

---

## Directory Tree (Planned)

```
nixtla-roi-calculator/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   └── nixtla-roi.md              # Slash command: Calculate ROI
├── scripts/
│   ├── roi_calculator_mcp.py      # MCP server (4 tools exposed)
│   ├── cost_modeler.py            # TCO calculation engine
│   ├── report_generator.py        # PDF/PPT generation
│   └── requirements.txt           # Python dependencies
├── templates/
│   ├── executive_summary.html     # 1-page executive template
│   ├── detailed_analysis.html     # Multi-page analysis template
│   └── salesforce_export.json     # Salesforce opportunity format
├── data/
│   └── industry_benchmarks.json   # Standard cost benchmarks
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (Planned plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-roi-calculator | Required |
| description | Enterprise ROI calculator for TimeGPT value... | Required |
| version | 0.1.0 | Required |
| author.name | Intent Solutions | Required |

---

## MCP Tools (4 planned)

| Tool Name | Purpose |
|-----------|---------|
| calculate_roi | Run ROI calculation with inputs |
| generate_report | Create PDF/PowerPoint report |
| compare_scenarios | Compare build vs buy approaches |
| export_salesforce | Export to Salesforce format |

---

## Slash Commands (1 planned)

| Command | Purpose |
|---------|---------|
| /nixtla-roi | Start ROI calculation wizard |

---

## Comparison Scenarios

| Scenario | Description |
|----------|-------------|
| TimeGPT vs Prophet | Open source comparison |
| TimeGPT vs In-house ML | Build vs buy analysis |
| TimeGPT vs Existing Vendor | Vendor switching ROI |
| Hybrid (SF + TimeGPT) | StatsForecast + API combo |

---

## Report Outputs

| Format | Use Case |
|--------|----------|
| PDF Executive Summary | C-level presentations |
| PDF Detailed Analysis | Procurement evaluation |
| PowerPoint Slides | Stakeholder meetings |
| Salesforce Export | CRM opportunity docs |

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| ROI calculation | <5 seconds |
| Report generation | <30 seconds |
| Offline capable | Yes (no external API) |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Sales teams, finance
- **What:** Interactive calculator for TimeGPT ROI estimation
- **When:** Sales demos, business case validation
- **Target Goal:** Generate ROI estimate from user inputs in <2 seconds
- **Production:** false (planned-business-growth)
