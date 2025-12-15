# Schema: nixtla-cost-optimizer

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Planned (Internal Efficiency)

---

## Directory Tree (Planned)

```
nixtla-cost-optimizer/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   ├── nixtla-optimize.md         # Slash command: Run cost audit
│   └── nixtla-cost-report.md      # Slash command: Generate report
├── scripts/
│   ├── cost_optimizer_mcp.py      # MCP server (6 tools exposed)
│   ├── usage_analyzer.py          # Usage pattern analysis
│   ├── redundancy_detector.py     # Duplicate forecast detection
│   ├── cache_recommender.py       # TTL recommendations
│   └── requirements.txt           # Python dependencies
├── skills/
│   └── nixtla-cost-analyst/
│       └── SKILL.md               # AI skill for cost analysis
├── data/
│   └── usage.db                   # SQLite usage database
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (Planned plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-cost-optimizer | Required |
| description | Intelligent cost optimization for TimeGPT API... | Required |
| version | 0.1.0 | Required |
| author.name | Intent Solutions | Required |

---

## MCP Tools (6 planned)

| Tool Name | Purpose |
|-----------|---------|
| analyze_usage | Import and analyze 30 days of usage |
| detect_redundancy | Find duplicate/redundant forecasts |
| generate_recommendations | Create cost-saving recommendations |
| apply_caching_rules | Apply approved caching configs |
| get_cost_snapshot | Retrieve cost summary for date range |
| export_report | Export analysis to CSV/JSON/PDF |

---

## Slash Commands (2 planned)

| Command | Purpose |
|---------|---------|
| /nixtla-optimize | Run comprehensive cost audit |
| /nixtla-cost-report | Generate executive cost report |

---

## Cost Reduction Targets

| Optimization | Expected Savings |
|--------------|------------------|
| Redundant forecast elimination | 20-30% |
| Intelligent caching (TTL) | 15-25% |
| Frequency optimization | 10-15% |
| Dormant series cleanup | 5-10% |
| **Total typical reduction** | **45-63%** |

---

## Cache Classification

| Class | TTL | Description |
|-------|-----|-------------|
| Critical | 0 | No caching (real-time required) |
| Important | 1h | Low-latency requirements |
| Standard | 24h | Daily refresh sufficient |
| Stable | 7d | Slow-changing series |

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Analysis speed | 245K records in ~42s |
| Memory usage | ~200MB for 30 days |
| Database size | ~50MB per month |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Cost management teams
- **What:** Forecast cloud costs and recommend optimizations
- **When:** Reduce cloud spend, predict overruns
- **Target Goal:** Generate cost forecast and optimization recommendations
- **Production:** false (planned-internal-efficiency)
