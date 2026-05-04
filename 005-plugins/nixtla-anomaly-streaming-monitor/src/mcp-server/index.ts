/**
 * Nixtla Anomaly Streaming Monitor - MCP Server
 *
 * ⚠️  PROOF OF CONCEPT — not for production use.
 *
 * This module is an exploratory PoC demonstrating an anomaly-detection API
 * surface for streaming protocol metrics (Kafka / Kinesis / HTTP webhooks).
 * All MCP tools currently return ILLUSTRATIVE FIXTURES, not live consumer
 * data. Every response includes a `_disclaimer` field making this explicit.
 *
 * Production deployment requires:
 *   - Real Kafka/Kinesis consumer code (kafkajs / @aws-sdk/client-kinesis)
 *   - Event queue + Python-worker IPC for batch dispatch to NixtlaClient
 *   - Real alert delivery (PagerDuty Events API / Slack webhooks / SMTP)
 *   - Stream lag monitoring + circuit breakers + dead-letter queue handling
 *
 * See README §"What's real vs PoC" for the full production-gap analysis.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const POC_DISCLAIMER =
  "PoC: this output is an illustrative fixture, not live stream data. " +
  "See README §'What's real vs PoC' for the production-gap analysis.";

const server = new Server(
  {
    name: "nixtla-anomaly-streaming-monitor",
    version: "1.0.0-poc",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions (every description prefixed [PoC])
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "stream_monitor_start",
        description: "[PoC] Demonstrate the stream-monitor-start API surface",
        inputSchema: {
          type: "object",
          properties: {
            source: {
              type: "string",
              enum: ["kafka", "kinesis", "webhook"],
              description: "Stream source type",
            },
            topic: {
              type: "string",
              description: "Topic or stream name",
            },
            threshold: {
              type: "number",
              description: "Anomaly confidence threshold (0.0-1.0)",
              default: 0.95,
            },
          },
          required: ["source", "topic"],
        },
      },
      {
        name: "stream_monitor_stop",
        description: "[PoC] Demonstrate the stream-monitor-stop API surface",
        inputSchema: {
          type: "object",
          properties: {
            monitor_id: {
              type: "string",
              description: "Monitor ID to stop",
            },
          },
          required: ["monitor_id"],
        },
      },
      {
        name: "stream_health_check",
        description: "[PoC] Demonstrate the consumer-health response shape",
        inputSchema: {
          type: "object",
          properties: {
            monitor_id: {
              type: "string",
              description: "Monitor ID to check",
            },
          },
        },
      },
      {
        name: "configure_alerts",
        description: "[PoC] Demonstrate the alert-configuration API surface",
        inputSchema: {
          type: "object",
          properties: {
            channel: {
              type: "string",
              enum: ["pagerduty", "slack", "email"],
            },
            webhook_url: {
              type: "string",
            },
            severity_threshold: {
              type: "string",
              enum: ["low", "medium", "high", "critical"],
            },
          },
          required: ["channel"],
        },
      },
      {
        name: "get_anomaly_stats",
        description: "[PoC] Demonstrate the anomaly-stats response shape",
        inputSchema: {
          type: "object",
          properties: {
            monitor_id: { type: "string" },
            timeframe: { type: "string", default: "1h" },
          },
        },
      },
      {
        name: "export_dashboard_config",
        description: "[PoC] Demonstrate the Grafana dashboard config response shape",
        inputSchema: {
          type: "object",
          properties: {
            monitor_id: { type: "string" },
          },
        },
      },
    ],
  };
});

// Tool execution — every response carries _disclaimer
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "stream_monitor_start":
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                _disclaimer: POC_DISCLAIMER,
                status: "started",
                monitor_id: `monitor_${Date.now()}`,
                source: args?.source,
                topic: args?.topic,
                threshold: args?.threshold || 0.95,
              },
              null,
              2
            ),
          },
        ],
      };

    case "stream_monitor_stop":
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              _disclaimer: POC_DISCLAIMER,
              status: "stopped",
              monitor_id: args?.monitor_id,
            }),
          },
        ],
      };

    case "stream_health_check":
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              _disclaimer: POC_DISCLAIMER,
              status: "healthy",
              lag: 0,
              events_per_second: 1250,
              anomalies_detected: 3,
            }),
          },
        ],
      };

    case "configure_alerts":
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              _disclaimer: POC_DISCLAIMER,
              status: "configured",
              channel: args?.channel,
            }),
          },
        ],
      };

    case "get_anomaly_stats":
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              _disclaimer: POC_DISCLAIMER,
              timeframe: args?.timeframe || "1h",
              total_events: 4500000,
              anomalies_detected: 127,
              anomaly_rate: 0.0028,
              avg_confidence: 0.97,
            }),
          },
        ],
      };

    case "export_dashboard_config":
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              _disclaimer: POC_DISCLAIMER,
              status: "exported",
              path: "config/grafana_dashboard.json",
              note: "Static fixture — see file in repo for the dashboard JSON shape.",
            }),
          },
        ],
      };

    default:
      return {
        content: [{ type: "text", text: `Unknown tool: ${name}` }],
      };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Nixtla Anomaly Streaming Monitor MCP server (PoC) running");
}

main().catch(console.error);
