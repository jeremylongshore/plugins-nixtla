#!/usr/bin/env python3
"""MCP Server for Nixtla ROI Calculator.

Exposes 4 tools:
- calculate_roi: Run ROI calculation with inputs
- generate_report: Create PDF/PowerPoint report
- compare_scenarios: Compare build vs buy approaches
- export_salesforce: Export to Salesforce format
"""

import json
import os
import statistics
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

app = Server("nixtla-roi-calculator")


@dataclass
class ROIInputs:
    """ROI calculation inputs."""

    current_tool_cost: float = 0.0
    fte_hours_per_week: float = 0.0
    fte_hourly_rate: float = 75.0
    infrastructure_cost: float = 0.0
    forecast_volume_monthly: int = 1000
    timegpt_price_per_1k: float = 0.10


def calculate_roi_internal(inputs: ROIInputs) -> dict[str, Any]:
    """Calculate 3-year ROI comparison."""
    # Current annual costs
    current_tool_annual = inputs.current_tool_cost * 12
    current_fte_annual = inputs.fte_hours_per_week * 52 * inputs.fte_hourly_rate
    current_infra_annual = inputs.infrastructure_cost * 12
    current_total_annual = current_tool_annual + current_fte_annual + current_infra_annual

    # TimeGPT annual costs
    timegpt_annual = (inputs.forecast_volume_monthly * 12 * inputs.timegpt_price_per_1k) / 1000
    timegpt_fte_reduction = 0.7  # 70% reduction in FTE time
    timegpt_fte_annual = current_fte_annual * (1 - timegpt_fte_reduction)
    timegpt_total_annual = timegpt_annual + timegpt_fte_annual

    # ROI calculation
    annual_savings = current_total_annual - timegpt_total_annual
    roi_percentage = (
        (annual_savings / current_total_annual) * 100 if current_total_annual > 0 else 0
    )
    payback_months = 1 if annual_savings > 0 else float("inf")

    return {
        "current_costs": {
            "tool_annual": current_tool_annual,
            "fte_annual": current_fte_annual,
            "infrastructure_annual": current_infra_annual,
            "total_annual": current_total_annual,
            "total_3year": current_total_annual * 3,
        },
        "timegpt_costs": {
            "api_annual": timegpt_annual,
            "fte_annual": timegpt_fte_annual,
            "total_annual": timegpt_total_annual,
            "total_3year": timegpt_total_annual * 3,
        },
        "savings": {
            "annual": annual_savings,
            "3year": annual_savings * 3,
            "roi_percentage": roi_percentage,
            "payback_months": payback_months,
        },
    }


def _format_currency(value: float) -> str:
    """Format a numeric value as a USD string (e.g. ``$12,345.67``)."""
    try:
        return f"${value:,.2f}"
    except (TypeError, ValueError):
        return str(value)


def _format_percent(value: float) -> str:
    """Format a numeric value as a percent string with one decimal."""
    try:
        return f"{value:.1f}%"
    except (TypeError, ValueError):
        return str(value)


def generate_pdf_report(
    roi_data: dict[str, Any],
    output_path: str,
    opportunity_name: str = "TimeGPT ROI Analysis",
) -> dict[str, Any]:
    """Generate a real PDF ROI report from ``calculate_roi_internal`` output.

    Sections produced:
        * Title page (opportunity name + tagline)
        * Executive summary (3-year ROI %, payback period, NPV-style 3-year savings)
        * Cost breakdown table (current vs TimeGPT, annual + 3-year)
        * FTE savings table (current vs TimeGPT FTE annual cost)
        * Recommendations bullets

    Args:
        roi_data: Dict matching the schema returned by ``calculate_roi_internal``
            (top-level keys ``current_costs``, ``timegpt_costs``, ``savings``).
        output_path: Filesystem path to write the PDF to.
        opportunity_name: Title shown on the cover page.

    Returns:
        Dict with keys ``status`` (``"success"`` or ``"error"``), ``output_path``,
        ``format`` (``"pdf"``), and a human-readable ``message``. When reportlab
        is unavailable, returns ``status="error"`` with an installation hint
        rather than raising.
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError:
        return {
            "status": "error",
            "output_path": output_path,
            "format": "pdf",
            "message": (
                "install reportlab to enable PDF export " "(pip install 'reportlab>=4.0.0')"
            ),
        }

    current = roi_data.get("current_costs", {})
    timegpt = roi_data.get("timegpt_costs", {})
    savings = roi_data.get("savings", {})

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story: list[Any] = []

    # --- Title page ---
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph(opportunity_name, styles["Title"]))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("TimeGPT vs Build-Your-Own Forecasting", styles["Heading2"]))
    story.append(Spacer(1, 0.25 * inch))
    story.append(
        Paragraph(
            "Generated by nixtla-roi-calculator",
            styles["Normal"],
        )
    )
    story.append(PageBreak())

    # --- Executive summary ---
    story.append(Paragraph("Executive Summary", styles["Heading1"]))
    story.append(Spacer(1, 0.2 * inch))
    payback = savings.get("payback_months", float("inf"))
    payback_str = (
        f"{payback:.1f} months"
        if isinstance(payback, (int, float)) and payback != float("inf")
        else "no payback (savings <= 0)"
    )
    summary_rows = [
        ["Metric", "Value"],
        ["3-year ROI", _format_percent(savings.get("roi_percentage", 0.0))],
        ["Payback Period", payback_str],
        ["Annual Savings", _format_currency(savings.get("annual", 0.0))],
        ["3-year Savings (NPV-equivalent)", _format_currency(savings.get("3year", 0.0))],
    ]
    summary_table = Table(summary_rows, colWidths=[3 * inch, 2.5 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a4480")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 0.3 * inch))

    # --- Cost breakdown ---
    story.append(Paragraph("Cost Breakdown", styles["Heading1"]))
    story.append(Spacer(1, 0.2 * inch))
    cost_rows = [
        ["Cost Category", "Current (Annual)", "TimeGPT (Annual)", "3-year Delta"],
        [
            "Tool / API",
            _format_currency(current.get("tool_annual", 0.0)),
            _format_currency(timegpt.get("api_annual", 0.0)),
            _format_currency(
                (current.get("tool_annual", 0.0) - timegpt.get("api_annual", 0.0)) * 3
            ),
        ],
        [
            "FTE",
            _format_currency(current.get("fte_annual", 0.0)),
            _format_currency(timegpt.get("fte_annual", 0.0)),
            _format_currency((current.get("fte_annual", 0.0) - timegpt.get("fte_annual", 0.0)) * 3),
        ],
        [
            "Infrastructure",
            _format_currency(current.get("infrastructure_annual", 0.0)),
            _format_currency(0.0),
            _format_currency(current.get("infrastructure_annual", 0.0) * 3),
        ],
        [
            "Total",
            _format_currency(current.get("total_annual", 0.0)),
            _format_currency(timegpt.get("total_annual", 0.0)),
            _format_currency(savings.get("3year", 0.0)),
        ],
    ]
    cost_table = Table(cost_rows, colWidths=[1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch])
    cost_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a4480")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e8eef7")),
            ]
        )
    )
    story.append(cost_table)
    story.append(Spacer(1, 0.3 * inch))

    # --- FTE savings ---
    story.append(Paragraph("FTE Savings", styles["Heading1"]))
    story.append(Spacer(1, 0.2 * inch))
    fte_current = current.get("fte_annual", 0.0)
    fte_timegpt = timegpt.get("fte_annual", 0.0)
    fte_reduction_pct = (
        ((fte_current - fte_timegpt) / fte_current * 100) if fte_current > 0 else 0.0
    )
    fte_rows = [
        ["Metric", "Value"],
        ["Current FTE Cost (Annual)", _format_currency(fte_current)],
        ["TimeGPT FTE Cost (Annual)", _format_currency(fte_timegpt)],
        ["FTE Cost Reduction", _format_percent(fte_reduction_pct)],
        ["3-year FTE Savings", _format_currency((fte_current - fte_timegpt) * 3)],
    ]
    fte_table = Table(fte_rows, colWidths=[3 * inch, 2.5 * inch])
    fte_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a4480")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]
        )
    )
    story.append(fte_table)
    story.append(Spacer(1, 0.3 * inch))

    # --- Recommendations ---
    story.append(Paragraph("Recommendations", styles["Heading1"]))
    story.append(Spacer(1, 0.15 * inch))
    roi_pct = savings.get("roi_percentage", 0.0)
    if roi_pct >= 50:
        recs = [
            "Strong ROI case — proceed with TimeGPT pilot in next quarter.",
            "Prioritize migration of highest-volume forecasting workloads first.",
            "Reinvest freed FTE capacity into adjacent ML initiatives.",
        ]
    elif roi_pct >= 15:
        recs = [
            "Moderate ROI — pilot on a single business unit before company-wide rollout.",
            "Validate FTE reduction assumptions with a 90-day measured trial.",
            "Negotiate volume pricing if forecast volume exceeds 100k/month.",
        ]
    else:
        recs = [
            "Marginal ROI — re-examine FTE hours and infrastructure assumptions.",
            "Consider hybrid approach: TimeGPT for new use cases, retain existing for stable ones.",
            "Revisit calculation after 6 months as TimeGPT pricing/features evolve.",
        ]
    for rec in recs:
        story.append(Paragraph(f"&bull; {rec}", styles["Normal"]))
        story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    return {
        "status": "success",
        "output_path": output_path,
        "format": "pdf",
        "message": f"PDF report written to {output_path}",
    }


def compare_scenarios_internal(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    """Run ``calculate_roi_internal`` over multiple scenarios and analyze them.

    Args:
        scenarios: List of scenario dicts. Each scenario may contain a ``name``
            key plus any of the ``ROIInputs`` fields (``current_tool_cost``,
            ``fte_hours_per_week``, ``fte_hourly_rate``, ``infrastructure_cost``,
            ``forecast_volume_monthly``, ``timegpt_price_per_1k``). Missing
            inputs fall back to ``ROIInputs`` defaults.

    Returns:
        Dict with keys:
            * ``scenarios``: list of ``{name, inputs, metrics}`` per scenario
            * ``ranking``: scenario names ordered by 3-year ROI (highest first)
            * ``best_case``, ``worst_case``, ``median_case``: scenario name +
              3-year ROI
            * ``sensitivity``: which input variable shows the largest
              correlation with 3-year ROI (key ``most_influential_variable``,
              with per-variable Pearson coefficients in ``coefficients``)
    """
    if not scenarios:
        return {
            "scenarios": [],
            "ranking": [],
            "best_case": None,
            "worst_case": None,
            "median_case": None,
            "sensitivity": {"most_influential_variable": None, "coefficients": {}},
        }

    evaluated: list[dict[str, Any]] = []
    for idx, raw in enumerate(scenarios):
        name = raw.get("name", f"scenario_{idx + 1}")
        inputs = ROIInputs(
            current_tool_cost=float(raw.get("current_tool_cost", 0.0)),
            fte_hours_per_week=float(raw.get("fte_hours_per_week", 0.0)),
            fte_hourly_rate=float(raw.get("fte_hourly_rate", 75.0)),
            infrastructure_cost=float(raw.get("infrastructure_cost", 0.0)),
            forecast_volume_monthly=int(raw.get("forecast_volume_monthly", 1000)),
            timegpt_price_per_1k=float(raw.get("timegpt_price_per_1k", 0.10)),
        )
        metrics = calculate_roi_internal(inputs)
        evaluated.append(
            {
                "name": name,
                "inputs": {
                    "current_tool_cost": inputs.current_tool_cost,
                    "fte_hours_per_week": inputs.fte_hours_per_week,
                    "fte_hourly_rate": inputs.fte_hourly_rate,
                    "infrastructure_cost": inputs.infrastructure_cost,
                    "forecast_volume_monthly": inputs.forecast_volume_monthly,
                    "timegpt_price_per_1k": inputs.timegpt_price_per_1k,
                },
                "metrics": metrics,
            }
        )

    # Rank by 3-year savings (proxy for 3-year ROI dollars).
    ranked = sorted(
        evaluated,
        key=lambda s: s["metrics"]["savings"]["3year"],
        reverse=True,
    )
    ranking = [s["name"] for s in ranked]

    def _summary(item: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": item["name"],
            "roi_percentage": item["metrics"]["savings"]["roi_percentage"],
            "savings_3year": item["metrics"]["savings"]["3year"],
        }

    best_case = _summary(ranked[0])
    worst_case = _summary(ranked[-1])
    median_case = _summary(ranked[len(ranked) // 2])

    # Sensitivity: Pearson correlation between each input variable and 3-year savings.
    coefficients: dict[str, float] = {}
    most_influential: str | None = None
    if len(evaluated) >= 2:
        savings_series = [s["metrics"]["savings"]["3year"] for s in evaluated]
        variables = [
            "current_tool_cost",
            "fte_hours_per_week",
            "fte_hourly_rate",
            "infrastructure_cost",
            "forecast_volume_monthly",
            "timegpt_price_per_1k",
        ]
        for var in variables:
            series = [float(s["inputs"][var]) for s in evaluated]
            try:
                if statistics.pstdev(series) == 0 or statistics.pstdev(savings_series) == 0:
                    coefficients[var] = 0.0
                else:
                    coefficients[var] = statistics.correlation(series, savings_series)
            except (statistics.StatisticsError, ValueError):
                coefficients[var] = 0.0
        if coefficients:
            most_influential = max(coefficients, key=lambda k: abs(coefficients[k]))

    return {
        "scenarios": evaluated,
        "ranking": ranking,
        "best_case": best_case,
        "worst_case": worst_case,
        "median_case": median_case,
        "sensitivity": {
            "most_influential_variable": most_influential,
            "coefficients": coefficients,
        },
    }


def export_to_salesforce(
    roi_data: dict[str, Any],
    opportunity_name: str,
) -> dict[str, Any]:
    """Export an ROI calculation as a Salesforce Opportunity record.

    Reads ``NIXTLA_SF_INSTANCE_URL`` and ``NIXTLA_SF_ACCESS_TOKEN`` from the
    environment. When both are set, makes a POST to
    ``{instance_url}/services/data/v59.0/sobjects/Opportunity`` with the
    Salesforce-shaped payload and returns the live API response. When either
    is missing, returns ``status="dry_run"`` with the payload that would have
    been sent — so the caller can validate the shape without SF credentials.

    Args:
        roi_data: Dict matching the schema returned by ``calculate_roi_internal``.
        opportunity_name: Salesforce Opportunity ``Name`` field value.

    Returns:
        Dict with keys ``status`` (``"success"``, ``"dry_run"``, or ``"error"``),
        ``payload`` (the JSON sent / would-be-sent), and either ``response``
        (live API JSON on success) or ``message`` (error / dry-run hint).
    """
    savings = roi_data.get("savings", {})
    current = roi_data.get("current_costs", {})
    timegpt = roi_data.get("timegpt_costs", {})

    payload: dict[str, Any] = {
        "Name": opportunity_name,
        "StageName": "Qualification",
        "CloseDate": "2026-12-31",
        "Amount": float(savings.get("3year", 0.0)),
        "Description": (
            f"TimeGPT ROI analysis: "
            f"{_format_percent(savings.get('roi_percentage', 0.0))} 3-year ROI, "
            f"{_format_currency(savings.get('annual', 0.0))} annual savings, "
            f"{_format_currency(savings.get('3year', 0.0))} 3-year savings."
        ),
        "Nixtla_ROI_Percentage__c": float(savings.get("roi_percentage", 0.0)),
        "Nixtla_Annual_Savings__c": float(savings.get("annual", 0.0)),
        "Nixtla_3Year_Savings__c": float(savings.get("3year", 0.0)),
        "Nixtla_Payback_Months__c": (
            float(savings.get("payback_months", 0.0))
            if savings.get("payback_months") not in (None, float("inf"))
            else None
        ),
        "Nixtla_Current_Annual_Cost__c": float(current.get("total_annual", 0.0)),
        "Nixtla_TimeGPT_Annual_Cost__c": float(timegpt.get("total_annual", 0.0)),
    }

    instance_url = os.environ.get("NIXTLA_SF_INSTANCE_URL")
    access_token = os.environ.get("NIXTLA_SF_ACCESS_TOKEN")

    if not instance_url or not access_token:
        return {
            "status": "dry_run",
            "payload": payload,
            "message": (
                "configure NIXTLA_SF_INSTANCE_URL and NIXTLA_SF_ACCESS_TOKEN "
                "env vars for live export; here is the Salesforce-shaped "
                "JSON payload that would be sent"
            ),
        }

    url = f"{instance_url.rstrip('/')}/services/data/v59.0/sobjects/Opportunity"
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            try:
                response_json = json.loads(response_body) if response_body else {}
            except json.JSONDecodeError:
                response_json = {"raw": response_body}
            return {
                "status": "success",
                "payload": payload,
                "response": response_json,
                "message": (f"Salesforce Opportunity created " f"(HTTP {response.status})"),
            }
    except urllib.error.HTTPError as exc:
        try:
            error_body = exc.read().decode("utf-8")
        except Exception:
            error_body = ""
        return {
            "status": "error",
            "payload": payload,
            "message": f"Salesforce HTTP {exc.code}: {error_body or exc.reason}",
        }
    except urllib.error.URLError as exc:
        return {
            "status": "error",
            "payload": payload,
            "message": f"Salesforce request failed: {exc.reason}",
        }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available ROI calculator tools."""
    return [
        Tool(
            name="calculate_roi",
            description="Calculate TimeGPT ROI based on current costs",
            inputSchema={
                "type": "object",
                "properties": {
                    "current_tool_cost": {
                        "type": "number",
                        "description": "Monthly tool/license cost",
                    },
                    "fte_hours_per_week": {
                        "type": "number",
                        "description": "Data scientist hours/week on forecasting",
                    },
                    "fte_hourly_rate": {
                        "type": "number",
                        "description": "Hourly rate (default: $75)",
                    },
                    "infrastructure_cost": {
                        "type": "number",
                        "description": "Monthly infrastructure cost",
                    },
                    "forecast_volume_monthly": {
                        "type": "integer",
                        "description": "Monthly forecast API calls",
                    },
                },
                "required": ["current_tool_cost", "forecast_volume_monthly"],
            },
        ),
        Tool(
            name="generate_report",
            description="Generate PDF/PowerPoint ROI report",
            inputSchema={
                "type": "object",
                "properties": {
                    "roi_data": {"type": "object", "description": "ROI calculation results"},
                    "format": {
                        "type": "string",
                        "enum": ["pdf", "pptx"],
                        "description": "Output format",
                    },
                    "output_path": {"type": "string", "description": "Output file path"},
                },
                "required": ["roi_data", "format"],
            },
        ),
        Tool(
            name="compare_scenarios",
            description="Compare build vs buy scenarios",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenarios": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Scenarios to compare",
                    }
                },
                "required": ["scenarios"],
            },
        ),
        Tool(
            name="export_salesforce",
            description="Export ROI data to Salesforce opportunity format",
            inputSchema={
                "type": "object",
                "properties": {
                    "roi_data": {"type": "object", "description": "ROI calculation results"},
                    "opportunity_name": {
                        "type": "string",
                        "description": "Salesforce opportunity name",
                    },
                },
                "required": ["roi_data", "opportunity_name"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute ROI calculator tool."""
    if name == "calculate_roi":
        inputs = ROIInputs(
            current_tool_cost=arguments.get("current_tool_cost", 0),
            fte_hours_per_week=arguments.get("fte_hours_per_week", 0),
            fte_hourly_rate=arguments.get("fte_hourly_rate", 75),
            infrastructure_cost=arguments.get("infrastructure_cost", 0),
            forecast_volume_monthly=arguments.get("forecast_volume_monthly", 1000),
        )
        result = calculate_roi_internal(inputs)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "generate_report":
        roi_data = arguments.get("roi_data", {})
        output_path = arguments.get("output_path", "roi_report.pdf")
        opportunity_name = arguments.get("opportunity_name", "TimeGPT ROI Analysis")
        result = generate_pdf_report(roi_data, output_path, opportunity_name)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "compare_scenarios":
        scenarios = arguments.get("scenarios", [])
        result = compare_scenarios_internal(scenarios)
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

    elif name == "export_salesforce":
        roi_data = arguments.get("roi_data", {})
        opportunity_name = arguments.get("opportunity_name", "TimeGPT ROI Analysis")
        result = export_to_salesforce(roi_data, opportunity_name)
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
