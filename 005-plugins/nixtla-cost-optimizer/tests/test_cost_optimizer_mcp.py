"""Unit tests for nixtla-cost-optimizer MCP server."""

from __future__ import annotations

import asyncio
import json

import cost_optimizer_mcp as mcp
import pytest

# ---------------------------------------------------------------------------
# _payload_signature
# ---------------------------------------------------------------------------


class TestPayloadSignature:
    def test_identical_payloads_same_signature(self):
        a = {"input_hash": "x", "horizon": 7, "freq": "D"}
        b = {"input_hash": "x", "horizon": 7, "freq": "D"}
        assert mcp._payload_signature(a) == mcp._payload_signature(b)

    def test_different_payloads_different_signature(self):
        a = {"input_hash": "x", "horizon": 7, "freq": "D"}
        b = {"input_hash": "y", "horizon": 7, "freq": "D"}
        assert mcp._payload_signature(a) != mcp._payload_signature(b)

    def test_signature_is_short_hex(self):
        sig = mcp._payload_signature({"input_hash": "x"})
        assert isinstance(sig, str)
        assert len(sig) == 16


# ---------------------------------------------------------------------------
# analyze_usage
# ---------------------------------------------------------------------------


class TestAnalyzeUsage:
    def test_empty_calls_returns_zero_totals(self):
        result = mcp.analyze_usage([])
        assert result["total_calls"] == 0
        assert result["total_series"] == 0
        assert result["estimated_monthly_cost_usd"] == 0.0

    def test_totals_match_input(self):
        calls = [{"series_count": 10}, {"series_count": 20}, {"series_count": 30}]
        result = mcp.analyze_usage(calls)
        assert result["total_calls"] == 3
        assert result["total_series"] == 60

    def test_avg_series_per_call(self):
        calls = [{"series_count": 10}, {"series_count": 30}]
        result = mcp.analyze_usage(calls)
        assert result["avg_series_per_call"] == 20.0

    def test_cost_calculation(self):
        # 10000 series * $0.10 / 1000 = $1.00
        calls = [{"series_count": 10000}]
        result = mcp.analyze_usage(calls, cost_per_1k_series=0.10)
        assert result["estimated_monthly_cost_usd"] == pytest.approx(1.00)

    def test_batching_opportunity_detected(self, small_batch_calls):
        result = mcp.analyze_usage(small_batch_calls)
        types = {o["type"] for o in result["opportunities"]}
        assert "batching" in types

    def test_caching_opportunity_detected(self, redundant_calls):
        result = mcp.analyze_usage(redundant_calls)
        types = {o["type"] for o in result["opportunities"]}
        assert "caching" in types

    def test_short_horizon_opportunity_detected(self, short_horizon_calls):
        result = mcp.analyze_usage(short_horizon_calls)
        types = {o["type"] for o in result["opportunities"]}
        assert "hybrid_short_horizon" in types

    def test_n_opportunities_matches_list(self, small_batch_calls):
        result = mcp.analyze_usage(small_batch_calls)
        assert result["n_opportunities"] == len(result["opportunities"])


# ---------------------------------------------------------------------------
# recommend_optimizations
# ---------------------------------------------------------------------------


class TestRecommendOptimizations:
    def test_no_opportunities_returns_empty_recs(self):
        usage = {"opportunities": [], "estimated_monthly_cost_usd": 100.0}
        result = mcp.recommend_optimizations(usage)
        assert result["recommendations"] == []
        assert result["n_recommendations"] == 0

    def test_caching_opportunity_produces_caching_rec(self):
        usage = {
            "estimated_monthly_cost_usd": 100.0,
            "opportunities": [
                {"type": "caching", "description": "test", "potential_savings_pct": 25}
            ],
        }
        result = mcp.recommend_optimizations(usage)
        assert result["n_recommendations"] == 1
        assert result["recommendations"][0]["category"] == "caching"

    def test_savings_usd_computed_from_pct(self):
        usage = {
            "estimated_monthly_cost_usd": 200.0,
            "opportunities": [
                {"type": "batching", "description": "x", "potential_savings_pct": 30}
            ],
        }
        result = mcp.recommend_optimizations(usage)
        # 30% of $200 = $60
        assert result["recommendations"][0]["estimated_savings_usd_per_month"] == 60.0

    def test_recommendations_sorted_by_savings_desc(self):
        usage = {
            "estimated_monthly_cost_usd": 100.0,
            "opportunities": [
                {"type": "batching", "description": "b", "potential_savings_pct": 10},
                {"type": "caching", "description": "c", "potential_savings_pct": 50},
                {"type": "single_series", "description": "s", "potential_savings_pct": 25},
            ],
        }
        result = mcp.recommend_optimizations(usage)
        savings = [r["estimated_savings_usd_per_month"] for r in result["recommendations"]]
        assert savings == sorted(savings, reverse=True)

    def test_total_savings_capped_at_95pct(self):
        # Create opportunities that would individually sum > 100%.
        usage = {
            "estimated_monthly_cost_usd": 100.0,
            "opportunities": [
                {"type": "caching", "description": "x", "potential_savings_pct": 60},
                {"type": "batching", "description": "x", "potential_savings_pct": 60},
            ],
        }
        result = mcp.recommend_optimizations(usage)
        assert result["total_estimated_savings_pct"] <= 95


# ---------------------------------------------------------------------------
# simulate_batching
# ---------------------------------------------------------------------------


class TestSimulateBatching:
    def test_zero_calls_returns_zero(self):
        result = mcp.simulate_batching({"total_calls": 0, "total_series": 0})
        assert result["before"]["calls"] == 0
        assert result["after"]["calls"] == 0
        assert result["savings_pct"] == 0.0

    def test_batching_reduces_call_count(self):
        usage = {"total_calls": 1000, "total_series": 2000}
        result = mcp.simulate_batching(usage, batch_size=100)
        # 2000 series / 100 per batch = 20 calls.
        assert result["after"]["calls"] == 20
        assert result["after"]["calls"] < result["before"]["calls"]

    def test_calls_eliminated_field(self):
        usage = {"total_calls": 1000, "total_series": 2000}
        result = mcp.simulate_batching(usage, batch_size=100)
        assert result["calls_eliminated"] == 1000 - 20

    def test_savings_positive_when_calls_drop(self):
        usage = {"total_calls": 1000, "total_series": 2000}
        result = mcp.simulate_batching(usage, batch_size=100)
        assert result["savings_pct"] > 0
        assert result["savings_usd"] > 0


# ---------------------------------------------------------------------------
# generate_hybrid_strategy
# ---------------------------------------------------------------------------


class TestGenerateHybridStrategy:
    def test_returns_decision_code_and_config(self):
        result = mcp.generate_hybrid_strategy()
        assert "decision_code" in result
        assert "config" in result
        assert "rules" in result["config"]
        assert isinstance(result["decision_code"], str)
        assert "def route_forecast" in result["decision_code"]

    def test_accuracy_critical_lowers_threshold(self):
        normal = mcp.generate_hybrid_strategy(usage_profile={"accuracy_critical": False})
        critical = mcp.generate_hybrid_strategy(usage_profile={"accuracy_critical": True})
        normal_thr = normal["config"]["thresholds"]["timegpt_horizon_threshold"]
        critical_thr = critical["config"]["thresholds"]["timegpt_horizon_threshold"]
        assert critical_thr <= normal_thr

    def test_realtime_sla_raises_threshold(self):
        result = mcp.generate_hybrid_strategy(usage_profile={"latency_sla_seconds": 0.5})
        # Real-time SLA pushes the threshold up (more goes to statsforecast).
        assert result["config"]["thresholds"]["timegpt_horizon_threshold"] >= 21

    def test_estimated_split_sums_to_100(self):
        result = mcp.generate_hybrid_strategy()
        split = result["estimated_split"]
        assert split["timegpt_pct"] + split["statsforecast_pct"] == 100


# ---------------------------------------------------------------------------
# export_report
# ---------------------------------------------------------------------------


class TestExportReport:
    @pytest.fixture
    def sample_outputs(self):
        return {
            "analysis": {
                "total_calls": 100,
                "total_series": 5000,
                "estimated_monthly_cost_usd": 0.50,
                "opportunities": [
                    {
                        "type": "batching",
                        "description": "small batches",
                        "potential_savings_pct": 40,
                    }
                ],
            },
            "recommendations": {
                "recommendations": [
                    {
                        "id": "rec_001",
                        "category": "batching",
                        "title": "Aggregate small calls",
                        "description": "x",
                        "estimated_savings_pct": 40,
                        "estimated_savings_usd_per_month": 0.20,
                        "implementation_effort": "medium",
                        "implementation_steps": ["step 1", "step 2"],
                    }
                ],
                "n_recommendations": 1,
                "total_estimated_savings_pct": 40,
                "total_estimated_savings_usd_per_month": 0.20,
                "current_monthly_cost_usd": 0.50,
            },
            "hybrid_strategy": mcp.generate_hybrid_strategy(),
            "batching_simulation": {
                "strategy": "Batch up to 100 series every 60s",
                "before": {"calls": 1000, "cost_usd": 0.5},
                "after": {"calls": 50, "cost_usd": 0.45},
                "savings_pct": 10.0,
                "savings_usd": 0.05,
            },
        }

    def test_markdown_format(self, sample_outputs):
        result = mcp.export_report(format="markdown", **sample_outputs)
        assert result["format"] == "markdown"
        assert "# Nixtla Cost Optimization Report" in result["content"]
        assert "rec_001" in result["content"]

    def test_json_format(self, sample_outputs):
        result = mcp.export_report(format="json", **sample_outputs)
        assert result["format"] == "json"
        parsed = json.loads(result["content"])
        assert "analysis" in parsed
        assert "recommendations" in parsed

    def test_csv_format(self, sample_outputs):
        result = mcp.export_report(format="csv", **sample_outputs)
        assert result["format"] == "csv"
        assert "id,category,title,savings_pct" in result["content"]
        assert "rec_001" in result["content"]


# ---------------------------------------------------------------------------
# call_tool dispatch
# ---------------------------------------------------------------------------


class TestCallTool:
    @pytest.fixture
    def run(self):
        def _run(coro):
            return asyncio.run(coro)

        return _run

    def test_analyze_usage_dispatch(self, run, small_batch_calls):
        result = run(mcp.call_tool("analyze_usage", {"api_calls": small_batch_calls}))
        parsed = json.loads(result[0].text)
        assert "total_calls" in parsed

    def test_unknown_tool(self, run):
        result = run(mcp.call_tool("nope", {}))
        assert "Unknown" in result[0].text

    def test_list_tools_includes_all_five(self, run):
        tools = run(mcp.list_tools())
        names = {t.name for t in tools}
        assert names == {
            "analyze_usage",
            "recommend_optimizations",
            "simulate_batching",
            "generate_hybrid_strategy",
            "export_report",
        }
