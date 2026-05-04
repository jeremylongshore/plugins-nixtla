"""Pytest unit tests for the nixtla-baseline-lab MCP server.

These tests exercise the public surface of NixtlaBaselineMCP without running
the full statsforecast pipeline. They cover:

  - tool registration shape (every tool has a name + description + inputSchema)
  - library version resolver
  - sMAPE / MASE math against known values
  - dispatch contract for handle_request (tools/list, tools/call)

The full smoke test (M4 download + forecast) lives in run_baseline_m4_smoke.py
and runs in CI as a separate job; we don't re-run it here.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"

# Make scripts/ importable for the MCP module
sys.path.insert(0, str(SCRIPTS_DIR))

from nixtla_baseline_mcp import NixtlaBaselineMCP  # noqa: E402


@pytest.fixture
def server():
    return NixtlaBaselineMCP()


# ---------------------------------------------------------------------------
# Library version resolver
# ---------------------------------------------------------------------------


class TestLibraryVersions:
    def test_returns_dict(self, server):
        versions = server._get_library_versions()
        assert isinstance(versions, dict)

    def test_includes_required_libraries(self, server):
        versions = server._get_library_versions()
        # statsforecast, pandas, numpy are core deps
        assert "statsforecast" in versions
        assert "pandas" in versions
        assert "numpy" in versions

    def test_versions_are_strings(self, server):
        versions = server._get_library_versions()
        for lib, ver in versions.items():
            assert isinstance(ver, str), f"{lib} version not a string: {ver!r}"


# ---------------------------------------------------------------------------
# Tool registration shape
# ---------------------------------------------------------------------------


class TestToolRegistration:
    def test_get_tools_returns_list(self, server):
        tools = server.get_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0

    def test_every_tool_has_name(self, server):
        for tool in server.get_tools():
            assert "name" in tool
            assert isinstance(tool["name"], str)
            assert len(tool["name"]) > 0

    def test_every_tool_has_description(self, server):
        for tool in server.get_tools():
            assert "description" in tool
            assert len(tool["description"]) > 10

    def test_every_tool_has_input_schema(self, server):
        for tool in server.get_tools():
            assert "inputSchema" in tool
            schema = tool["inputSchema"]
            assert schema["type"] == "object"
            # Tools either accept zero args or define a properties dict.
            assert "properties" in schema

    def test_includes_run_baselines_tool(self, server):
        names = {t["name"] for t in server.get_tools()}
        assert "run_baselines" in names

    def test_includes_compatibility_info_tool(self, server):
        names = {t["name"] for t in server.get_tools()}
        assert "get_nixtla_compatibility_info" in names


# ---------------------------------------------------------------------------
# Compatibility info
# ---------------------------------------------------------------------------


class TestCompatibilityInfo:
    def test_returns_dict(self, server):
        info = server.get_nixtla_compatibility_info()
        assert isinstance(info, dict)

    def test_has_library_versions(self, server):
        info = server.get_nixtla_compatibility_info()
        assert "library_versions" in info
        assert isinstance(info["library_versions"], dict)


# ---------------------------------------------------------------------------
# sMAPE math (asymmetric inputs, not tautologies)
# ---------------------------------------------------------------------------


class TestSMAPE:
    def test_perfect_forecast_is_zero(self, server):
        # Perfect prediction → sMAPE = 0 exactly.
        actual = [10.0, 20.0, 30.0, 40.0]
        predicted = [10.0, 20.0, 30.0, 40.0]
        assert server._calculate_smape(actual, predicted) == pytest.approx(0.0, abs=1e-9)

    def test_known_value_simple_case(self, server):
        # actual=[100], predicted=[110]
        # numerator: |100-110| = 10
        # denominator: (|100| + |110|) / 2 = 105
        # smape = 100 * (10/105) ≈ 9.5238
        actual = [100.0]
        predicted = [110.0]
        result = server._calculate_smape(actual, predicted)
        assert result == pytest.approx(9.5238, abs=1e-3)

    def test_constant_offset(self, server):
        # actual=[10, 10], predicted=[20, 20]
        # per-element: |10-20|/((10+20)/2) = 10/15 = 0.667
        # smape = 100 * 0.667 = 66.67
        actual = [10.0, 10.0]
        predicted = [20.0, 20.0]
        result = server._calculate_smape(actual, predicted)
        assert result == pytest.approx(66.667, abs=1e-2)

    def test_handles_zeros_safely(self, server):
        # Both actual and predicted zero — implementation guards against
        # divide-by-zero with a 1e-10 floor; result is very small, not NaN.
        actual = [0.0, 0.0]
        predicted = [0.0, 0.0]
        result = server._calculate_smape(actual, predicted)
        # 100 * mean(0/1e-10) = 0 since numerator is also 0
        assert result == pytest.approx(0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# MASE math
# ---------------------------------------------------------------------------


class TestMASE:
    def test_perfect_forecast_is_zero(self, server):
        actual = [10.0, 20.0, 30.0]
        predicted = [10.0, 20.0, 30.0]
        train = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        result = server._calculate_mase(actual, predicted, train, season_length=7)
        assert result == pytest.approx(0.0, abs=1e-9)

    def test_naive_seasonal_returns_one(self, server):
        # If the forecast is itself the naive-seasonal forecast on identical
        # data, MASE should be ≈ 1.
        train = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        season_length = 7
        # Naive seasonal forecast for the next step: y_{t} = y_{t-season_length}
        actual = [9.0]
        predicted = [train[-season_length]]  # = train[-7] = 2.0
        result = server._calculate_mase(actual, predicted, train, season_length=season_length)
        # mae_forecast = |9-2| = 7
        # mae_naive = mean(|train[7:]-train[:-7]|) = mean(|8-1|) = 7
        # mase = 7/7 = 1.0
        assert result == pytest.approx(1.0, abs=1e-9)

    def test_short_series_falls_back_to_simple_naive(self, server):
        # train_series shorter than season_length triggers diff-based fallback.
        actual = [10.0]
        predicted = [12.0]
        train = [1.0, 2.0, 3.0]  # length 3, season_length 7 → fallback
        result = server._calculate_mase(actual, predicted, train, season_length=7)
        # mae_forecast = 2; mae_naive = mean(|diff(train)|) = mean(1,1) = 1
        # mase = 2/1 = 2.0
        assert result == pytest.approx(2.0, abs=1e-9)


# ---------------------------------------------------------------------------
# handle_request dispatch contract
# ---------------------------------------------------------------------------


class TestHandleRequest:
    def test_tools_list(self, server):
        # The implementation returns the tools list directly (not wrapped in
        # a JSON-RPC `result` envelope — wrapping happens in run() before
        # writing to stdout).
        request = {"method": "tools/list", "params": {}}
        response = server.handle_request(request)
        assert "tools" in response
        names = {t["name"] for t in response["tools"]}
        assert "run_baselines" in names
        assert "get_nixtla_compatibility_info" in names

    def test_tools_call_compatibility_info(self, server):
        request = {
            "method": "tools/call",
            "params": {"name": "get_nixtla_compatibility_info", "arguments": {}},
        }
        response = server.handle_request(request)
        assert "content" in response
        # MCP envelope: list of {type: "text", text: "<json>"} items.
        assert isinstance(response["content"], list)
        assert response["content"][0]["type"] == "text"

    def test_tools_call_unknown_tool_returns_error(self, server):
        request = {
            "method": "tools/call",
            "params": {"name": "no_such_tool", "arguments": {}},
        }
        response = server.handle_request(request)
        assert "error" in response
        assert "no_such_tool" in response["error"]

    def test_unknown_method_returns_error(self, server):
        request = {"method": "totally/fake", "params": {}}
        response = server.handle_request(request)
        assert "error" in response
        assert "totally/fake" in response["error"]
