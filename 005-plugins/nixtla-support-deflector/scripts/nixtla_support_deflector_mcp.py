#!/usr/bin/env python3
"""MCP server for nixtla-support-deflector (v0.1.0-wip).

WORK IN PROGRESS scaffold. Every tool returns illustrative output — see
the README for the full What's-real-vs-roadmap matrix. Production
implementations land at v1.0 (Epic 5.1).
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
    "Track v1.0 build at Epic 5.1."
)

app = Server("nixtla-support-deflector")


async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="classify_question",
            description="[WIP] Tag an inbound question as docs / bug / feature-request / billing. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="answer_from_docs",
            description="[WIP] Search the indexed Nixtla docs and emit an answer with cited sources. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="escalate_to_human",
            description="[WIP] Emit a structured handoff payload for the on-call support engineer. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="learn_from_resolution",
            description="[WIP] Record a resolved question's final answer for future retrieval. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        "classify_question": _handle_classify_question,
        "answer_from_docs": _handle_answer_from_docs,
        "escalate_to_human": _handle_escalate_to_human,
        "learn_from_resolution": _handle_learn_from_resolution,
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

def _handle_classify_question(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for classify_question. Returns illustrative output."""
    return {
        "tool": "classify_question",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Tag an inbound question as docs / bug / feature-request / billing.",
    }


def _handle_answer_from_docs(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for answer_from_docs. Returns illustrative output."""
    return {
        "tool": "answer_from_docs",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Search the indexed Nixtla docs and emit an answer with cited sources.",
    }


def _handle_escalate_to_human(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for escalate_to_human. Returns illustrative output."""
    return {
        "tool": "escalate_to_human",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Emit a structured handoff payload for the on-call support engineer.",
    }


def _handle_learn_from_resolution(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for learn_from_resolution. Returns illustrative output."""
    return {
        "tool": "learn_from_resolution",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Record a resolved question's final answer for future retrieval.",
    }


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
