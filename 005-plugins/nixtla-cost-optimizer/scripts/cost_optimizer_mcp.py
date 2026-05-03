#!/usr/bin/env python3
"""MCP Server for Nixtla Cost Optimizer.

Real cost-optimization for Nixtla TimeGPT customers. Analyzes API call
patterns, recommends optimizations, simulates batching impact, generates
hybrid TimeGPT + StatsForecast routing strategies, and exports reports.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

app = Server("nixtla-cost-optimizer")


# ---------------------------------------------------------------------------
# Tool: analyze_usage
# ---------------------------------------------------------------------------


def _payload_signature(call: dict) -> str:
    """Build a deterministic hash of the inputs that drive a TimeGPT call.

    Two calls with the same payload signature would return identical results,
    so they're cache candidates.
    """
    sig_keys = ("input_hash", "series_ids", "horizon", "freq", "model")
    parts = []
    for k in sig_keys:
        v = call.get(k)
        if v is not None:
            parts.append(f"{k}={json.dumps(v, sort_keys=True, default=str)}")
    blob = "|".join(parts)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def analyze_usage(api_calls: list[dict], cost_per_1k_series: float = 0.10) -> dict[str, Any]:
    """Analyze a list of TimeGPT API call records and surface patterns.

    Args:
        api_calls: list of dicts. Each call may carry: series_count (int),
            timestamp (ISO str / unix), horizon (int), freq (str), model (str),
            input_hash (str), series_ids (list[str]).
        cost_per_1k_series: TimeGPT pricing (default $0.10 per 1K series).

    Returns:
        Dict with totals, averages, and a list of detected opportunities
        keyed by type (batching / caching / single_series / high_frequency).
    """
    total_calls = len(api_calls)
    total_series = sum(int(c.get("series_count", 1)) for c in api_calls)
    estimated_cost = (total_series / 1000.0) * cost_per_1k_series

    avg_series_per_call = (total_series / total_calls) if total_calls else 0.0

    # Pattern detection.
    opportunities: list[dict[str, Any]] = []

    # Batching: many small calls are batchable.
    small_batch_calls = sum(1 for c in api_calls if int(c.get("series_count", 1)) < 10)
    if total_calls > 0 and small_batch_calls / total_calls > 0.3:
        opportunities.append(
            {
                "type": "batching",
                "description": (
                    f"{small_batch_calls}/{total_calls} calls have <10 series — "
                    f"batching reduces request overhead"
                ),
                "potential_savings_pct": min(60, int(50 * small_batch_calls / total_calls)),
                "evidence_count": small_batch_calls,
            }
        )

    # Caching: duplicate payload signatures.
    sigs = [_payload_signature(c) for c in api_calls]
    unique_sigs = len(set(sigs))
    redundant_calls = total_calls - unique_sigs
    if total_calls > 0 and redundant_calls / total_calls > 0.05:
        opportunities.append(
            {
                "type": "caching",
                "description": (
                    f"{redundant_calls}/{total_calls} calls are redundant duplicates — "
                    f"caching eliminates them"
                ),
                "potential_savings_pct": int(100 * redundant_calls / total_calls),
                "evidence_count": redundant_calls,
            }
        )

    # Single-series calls: candidate for the multi-series endpoint.
    single_series = sum(1 for c in api_calls if int(c.get("series_count", 1)) == 1)
    if total_calls > 0 and single_series / total_calls > 0.4:
        opportunities.append(
            {
                "type": "single_series",
                "description": (
                    f"{single_series}/{total_calls} calls forecast a single series — "
                    f"the multi-series endpoint is cheaper per-series"
                ),
                "potential_savings_pct": min(40, int(30 * single_series / total_calls)),
                "evidence_count": single_series,
            }
        )

    # High-frequency short-horizon: candidates for statsforecast.
    short_horizon = sum(1 for c in api_calls if int(c.get("horizon", 30)) <= 3)
    if total_calls > 0 and short_horizon / total_calls > 0.2:
        opportunities.append(
            {
                "type": "hybrid_short_horizon",
                "description": (
                    f"{short_horizon}/{total_calls} calls have horizon<=3 — "
                    f"these are candidates for statsforecast (faster, free)"
                ),
                "potential_savings_pct": int(20 * short_horizon / total_calls),
                "evidence_count": short_horizon,
            }
        )

    return {
        "total_calls": total_calls,
        "total_series": total_series,
        "avg_series_per_call": round(avg_series_per_call, 3),
        "estimated_monthly_cost_usd": round(estimated_cost, 4),
        "cost_per_1k_series": cost_per_1k_series,
        "opportunities": opportunities,
        "n_opportunities": len(opportunities),
    }


# ---------------------------------------------------------------------------
# Tool: recommend_optimizations
# ---------------------------------------------------------------------------


def recommend_optimizations(
    usage: dict[str, Any], cost_per_1k_series: float = 0.10
) -> dict[str, Any]:
    """Apply rule-based recommendations on `analyze_usage` output.

    Returns recommendations sorted by estimated USD savings (descending).
    """
    monthly_cost = float(usage.get("estimated_monthly_cost_usd", 0.0))
    opps = usage.get("opportunities", [])

    recs: list[dict[str, Any]] = []
    for i, opp in enumerate(opps, start=1):
        savings_pct = float(opp.get("potential_savings_pct", 0))
        savings_usd = round(monthly_cost * savings_pct / 100.0, 2)

        if opp["type"] == "caching":
            rec = {
                "id": f"rec_{i:03d}",
                "category": "caching",
                "title": "Add request caching",
                "description": opp["description"],
                "estimated_savings_pct": savings_pct,
                "estimated_savings_usd_per_month": savings_usd,
                "implementation_effort": "low",
                "implementation_steps": [
                    "Hash each (input_hash, horizon, freq, model) tuple",
                    "Store responses in Redis or local LRU with TTL=1h",
                    "Check cache before calling NixtlaClient.forecast",
                ],
                "validation_criteria": [
                    "Cache hit rate >= 5% in production",
                    "p99 latency unchanged on cache miss",
                ],
            }
        elif opp["type"] == "batching":
            rec = {
                "id": f"rec_{i:03d}",
                "category": "batching",
                "title": "Aggregate small calls into batches",
                "description": opp["description"],
                "estimated_savings_pct": savings_pct,
                "estimated_savings_usd_per_month": savings_usd,
                "implementation_effort": "medium",
                "implementation_steps": [
                    "Buffer calls in a 60-second window",
                    "Send up to 100 series per multi-series API call",
                    "Fan-out responses to original callers",
                ],
                "validation_criteria": [
                    "Average series_count per call >= 50 post-implementation",
                    "p95 end-to-end latency <= 60s + API call latency",
                ],
            }
        elif opp["type"] == "single_series":
            rec = {
                "id": f"rec_{i:03d}",
                "category": "endpoint",
                "title": "Switch to multi-series endpoint",
                "description": opp["description"],
                "estimated_savings_pct": savings_pct,
                "estimated_savings_usd_per_month": savings_usd,
                "implementation_effort": "low",
                "implementation_steps": [
                    "Group series by (freq, horizon)",
                    "Send each group as one NixtlaClient.forecast call with multi-series df",
                ],
                "validation_criteria": [
                    "Per-series API cost reduced",
                ],
            }
        elif opp["type"] == "hybrid_short_horizon":
            rec = {
                "id": f"rec_{i:03d}",
                "category": "hybrid",
                "title": "Route short-horizon calls to statsforecast",
                "description": opp["description"],
                "estimated_savings_pct": savings_pct,
                "estimated_savings_usd_per_month": savings_usd,
                "implementation_effort": "high",
                "implementation_steps": [
                    "Add a routing layer (route_forecast(metadata) -> 'timegpt'|'statsforecast')",
                    "Threshold: horizon <= 3 -> statsforecast (AutoETS)",
                    "Run accuracy comparison on a sample to verify quality",
                ],
                "validation_criteria": [
                    "sMAPE delta <= 2% vs all-TimeGPT baseline",
                    "Wall-time p50 <= 100ms for short-horizon calls",
                ],
            }
        else:
            continue
        recs.append(rec)

    recs.sort(key=lambda r: r["estimated_savings_usd_per_month"], reverse=True)

    total_pct = sum(r["estimated_savings_pct"] for r in recs)
    total_usd = round(sum(r["estimated_savings_usd_per_month"] for r in recs), 2)

    return {
        "recommendations": recs,
        "n_recommendations": len(recs),
        "total_estimated_savings_pct": min(95, total_pct),  # Cap at 95% (can't compound to 100+).
        "total_estimated_savings_usd_per_month": total_usd,
        "current_monthly_cost_usd": round(monthly_cost, 2),
    }


# ---------------------------------------------------------------------------
# Tool: simulate_batching
# ---------------------------------------------------------------------------


def simulate_batching(
    usage: dict[str, Any],
    batch_size: int = 100,
    batch_window_seconds: int = 60,
    cost_per_1k_series: float = 0.10,
) -> dict[str, Any]:
    """Simulate the cost impact of a batching strategy."""
    total_calls = int(usage.get("total_calls", 0))
    total_series = int(usage.get("total_series", 0))

    if total_calls == 0:
        return {
            "strategy": f"Batch up to {batch_size} series every {batch_window_seconds}s",
            "before": {"calls": 0, "cost_usd": 0.0},
            "after": {"calls": 0, "cost_usd": 0.0},
            "savings_pct": 0.0,
            "savings_usd": 0.0,
        }

    # After batching: ceil(total_series / batch_size) calls (per windowed group).
    # Cost is series-driven (still total_series) but per-call overhead is lower.
    # We model only the per-call savings since TimeGPT charges per-series; batching's
    # benefit here is request overhead amortization (auth, network, request setup).
    after_calls = max(1, (total_series + batch_size - 1) // batch_size)
    overhead_per_call_usd = 0.001  # nominal overhead model

    before_cost = (total_series / 1000.0) * cost_per_1k_series + (
        total_calls * overhead_per_call_usd
    )
    after_cost = (total_series / 1000.0) * cost_per_1k_series + (
        after_calls * overhead_per_call_usd
    )
    savings = before_cost - after_cost
    savings_pct = (savings / before_cost * 100.0) if before_cost > 0 else 0.0

    return {
        "strategy": f"Batch up to {batch_size} series every {batch_window_seconds}s",
        "before": {"calls": total_calls, "cost_usd": round(before_cost, 4)},
        "after": {"calls": after_calls, "cost_usd": round(after_cost, 4)},
        "savings_pct": round(savings_pct, 2),
        "savings_usd": round(savings, 4),
        "calls_eliminated": total_calls - after_calls,
    }


# ---------------------------------------------------------------------------
# Tool: generate_hybrid_strategy
# ---------------------------------------------------------------------------


def generate_hybrid_strategy(
    usage_profile: dict[str, Any] | None = None,
    timegpt_horizon_threshold: int = 14,
    timegpt_min_history: int = 100,
) -> dict[str, Any]:
    """Generate a routing strategy between TimeGPT and statsforecast.

    Args:
        usage_profile: Optional dict with `avg_horizon`, `n_series`, `latency_sla_seconds`,
            `accuracy_critical` keys. When provided, used to bias the routing thresholds.
        timegpt_horizon_threshold: Horizons >= this go to TimeGPT (default 14).
        timegpt_min_history: Series with < this many historical points go to TimeGPT
            (statsforecast struggles on sparse history).
    """
    profile = usage_profile or {}
    avg_horizon = int(profile.get("avg_horizon", 7))
    accuracy_critical = bool(profile.get("accuracy_critical", False))
    latency_sla = float(profile.get("latency_sla_seconds", 30.0))

    # Tune thresholds based on profile.
    if accuracy_critical:
        timegpt_horizon_threshold = max(7, timegpt_horizon_threshold - 4)
    if latency_sla < 1.0:
        # Real-time SLA — push more to statsforecast (faster local).
        timegpt_horizon_threshold = max(timegpt_horizon_threshold, 21)

    decision_code = f'''def route_forecast(series_metadata: dict) -> str:
    """Decide TimeGPT vs statsforecast for a single forecasting request.

    Args:
        series_metadata: dict with keys: horizon, history_length, has_exog,
            latency_sla_seconds, sparse_history.

    Returns:
        "timegpt" or "statsforecast".
    """
    horizon = series_metadata.get("horizon", 7)
    history = series_metadata.get("history_length", 0)
    has_exog = series_metadata.get("has_exog", False)
    sparse = series_metadata.get("sparse_history", False)

    # TimeGPT for long horizons, exogenous variables, or sparse history.
    if horizon >= {timegpt_horizon_threshold}:
        return "timegpt"
    if has_exog:
        return "timegpt"
    if sparse or history < {timegpt_min_history}:
        return "timegpt"

    # Otherwise statsforecast (faster, free, deterministic).
    return "statsforecast"
'''

    config = {
        "rules": [
            {"if": f"horizon >= {timegpt_horizon_threshold}", "then": "timegpt"},
            {"if": "has_exog == True", "then": "timegpt"},
            {
                "if": f"history_length < {timegpt_min_history} OR sparse_history == True",
                "then": "timegpt",
            },
            {"else": "statsforecast"},
        ],
        "default_engine": "statsforecast",
        "fallback_engine": "timegpt",
        "thresholds": {
            "timegpt_horizon_threshold": timegpt_horizon_threshold,
            "timegpt_min_history": timegpt_min_history,
        },
    }

    # Estimate split based on the profile.
    timegpt_pct_estimate = 30 if avg_horizon >= timegpt_horizon_threshold else 15
    statsforecast_pct_estimate = 100 - timegpt_pct_estimate

    return {
        "strategy": "Hybrid statsforecast + TimeGPT",
        "decision_code": decision_code,
        "config": config,
        "estimated_split": {
            "timegpt_pct": timegpt_pct_estimate,
            "statsforecast_pct": statsforecast_pct_estimate,
        },
    }


# ---------------------------------------------------------------------------
# Tool: export_report
# ---------------------------------------------------------------------------


def export_report(
    *,
    analysis: dict[str, Any] | None = None,
    recommendations: dict[str, Any] | None = None,
    hybrid_strategy: dict[str, Any] | None = None,
    batching_simulation: dict[str, Any] | None = None,
    format: str = "markdown",
) -> dict[str, Any]:
    """Compose a cost-optimization report from the prior tool outputs."""
    analysis = analysis or {}
    recommendations = recommendations or {}
    hybrid_strategy = hybrid_strategy or {}
    batching_simulation = batching_simulation or {}

    if format == "json":
        body = json.dumps(
            {
                "analysis": analysis,
                "recommendations": recommendations,
                "hybrid_strategy": hybrid_strategy,
                "batching_simulation": batching_simulation,
            },
            indent=2,
        )
        return {"format": "json", "content": body}

    if format == "csv":
        lines = ["id,category,title,savings_pct,savings_usd_per_month,effort"]
        for r in recommendations.get("recommendations", []):
            lines.append(
                f'{r["id"]},{r["category"]},"{r["title"]}",'
                f'{r["estimated_savings_pct"]},'
                f'{r["estimated_savings_usd_per_month"]},'
                f'{r["implementation_effort"]}'
            )
        return {"format": "csv", "content": "\n".join(lines)}

    # Default: markdown.
    md: list[str] = []
    md.append("# Nixtla Cost Optimization Report")
    md.append("")
    md.append("## Executive Summary")
    md.append("")
    monthly = analysis.get("estimated_monthly_cost_usd", 0.0)
    proj_savings = recommendations.get("total_estimated_savings_usd_per_month", 0.0)
    proj_pct = recommendations.get("total_estimated_savings_pct", 0)
    md.append(f"- **Current monthly cost**: ${monthly:,.2f}")
    md.append(f"- **Projected savings**: ${proj_savings:,.2f}/month ({proj_pct}% reduction)")
    md.append(f"- **Recommendations**: {recommendations.get('n_recommendations', 0)}")
    md.append("")

    md.append("## Detected Patterns")
    md.append("")
    md.append("| Type | Description | Savings |")
    md.append("|---|---|---|")
    for opp in analysis.get("opportunities", []):
        md.append(
            f"| {opp['type']} | {opp['description']} | " f"{opp.get('potential_savings_pct', 0)}% |"
        )
    md.append("")

    md.append("## Ranked Recommendations")
    md.append("")
    for r in recommendations.get("recommendations", []):
        md.append(f"### {r['id']} — {r['title']}")
        md.append("")
        md.append(f"- **Category**: {r['category']}")
        md.append(f"- **Effort**: {r['implementation_effort']}")
        md.append(
            f"- **Savings**: {r['estimated_savings_pct']}% "
            f"(${r['estimated_savings_usd_per_month']:,.2f}/month)"
        )
        md.append(f"- **Description**: {r['description']}")
        md.append("- **Steps**:")
        for s in r.get("implementation_steps", []):
            md.append(f"  - {s}")
        md.append("")

    if hybrid_strategy.get("decision_code"):
        md.append("## Hybrid Routing Strategy")
        md.append("")
        md.append("```python")
        md.append(hybrid_strategy["decision_code"])
        md.append("```")
        md.append("")
        split = hybrid_strategy.get("estimated_split", {})
        md.append(
            f"Estimated split: TimeGPT {split.get('timegpt_pct', '?')}% / "
            f"statsforecast {split.get('statsforecast_pct', '?')}%"
        )
        md.append("")

    if batching_simulation.get("strategy"):
        md.append("## Batching Simulation")
        md.append("")
        md.append(f"Strategy: {batching_simulation['strategy']}")
        before = batching_simulation.get("before", {})
        after = batching_simulation.get("after", {})
        md.append(f"- Before: {before.get('calls', 0)} calls, ${before.get('cost_usd', 0):.4f}")
        md.append(f"- After: {after.get('calls', 0)} calls, ${after.get('cost_usd', 0):.4f}")
        md.append(
            f"- Savings: {batching_simulation.get('savings_pct', 0)}% "
            f"(${batching_simulation.get('savings_usd', 0):.4f})"
        )

    return {"format": "markdown", "content": "\n".join(md)}


# ---------------------------------------------------------------------------
# MCP server surface
# ---------------------------------------------------------------------------


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_usage",
            description="Analyze TimeGPT API usage patterns from a list of call records.",
            inputSchema={
                "type": "object",
                "properties": {
                    "api_calls": {
                        "type": "array",
                        "description": "List of call records with series_count, horizon, "
                        "freq, model, input_hash, etc.",
                    },
                    "cost_per_1k_series": {
                        "type": "number",
                        "default": 0.10,
                    },
                },
                "required": ["api_calls"],
            },
        ),
        Tool(
            name="recommend_optimizations",
            description="Generate ranked optimization recommendations from analyze_usage output.",
            inputSchema={
                "type": "object",
                "properties": {
                    "usage": {"type": "object"},
                    "cost_per_1k_series": {"type": "number", "default": 0.10},
                },
                "required": ["usage"],
            },
        ),
        Tool(
            name="simulate_batching",
            description="Simulate cost reduction from a batching strategy.",
            inputSchema={
                "type": "object",
                "properties": {
                    "usage": {"type": "object"},
                    "batch_size": {"type": "integer", "default": 100},
                    "batch_window_seconds": {"type": "integer", "default": 60},
                    "cost_per_1k_series": {"type": "number", "default": 0.10},
                },
                "required": ["usage"],
            },
        ),
        Tool(
            name="generate_hybrid_strategy",
            description="Generate a TimeGPT + statsforecast routing strategy with code + config.",
            inputSchema={
                "type": "object",
                "properties": {
                    "usage_profile": {"type": "object"},
                    "timegpt_horizon_threshold": {"type": "integer", "default": 14},
                    "timegpt_min_history": {"type": "integer", "default": 100},
                },
            },
        ),
        Tool(
            name="export_report",
            description="Compose a markdown / json / csv report from prior tool outputs.",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis": {"type": "object"},
                    "recommendations": {"type": "object"},
                    "hybrid_strategy": {"type": "object"},
                    "batching_simulation": {"type": "object"},
                    "format": {
                        "type": "string",
                        "enum": ["markdown", "json", "csv"],
                        "default": "markdown",
                    },
                },
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "analyze_usage":
        result = analyze_usage(
            arguments.get("api_calls", []),
            cost_per_1k_series=float(arguments.get("cost_per_1k_series", 0.10)),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "recommend_optimizations":
        result = recommend_optimizations(
            arguments.get("usage", {}),
            cost_per_1k_series=float(arguments.get("cost_per_1k_series", 0.10)),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "simulate_batching":
        result = simulate_batching(
            arguments.get("usage", {}),
            batch_size=int(arguments.get("batch_size", 100)),
            batch_window_seconds=int(arguments.get("batch_window_seconds", 60)),
            cost_per_1k_series=float(arguments.get("cost_per_1k_series", 0.10)),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "generate_hybrid_strategy":
        result = generate_hybrid_strategy(
            usage_profile=arguments.get("usage_profile"),
            timegpt_horizon_threshold=int(arguments.get("timegpt_horizon_threshold", 14)),
            timegpt_min_history=int(arguments.get("timegpt_min_history", 100)),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "export_report":
        result = export_report(
            analysis=arguments.get("analysis"),
            recommendations=arguments.get("recommendations"),
            hybrid_strategy=arguments.get("hybrid_strategy"),
            batching_simulation=arguments.get("batching_simulation"),
            format=str(arguments.get("format", "markdown")),
        )
        return [TextContent(type="text", text=result["content"])]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
