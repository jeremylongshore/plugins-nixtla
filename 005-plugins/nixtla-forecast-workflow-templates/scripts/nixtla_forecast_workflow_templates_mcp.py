#!/usr/bin/env python3
"""MCP server for nixtla-forecast-workflow-templates (v0.1.0-wip).

WORK IN PROGRESS scaffold. Every tool returns illustrative output — see
the README for the full What's-real-vs-roadmap matrix. Production
implementations land at v1.0 (Epic 4.2).
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
    "Track v1.0 build at Epic 4.2."
)

app = Server("nixtla-forecast-workflow-templates")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_templates",
            description="[WIP] Return the catalog of available workflow templates by industry. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_template",
            description="[WIP] Fetch a single template's full source by id. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="instantiate_template",
            description="[WIP] Generate a customized template with the user's column schema. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="validate_template_inputs",
            description="[WIP] Lint a user's data against a template's expected schema. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        "list_templates": _handle_list_templates,
        "get_template": _handle_get_template,
        "instantiate_template": _handle_instantiate_template,
        "validate_template_inputs": _handle_validate_template_inputs,
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


def _handle_list_templates(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for list_templates. Returns illustrative output."""
    return {
        "tool": "list_templates",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Return the catalog of available workflow templates by industry.",
    }


def _handle_get_template(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for get_template. Returns illustrative output."""
    return {
        "tool": "get_template",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Fetch a single template's full source by id.",
    }


def _handle_instantiate_template(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for instantiate_template. Returns illustrative output."""
    return {
        "tool": "instantiate_template",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Generate a customized template with the user's column schema.",
    }


def _handle_validate_template_inputs(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for validate_template_inputs. Returns illustrative output."""
    return {
        "tool": "validate_template_inputs",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Lint a user's data against a template's expected schema.",
    }


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
