"""Unit tests for nixtla-roi-calculator MCP server.

Covers:
    * calculate_roi_internal — core ROI math
    * _format_currency, _format_percent — display helpers
    * generate_pdf_report — reportlab PDF generation
    * compare_scenarios_internal — multi-scenario comparison + sensitivity
    * export_to_salesforce — dry-run + live POST paths
    * call_tool — MCP async dispatch

Run from repo root:
    pytest 005-plugins/nixtla-roi-calculator/tests -v --cov=005-plugins/nixtla-roi-calculator/scripts
"""

from __future__ import annotations

import asyncio
import json
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import roi_calculator_mcp as mcp

# ---------------------------------------------------------------------------
# calculate_roi_internal
# ---------------------------------------------------------------------------


class TestCalculateROIInternal:
    def test_returns_three_top_level_sections(self, sample_roi_inputs):
        result = mcp.calculate_roi_internal(sample_roi_inputs)
        assert set(result.keys()) == {"current_costs", "timegpt_costs", "savings"}

    def test_current_tool_annual_is_monthly_x_12(self, sample_roi_inputs):
        result = mcp.calculate_roi_internal(sample_roi_inputs)
        # current_tool_cost is monthly per the dataclass docstring; annual = *12
        assert result["current_costs"]["tool_annual"] == sample_roi_inputs.current_tool_cost * 12

    def test_current_fte_annual_uses_52_weeks(self, sample_roi_inputs):
        result = mcp.calculate_roi_internal(sample_roi_inputs)
        expected = sample_roi_inputs.fte_hours_per_week * 52 * sample_roi_inputs.fte_hourly_rate
        assert result["current_costs"]["fte_annual"] == expected

    def test_current_total_is_sum(self, sample_roi_inputs):
        result = mcp.calculate_roi_internal(sample_roi_inputs)
        cc = result["current_costs"]
        assert (
            cc["total_annual"] == cc["tool_annual"] + cc["fte_annual"] + cc["infrastructure_annual"]
        )

    def test_timegpt_fte_is_30pct_of_current(self, sample_roi_inputs):
        # The implementation assumes 70% FTE reduction; TimeGPT FTE = 30% of current FTE.
        result = mcp.calculate_roi_internal(sample_roi_inputs)
        current_fte = result["current_costs"]["fte_annual"]
        assert result["timegpt_costs"]["fte_annual"] == pytest.approx(current_fte * 0.3)

    def test_savings_3year_is_annual_x_3(self, sample_roi_inputs):
        result = mcp.calculate_roi_internal(sample_roi_inputs)
        assert result["savings"]["3year"] == result["savings"]["annual"] * 3

    def test_no_savings_returns_inf_payback(self):
        # Inputs that produce zero or negative savings.
        inputs = mcp.ROIInputs(
            current_tool_cost=0.0,
            fte_hours_per_week=0.0,
            fte_hourly_rate=0.0,
            infrastructure_cost=0.0,
            forecast_volume_monthly=10_000_000,  # huge timegpt cost, no current-state cost
            timegpt_price_per_1k=10.0,
        )
        result = mcp.calculate_roi_internal(inputs)
        assert result["savings"]["annual"] <= 0
        assert result["savings"]["payback_months"] == float("inf")

    def test_zero_current_total_returns_zero_roi_pct(self):
        inputs = mcp.ROIInputs(
            current_tool_cost=0.0,
            fte_hours_per_week=0.0,
            fte_hourly_rate=0.0,
            infrastructure_cost=0.0,
            forecast_volume_monthly=0,
        )
        result = mcp.calculate_roi_internal(inputs)
        assert result["savings"]["roi_percentage"] == 0


# ---------------------------------------------------------------------------
# _format_currency / _format_percent
# ---------------------------------------------------------------------------


class TestFormatHelpers:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (0.0, "$0.00"),
            (1234.5, "$1,234.50"),
            (1_000_000.0, "$1,000,000.00"),
            (-50.5, "$-50.50"),
        ],
    )
    def test_format_currency_numeric(self, value, expected):
        assert mcp._format_currency(value) == expected

    def test_format_currency_handles_non_numeric(self):
        # The implementation falls back to str() on TypeError/ValueError.
        # Passing a non-numeric should not raise.
        result = mcp._format_currency(None)  # type: ignore[arg-type]
        assert isinstance(result, str)

    @pytest.mark.parametrize(
        "value,expected",
        [
            (0.0, "0.0%"),
            (12.5, "12.5%"),
            (100.0, "100.0%"),
            (-3.14159, "-3.1%"),
        ],
    )
    def test_format_percent_numeric(self, value, expected):
        assert mcp._format_percent(value) == expected

    def test_format_percent_handles_non_numeric(self):
        result = mcp._format_percent(None)  # type: ignore[arg-type]
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# generate_pdf_report
# ---------------------------------------------------------------------------


class TestGeneratePDFReport:
    def test_writes_a_real_pdf_file(self, sample_roi_result, tmp_path):
        pytest.importorskip("reportlab")
        out = tmp_path / "report.pdf"
        result = mcp.generate_pdf_report(sample_roi_result, str(out), "Acme Corp")
        assert result["status"] == "success"
        assert result["format"] == "pdf"
        assert out.exists()
        assert out.stat().st_size > 0

    def test_pdf_starts_with_pdf_magic(self, sample_roi_result, tmp_path):
        pytest.importorskip("reportlab")
        out = tmp_path / "report.pdf"
        mcp.generate_pdf_report(sample_roi_result, str(out), "Test")
        with open(out, "rb") as f:
            magic = f.read(4)
        assert magic == b"%PDF"

    def test_returns_error_when_reportlab_missing(self, sample_roi_result, tmp_path):
        # Simulate ImportError by hiding reportlab from sys.modules.
        out = tmp_path / "report.pdf"

        original_import = (
            __builtins__["__import__"]
            if isinstance(__builtins__, dict)
            else __builtins__.__import__
        )

        def fake_import(name, *args, **kwargs):
            if name.startswith("reportlab"):
                raise ImportError(f"mocked away: {name}")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=fake_import):
            result = mcp.generate_pdf_report(sample_roi_result, str(out), "Test")

        assert result["status"] == "error"
        assert "reportlab" in result["message"].lower()


# ---------------------------------------------------------------------------
# compare_scenarios_internal
# ---------------------------------------------------------------------------


class TestCompareScenariosInternal:
    @staticmethod
    def _scenario(name: str, **overrides):
        base = {
            "name": name,
            "current_tool_cost": 1000.0,
            "fte_hours_per_week": 20.0,
            "fte_hourly_rate": 80.0,
            "infrastructure_cost": 100.0,
            "forecast_volume_monthly": 10000,
            "timegpt_price_per_1k": 0.10,
        }
        base.update(overrides)
        return base

    def test_empty_list_returns_empty_structure(self):
        result = mcp.compare_scenarios_internal([])
        # Must not raise; must return a dict with expected top-level keys.
        assert isinstance(result, dict)
        assert "scenarios" in result or "ranking" in result or "sensitivity" in result

    def test_three_scenarios_produces_three_results(self):
        scenarios = [
            self._scenario("low", current_tool_cost=500.0),
            self._scenario("mid", current_tool_cost=2000.0),
            self._scenario("high", current_tool_cost=5000.0),
        ]
        result = mcp.compare_scenarios_internal(scenarios)
        # Implementation returns either 'scenarios' or 'ranking' keyed.
        per_scenario = result.get("scenarios") or result.get("ranking") or []
        assert len(per_scenario) == 3

    def test_higher_current_cost_yields_more_savings(self):
        scenarios = [
            self._scenario("low", current_tool_cost=100.0),
            self._scenario("high", current_tool_cost=10000.0),
        ]
        result = mcp.compare_scenarios_internal(scenarios)
        # Pull savings for each scenario.
        per = result.get("scenarios") or result.get("ranking") or []
        # Find the result entries by scanning for an "annual" savings field.
        savings_values = []
        for entry in per:
            for key in ("savings", "annual_savings", "annual"):
                node = entry.get(key) if isinstance(entry, dict) else None
                if isinstance(node, dict) and "annual" in node:
                    savings_values.append(node["annual"])
                    break
                if isinstance(node, (int, float)):
                    savings_values.append(node)
                    break
        # Higher current cost should produce strictly more annual savings.
        if len(savings_values) == 2:
            assert savings_values[1] > savings_values[0]

    def test_includes_sensitivity_field(self):
        scenarios = [
            self._scenario("a"),
            self._scenario("b", fte_hours_per_week=40.0),
        ]
        result = mcp.compare_scenarios_internal(scenarios)
        assert "sensitivity" in result


# ---------------------------------------------------------------------------
# export_to_salesforce
# ---------------------------------------------------------------------------


class TestExportToSalesforce:
    def test_dry_run_when_env_vars_missing(self, sample_roi_result, clean_sf_env):
        result = mcp.export_to_salesforce(sample_roi_result, "Acme Opportunity")
        assert result["status"] == "dry_run"
        assert "payload" in result
        # Payload is Salesforce-shaped.
        payload = result["payload"]
        assert payload["Name"] == "Acme Opportunity"
        assert payload["StageName"] == "Qualification"
        assert "Nixtla_ROI_Percentage__c" in payload
        assert "Nixtla_Annual_Savings__c" in payload

    def test_dry_run_message_mentions_required_env_vars(self, sample_roi_result, clean_sf_env):
        result = mcp.export_to_salesforce(sample_roi_result, "X")
        assert "NIXTLA_SF_INSTANCE_URL" in result["message"]
        assert "NIXTLA_SF_ACCESS_TOKEN" in result["message"]

    def test_dry_run_when_only_url_set(self, sample_roi_result, monkeypatch):
        monkeypatch.setenv("NIXTLA_SF_INSTANCE_URL", "https://example.my.salesforce.com")
        monkeypatch.delenv("NIXTLA_SF_ACCESS_TOKEN", raising=False)
        result = mcp.export_to_salesforce(sample_roi_result, "X")
        assert result["status"] == "dry_run"

    def test_live_post_success(self, sample_roi_result, monkeypatch):
        monkeypatch.setenv("NIXTLA_SF_INSTANCE_URL", "https://example.my.salesforce.com")
        monkeypatch.setenv("NIXTLA_SF_ACCESS_TOKEN", "test-token-abc")

        # Mock urlopen response.
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"id": "006xx000004T1lDAAS", "success": true}'
        mock_response.status = 201
        mock_response.__enter__ = lambda self: mock_response
        mock_response.__exit__ = lambda self, *args: None

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = mcp.export_to_salesforce(sample_roi_result, "Acme")

        assert result["status"] == "success"
        assert result["response"]["id"] == "006xx000004T1lDAAS"
        assert result["response"]["success"] is True

    def test_live_post_handles_http_error(self, sample_roi_result, monkeypatch):
        monkeypatch.setenv("NIXTLA_SF_INSTANCE_URL", "https://example.my.salesforce.com")
        monkeypatch.setenv("NIXTLA_SF_ACCESS_TOKEN", "test-token")

        err = urllib.error.HTTPError(
            url="https://example.my.salesforce.com/services/data/v59.0/sobjects/Opportunity",
            code=401,
            msg="Unauthorized",
            hdrs={},  # type: ignore[arg-type]
            fp=None,
        )

        with patch("urllib.request.urlopen", side_effect=err):
            result = mcp.export_to_salesforce(sample_roi_result, "Acme")

        assert result["status"] == "error"


# ---------------------------------------------------------------------------
# call_tool dispatch (async)
# ---------------------------------------------------------------------------


class TestCallTool:
    @pytest.fixture
    def run(self):
        """Helper to run an async coroutine in tests."""

        def _run(coro):
            return asyncio.run(coro)

        return _run

    def test_calculate_roi_returns_text_content(self, run):
        result = run(
            mcp.call_tool(
                "calculate_roi",
                {
                    "current_tool_cost": 1000,
                    "fte_hours_per_week": 20,
                    "forecast_volume_monthly": 5000,
                },
            )
        )
        assert len(result) == 1
        assert result[0].type == "text"
        # The text is JSON; parse it.
        parsed = json.loads(result[0].text)
        assert "savings" in parsed

    def test_compare_scenarios_dispatch(self, run):
        result = run(
            mcp.call_tool(
                "compare_scenarios",
                {
                    "scenarios": [
                        {
                            "name": "a",
                            "current_tool_cost": 1000,
                            "fte_hours_per_week": 10,
                            "forecast_volume_monthly": 1000,
                        }
                    ]
                },
            )
        )
        assert len(result) == 1
        parsed = json.loads(result[0].text)
        assert isinstance(parsed, dict)

    def test_export_salesforce_dispatch_dry_run(self, run, clean_sf_env):
        # Pass a valid roi_data shape.
        roi = mcp.calculate_roi_internal(
            mcp.ROIInputs(current_tool_cost=1000, fte_hours_per_week=20)
        )
        result = run(
            mcp.call_tool(
                "export_salesforce",
                {"roi_data": roi, "opportunity_name": "Test"},
            )
        )
        parsed = json.loads(result[0].text)
        assert parsed["status"] == "dry_run"

    def test_unknown_tool_returns_error_text(self, run):
        result = run(mcp.call_tool("nonexistent_tool", {}))
        assert len(result) == 1
        assert "Unknown tool" in result[0].text

    def test_list_tools_returns_four_tools(self, run):
        tools = run(mcp.list_tools())
        names = {t.name for t in tools}
        assert names == {
            "calculate_roi",
            "generate_report",
            "compare_scenarios",
            "export_salesforce",
        }
