"""Verify WIP labeling integrity for nixtla-support-deflector.

This plugin is intentionally a v0.1.0-wip scaffold. The labels below are
load-bearing: callers rely on the [WIP] prefix and the _disclaimer field
to know the output is illustrative, not production. If you change any
of these labels, update the labels everywhere — README, plugin.json,
list_tools, and call_tool — and re-run this suite.
"""

from __future__ import annotations

import asyncio
import json

import pytest

# ---------------------------------------------------------------------------
# plugin.json
# ---------------------------------------------------------------------------


class TestPluginManifest:
    def test_version_is_wip(self, plugin_manifest):
        assert plugin_manifest["version"] == "0.1.0-wip"

    def test_description_marks_wip(self, plugin_manifest):
        assert "WORK IN PROGRESS" in plugin_manifest["description"]

    def test_canonical_8_field_set(self, plugin_manifest):
        for field in (
            "name",
            "version",
            "description",
            "author",
            "homepage",
            "repository",
            "license",
            "keywords",
        ):
            assert field in plugin_manifest, f"missing canonical field: {field}"

    def test_author_url_is_jeremylongshore(self, plugin_manifest):
        assert plugin_manifest["author"]["url"] == "https://github.com/jeremylongshore"

    def test_keywords_include_work_in_progress(self, plugin_manifest):
        assert "work-in-progress" in plugin_manifest["keywords"]


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------


class TestReadme:
    def test_has_wip_banner(self, readme_source):
        assert "WORK IN PROGRESS" in readme_source

    def test_has_whats_real_vs_roadmap(self, readme_source):
        assert "What's real vs roadmap" in readme_source

    def test_documents_production_gap(self, readme_source):
        assert "## Production gap" in readme_source


# ---------------------------------------------------------------------------
# MCP server source
# ---------------------------------------------------------------------------


class TestMcpServer:
    def test_has_wip_disclaimer_constant(self, mcp_source):
        assert "WIP_DISCLAIMER" in mcp_source
        assert "WORK IN PROGRESS" in mcp_source

    def test_every_tool_description_prefixed_wip(self, mcp_source):
        # Every Tool(description="...") should start with [WIP].
        # Match the description= line and verify the prefix.
        import re

        descriptions = re.findall(r'description="([^"]+)"', mcp_source)
        # Filter to top-level Tool descriptions (skip the "no description=" lines).
        # The MCP scaffold emits exactly 4 Tool entries with description=.
        wip_descriptions = [d for d in descriptions if d.startswith("[WIP]")]
        assert len(wip_descriptions) >= 4, (
            f"Expected >=4 [WIP]-prefixed tool descriptions, found "
            f"{len(wip_descriptions)}: {descriptions}"
        )

    def test_call_tool_attaches_disclaimer(self, mcp_source):
        # The dispatcher must set payload["_disclaimer"] before returning.
        assert 'payload["_disclaimer"] = WIP_DISCLAIMER' in mcp_source


# ---------------------------------------------------------------------------
# Async dispatch — exercise the call_tool surface
# ---------------------------------------------------------------------------


def _import_mcp_module():
    import nixtla_support_deflector_mcp as mod

    return mod


@pytest.fixture
def mcp_module():
    return _import_mcp_module()


class TestDispatch:
    def test_list_tools_returns_4(self, mcp_module):
        tools = asyncio.run(mcp_module.list_tools())
        assert len(tools) == 4

    def test_known_tool_returns_disclaimer(self, mcp_module):
        tools = asyncio.run(mcp_module.list_tools())
        first_tool_name = tools[0].name
        result = asyncio.run(mcp_module.call_tool(first_tool_name, {}))
        payload = json.loads(result[0].text)
        assert "_disclaimer" in payload
        assert "WORK IN PROGRESS" in payload["_disclaimer"]

    def test_unknown_tool_returns_disclaimer(self, mcp_module):
        result = asyncio.run(mcp_module.call_tool("fake_tool", {}))
        payload = json.loads(result[0].text)
        assert "error" in payload
        assert "_disclaimer" in payload
