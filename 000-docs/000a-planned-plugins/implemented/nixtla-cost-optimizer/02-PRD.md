# Cost Optimizer - Product Requirements Document

**Plugin:** nixtla-cost-optimizer
**Version:** 0.1.0
**Status:** Specified
**Last Updated:** 2025-12-12

---

## Overview

Intelligent cost optimization system for Nixtla TimeGPT API usage. Analyzes usage patterns, detects redundant forecasts, implements intelligent caching, and provides actionable cost-saving recommendations.

---

## Problem Statement

Bill shock leads to immediate churn:
> "10,000 SKUs × 24 hours × 30 days = 7.2 million forecasts/month. An intern sets a cron job to run every minute instead of every hour. The company receives a massive bill. Reaction: 'Cancel this service immediately.'"

This plugin prevents that.

---

## Goals

1. Detect and eliminate redundant forecasts (identical data re-forecasted)
2. Implement intelligent caching with configurable TTL
3. Identify over-forecasting (hourly when daily suffices)
4. Flag dormant series still consuming API calls
5. Provide cost spike investigation and root cause analysis
6. Achieve 45-63% typical cost reduction

## Non-Goals

- Replace Nixtla's billing system
- Modify actual forecasting behavior
- Guarantee specific savings percentages
- Handle non-Nixtla forecasting costs

---

## Target Users

| User | Need |
|------|------|
| Enterprise customers | Scale TimeGPT without bill shock |
| Data engineering teams | Optimize forecast workflows |
| FinOps teams | Control cloud spend |
| Nixtla CRO | Reduce churn from cost complaints |

---

## Functional Requirements

### FR-1: Usage Pattern Analysis
- Import 30 days of usage logs from Nixtla Billing API
- Hash all input datasets (SHA256) for comparison
- Store in SQLite database for trend analysis
- Track cost per series, per model, per time period

### FR-2: Redundancy Detection
- Identify identical forecasts (95%+ similarity threshold)
- Detect stale data (unchanged for >24 hours)
- Find unnecessary frequency (minutely/hourly when daily suffices)
- Flag dormant series (zero activity 90+ days)

### FR-3: Caching Recommendations
- Generate TTL recommendations per series based on volatility
- Classify series: Critical (no cache), Important (1h TTL), Standard (24h TTL)
- Calculate projected savings for each recommendation
- Mark safe vs. requires-approval recommendations

### FR-4: Cost Spike Investigation
- Compare current month vs previous month
- Identify root cause (script, user, timestamp)
- Provide immediate fix recommendations
- Generate incident reports

### FR-5: Report Generation
- Console output (real-time summary)
- JSON export (programmatic access)
- CSV export (spreadsheet analysis)
- PDF executive summary
- Slack alerts (configurable threshold)

### FR-6: MCP Server Tools
Expose 6 tools to Claude Code:
1. `analyze_usage` - Import and analyze historical usage
2. `detect_redundancy` - Find duplicate/redundant forecasts
3. `generate_recommendations` - Create cost-saving recommendations
4. `apply_caching_rules` - Apply approved caching configurations
5. `get_cost_snapshot` - Retrieve cost summary for date range
6. `export_report` - Export analysis to CSV/JSON/PDF

---

## Non-Functional Requirements

### NFR-1: Performance
- Analysis speed: 245,000 records in ~42 seconds
- Memory usage: ~200MB for 30 days of data
- Database size: ~50MB per month of history

### NFR-2: Dependencies
- Python 3.10+
- SQLite (local database)
- Nixtla API key (required)
- Nixtla Billing API key (optional, enhanced data)

### NFR-3: Security
- API keys stored in `.env` file (not committed)
- Sensitive cost data never logged to console
- No PII in exported reports (series IDs only)

---

## User Stories

### US-1: Monthly Cost Audit
> "As a data engineering manager, I want to run monthly cost audits so I can understand where money is going and identify savings opportunities."

**Acceptance:**
- Run `/nixtla-optimize` and receive comprehensive report
- See top 10 cost offenders with specific recommendations
- Export detailed CSV for FinOps review

### US-2: Bill Shock Investigation
> "As a DevOps engineer, I want to investigate cost spikes so I can fix the root cause and prevent recurrence."

**Acceptance:**
- Run `/nixtla-optimize --spike-detection`
- Identify exact script/user/timestamp causing spike
- Receive immediate fix recommendation
- Generate incident report for team

### US-3: Pre-Scale Optimization
> "As a VP of Data Science, I want to optimize before scaling 10x so I don't get 10x costs."

**Acceptance:**
- Run cost projection for 10x scale
- Receive tiered caching strategy
- Implementation plan with timeline
- Projected costs with vs. without optimization

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Typical cost reduction | 45-63% |
| Cache hit rate (post-optimization) | 60%+ |
| Analysis time (30 days data) | <60 seconds |
| Time to identify bill shock root cause | <15 minutes |

---

## Scope

### In Scope
- Nixtla TimeGPT API cost analysis
- Redundancy detection and elimination
- Intelligent caching recommendations
- Cost spike investigation
- Slack/PagerDuty alert integration
- SQLite local database

### Out of Scope
- StatsForecast costs (open source, no API)
- Other cloud provider costs
- Real-time cost prevention (monitoring only)
- Automatic script modification without approval

---

## API Keys Required

```bash
# Required
NIXTLA_API_KEY=nixak-...          # TimeGPT API access

# Optional (enhanced features)
NIXTLA_BILLING_API_KEY=...        # Detailed billing data
SLACK_WEBHOOK_URL=...             # Cost alerts
PAGERDUTY_API_KEY=...             # Critical alerts (>$5k spike)
GCP_PROJECT_ID=...                # BigQuery integration
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  USER INTERFACE                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ /optimize    │  │ Agent Skill  │  │  MCP Server     │  │
│  │ /cost-report │  │ (Auto-invoke)│  │  (6 tools)      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  CORE LOGIC                                                 │
│  - Usage pattern detection                                  │
│  - Redundancy analysis                                      │
│  - Caching recommendations                                  │
│  - Cost projection modeling                                 │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │  SQLite DB  │  │  JSON Cache │  │  Nixtla API      │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## References

- **Full Specification:** `000-docs/000b-archive-001-096/009-AT-ARCH-plugin-01-nixtla-cost-optimizer.md`
- **Category:** Internal Efficiency
- **Priority:** Tier 1 (Immediate Value)
