"""Unit tests for nixtla-defi-sentinel MCP server.

This plugin is an intentional Proof of Concept; tests verify that:
  - The PoC disclaimer is present on every tool response.
  - Tool input/output shapes are stable (so production-mode replacement
    code can drop in without breaking callers).
  - The dispatcher routes correctly.

Tests do NOT verify real DeFi data — there is none to verify. That's the point.
"""

from __future__ import annotations

import asyncio
import json

import defi_sentinel_mcp as mcp
import pytest

TOOL_NAMES = {
    "monitor_protocol",
    "get_protocol_status",
    "configure_alerts",
    "run_anomaly_scan",
    "generate_risk_report",
    "compare_protocols",
}


@pytest.fixture
def run():
    def _run(coro):
        return asyncio.run(coro)

    return _run


# ---------------------------------------------------------------------------
# PoC disclaimer present on every response
# ---------------------------------------------------------------------------


class TestPoCDisclaimer:
    def test_monitor_protocol_has_disclaimer(self, run):
        result = run(mcp.call_tool("monitor_protocol", {"protocol": "aave"}))
        parsed = json.loads(result[0].text)
        assert "_disclaimer" in parsed
        assert "PoC" in parsed["_disclaimer"]

    def test_get_protocol_status_has_disclaimer(self, run):
        result = run(mcp.call_tool("get_protocol_status", {"protocol": "aave"}))
        parsed = json.loads(result[0].text)
        assert "_disclaimer" in parsed

    def test_configure_alerts_has_disclaimer(self, run):
        result = run(mcp.call_tool("configure_alerts", {"protocol": "aave", "channel": "telegram"}))
        parsed = json.loads(result[0].text)
        assert "_disclaimer" in parsed

    def test_run_anomaly_scan_has_disclaimer(self, run):
        result = run(mcp.call_tool("run_anomaly_scan", {"protocol": "aave"}))
        parsed = json.loads(result[0].text)
        assert "_disclaimer" in parsed

    def test_generate_risk_report_has_disclaimer(self, run):
        result = run(mcp.call_tool("generate_risk_report", {"protocol": "aave"}))
        parsed = json.loads(result[0].text)
        assert "_disclaimer" in parsed

    def test_compare_protocols_has_disclaimer(self, run):
        result = run(mcp.call_tool("compare_protocols", {"protocols": ["aave", "compound"]}))
        parsed = json.loads(result[0].text)
        assert "_disclaimer" in parsed


# ---------------------------------------------------------------------------
# Response shape stability
# ---------------------------------------------------------------------------


class TestResponseShapes:
    def test_monitor_protocol_shape(self, run):
        result = run(mcp.call_tool("monitor_protocol", {"protocol": "aave"}))
        parsed = json.loads(result[0].text)
        assert {"status", "protocol", "metrics", "threshold", "data_source"} <= parsed.keys()

    def test_get_protocol_status_shape(self, run):
        result = run(mcp.call_tool("get_protocol_status", {"protocol": "compound"}))
        parsed = json.loads(result[0].text)
        assert {"protocol", "status", "current_tvl", "tvl_change_24h"} <= parsed.keys()

    def test_run_anomaly_scan_shape(self, run):
        result = run(mcp.call_tool("run_anomaly_scan", {"protocol": "aave", "lookback_days": 7}))
        parsed = json.loads(result[0].text)
        assert {
            "protocol",
            "scan_period",
            "anomalies_found",
            "risk_score",
            "risk_level",
        } <= parsed.keys()
        assert isinstance(parsed["anomalies_found"], list)

    def test_generate_risk_report_shape(self, run):
        result = run(mcp.call_tool("generate_risk_report", {"protocol": "aave"}))
        parsed = json.loads(result[0].text)
        assert {"protocol", "overall_risk", "risk_factors"} <= parsed.keys()
        assert isinstance(parsed["risk_factors"], list)

    def test_compare_protocols_shape(self, run):
        result = run(mcp.call_tool("compare_protocols", {"protocols": ["aave", "compound"]}))
        parsed = json.loads(result[0].text)
        assert "comparison" in parsed
        assert isinstance(parsed["comparison"], list)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_supported_protocols_includes_top_protocols(self):
        for p in ("aave", "compound", "uniswap", "curve", "maker"):
            assert p in mcp.SUPPORTED_PROTOCOLS

    def test_metrics_constants(self):
        assert set(mcp.METRICS) == {"tvl", "apy", "volume", "liquidity", "price"}

    def test_disclaimer_string_is_set(self):
        assert isinstance(mcp.POC_DISCLAIMER, str)
        assert "PoC" in mcp.POC_DISCLAIMER


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


class TestCallTool:
    def test_unknown_tool_returns_error(self, run):
        result = run(mcp.call_tool("nonexistent_tool", {}))
        assert "Unknown" in result[0].text

    def test_list_tools_returns_all_six(self, run):
        tools = run(mcp.list_tools())
        names = {t.name for t in tools}
        assert names == TOOL_NAMES

    def test_all_tools_marked_poc_in_description(self, run):
        tools = run(mcp.list_tools())
        for t in tools:
            assert "[PoC]" in t.description, f"{t.name} description missing [PoC] marker"
