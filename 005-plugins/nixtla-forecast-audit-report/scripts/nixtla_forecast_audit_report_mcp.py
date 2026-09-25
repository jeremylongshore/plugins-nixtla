#!/usr/bin/env python3
"""MCP server for nixtla-forecast-audit-report (v0.1.0-wip).

WORK IN PROGRESS scaffold. Every tool returns illustrative output — see
the README for the full What's-real-vs-roadmap matrix. Production
implementations land at v1.0 (Epic 4.3).
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    ListToolsResult,
    PaginatedRequestParams,
    TextContent,
    Tool,
)

logger = logging.getLogger(__name__)

WIP_DISCLAIMER = (
    "This is a WORK IN PROGRESS scaffold (v0.1.0-wip). The output above is "
    "ILLUSTRATIVE — not production data. Do not rely on it for real decisions. "
    "Track v1.0 build at Epic 4.3."
)

app = Server("nixtla-forecast-audit-report")


async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="ingest_forecast_run",
            description="[WIP] Load a TimeGPT forecast manifest + outputs into the audit context. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="generate_audit_report",
            description="[WIP] Emit the full audit-grade markdown report. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="compute_residual_diagnostics",
            description="[WIP] Calculate Ljung-Box, Jarque-Bera, and ACF on residuals. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="export_model_card",
            description="[WIP] Generate a TimeGPT model-card section conforming to Google's Model Cards spec. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        "ingest_forecast_run": _handle_ingest_forecast_run,
        "generate_audit_report": _handle_generate_audit_report,
        "compute_residual_diagnostics": _handle_compute_residual_diagnostics,
        "export_model_card": _handle_export_model_card,
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


async def _on_list_tools(ctx: Any, params: PaginatedRequestParams | None) -> ListToolsResult:
    return ListToolsResult(tools=await list_tools())


async def _on_call_tool(ctx: Any, params: CallToolRequestParams) -> CallToolResult:
    # The 1.x decorator turned a raised exception into an isError result; keep that.
    try:
        return CallToolResult(content=await call_tool(params.name, dict(params.arguments or {})))
    except Exception as exc:  # noqa: BLE001 - every failure becomes a tool error result
        text = TextContent(type="text", text=f"{type(exc).__name__}: {exc}")
        return CallToolResult(content=[text], is_error=True)


# MCP Python SDK 2.x: the @app.list_tools()/@app.call_tool() decorators no
# longer exist; handlers are registered by method, mirroring what the 2.x
# Server constructor does with on_list_tools / on_call_tool.
app.add_request_handler("tools/list", PaginatedRequestParams, _on_list_tools)
app.add_request_handler("tools/call", CallToolRequestParams, _on_call_tool)


def _handle_ingest_forecast_run(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for ingest_forecast_run. Returns illustrative output."""
    return {
        "tool": "ingest_forecast_run",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Load a TimeGPT forecast manifest + outputs into the audit context.",
    }


def _handle_generate_audit_report(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for generate_audit_report. Returns illustrative output."""
    return {
        "tool": "generate_audit_report",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Emit the full audit-grade markdown report.",
    }


def _handle_compute_residual_diagnostics(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for compute_residual_diagnostics. Returns illustrative output."""
    return {
        "tool": "compute_residual_diagnostics",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Calculate Ljung-Box, Jarque-Bera, and ACF on residuals.",
    }


def _handle_export_model_card(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for export_model_card. Returns illustrative output."""
    return {
        "tool": "export_model_card",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Generate a TimeGPT model-card section conforming to Google's Model Cards spec.",
    }


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
