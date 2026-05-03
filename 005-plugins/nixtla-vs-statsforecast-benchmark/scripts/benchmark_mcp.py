#!/usr/bin/env python3
"""MCP Server for TimeGPT vs StatsForecast Benchmark.

Exposes 4 tools:
- run_benchmark: Execute head-to-head comparison
- load_data: Load and validate time series data
- generate_report: Create comparison report
- get_recommendations: Get migration recommendations
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Configure logging to stderr (stdout is reserved for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("nixtla-vs-statsforecast-benchmark")

app = Server("nixtla-vs-statsforecast-benchmark")


# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------


def _smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Symmetric Mean Absolute Percentage Error (in percent, 0-200 range).

    Uses the standard M4 definition:
        sMAPE = mean( 2 * |y - yhat| / (|y| + |yhat|) ) * 100
    Pairs where both numerator and denominator are zero contribute 0.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    denom = np.abs(y_true) + np.abs(y_pred)
    with np.errstate(divide="ignore", invalid="ignore"):
        smape = np.where(denom == 0, 0.0, 2.0 * np.abs(y_true - y_pred) / denom)
    return float(np.mean(smape) * 100.0)


def _mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error."""
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def _rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Error."""
    diff = np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float)
    return float(np.sqrt(np.mean(diff * diff)))


def _mase(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_train: np.ndarray,
    seasonality: int = 1,
) -> float:
    """Mean Absolute Scaled Error against a seasonal-naive in-sample baseline.

    Returns NaN if the in-sample seasonal-naive denominator is zero (constant
    training series) — caller should treat that case as "not meaningful".
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    y_train = np.asarray(y_train, dtype=float)
    if len(y_train) <= seasonality:
        return float("nan")
    naive_errors = np.abs(y_train[seasonality:] - y_train[:-seasonality])
    scale = np.mean(naive_errors)
    if scale == 0 or not np.isfinite(scale):
        return float("nan")
    return float(np.mean(np.abs(y_true - y_pred)) / scale)


# ---------------------------------------------------------------------------
# Data loading / splitting
# ---------------------------------------------------------------------------


REQUIRED_COLUMNS = ("unique_id", "ds", "y")


def _load_dataframe(data: Union[str, pd.DataFrame]) -> pd.DataFrame:
    """Accept a DataFrame or a CSV path. Validate required columns + sort."""
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        path = Path(str(data))
        if not path.exists():
            raise FileNotFoundError(f"Data path not found: {path}")
        df = pd.read_csv(path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Input data missing required columns {missing}. Required: {list(REQUIRED_COLUMNS)}"
        )

    df["ds"] = pd.to_datetime(df["ds"])
    df = df.sort_values(["unique_id", "ds"]).reset_index(drop=True)
    return df


def _split_train_test(df: pd.DataFrame, horizon: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Hold out the last `horizon` rows per series as test, rest as train."""
    test = df.groupby("unique_id", group_keys=False).tail(horizon).reset_index(drop=True)
    train = (
        df.merge(test[["unique_id", "ds"]].assign(_is_test=1), on=["unique_id", "ds"], how="left")
        .query("_is_test.isna()")
        .drop(columns=["_is_test"])
        .reset_index(drop=True)
    )
    return train, test


def _seasonality_for_freq(freq: str) -> int:
    """Default seasonal period for MASE / SeasonalNaive given a pandas freq."""
    f = (freq or "").upper()
    if f.startswith("H"):
        return 24
    if f.startswith("D"):
        return 7
    if f.startswith("W"):
        return 52
    if f.startswith("M"):
        return 12
    if f.startswith("Q"):
        return 4
    if f.startswith("Y") or f.startswith("A"):
        return 1
    return 1


# ---------------------------------------------------------------------------
# StatsForecast runner
# ---------------------------------------------------------------------------


def _per_model_metrics(
    forecasts: pd.DataFrame,
    test: pd.DataFrame,
    train: pd.DataFrame,
    model_cols: List[str],
    seasonality: int,
) -> Dict[str, Dict[str, float]]:
    """Compute sMAPE / MASE / MAE / RMSE for each model column in `forecasts`."""
    merged = forecasts.merge(test[["unique_id", "ds", "y"]], on=["unique_id", "ds"], how="inner")
    out: Dict[str, Dict[str, float]] = {}

    train_y_by_id = {uid: g["y"].to_numpy() for uid, g in train.groupby("unique_id")}

    for col in model_cols:
        if col not in merged.columns:
            continue
        y_true = merged["y"].to_numpy()
        y_pred = merged[col].to_numpy()

        # Aggregate MASE across series (mean of per-series MASE, NaN-safe)
        mase_vals: List[float] = []
        for uid, g in merged.groupby("unique_id"):
            yt = g["y"].to_numpy()
            yp = g[col].to_numpy()
            ytrain = train_y_by_id.get(uid, np.array([]))
            v = _mase(yt, yp, ytrain, seasonality=seasonality)
            if np.isfinite(v):
                mase_vals.append(v)

        out[col] = {
            "smape": _smape(y_true, y_pred),
            "mase": float(np.mean(mase_vals)) if mase_vals else float("nan"),
            "mae": _mae(y_true, y_pred),
            "rmse": _rmse(y_true, y_pred),
        }
    return out


def _run_statsforecast(
    train: pd.DataFrame,
    test: pd.DataFrame,
    horizon: int,
    freq: str,
    seasonality: int,
) -> Dict[str, Any]:
    """Run AutoETS, AutoTheta, SeasonalNaive on `train` and score on `test`."""
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

    models = [
        AutoETS(season_length=seasonality),
        AutoTheta(season_length=seasonality),
        SeasonalNaive(season_length=seasonality),
    ]
    sf = StatsForecast(models=models, freq=freq, n_jobs=1)

    t0 = time.time()
    forecasts = sf.forecast(df=train, h=horizon)
    wall = time.time() - t0

    # statsforecast returns columns named after the models' alias (e.g. AutoETS,
    # AutoTheta, SeasonalNaive). Normalize via repr of each model.
    model_cols = [m.alias if hasattr(m, "alias") else type(m).__name__ for m in models]
    metrics = _per_model_metrics(
        forecasts.reset_index(),
        test,
        train,
        model_cols=model_cols,
        seasonality=seasonality,
    )

    # Pick best model by sMAPE (lower is better); ties broken by RMSE.
    best_model = None
    if metrics:
        best_model = min(
            metrics.keys(),
            key=lambda k: (metrics[k]["smape"], metrics[k]["rmse"]),
        )

    return {
        "models": metrics,
        "wall_time_seconds": float(wall),
        "best_model": best_model,
    }


# ---------------------------------------------------------------------------
# TimeGPT runner
# ---------------------------------------------------------------------------


def _run_timegpt(
    train: pd.DataFrame,
    test: pd.DataFrame,
    horizon: int,
    freq: str,
    seasonality: int,
) -> Dict[str, Any]:
    """Run TimeGPT forecast against train; score on test.

    Returns a dict with `metrics`, `wall_time_seconds`, and `skipped_reason`.
    `skipped_reason` is non-null when TimeGPT could not run.
    """
    api_key = os.environ.get("NIXTLA_API_KEY") or os.environ.get("NIXTLA_TIMEGPT_API_KEY")
    if not api_key:
        return {
            "metrics": None,
            "wall_time_seconds": None,
            "skipped_reason": "NIXTLA_API_KEY not set",
        }

    try:
        from nixtla import NixtlaClient
    except ImportError as exc:  # pragma: no cover - env guard
        return {
            "metrics": None,
            "wall_time_seconds": None,
            "skipped_reason": f"nixtla SDK import failed: {exc}",
        }

    try:
        client = NixtlaClient(api_key=api_key)
        t0 = time.time()
        forecast = client.forecast(df=train, h=horizon, freq=freq)
        wall = time.time() - t0
    except Exception as exc:  # pragma: no cover - network/auth guard
        logger.warning("TimeGPT forecast failed: %s", exc)
        return {
            "metrics": None,
            "wall_time_seconds": None,
            "skipped_reason": f"TimeGPT call failed: {exc}",
        }

    # TimeGPT returns column "TimeGPT" by default.
    tg_col = "TimeGPT"
    if tg_col not in forecast.columns:
        # Fall back to first non-key column
        candidates = [c for c in forecast.columns if c not in ("unique_id", "ds")]
        tg_col = candidates[0] if candidates else None
    if tg_col is None:
        return {
            "metrics": None,
            "wall_time_seconds": float(wall),
            "skipped_reason": "TimeGPT response had no forecast column",
        }

    metrics = _per_model_metrics(
        forecast.reset_index(drop=True),
        test,
        train,
        model_cols=[tg_col],
        seasonality=seasonality,
    )
    return {
        "metrics": metrics.get(tg_col),
        "wall_time_seconds": float(wall),
        "skipped_reason": None,
    }


# ---------------------------------------------------------------------------
# Top-level benchmark orchestration
# ---------------------------------------------------------------------------


def _decide_winner(
    sf_result: Dict[str, Any],
    tg_result: Dict[str, Any],
) -> Tuple[str, str]:
    """Return (winner, rationale). Winner is 'timegpt' | 'statsforecast' | 'tie'."""
    sf_models = sf_result.get("models") or {}
    sf_best = sf_result.get("best_model")
    sf_best_smape = sf_models.get(sf_best, {}).get("smape") if sf_best else None

    tg_metrics = tg_result.get("metrics")
    tg_skipped = tg_result.get("skipped_reason")

    if tg_skipped or tg_metrics is None:
        if sf_best is None:
            return ("tie", "No models produced metrics.")
        return (
            "statsforecast",
            f"TimeGPT skipped ({tg_skipped or 'no metrics'}); statsforecast {sf_best} wins.",
        )

    tg_smape = tg_metrics.get("smape")
    if sf_best_smape is None and tg_smape is None:
        return ("tie", "Neither side produced finite metrics.")
    if sf_best_smape is None:
        return ("timegpt", "Only TimeGPT produced metrics.")
    if tg_smape is None:
        return ("statsforecast", "Only statsforecast produced metrics.")

    # Within 1% relative sMAPE = tie
    rel = (sf_best_smape - tg_smape) / max(abs(sf_best_smape), 1e-9)
    if abs(rel) < 0.01:
        return (
            "tie",
            f"sMAPE within 1% (TimeGPT {tg_smape:.3f} vs {sf_best} {sf_best_smape:.3f}).",
        )
    if tg_smape < sf_best_smape:
        return (
            "timegpt",
            f"TimeGPT sMAPE {tg_smape:.3f} beats statsforecast {sf_best} {sf_best_smape:.3f} "
            f"(relative improvement {rel * 100:.1f}%).",
        )
    return (
        "statsforecast",
        f"statsforecast {sf_best} sMAPE {sf_best_smape:.3f} beats TimeGPT {tg_smape:.3f}.",
    )


def run_benchmark(
    data: Union[str, pd.DataFrame],
    horizon: int,
    freq: str = "D",
    seasonality: Optional[int] = None,
) -> Dict[str, Any]:
    """Run the full TimeGPT vs statsforecast benchmark.

    Args:
        data: Either a CSV path or a pandas DataFrame with columns
            `unique_id`, `ds`, `y`.
        horizon: Forecast horizon (number of periods to predict).
        freq: Pandas frequency string (default "D" daily).
        seasonality: Override seasonal period for MASE / SeasonalNaive.
            Defaults to a frequency-appropriate value.

    Returns:
        A dict shaped as documented in the module docstring (statsforecast,
        timegpt, horizon, n_series, winner, winner_rationale).
    """
    if horizon <= 0:
        raise ValueError(f"horizon must be positive, got {horizon}")

    df = _load_dataframe(data)
    if seasonality is None:
        seasonality = _seasonality_for_freq(freq)

    train, test = _split_train_test(df, horizon)
    n_series = int(df["unique_id"].nunique())

    # Sanity check: each series must have at least 2 * seasonality + horizon points
    min_required = 2 * seasonality + horizon
    series_lengths = df.groupby("unique_id").size()
    too_short = series_lengths[series_lengths < min_required]
    if len(too_short) > 0:
        logger.warning(
            "%d/%d series have fewer than %d points; results for those series may be unstable.",
            len(too_short),
            n_series,
            min_required,
        )

    logger.info(
        "Running benchmark: n_series=%d horizon=%d freq=%s seasonality=%d",
        n_series,
        horizon,
        freq,
        seasonality,
    )

    sf_result = _run_statsforecast(train, test, horizon, freq, seasonality)
    tg_result = _run_timegpt(train, test, horizon, freq, seasonality)

    winner, rationale = _decide_winner(sf_result, tg_result)

    return {
        "statsforecast": sf_result,
        "timegpt": tg_result,
        "horizon": int(horizon),
        "freq": freq,
        "seasonality": int(seasonality),
        "n_series": n_series,
        "winner": winner,
        "winner_rationale": rationale,
    }


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------


def get_recommendations(results: Dict[str, Any]) -> Dict[str, Any]:
    """Apply rule-based recommendations to a benchmark result.

    Returns a dict with `recommendations` (list of strings) and a `verdict`
    (one-paragraph plain-English summary).
    """
    recs: List[str] = []
    sf = results.get("statsforecast") or {}
    tg = results.get("timegpt") or {}
    sf_models = sf.get("models") or {}
    sf_best = sf.get("best_model")
    sf_best_metrics = sf_models.get(sf_best, {}) if sf_best else {}
    sf_best_smape = sf_best_metrics.get("smape")
    sf_wall = sf.get("wall_time_seconds") or 0.0
    tg_skipped = tg.get("skipped_reason")
    tg_metrics = tg.get("metrics") or {}
    tg_smape = tg_metrics.get("smape") if tg_metrics else None
    tg_wall = tg.get("wall_time_seconds") or 0.0
    n_series = max(int(results.get("n_series") or 1), 1)
    winner = results.get("winner")

    # Rule 1: TimeGPT skipped → recommend trying it
    if tg_skipped:
        recs.append(
            "TimeGPT was not evaluated because the API key was unavailable. "
            "For higher-stakes forecasts (revenue, inventory, anomaly detection) "
            "set NIXTLA_API_KEY and re-run — TimeGPT often closes accuracy gaps "
            "that classical baselines cannot."
        )

    # Rule 2: TimeGPT wins big AND fast per series → recommend TimeGPT for prod
    if sf_best_smape is not None and tg_smape is not None and sf_best_smape > 0:
        improvement = (sf_best_smape - tg_smape) / sf_best_smape
        per_series = tg_wall / n_series if n_series else tg_wall
        if improvement > 0.10 and per_series < 5.0:
            recs.append(
                f"TimeGPT delivers {improvement * 100:.1f}% lower sMAPE than the best "
                f"open-source model ({sf_best}) at {per_series:.2f}s/series. "
                "Recommend TimeGPT as the default for production forecasts."
            )

    # Rule 3: SeasonalNaive wins or ties for best → data is highly seasonal,
    # simple model suffices
    if sf_best == "SeasonalNaive" or (winner == "tie" and sf_best == "SeasonalNaive"):
        recs.append(
            "SeasonalNaive matches or beats every other model — your series are "
            "dominated by the seasonal cycle. Consider keeping the simple "
            "baseline in production; complexity is not buying accuracy."
        )

    # Rule 4: Wall-time delta >50x for similar accuracy → batch-vs-adhoc split
    if sf_best_smape is not None and tg_smape is not None and sf_wall > 0 and tg_wall > 0:
        # similar accuracy = within 5% relative sMAPE
        rel = abs(sf_best_smape - tg_smape) / max(abs(sf_best_smape), 1e-9)
        ratio = max(sf_wall, tg_wall) / max(min(sf_wall, tg_wall), 1e-9)
        if rel < 0.05 and ratio > 50:
            faster = "statsforecast" if sf_wall < tg_wall else "TimeGPT"
            slower = "TimeGPT" if faster == "statsforecast" else "statsforecast"
            recs.append(
                f"Accuracy is statistically similar but {slower} is {ratio:.0f}x slower. "
                f"Use {faster} for batch / scheduled forecasts and reserve "
                f"{slower} for ad-hoc, high-value queries."
            )

    if not recs:
        recs.append(
            "No strong rule-based recommendation triggered. Review per-model "
            "metrics in the report and weigh accuracy gains against integration cost."
        )

    # Verdict: 1-paragraph summary
    rationale = results.get("winner_rationale") or ""
    if winner == "timegpt":
        verdict = (
            f"TimeGPT is the better choice for this dataset across {n_series} series "
            f"at horizon {results.get('horizon')}. {rationale} "
            "Adopt TimeGPT for production unless infrastructure constraints "
            "(air-gapped, no outbound API) preclude it."
        )
    elif winner == "statsforecast":
        verdict = (
            f"Open-source statsforecast (best model: {sf_best}) wins on this dataset. "
            f"{rationale} Stick with statsforecast — TimeGPT does not justify the "
            "additional dependency and per-call cost here."
        )
    else:
        verdict = (
            f"The two systems are effectively tied on accuracy. {rationale} "
            "Choose based on operational fit: statsforecast for offline / batch, "
            "TimeGPT for low-latency or sparse-data scenarios."
        )

    return {"recommendations": recs, "verdict": verdict}


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------


def _fmt(x: Optional[float], digits: int = 4) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.{digits}f}"


def generate_report(
    results: Dict[str, Any],
    dataset_name: str = "dataset",
) -> str:
    """Render a markdown report from a benchmark result dict."""
    horizon = results.get("horizon")
    n_series = results.get("n_series")
    freq = results.get("freq", "?")
    seasonality = results.get("seasonality", "?")
    winner = results.get("winner")
    rationale = results.get("winner_rationale") or ""

    sf = results.get("statsforecast") or {}
    tg = results.get("timegpt") or {}
    sf_models = sf.get("models") or {}
    sf_best = sf.get("best_model")
    sf_wall = sf.get("wall_time_seconds")

    tg_metrics = tg.get("metrics") or {}
    tg_wall = tg.get("wall_time_seconds")
    tg_skipped = tg.get("skipped_reason")

    recs = get_recommendations(results)

    lines: List[str] = []
    lines.append(f"# TimeGPT vs StatsForecast Benchmark — {dataset_name}")
    lines.append("")
    lines.append(
        f"**Horizon:** {horizon} · **Series:** {n_series} · "
        f"**Frequency:** `{freq}` · **Seasonality:** {seasonality}"
    )
    lines.append("")

    # Methodology
    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "Each series is split into train (all but the last `horizon` periods) and a "
        "held-out test of the last `horizon` periods. Both stacks forecast the same "
        "horizon from the same train data; metrics (sMAPE, MASE, MAE, RMSE) are "
        "computed on the held-out test."
    )
    lines.append("")

    # Per-model metrics
    lines.append("## Per-model metrics")
    lines.append("")
    lines.append("| Model | sMAPE | MASE | MAE | RMSE |")
    lines.append("|---|---:|---:|---:|---:|")
    for name, m in sf_models.items():
        marker = " (best)" if name == sf_best else ""
        lines.append(
            f"| {name}{marker} | {_fmt(m.get('smape'))} | {_fmt(m.get('mase'))} | "
            f"{_fmt(m.get('mae'))} | {_fmt(m.get('rmse'))} |"
        )
    if tg_metrics:
        lines.append(
            f"| TimeGPT | {_fmt(tg_metrics.get('smape'))} | {_fmt(tg_metrics.get('mase'))} | "
            f"{_fmt(tg_metrics.get('mae'))} | {_fmt(tg_metrics.get('rmse'))} |"
        )
    elif tg_skipped:
        lines.append(f"| TimeGPT | _skipped: {tg_skipped}_ | — | — | — |")
    lines.append("")

    # Wall-time
    lines.append("## Wall-time comparison")
    lines.append("")
    lines.append("| Stack | Wall time (s) | Per-series (s) |")
    lines.append("|---|---:|---:|")
    if sf_wall is not None:
        per = sf_wall / max(int(n_series or 1), 1)
        lines.append(f"| statsforecast (3 models) | {_fmt(sf_wall, 3)} | {_fmt(per, 3)} |")
    if tg_wall is not None:
        per = tg_wall / max(int(n_series or 1), 1)
        lines.append(f"| TimeGPT | {_fmt(tg_wall, 3)} | {_fmt(per, 3)} |")
    elif tg_skipped:
        lines.append(f"| TimeGPT | _skipped: {tg_skipped}_ | — |")
    lines.append("")

    # Winner
    lines.append("## Winner")
    lines.append("")
    lines.append(f"**{winner}** — {rationale}")
    lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    lines.append(recs["verdict"])
    lines.append("")
    for r in recs["recommendations"]:
        lines.append(f"- {r}")
    lines.append("")

    # Raw appendix
    lines.append("## Appendix: raw results")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(results, indent=2, default=str))
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MCP tool dispatch
# ---------------------------------------------------------------------------


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available benchmark tools."""
    return [
        Tool(
            name="run_benchmark",
            description="Run TimeGPT vs StatsForecast benchmark on data",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_path": {"type": "string", "description": "Path to CSV data"},
                    "horizon": {"type": "integer", "description": "Forecast horizon"},
                    "freq": {"type": "string", "description": "Frequency (D, H, W, M)"},
                    "seasonality": {
                        "type": "integer",
                        "description": "Seasonal period (default inferred from freq)",
                    },
                },
                "required": ["data_path", "horizon"],
            },
        ),
        Tool(
            name="load_data",
            description="Load and validate time series data",
            inputSchema={
                "type": "object",
                "properties": {"data_path": {"type": "string", "description": "Path to CSV data"}},
                "required": ["data_path"],
            },
        ),
        Tool(
            name="generate_report",
            description="Generate benchmark comparison report",
            inputSchema={
                "type": "object",
                "properties": {
                    "results": {"type": "object", "description": "Benchmark results"},
                    "dataset_name": {"type": "string", "description": "Dataset label"},
                },
                "required": ["results"],
            },
        ),
        Tool(
            name="get_recommendations",
            description="Get recommendations based on benchmark results",
            inputSchema={
                "type": "object",
                "properties": {"results": {"type": "object", "description": "Benchmark results"}},
                "required": ["results"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute benchmark tool."""
    try:
        if name == "run_benchmark":
            data_path = arguments.get("data_path")
            horizon = int(arguments.get("horizon", 0))
            freq = arguments.get("freq", "D")
            seasonality = arguments.get("seasonality")
            if seasonality is not None:
                seasonality = int(seasonality)
            if not data_path:
                return [TextContent(type="text", text="Error: data_path is required")]
            results = run_benchmark(
                data=data_path,
                horizon=horizon,
                freq=freq,
                seasonality=seasonality,
            )
            return [TextContent(type="text", text=json.dumps(results, indent=2, default=str))]

        elif name == "load_data":
            data_path = arguments.get("data_path")
            if not data_path or not os.path.exists(data_path):
                return [TextContent(type="text", text="File not found")]
            df = _load_dataframe(data_path)
            summary = {
                "rows": len(df),
                "columns": list(df.columns),
                "n_series": int(df["unique_id"].nunique()),
                "ds_min": str(df["ds"].min()),
                "ds_max": str(df["ds"].max()),
            }
            return [TextContent(type="text", text=json.dumps(summary, indent=2, default=str))]

        elif name == "generate_report":
            results = arguments.get("results") or {}
            dataset_name = arguments.get("dataset_name", "dataset")
            md = generate_report(results, dataset_name=dataset_name)
            return [TextContent(type="text", text=md)]

        elif name == "get_recommendations":
            results = arguments.get("results") or {}
            recs = get_recommendations(results)
            return [TextContent(type="text", text=json.dumps(recs, indent=2, default=str))]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as exc:
        logger.exception("Tool %s failed", name)
        return [TextContent(type="text", text=f"Error in {name}: {exc}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
