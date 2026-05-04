#!/usr/bin/env python3
"""MCP server for nixtla-sales-demo-builder (v0.1.0-wip).

WORK IN PROGRESS scaffold. Every tool returns illustrative output — see
the README for the full What's-real-vs-roadmap matrix. Production
implementations land at v1.0 (Epic 4.1).
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
    "Track v1.0 build at Epic 4.1."
)

app = Server("nixtla-sales-demo-builder")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="scaffold_demo",
            description="[WIP] Build a TimeGPT demo project for the given industry + data shape. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="generate_synthetic_data",
            description="[WIP] Emit a CSV that matches the customer's described schema. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="write_demo_script",
            description="[WIP] Produce a runnable Python script that calls NixtlaClient.forecast() against the synthetic data. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="draft_slide_outline",
            description="[WIP] Write a 5-7 slide outline narrating the demo for a 30-minute pitch. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        "scaffold_demo": _handle_scaffold_demo,
        "generate_synthetic_data": _handle_generate_synthetic_data,
        "write_demo_script": _handle_write_demo_script,
        "draft_slide_outline": _handle_draft_slide_outline,
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


def _handle_scaffold_demo(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for scaffold_demo. Returns illustrative output."""
    return {
        "tool": "scaffold_demo",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Build a TimeGPT demo project for the given industry + data shape.",
    }


def _handle_generate_synthetic_data(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for generate_synthetic_data. Returns illustrative output."""
    return {
        "tool": "generate_synthetic_data",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Emit a CSV that matches the customer's described schema.",
    }


def _handle_write_demo_script(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for write_demo_script. Returns illustrative output."""
    return {
        "tool": "write_demo_script",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Produce a runnable Python script that calls NixtlaClient.forecast() against the ",
    }


def _handle_draft_slide_outline(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for draft_slide_outline. Returns illustrative output."""
    return {
        "tool": "draft_slide_outline",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Write a 5-7 slide outline narrating the demo for a 30-minute pitch.",
    }


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
