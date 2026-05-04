#!/usr/bin/env python3
"""MCP server for nixtla-embedded-forecast-widget (v0.1.0-wip).

WORK IN PROGRESS scaffold. Every tool returns illustrative output — see
the README for the full What's-real-vs-roadmap matrix. Production
implementations land at v1.0 (Epic 5.3).
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

logger = logging.getLogger(__name__)

WIP_DISCLAIMER = (
    "This is a WORK IN PROGRESS scaffold (v0.1.0-wip). The output above is "
    "ILLUSTRATIVE — not production data. Do not rely on it for real decisions. "
    "Track v1.0 build at Epic 5.3."
)

app = Server("nixtla-embedded-forecast-widget")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="generate_widget_html",
            description="[WIP] Produce the <script>+<div> snippet for embedding. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="scaffold_proxy_backend",
            description="[WIP] Emit a Cloud Run / Cloud Functions backend that hides the TimeGPT API key. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="preview_forecast",
            description="[WIP] Render a static SVG preview of the forecast for design review. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="export_widget_bundle",
            description="[WIP] Emit a versioned JS bundle for CDN deploy. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        "generate_widget_html": _handle_generate_widget_html,
        "scaffold_proxy_backend": _handle_scaffold_proxy_backend,
        "preview_forecast": _handle_preview_forecast,
        "export_widget_bundle": _handle_export_widget_bundle,
    }
    if name not in handlers:
        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "error": f"Unknown tool: {name}",
                        "_disclaimer": WIP_DISCLAIMER,
                    },
                    indent=2,
                ),
            )
        ]

    payload = handlers[name](arguments)
    payload["_disclaimer"] = WIP_DISCLAIMER
    return [TextContent(type="text", text=json.dumps(payload, indent=2))]


def _handle_generate_widget_html(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for generate_widget_html. Returns illustrative output."""
    return {
        "tool": "generate_widget_html",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Produce the <script>+<div> snippet for embedding.",
    }


def _handle_scaffold_proxy_backend(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for scaffold_proxy_backend. Returns illustrative output."""
    return {
        "tool": "scaffold_proxy_backend",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Emit a Cloud Run / Cloud Functions backend that hides the TimeGPT API key.",
    }


def _handle_preview_forecast(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for preview_forecast. Returns illustrative output."""
    return {
        "tool": "preview_forecast",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Render a static SVG preview of the forecast for design review.",
    }


def _handle_export_widget_bundle(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for export_widget_bundle. Returns illustrative output."""
    return {
        "tool": "export_widget_bundle",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Emit a versioned JS bundle for CDN deploy.",
    }


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
