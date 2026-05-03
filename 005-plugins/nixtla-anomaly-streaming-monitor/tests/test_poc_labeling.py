"""Verify PoC labeling integrity for nixtla-anomaly-streaming-monitor.

The MCP server is TypeScript (kafkajs / aws-sdk integration is the production
target), so we don't run Node-runtime tests here. Instead, we assert that the
plugin's PoC posture is consistent across:

  - plugin.json (description, version)
  - README.md (banner, what's-real-vs-PoC matrix)
  - src/mcp-server/index.ts (every tool description prefixed [PoC],
    every tool response carries _disclaimer)

This is the contract a production drop-in replacement must preserve.
"""

from __future__ import annotations

import json
import re

import pytest

# ---------------------------------------------------------------------------
# plugin.json
# ---------------------------------------------------------------------------


class TestPluginManifest:
    def test_version_is_poc(self, plugin_manifest):
        assert "poc" in plugin_manifest["version"].lower()

    def test_description_marks_poc(self, plugin_manifest):
        assert "PROOF OF CONCEPT" in plugin_manifest["description"]

    def test_canonical_fields_present(self, plugin_manifest):
        for field in ("name", "version", "description", "author", "license", "keywords"):
            assert field in plugin_manifest, f"missing canonical field: {field}"

    def test_author_url_correct(self, plugin_manifest):
        assert plugin_manifest["author"]["url"] == "https://github.com/jeremylongshore"

    def test_keywords_include_poc(self, plugin_manifest):
        assert "proof-of-concept" in plugin_manifest["keywords"]


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------


class TestReadme:
    def test_has_proof_of_concept_banner(self, readme_source):
        assert "**PROOF OF CONCEPT" in readme_source

    def test_has_origin_section(self, readme_source):
        assert "## Origin" in readme_source

    def test_has_whats_real_vs_poc_section(self, readme_source):
        assert "What's real vs PoC" in readme_source

    def test_lists_all_six_tools(self, readme_source):
        for tool in (
            "stream_monitor_start",
            "stream_monitor_stop",
            "stream_health_check",
            "configure_alerts",
            "get_anomaly_stats",
            "export_dashboard_config",
        ):
            assert tool in readme_source, f"README missing tool: {tool}"


# ---------------------------------------------------------------------------
# index.ts (TypeScript MCP server)
# ---------------------------------------------------------------------------


class TestTypescriptServer:
    def test_has_module_poc_disclaimer(self, ts_server_source):
        assert "PROOF OF CONCEPT" in ts_server_source
        assert "POC_DISCLAIMER" in ts_server_source

    def test_version_string_is_poc(self, ts_server_source):
        # version: "1.0.0-poc" or similar
        assert re.search(
            r'version:\s*"[^"]*-poc"', ts_server_source
        ), "TS server version should carry -poc suffix"

    def test_every_tool_description_marked_poc(self, ts_server_source):
        # Find all `description: "..."` fields. Every Tool object's description
        # in the listTools output should start with `[PoC]`.
        # Match `description: "[PoC] ..."` patterns inside the Tool array.
        tool_blocks = re.findall(r'name:\s*"(\w+)",\s*description:\s*"([^"]+)"', ts_server_source)
        # Filter to tool-array entries (the property descriptions inside
        # inputSchema also match name+description but we want top-level Tool
        # objects only). Easiest filter: at least one is named like a tool.
        tool_names = {
            "stream_monitor_start",
            "stream_monitor_stop",
            "stream_health_check",
            "configure_alerts",
            "get_anomaly_stats",
            "export_dashboard_config",
        }
        tool_descs = [(n, d) for n, d in tool_blocks if n in tool_names]
        assert len(tool_descs) == 6, f"expected 6 tools, got {len(tool_descs)}: {tool_descs}"
        for name, desc in tool_descs:
            assert desc.startswith("[PoC]"), f"{name} description not [PoC]-prefixed: {desc}"

    def test_every_response_carries_disclaimer(self, ts_server_source):
        # Each `case "<name>":` branch should reference `POC_DISCLAIMER` (or
        # `_disclaimer:`) within its return.
        tool_names = [
            "stream_monitor_start",
            "stream_monitor_stop",
            "stream_health_check",
            "configure_alerts",
            "get_anomaly_stats",
            "export_dashboard_config",
        ]
        for name in tool_names:
            # Find the case block.
            pattern = rf'case "{name}":(.*?)(?=case "|default:)'
            match = re.search(pattern, ts_server_source, re.DOTALL)
            assert match, f"missing case block for {name}"
            block = match.group(1)
            assert (
                "POC_DISCLAIMER" in block or "_disclaimer" in block
            ), f"{name} response missing POC_DISCLAIMER / _disclaimer field"


# ---------------------------------------------------------------------------
# Cross-artifact consistency
# ---------------------------------------------------------------------------


class TestConsistency:
    def test_plugin_name_matches_directory(self, plugin_manifest, plugin_root):
        assert plugin_manifest["name"] == plugin_root.name

    def test_repository_url_consistent(self, plugin_manifest, readme_source):
        # README should reference the owner (case-insensitive — README author name
        # is "Jeremy Longshore", plugin.json owner URL is github.com/jeremylongshore).
        readme_lower = readme_source.lower()
        assert (
            plugin_manifest["repository"].lower() in readme_lower
            or "jeremy longshore" in readme_lower
            or "jeremylongshore" in readme_lower
        ), "README should reference the plugin owner / repo URL"
