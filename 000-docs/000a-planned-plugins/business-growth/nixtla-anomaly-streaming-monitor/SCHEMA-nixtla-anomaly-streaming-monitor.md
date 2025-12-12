# Schema: nixtla-anomaly-streaming-monitor

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Planned (Business Growth)

---

## Directory Tree (Planned)

```
nixtla-anomaly-streaming-monitor/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration (TypeScript)
├── commands/
│   └── nixtla-stream-monitor.md   # Slash command: Start monitoring
├── src/
│   ├── mcp-server/                # TypeScript MCP server
│   │   ├── index.ts               # MCP server entry
│   │   ├── kafka-consumer.ts      # Kafka stream consumer
│   │   ├── kinesis-consumer.ts    # AWS Kinesis consumer
│   │   ├── webhook-server.ts      # HTTP webhook ingestion
│   │   └── alert-engine.ts        # PagerDuty/Slack alerts
│   └── python-worker/             # Python anomaly detection
│       ├── anomaly_detector.py    # Nixtla TimeGPT integration
│       ├── batch_processor.py     # 100 events/call batching
│       └── metrics_exporter.py    # Prometheus metrics
├── config/
│   ├── grafana_dashboard.json     # Grafana dashboard template
│   └── prometheus_rules.yml       # Alert rules
├── tests/
│   ├── test_kafka_consumer.ts
│   └── test_anomaly_detector.py
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (Planned plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-anomaly-streaming-monitor | Required |
| description | Real-time streaming anomaly detection... | Required |
| version | 0.1.0 | Required |
| author.name | Intent Solutions | Required |

---

## MCP Tools (6 planned)

| Tool Name | Purpose |
|-----------|---------|
| stream_monitor_start | Start monitoring a stream |
| stream_monitor_stop | Stop monitoring |
| stream_health_check | Check consumer health |
| configure_alerts | Set up alerting rules |
| get_anomaly_stats | Get real-time statistics |
| export_dashboard_config | Generate Grafana dashboard |

---

## Stream Sources Supported

| Source | Technology | Status |
|--------|------------|--------|
| Kafka | node-rdkafka | Phase 1 |
| AWS Kinesis | aws-sdk | Phase 1 |
| HTTP Webhooks | Express.js | Phase 1 |
| Google Pub/Sub | @google-cloud/pubsub | Phase 2 |

---

## Alert Channels

| Channel | Integration |
|---------|-------------|
| PagerDuty | REST API |
| Slack | Webhook |
| Email | SMTP |
| SMS | Twilio (optional) |

---

## Architecture (Hybrid)

| Component | Language | Purpose |
|-----------|----------|---------|
| MCP Server | TypeScript | Stream processing, alerting |
| Anomaly Worker | Python | Nixtla API calls, detection |
| Cache | Redis | Distributed result caching |
| Metrics | Prometheus | Observability export |

---

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Processing latency | <1 second |
| Throughput | 10,000+ events/sec |
| Memory usage | <2GB |
| Anomaly accuracy | >95% |
| False positive rate | <5% |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** FinTech teams, SRE teams, E-commerce, IoT platforms
- **What:** Real-time streaming anomaly detection for Kafka/Kinesis
- **When:** Payment fraud, infrastructure monitoring, sensor streams
- **Target Goal:** Detect anomaly within 30 seconds of occurrence
- **Production:** false (planned-business-growth)
