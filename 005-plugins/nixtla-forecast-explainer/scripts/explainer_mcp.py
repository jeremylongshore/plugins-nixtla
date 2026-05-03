#!/usr/bin/env python3
"""MCP Server for Nixtla Forecast Explainer.

Generates plain-English explanations of TimeGPT forecasts.
"""

import json
from typing import Any

import numpy as np
import pandas as pd
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from scipy import stats
from statsmodels.tsa.seasonal import STL

app = Server("nixtla-forecast-explainer")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _coerce_series(data: Any, value_key: str = "y") -> pd.Series:
    """Coerce a variety of series-like inputs into a 1-D pandas Series of floats.

    Accepts:
        - list[float] / list[int]
        - list[dict] with `ds` and `value_key` keys
        - dict with `ds` and `value_key` arrays
        - pandas DataFrame with `ds` and `value_key` columns
        - pandas Series

    Args:
        data: The series-like input to coerce.
        value_key: Column name to extract from dict / DataFrame inputs.

    Returns:
        A 1-D pandas Series of float64 values, indexed by ds when available
        (datetime if parseable, otherwise position).
    """
    if isinstance(data, pd.Series):
        return data.astype(float)

    if isinstance(data, pd.DataFrame):
        if value_key not in data.columns:
            raise ValueError(f"DataFrame missing required column '{value_key}'")
        if "ds" in data.columns:
            ds = pd.to_datetime(data["ds"], errors="coerce")
            series = pd.Series(data[value_key].astype(float).values, index=ds)
        else:
            series = data[value_key].astype(float).reset_index(drop=True)
        return series

    if isinstance(data, dict):
        if value_key not in data:
            raise ValueError(f"Dict missing required key '{value_key}'")
        values = list(data[value_key])
        if "ds" in data:
            ds = pd.to_datetime(list(data["ds"]), errors="coerce")
            return pd.Series([float(v) for v in values], index=ds)
        return pd.Series([float(v) for v in values])

    if isinstance(data, list):
        if not data:
            return pd.Series([], dtype=float)
        first = data[0]
        if isinstance(first, dict):
            values = [float(row[value_key]) for row in data]
            if "ds" in first:
                ds = pd.to_datetime([row["ds"] for row in data], errors="coerce")
                return pd.Series(values, index=ds)
            return pd.Series(values)
        return pd.Series([float(v) for v in data])

    raise TypeError(f"Unsupported series input type: {type(data).__name__}")


def _infer_period(series: pd.Series, default: int = 7) -> int:
    """Infer a seasonal period from a Series' DatetimeIndex when possible.

    Falls back to ``default`` (7, weekly) when the index is not a DatetimeIndex
    or when the inferred frequency is not recognized. STL requires period >= 2.

    Args:
        series: Source series whose index may carry frequency information.
        default: Period to use when inference fails.

    Returns:
        An integer >= 2 suitable for STL's ``period`` argument.
    """
    if isinstance(series.index, pd.DatetimeIndex):
        freq = series.index.inferred_freq
        if freq is None:
            freq = pd.infer_freq(series.index) if len(series.index) >= 3 else None
        if freq is not None:
            f = freq.upper().split("-")[0]
            mapping = {
                "H": 24,
                "D": 7,
                "B": 5,
                "W": 52,
                "M": 12,
                "MS": 12,
                "Q": 4,
                "QS": 4,
                "A": 1,
                "Y": 1,
                "AS": 1,
                "YS": 1,
            }
            if f in mapping:
                return max(2, mapping[f])
    return max(2, default)


def _strength(component: np.ndarray, residual: np.ndarray) -> float:
    """Hyndman strength-of-component measure.

    Defined as ``max(0, 1 - var(R) / var(R + C))`` where R is the residual
    and C is the trend or seasonal component. Bounded to [0, 1].

    Args:
        component: Trend or seasonal component (numpy array).
        residual: STL residual component (numpy array).

    Returns:
        Float strength in ``[0, 1]``. ``0.0`` if denominator is zero or NaN.
    """
    combined = residual + component
    denom = float(np.var(combined))
    if denom == 0 or not np.isfinite(denom):
        return 0.0
    num = float(np.var(residual))
    return float(max(0.0, min(1.0, 1.0 - (num / denom))))


# ---------------------------------------------------------------------------
# Tool: decompose_forecast
# ---------------------------------------------------------------------------


def decompose_forecast(
    data: Any, period: int | None = None, value_key: str = "y"
) -> dict[str, Any]:
    """STL-decompose a time series into trend, seasonal, and residual components.

    Uses ``statsmodels.tsa.seasonal.STL`` (robust=True) with the supplied or
    inferred seasonal period. Strength metrics follow Hyndman & Athanasopoulos
    (Forecasting: Principles and Practice, 3e, Ch. 6.7).

    Args:
        data: Series-like input (DataFrame with ``ds``/``y`` columns, list of
            dicts, dict of arrays, list of floats, or pandas Series).
        period: Optional integer seasonal period. When ``None``, inferred from
            the series' DatetimeIndex frequency (default 7 if not inferable).
        value_key: Column / key for the target values when not the default ``y``.

    Returns:
        Dict with:
            - ``trend``: list[float], length = len(series)
            - ``seasonal``: list[float]
            - ``residual``: list[float]
            - ``strength_of_trend``: float in [0, 1]
            - ``strength_of_seasonality``: float in [0, 1]
            - ``period``: int, the seasonal period actually used
            - ``n_obs``: int, observations decomposed
    """
    series = _coerce_series(data, value_key=value_key)
    if len(series) < 4:
        raise ValueError(f"STL requires at least 4 observations; received {len(series)}.")

    used_period = int(period) if period is not None else _infer_period(series)
    if used_period < 2:
        raise ValueError(f"period must be >= 2; got {used_period}")
    if len(series) < 2 * used_period:
        raise ValueError(
            f"STL requires at least 2 full seasonal cycles "
            f"({2 * used_period} obs for period={used_period}); "
            f"received {len(series)}."
        )

    stl_result = STL(series.values.astype(float), period=used_period, robust=True).fit()

    trend = np.asarray(stl_result.trend, dtype=float)
    seasonal = np.asarray(stl_result.seasonal, dtype=float)
    residual = np.asarray(stl_result.resid, dtype=float)

    return {
        "trend": trend.tolist(),
        "seasonal": seasonal.tolist(),
        "residual": residual.tolist(),
        "strength_of_trend": _strength(trend, residual),
        "strength_of_seasonality": _strength(seasonal, residual),
        "period": used_period,
        "n_obs": int(len(series)),
    }


# ---------------------------------------------------------------------------
# Tool: identify_drivers
# ---------------------------------------------------------------------------


def identify_drivers(
    target: Any,
    candidates: dict[str, Any],
    max_lag: int = 7,
    value_key: str = "y",
) -> dict[str, Any]:
    """Rank candidate exogenous series by Pearson correlation with the target.

    For each candidate, scans lags 0..``max_lag`` (candidate is shifted forward,
    i.e., predictor leads the target by k) and reports the lag whose absolute
    correlation is largest. Lag 0 means contemporaneous; lag k > 0 means the
    candidate at time t-k aligns with the target at time t (predictor leads).

    Args:
        target: Target series (DataFrame / list / dict / Series; see
            :func:`_coerce_series`).
        candidates: Mapping of driver name to series-like input. All candidates
            are aligned to the target's length (trimmed or NaN-padded as
            needed by pandas).
        max_lag: Maximum lag (in periods) to scan, inclusive. Defaults to 7.
        value_key: Column / key for target values when not the default ``y``.

    Returns:
        Dict with:
            - ``drivers``: list of driver dicts, sorted by ``abs(correlation)``
              descending. Each entry has ``name``, ``correlation``, ``p_value``,
              and ``lag_optimal`` keys.
            - ``n_candidates``: count of candidates evaluated.
            - ``max_lag``: the lag scan ceiling actually used.
    """
    if max_lag < 0:
        raise ValueError(f"max_lag must be >= 0; got {max_lag}")

    y = _coerce_series(target, value_key=value_key).reset_index(drop=True)
    if len(y) < 3:
        raise ValueError(
            f"Need at least 3 target observations to compute correlation; got {len(y)}."
        )

    drivers: list[dict[str, Any]] = []
    for name, series_input in candidates.items():
        try:
            x = _coerce_series(series_input, value_key=value_key).reset_index(drop=True)
        except (ValueError, TypeError):
            # Candidate may be a plain list of values (no ds/y structure).
            x = pd.Series([float(v) for v in series_input])

        n = min(len(x), len(y))
        if n < 3:
            continue
        x_aligned = x.iloc[:n].astype(float)
        y_aligned = y.iloc[:n].astype(float)

        best_corr = 0.0
        best_p = 1.0
        best_lag = 0
        found = False
        for lag in range(0, max_lag + 1):
            if lag >= n - 2:
                break
            if lag == 0:
                xs, ys = x_aligned, y_aligned
            else:
                # Predictor at t-lag aligns with target at t (predictor leads).
                xs = x_aligned.iloc[: n - lag].reset_index(drop=True)
                ys = y_aligned.iloc[lag:].reset_index(drop=True)

            mask = (~xs.isna()) & (~ys.isna())
            xs_clean = xs[mask]
            ys_clean = ys[mask]
            if len(xs_clean) < 3:
                continue
            if xs_clean.std(ddof=0) == 0 or ys_clean.std(ddof=0) == 0:
                continue

            corr, p_value = stats.pearsonr(xs_clean.values, ys_clean.values)
            if not np.isfinite(corr):
                continue
            if not found or abs(corr) > abs(best_corr):
                best_corr = float(corr)
                best_p = float(p_value)
                best_lag = lag
                found = True

        if found:
            drivers.append(
                {
                    "name": name,
                    "correlation": round(best_corr, 6),
                    "p_value": round(best_p, 6),
                    "lag_optimal": best_lag,
                }
            )

    drivers.sort(key=lambda d: abs(d["correlation"]), reverse=True)

    return {
        "drivers": drivers,
        "n_candidates": len(candidates),
        "max_lag": max_lag,
    }


# ---------------------------------------------------------------------------
# Tool: generate_narrative (UNCHANGED — production tool, leave alone)
# ---------------------------------------------------------------------------


def generate_narrative(forecast_data: dict, audience: str = "executive") -> str:
    """Generate plain-English narrative from forecast data."""
    if audience == "executive":
        return f"""Executive Summary:

Q4 revenue is forecasted at ${forecast_data.get('forecast_value', 2150000):,.0f}, representing a {forecast_data.get('growth_pct', 15.2):.1f}% increase over Q3 2025. This growth is driven by three key factors:

1. **Seasonal Q4 Pattern (+{forecast_data.get('seasonal_contrib', 8.7):.1f}%)**: Historical data shows consistent Q4 revenue increases averaging 8-10% over the past 5 years.

2. **Recent Momentum (+{forecast_data.get('momentum_contrib', 4.2):.1f}%)**: The last 30 days show accelerating growth {forecast_data.get('momentum_contrib', 4.2):.1f}% above the 90-day average.

3. **Trend Contribution (+{forecast_data.get('trend_contrib', 2.3):.1f}%)**: Long-term growth trajectory continues upward.

With {forecast_data.get('confidence', 95)}% confidence, Q4 revenue will fall between ${forecast_data.get('lower_bound', 1980000):,.0f} and ${forecast_data.get('upper_bound', 2310000):,.0f}.

**Risk Factors:**
- Forecast extends {forecast_data.get('beyond_historical', 12)}% beyond historical maximum
- Economic uncertainty may impact consumer spending
"""
    else:
        return "Technical analysis report placeholder"


# ---------------------------------------------------------------------------
# Tool: generate_report
# ---------------------------------------------------------------------------


def generate_report(
    title: str = "Forecast Explanation Report",
    summary: str | None = None,
    decomposition: dict[str, Any] | None = None,
    drivers: dict[str, Any] | list[dict[str, Any]] | None = None,
    risk_factors: dict[str, Any] | list[dict[str, Any]] | None = None,
    narrative: str | None = None,
    recommendations: list[str] | None = None,
) -> str:
    """Compose a markdown report from explainer outputs.

    Stitches the upstream tool outputs into a single human-readable document
    suitable for stakeholders. All inputs are optional — sections are omitted
    when their input is missing or empty.

    Args:
        title: Report title.
        summary: 1-2 sentence executive summary.
        decomposition: Output of :func:`decompose_forecast` (or any dict carrying
            ``strength_of_trend``, ``strength_of_seasonality``, ``period``,
            ``n_obs``).
        drivers: Either the dict returned by :func:`identify_drivers` (with a
            ``drivers`` key) or a bare list of driver entries.
        risk_factors: Either the dict from ``assess_risk_factors`` (with
            ``risk_factors`` and ``overall_confidence``) or a bare list.
        narrative: Free-text narrative paragraph (e.g., from
            :func:`generate_narrative`).
        recommendations: Optional list of recommendation bullet strings.

    Returns:
        Markdown-formatted report as a single string.
    """
    lines: list[str] = [f"# {title}", ""]

    if summary:
        lines += ["## Summary", "", summary.strip(), ""]

    if decomposition:
        lines += [
            "## Decomposition Findings",
            "",
            f"- **Period analyzed**: {decomposition.get('period', 'n/a')}",
            f"- **Observations**: {decomposition.get('n_obs', 'n/a')}",
            f"- **Strength of trend**: "
            f"{decomposition.get('strength_of_trend', float('nan')):.3f}",
            f"- **Strength of seasonality**: "
            f"{decomposition.get('strength_of_seasonality', float('nan')):.3f}",
            "",
            "Strength values follow Hyndman's formulation: 0 indicates no "
            "component, 1 indicates the component fully explains the variance "
            "of (component + residual).",
            "",
        ]

    if drivers:
        if isinstance(drivers, dict):
            driver_list = drivers.get("drivers", [])
        else:
            driver_list = list(drivers)
        if driver_list:
            lines += [
                "## Top Drivers",
                "",
                "| Rank | Driver | Correlation | p-value | Optimal Lag |",
                "| --- | --- | --- | --- | --- |",
            ]
            for i, d in enumerate(driver_list, start=1):
                lines.append(
                    f"| {i} | {d.get('name', 'unknown')} | "
                    f"{d.get('correlation', float('nan')):+.4f} | "
                    f"{d.get('p_value', float('nan')):.4f} | "
                    f"{d.get('lag_optimal', 0)} |"
                )
            lines.append("")

    if risk_factors:
        if isinstance(risk_factors, dict):
            risk_list = risk_factors.get("risk_factors", [])
            overall = risk_factors.get("overall_confidence")
        else:
            risk_list = list(risk_factors)
            overall = None
        lines += ["## Risk Factors", ""]
        if overall:
            lines += [f"**Overall confidence**: {overall}", ""]
        for r in risk_list:
            if isinstance(r, dict):
                factor = r.get("factor", "unspecified")
                severity = r.get("severity", "")
                sev_part = f" _(severity: {severity})_" if severity else ""
                lines.append(f"- {factor}{sev_part}")
            else:
                lines.append(f"- {r}")
        lines.append("")

    if narrative:
        lines += ["## Narrative", "", narrative.strip(), ""]

    if recommendations:
        lines += ["## Recommendations", ""]
        for rec in recommendations:
            lines.append(f"- {rec}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="decompose_forecast",
            description="Run STL decomposition on forecast data",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "description": (
                            "Time series: DataFrame-like with ds/y columns, "
                            "list of dicts {ds, y}, dict {ds: [...], y: [...]}, "
                            "or list of floats."
                        ),
                    },
                    "data_path": {
                        "type": "string",
                        "description": "Optional CSV path (alternative to inline data)",
                    },
                    "period": {"type": "integer", "description": "Seasonal period"},
                    "value_key": {
                        "type": "string",
                        "description": "Target column name (default 'y')",
                    },
                },
            },
        ),
        Tool(
            name="identify_drivers",
            description="Identify forecast drivers via lagged Pearson correlation",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"description": "Target series (same shapes as decompose data)"},
                    "candidates": {
                        "type": "object",
                        "description": "Mapping of driver name to candidate series",
                    },
                    "max_lag": {
                        "type": "integer",
                        "description": "Max lag to scan (default 7)",
                    },
                    "value_key": {
                        "type": "string",
                        "description": "Target column name (default 'y')",
                    },
                },
                "required": ["target", "candidates"],
            },
        ),
        Tool(
            name="generate_narrative",
            description="Generate plain-English explanation",
            inputSchema={
                "type": "object",
                "properties": {
                    "forecast_data": {"type": "object"},
                    "audience": {
                        "type": "string",
                        "enum": ["executive", "technical", "compliance"],
                    },
                },
            },
        ),
        Tool(
            name="generate_report",
            description="Compose a markdown report from explainer outputs",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "decomposition": {"type": "object"},
                    "drivers": {"description": "dict from identify_drivers or list"},
                    "risk_factors": {
                        "description": "dict from assess_risk_factors or list",
                    },
                    "narrative": {"type": "string"},
                    "recommendations": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        ),
        Tool(
            name="assess_risk_factors",
            description="Identify and flag high uncertainty periods",
            inputSchema={"type": "object", "properties": {"forecast_data": {"type": "object"}}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "decompose_forecast":
        data = arguments.get("data")
        if data is None and "data_path" in arguments:
            data = pd.read_csv(arguments["data_path"])
        if data is None:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"error": "decompose_forecast requires 'data' or 'data_path'"}),
                )
            ]
        try:
            result = decompose_forecast(
                data,
                period=arguments.get("period"),
                value_key=arguments.get("value_key", "y"),
            )
        except (ValueError, TypeError) as exc:
            return [TextContent(type="text", text=json.dumps({"error": str(exc)}))]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "identify_drivers":
        target = arguments.get("target")
        candidates = arguments.get("candidates", {})
        if target is None:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"error": "identify_drivers requires 'target'"}),
                )
            ]
        try:
            result = identify_drivers(
                target,
                candidates,
                max_lag=int(arguments.get("max_lag", 7)),
                value_key=arguments.get("value_key", "y"),
            )
        except (ValueError, TypeError) as exc:
            return [TextContent(type="text", text=json.dumps({"error": str(exc)}))]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "generate_narrative":
        forecast_data = arguments.get("forecast_data", {})
        audience = arguments.get("audience", "executive")
        narrative = generate_narrative(forecast_data, audience)
        return [TextContent(type="text", text=narrative)]

    elif name == "generate_report":
        markdown = generate_report(
            title=arguments.get("title", "Forecast Explanation Report"),
            summary=arguments.get("summary"),
            decomposition=arguments.get("decomposition"),
            drivers=arguments.get("drivers"),
            risk_factors=arguments.get("risk_factors"),
            narrative=arguments.get("narrative"),
            recommendations=arguments.get("recommendations"),
        )
        return [TextContent(type="text", text=markdown)]

    elif name == "assess_risk_factors":
        result = {
            "risk_factors": [
                {"factor": "Forecast extends beyond historical range", "severity": "medium"},
                {"factor": "Increasing prediction interval width", "severity": "low"},
                {"factor": "Recent volatility spike", "severity": "low"},
            ],
            "overall_confidence": "HIGH",
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
