#!/usr/bin/env python3
"""MCP server for nixtla-docs-qa-generator (v0.1.0-wip).

WORK IN PROGRESS scaffold. Every tool returns illustrative output — see
the README for the full What's-real-vs-roadmap matrix. Production
implementations land at v1.0 (Epic 5.2).
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
    "Track v1.0 build at Epic 5.2."
)

app = Server("nixtla-docs-qa-generator")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="crawl_docs",
            description="[WIP] Walk the Nixtla docs sitemap and pull canonical content. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="extract_qa_pairs",
            description="[WIP] Generate Q&A pairs from a crawled section. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="dedupe_qa_pairs",
            description="[WIP] Collapse near-duplicate questions into a single canonical entry. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="export_faq_html",
            description="[WIP] Emit the Q&A set as embeddable FAQ HTML. Returns illustrative output only.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        "crawl_docs": _handle_crawl_docs,
        "extract_qa_pairs": _handle_extract_qa_pairs,
        "dedupe_qa_pairs": _handle_dedupe_qa_pairs,
        "export_faq_html": _handle_export_faq_html,
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


def _handle_crawl_docs(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for crawl_docs. Returns illustrative output."""
    return {
        "tool": "crawl_docs",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Walk the Nixtla docs sitemap and pull canonical content.",
    }


def _handle_extract_qa_pairs(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for extract_qa_pairs. Returns illustrative output."""
    return {
        "tool": "extract_qa_pairs",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Generate Q&A pairs from a crawled section.",
    }


def _handle_dedupe_qa_pairs(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for dedupe_qa_pairs. Returns illustrative output."""
    return {
        "tool": "dedupe_qa_pairs",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Collapse near-duplicate questions into a single canonical entry.",
    }


def _handle_export_faq_html(args: dict[str, Any]) -> dict[str, Any]:
    """Stub for export_faq_html. Returns illustrative output."""
    return {
        "tool": "export_faq_html",
        "status": "wip-stub",
        "received_args": args,
        "illustrative_output": "Emit the Q&A set as embeddable FAQ HTML.",
    }


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
