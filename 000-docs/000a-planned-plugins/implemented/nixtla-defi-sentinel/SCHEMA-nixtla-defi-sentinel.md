# Schema: nixtla-defi-sentinel

**Generated:** 2025-12-12
**Plugin Version:** 1.0
**Status:** Planned (Vertical DeFi)

---

## Directory Tree (Planned)

```
nixtla-defi-sentinel/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   └── nixtla-defi-sentinel.md    # Slash command: Monitor contracts
├── scripts/
│   ├── defi_sentinel_mcp.py       # MCP server (5 tools exposed)
│   ├── blockchain_monitor.py      # Real-time blockchain data ingestion
│   ├── anomaly_detector.py        # TimeGPT anomaly detection
│   ├── alert_dispatcher.py        # Multi-channel alert system
│   └── requirements.txt           # Python dependencies
├── skills/
│   └── nixtla-defi-analyst/
│       └── SKILL.md               # AI skill for anomaly interpretation
├── tests/
│   ├── test_anomaly_detection.py  # Anomaly detection tests
│   └── test_alerts.py             # Alert delivery tests
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (Planned plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-defi-sentinel | Required |
| description | AI-powered DeFi security monitoring... | Required |
| version | 1.0.0 | Required |
| author.name | Intent Solutions | Required |
| keywords | defi, security, anomaly, blockchain, timegpt | Optional |

---

## MCP Tools (5 planned)

| Tool Name | Purpose |
|-----------|---------|
| monitor_contract | Add contract to monitoring (address, chain) |
| get_contract_status | Get health status and recent anomalies |
| list_monitored_contracts | List all monitored contracts |
| get_recent_alerts | Retrieve recent alert history |
| forecast_contract_metrics | Predict TVL/volume (24hr horizon) |

---

## Slash Commands (1 planned)

| Command | Purpose |
|---------|---------|
| /nixtla-defi-sentinel | Start contract monitoring wizard |

---

## Supported Blockchains

| Chain | Phase | Support Level |
|-------|-------|---------------|
| Ethereum | Phase 1 | Full |
| BSC | Phase 1 | Full |
| Base | Phase 2 | Full |
| Polygon | Phase 3 | Planned |
| Arbitrum | Phase 3 | Planned |
| Optimism | Phase 3 | Planned |

---

## Anomaly Types Detected

| Type | Threshold | Severity |
|------|-----------|----------|
| TVL Drop | >10% in 1 block | Critical |
| Tx Volume Spike | >3 std dev | High |
| Gas Pattern Anomaly | Unusual consumption | Medium |
| Function Call Sequence | Abnormal patterns | High |
| Large Transfer | >$1M to new address | Critical |

---

## Alert Channels

| Channel | Status |
|---------|--------|
| Slack webhook | Planned |
| Discord webhook | Planned |
| Email | Planned |
| SMS (Twilio) | Planned |
| PagerDuty | Phase 2 |

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Detection latency | <30 seconds |
| Alert delivery | <5 seconds |
| False positive rate | <5% |
| True positive rate | >70% |
| System uptime | 99.5% |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** DeFi security teams, crypto traders
- **What:** Anomaly detection on blockchain metrics for exploit detection
- **When:** Monitor TVL, gas patterns
- **Target Goal:** Detect anomaly in blockchain data stream
- **Production:** false (planned-vertical-defi)
