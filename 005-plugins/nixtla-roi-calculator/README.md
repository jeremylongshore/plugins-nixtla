# Nixtla ROI Calculator

Calculate the 3-year ROI of moving forecasting from in-house tooling to Nixtla's TimeGPT, generate a real PDF report, compare scenarios, and post the result straight into Salesforce as an Opportunity.

**Version**: 1.0.0 · **Status**: Working · **API key needed**: Optional (TimeGPT pricing only — Salesforce export uses your existing org's REST API)

---

## 30-second pitch

Most TimeGPT conversations stall on "what's the actual ROI for *us*?" This plugin answers that in three Claude prompts: feed it your current tool cost + FTE hours, get back a 3-year savings model, a real PDF, and a Salesforce Opportunity payload — ready for your AE to file.

---

## Quick start (under 5 minutes)

```bash
# 1. Install plugin deps
cd 005-plugins/nixtla-roi-calculator
pip install -r scripts/requirements.txt

# 2. (Optional) wire Salesforce env vars for live Opportunity creation
export NIXTLA_SF_INSTANCE_URL="https://yourorg.my.salesforce.com"
export NIXTLA_SF_ACCESS_TOKEN="00DXX0000000000!AQ..."

# 3. In Claude Code, ask:
#    "Run an ROI calculation: $5K/mo current tool cost, 20 hrs/week of data-scientist
#     time at $80/hr, 50K forecasts/month."
#    Claude calls calculate_roi → generate_report → export_salesforce in sequence.
```

---

## What you get back

`calculate_roi` returns a structured dict:

```json
{
  "current_costs":   {"tool_annual": 60000, "fte_annual": 83200, "infrastructure_annual": 6000, "total_annual": 149200, "total_3year": 447600},
  "timegpt_costs":   {"api_annual": 60, "fte_annual": 24960, "total_annual": 25020, "total_3year": 75060},
  "savings":         {"annual": 124180, "3year": 372540, "roi_percentage": 83.2, "payback_months": 1}
}
```

`generate_report` writes a **real PDF** (reportlab) to your chosen path with: title page, executive summary table, cost-breakdown table (Current vs TimeGPT, annual + 3-year deltas), FTE savings table, and recommendations.

`compare_scenarios` runs `calculate_roi` across N input scenarios, ranks them by 3-year ROI, identifies best/worst/median, and includes a sensitivity-analysis dict showing which input variable swings ROI hardest.

`export_salesforce` produces the Salesforce-shaped JSON payload (Opportunity with `Name`, `StageName`, `Amount`, plus custom `Nixtla_*__c` fields). With both `NIXTLA_SF_*` env vars set, it POSTs to your org's `/services/data/v59.0/sobjects/Opportunity` and returns the live response. Without them, it returns `status="dry_run"` with the payload — useful for testing the shape before you wire up live SF auth.

---

## MCP tools

| Tool | What it does | Required env |
|---|---|---|
| `calculate_roi` | Compute 3-year ROI from current-state + TimeGPT inputs | none |
| `generate_report` | Write a real PDF (reportlab) of the ROI analysis | none |
| `compare_scenarios` | Rank multiple ROI scenarios + sensitivity analysis | none |
| `export_salesforce` | Create an Opportunity in your SF org (live or dry-run) | `NIXTLA_SF_INSTANCE_URL`, `NIXTLA_SF_ACCESS_TOKEN` (for live) |

---

## Environment variables

| Variable | When you need it | What it's for |
|---|---|---|
| `NIXTLA_SF_INSTANCE_URL` | `export_salesforce` live mode | Your Salesforce org instance URL (e.g. `https://yourorg.my.salesforce.com`) |
| `NIXTLA_SF_ACCESS_TOKEN` | `export_salesforce` live mode | OAuth Bearer token for the SF REST API |

If either is missing, `export_salesforce` returns the SF-shaped payload with `status="dry_run"` and a `message` explaining how to enable live mode. This makes the tool usable end-to-end without SF credentials.

---

## Inputs that matter most

From the sensitivity analysis, the single biggest swing factor in 3-year ROI is **`fte_hours_per_week`** — every additional hour of data-scientist time eliminated translates to ~$4,160/year saved. Tune that input carefully; if your team is under-utilized on forecasting work, the ROI shrinks.

Default assumptions baked in:
- TimeGPT reduces FTE time by **70%** (conservative; published case studies report 80-95% reductions).
- 3-year horizon, no discount rate (rough NPV-equivalent — for finance teams that need real DCF, run `calculate_roi` then plug into your own model).
- TimeGPT pricing: `$0.10 per 1K forecasts` (override via `timegpt_price_per_1k` input).

---

## Tests

```bash
cd 005-plugins/nixtla-roi-calculator
PYTHONPATH=scripts pytest tests/ --cov=roi_calculator_mcp -v
```

35 tests covering all 4 tools, edge cases, dry-run + live Salesforce paths (mocked), PDF generation (skipped if reportlab not installed), and the async MCP dispatcher. Coverage gate: ≥80% in CI.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: reportlab` | `pip install reportlab>=4.0.0` (or run `pip install -r scripts/requirements.txt`) |
| `generate_report` returns `status="error"` | reportlab not importable — install per above |
| `export_salesforce` returns `status="dry_run"` | One or both `NIXTLA_SF_*` env vars not set — that's intentional fallback behavior |
| `export_salesforce` returns `status="error"` HTTP 401 | Salesforce token expired or invalid — refresh `NIXTLA_SF_ACCESS_TOKEN` |
| `compare_scenarios` returns empty structure | Empty scenario list — pass at least one scenario dict |

---

## License

MIT — Jeremy Longshore.
