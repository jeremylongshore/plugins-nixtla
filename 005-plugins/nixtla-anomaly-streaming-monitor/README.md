# Nixtla Anomaly Streaming Monitor

> ⚠️ **PROOF OF CONCEPT — not for production use.** This plugin demonstrates an anomaly-detection API surface for streaming protocol metrics (Kafka / AWS Kinesis / HTTP webhooks). All MCP tools currently return **illustrative fixtures** — not live consumer data. Production deployment is a multi-week build (real consumers, alert delivery, observability) — see *What's real vs PoC* below.

**Version**: 1.0.0-poc · **Status**: Proof of Concept · **API key needed**: None for the PoC; production would need Nixtla API + broker creds + alert webhook tokens

---

## Origin

This plugin sketches what real-time TimeGPT-powered anomaly detection could look like for a streaming pipeline. The design demonstrates the API a SRE / platform team would use: start a monitor on a Kafka topic, get health checks, configure alerting, query stats. The PoC fixes the API surface — production code can drop in behind these tool signatures without breaking callers.

---

## What's real vs PoC

Every tool currently returns a fixture with a `_disclaimer` field making the PoC status explicit. Production deployment requires real work in three layers:

| MCP tool | What's there now | What production would need |
|---|---|---|
| `stream_monitor_start` | Returns a generated `monitor_id` + the requested config | Real Kafka consumer (kafkajs) or Kinesis consumer (@aws-sdk/client-kinesis) bound to a worker pool; persistent monitor state |
| `stream_monitor_stop` | Returns `{status: stopped}` | Real consumer-shutdown + offset commit + cleanup |
| `stream_health_check` | Returns fixture lag/EPS values | Real consumer-group lag query against the broker; per-monitor metrics from the worker |
| `configure_alerts` | Returns `{status: configured}` | Real alert routing config persistence + validation against the chosen channel's API |
| `get_anomaly_stats` | Returns fixture totals + anomaly rate | Real aggregation from Prometheus / time-series store; deduplication by anomaly fingerprint |
| `export_dashboard_config` | Returns a reference to the static `config/grafana_dashboard.json` fixture | Real templated dashboard generation parameterized by the active monitors |

Plus the missing bits that are out of scope here entirely:
- Event queue between consumer and Python worker (Redis / nats / in-memory channel)
- Python worker actually wired to `NixtlaClient.detect_anomalies()` with batch dispatch
- Real alert delivery to PagerDuty Events API v2 / Slack webhooks / SMTP
- Circuit breakers, dead-letter handling, structured logging, OTEL traces

Production-build estimate: ~6–10 weeks of focused engineering. Out of scope for this PoC.

---

## Quick start (PoC mode)

```bash
cd 005-plugins/nixtla-anomaly-streaming-monitor

# Install dev dependencies (when wired)
npm install                                            # MCP server (TypeScript)
pip install -r src/python-worker/requirements.txt 2>/dev/null || true   # Python worker

# In Claude Code:
# "Start the streaming monitor on the events kafka topic with threshold 0.95."
# Claude calls stream_monitor_start; the response includes _disclaimer="PoC: ..."
```

Every response includes a `_disclaimer` field so callers — including LLM agents — can clearly distinguish PoC fixtures from real data.

---

## MCP tools (all PoC)

| Tool | Purpose |
|---|---|
| `stream_monitor_start` | Demonstrate the start-monitor API |
| `stream_monitor_stop` | Demonstrate the stop-monitor API |
| `stream_health_check` | Demonstrate the consumer-health response shape |
| `configure_alerts` | Demonstrate the alert-config API |
| `get_anomaly_stats` | Demonstrate the stats-aggregation response shape |
| `export_dashboard_config` | Demonstrate the dashboard-export response shape |

---

## Architecture (production target)

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Kafka/    │────▶│   Consumer   │────▶│   Worker    │
│   Kinesis   │     │  (TS / SDK)  │     │   (Python)  │
└─────────────┘     └──────────────┘     │ NixtlaClient│
                                         │ .detect_    │
                                         │ anomalies() │
                                         └──────┬──────┘
                                                │
                                                ▼
                                         ┌──────────────┐
                                         │   Alerting   │
                                         │ (PD / Slack /│
                                         │   Email)     │
                                         └──────────────┘
```

Today only the API surface (the box on the left of the consumer) exists.

---

## Environment variables (production only — not used in PoC)

```bash
NIXTLA_API_KEY=...                # for detect_anomalies()
KAFKA_BROKERS=...                 # for kafkajs consumer
AWS_ACCESS_KEY_ID=...             # for Kinesis consumer
PAGERDUTY_INTEGRATION_KEY=...     # for alert delivery
SLACK_WEBHOOK_URL=...             # for alert delivery
```

---

## License

MIT — Jeremy Longshore.
