# Nixtla DeFi Sentinel

> ⚠️ **PROOF OF CONCEPT — not for production use.** This plugin demonstrates an anomaly-detection API surface for DeFi protocol monitoring. It was built in response to a real DeFi exploit to explore how Nixtla's anomaly-detection primitives could be applied to surface protocol-risk signals (TVL drops, APY spikes, volume anomalies). The MCP tools currently return illustrative fixtures — **not live protocol data**.

**Version**: 1.0.0-poc · **Status**: Proof of Concept · **API key needed**: None for the PoC; production would need Nixtla API + DeFiLlama + alert webhook tokens

---

## Origin

This plugin was built as an exploration after a real DeFi exploit. The thesis: Nixtla's `detect_anomalies()` primitive — applied to time-series protocol metrics — could surface precursor signals (unusual TVL outflows, abnormal APY divergence, volume spikes) that humans miss in raw dashboards. The PoC demonstrates the API surface a production version would expose. The illustrative fixtures show what every tool would return *if* it were wired to live data sources.

---

## What's real vs PoC

Every tool currently returns a fixture with a `_disclaimer` field making the PoC status explicit. Production deployment requires real work in three layers:

| MCP tool | What's there now | What production would need |
|---|---|---|
| `monitor_protocol` | Returns the requested protocol/metrics dict + 5-min cadence string | Live polling of [DeFiLlama](https://defillama.com/) / [The Graph](https://thegraph.com/) / on-chain RPC; persistent monitoring state in Redis or similar |
| `get_protocol_status` | Returns 2024-dated TVL + APY fixtures | Live query against the polling layer; cached aggregates |
| `configure_alerts` | Returns the configured channel + alert types | Real PagerDuty / Telegram / Discord / Slack webhook delivery; alert rate limiting |
| `run_anomaly_scan` | Returns a single 2024-dated synthetic anomaly | Real Nixtla `detect_anomalies()` call against historical metric series; per-metric thresholds; severity classification |
| `generate_risk_report` | Returns fixture risk factors + a 7-day TVL forecast | Real risk-factor scoring (smart contract audit history, liquidity concentration, governance metrics); real Nixtla forecast on TVL series |
| `compare_protocols` | Returns 2-protocol fixture comparison | Real cross-protocol analytics with current TVL / risk / APY |

Production-build estimate: ~6–8 weeks of focused engineering (data layer, anomaly engine wiring, alert delivery, observability). Out of scope for this PoC.

---

## Quick start (PoC mode)

```bash
cd 005-plugins/nixtla-defi-sentinel
pip install -r scripts/requirements.txt

# In Claude Code:
# "Show me the status of the aave protocol via the DeFi sentinel."
# Claude calls get_protocol_status; the response includes _disclaimer="PoC: ..."
```

Every response includes a `_disclaimer` field so callers — including LLM agents — can clearly distinguish PoC fixtures from real data.

---

## MCP tools (all PoC)

| Tool | Purpose |
|---|---|
| `monitor_protocol` | Demonstrate the protocol-monitoring API |
| `get_protocol_status` | Demonstrate the status response shape |
| `configure_alerts` | Demonstrate the alert-config API |
| `run_anomaly_scan` | Demonstrate the anomaly-scan response shape |
| `generate_risk_report` | Demonstrate the risk-report response shape |
| `compare_protocols` | Demonstrate the cross-protocol comparison shape |

---

## Supported protocols (illustrative)

aave · compound · uniswap · curve · makerdao · lido · convex · yearn · balancer · sushiswap

In production these would come from a live DeFiLlama query of the top-N protocols by TVL.

---

## Metrics

| Metric | Description |
|---|---|
| TVL | Total Value Locked |
| APY | Annual Percentage Yield |
| Volume | Trading volume |
| Liquidity | Available liquidity |
| Price | Token prices |

---

## Environment variables (production only — not used in PoC)

```bash
NIXTLA_API_KEY=...           # for detect_anomalies()
DEFILLAMA_API_KEY=...        # for live protocol polling
TELEGRAM_BOT_TOKEN=...       # for alert delivery
PAGERDUTY_INTEGRATION_KEY=...
```

---

## License

MIT — Jeremy Longshore.
