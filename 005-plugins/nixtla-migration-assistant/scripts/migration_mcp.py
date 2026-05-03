#!/usr/bin/env python3
"""MCP Server for Nixtla Migration Assistant.

Real migration assistant for moving from Prophet / statsmodels / sklearn
forecasting to Nixtla TimeGPT or StatsForecast. Provides:

  - analyze_code: AST-based detection of source forecasting library.
  - transform_data: real pandas reshape from source schema -> Nixtla
    canonical schema (unique_id, ds, y).
  - generate_code: real Nixtla-equivalent code from a source library +
    target engine.
  - generate_plan: phased migration plan derived from analyze_code
    output (line counts -> phase sizing).
  - compare_accuracy: optional real model fits on the same train/test
    split with sMAPE/MAE comparison.
"""

from __future__ import annotations

import ast
import json
from datetime import datetime
from typing import Any, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

app = Server("nixtla-migration-assistant")


# ---------------------------------------------------------------------------
# Code templates (per source -> target combo)
# ---------------------------------------------------------------------------


PROPHET_TO_TIMEGPT_TEMPLATE = '''"""
Migrated from Prophet to Nixtla TimeGPT.
Original file: {original_file}
Migration date: {migration_date}
"""

import pandas as pd
from nixtla import NixtlaClient

client = NixtlaClient()  # reads NIXTLA_API_KEY

# Load data — Prophet expects ds/y columns; Nixtla also wants unique_id.
df = pd.read_csv({data_path!r})
df = df.rename(columns={{{rename_map}}})
{group_by_line}

# Equivalent of Prophet .fit() + .predict():
forecast = client.forecast(
    df=df,
    h={horizon},
    freq={freq!r},
    level=[80, 95],
)

# Output columns: ds, TimeGPT, TimeGPT-lo-80, TimeGPT-hi-80, TimeGPT-lo-95, TimeGPT-hi-95
print(forecast)
'''


PROPHET_TO_STATSFORECAST_TEMPLATE = '''"""
Migrated from Prophet to open-source StatsForecast.
Original file: {original_file}
Migration date: {migration_date}
"""

import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

df = pd.read_csv({data_path!r})
df = df.rename(columns={{{rename_map}}})
{group_by_line}

sf = StatsForecast(
    models=[AutoETS(season_length={season_length}), AutoTheta(season_length={season_length}), SeasonalNaive(season_length={season_length})],
    freq={freq!r},
    n_jobs=-1,
)

forecast = sf.forecast(df=df, h={horizon}, level=[80, 95])
print(forecast)
'''


STATSMODELS_ARIMA_TO_STATSFORECAST_TEMPLATE = '''"""
Migrated from statsmodels.ARIMA to StatsForecast.AutoARIMA.
Original file: {original_file}
Migration date: {migration_date}
"""

import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA

df = pd.read_csv({data_path!r})
df = df.rename(columns={{{rename_map}}})
{group_by_line}

sf = StatsForecast(
    models=[AutoARIMA(season_length={season_length})],
    freq={freq!r},
)

forecast = sf.forecast(df=df, h={horizon})
print(forecast)
'''


STATSMODELS_ETS_TO_STATSFORECAST_TEMPLATE = '''"""
Migrated from statsmodels.ExponentialSmoothing to StatsForecast.AutoETS.
Original file: {original_file}
Migration date: {migration_date}
"""

import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoETS

df = pd.read_csv({data_path!r})
df = df.rename(columns={{{rename_map}}})
{group_by_line}

sf = StatsForecast(
    models=[AutoETS(season_length={season_length})],
    freq={freq!r},
)

forecast = sf.forecast(df=df, h={horizon})
print(forecast)
'''


SKLEARN_TO_STATSFORECAST_TEMPLATE = '''"""
Migrated from sklearn-style forecasting to StatsForecast.
Original file: {original_file}
Migration date: {migration_date}

Note: sklearn doesn't have a native time-series model; common patterns use
LinearRegression on lag features. AutoETS / AutoARIMA / AutoTheta are usually
strict upgrades for univariate forecasting.
"""

import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta

df = pd.read_csv({data_path!r})
df = df.rename(columns={{{rename_map}}})
{group_by_line}

sf = StatsForecast(
    models=[AutoETS(season_length={season_length}), AutoTheta(season_length={season_length})],
    freq={freq!r},
)

forecast = sf.forecast(df=df, h={horizon})
print(forecast)
'''


CODE_TEMPLATES: dict[tuple[str, str], str] = {
    ("prophet", "timegpt"): PROPHET_TO_TIMEGPT_TEMPLATE,
    ("prophet", "statsforecast"): PROPHET_TO_STATSFORECAST_TEMPLATE,
    ("statsmodels.arima", "statsforecast"): STATSMODELS_ARIMA_TO_STATSFORECAST_TEMPLATE,
    ("statsmodels.ets", "statsforecast"): STATSMODELS_ETS_TO_STATSFORECAST_TEMPLATE,
    ("sklearn", "statsforecast"): SKLEARN_TO_STATSFORECAST_TEMPLATE,
}


# ---------------------------------------------------------------------------
# Tool: analyze_code
# ---------------------------------------------------------------------------


def analyze_code(code: str) -> dict[str, Any]:
    """Analyze Python source for forecasting library usage via AST.

    Returns:
        Dict with: imports (list), patterns (list of {library, confidence,
        migration_target}), complexity (low/medium/high), line_count.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return {"error": f"Invalid Python syntax: {exc}"}

    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    patterns: list[dict[str, Any]] = []

    if any("prophet" in imp.lower() for imp in imports):
        patterns.append(
            {
                "library": "Prophet",
                "confidence": "high",
                "migration_target": "TimeGPT",
                "alt_target": "StatsForecast",
            }
        )

    if any("statsmodels" in imp for imp in imports):
        if any("arima" in imp.lower() for imp in imports):
            patterns.append(
                {
                    "library": "statsmodels.ARIMA",
                    "confidence": "high",
                    "migration_target": "StatsForecast.AutoARIMA",
                }
            )
        if any("exponential" in imp.lower() or "holtwinter" in imp.lower() for imp in imports):
            patterns.append(
                {
                    "library": "statsmodels.ExponentialSmoothing",
                    "confidence": "high",
                    "migration_target": "StatsForecast.AutoETS",
                }
            )
        if any("statespace" in imp.lower() for imp in imports):
            patterns.append(
                {
                    "library": "statsmodels.statespace",
                    "confidence": "medium",
                    "migration_target": "StatsForecast / TimeGPT",
                }
            )

    if any("sklearn" in imp for imp in imports):
        patterns.append(
            {
                "library": "sklearn",
                "confidence": "medium",
                "migration_target": "StatsForecast",
            }
        )

    line_count = len(code.splitlines())
    if len(patterns) >= 3 or line_count > 500:
        complexity = "high"
    elif len(patterns) >= 2 or line_count > 200:
        complexity = "medium"
    else:
        complexity = "low"

    return {
        "imports": imports,
        "patterns": patterns,
        "complexity": complexity,
        "line_count": line_count,
        "n_patterns": len(patterns),
    }


# ---------------------------------------------------------------------------
# Tool: transform_data
# ---------------------------------------------------------------------------


def transform_data(
    data_path: str,
    timestamp_col: str = "ds",
    value_col: str = "y",
    group_col: Optional[str] = None,
    nan_strategy: str = "interpolate",
) -> dict[str, Any]:
    """Real pandas-based transform: source schema -> Nixtla canonical (unique_id, ds, y).

    Returns:
        Dict with status, input/output column lists, rows_in/rows_out, n_series,
        warnings list, and a transformed_preview (first 5 rows as list-of-dicts).
    """
    try:
        import pandas as pd
    except ImportError:
        return {
            "status": "error",
            "message": "pandas not installed; install with: pip install pandas",
        }

    warnings: list[str] = []

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        return {"status": "error", "message": f"File not found: {data_path}"}
    except Exception as exc:
        return {"status": "error", "message": f"Failed to read {data_path}: {exc}"}

    rows_in = len(df)
    input_columns = list(df.columns)

    # Validate required columns exist.
    missing = [c for c in (timestamp_col, value_col) if c not in df.columns]
    if missing:
        return {
            "status": "error",
            "message": f"Required columns missing: {missing}. Found: {input_columns}",
        }

    # Rename to canonical schema.
    df = df.rename(columns={timestamp_col: "ds", value_col: "y"})
    if group_col and group_col in df.columns:
        df = df.rename(columns={group_col: "unique_id"})
    elif "unique_id" not in df.columns:
        df["unique_id"] = "series_0"
        warnings.append("No group column provided; assigned unique_id='series_0' (single-series).")

    # Coerce ds to datetime.
    df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
    n_bad_dates = int(df["ds"].isna().sum())
    if n_bad_dates > 0:
        warnings.append(f"{n_bad_dates} rows had unparseable timestamps; dropped.")
        df = df.dropna(subset=["ds"])

    # Coerce y to numeric.
    df["y"] = pd.to_numeric(df["y"], errors="coerce")

    # Handle NaN in y.
    n_nan_y = int(df["y"].isna().sum())
    if n_nan_y > 0:
        if nan_strategy == "interpolate":
            df["y"] = df.groupby("unique_id", group_keys=False)["y"].apply(
                lambda s: s.interpolate(method="linear", limit_direction="both")
            )
            still_nan = int(df["y"].isna().sum())
            if still_nan > 0:
                df = df.dropna(subset=["y"])
            warnings.append(
                f"{n_nan_y} NaN values in '{value_col}' interpolated"
                + (f"; {still_nan} unrecoverable rows dropped" if still_nan else "")
                + "."
            )
        elif nan_strategy == "drop":
            df = df.dropna(subset=["y"])
            warnings.append(f"{n_nan_y} NaN values in '{value_col}' dropped.")
        else:
            warnings.append(
                f"{n_nan_y} NaN values in '{value_col}' kept (nan_strategy={nan_strategy})."
            )

    # Sort canonically.
    df = df.sort_values(["unique_id", "ds"]).reset_index(drop=True)

    rows_out = len(df)
    n_series = int(df["unique_id"].nunique())
    output_columns = ["unique_id", "ds", "y"]
    schema_changes = [f"renamed {timestamp_col} -> ds", f"renamed {value_col} -> y"]
    if group_col and group_col in input_columns:
        schema_changes.append(f"renamed {group_col} -> unique_id")
    elif "unique_id" not in input_columns:
        schema_changes.append("added unique_id (default 'series_0')")

    preview = df.head(5).copy()
    preview["ds"] = preview["ds"].astype(str)

    return {
        "status": "success",
        "input_columns": input_columns,
        "output_columns": output_columns,
        "rows_in": rows_in,
        "rows_out": rows_out,
        "n_series": n_series,
        "schema_changes": schema_changes,
        "warnings": warnings,
        "transformed_preview": preview.to_dict(orient="records"),
    }


# ---------------------------------------------------------------------------
# Tool: generate_code
# ---------------------------------------------------------------------------


def generate_code(
    source_library: str,
    target_library: str = "timegpt",
    horizon: int = 14,
    freq: str = "D",
    season_length: int = 7,
    data_path: str = "data.csv",
    timestamp_col: str = "ds",
    value_col: str = "y",
    group_col: Optional[str] = None,
    original_file: str = "original_model.py",
) -> dict[str, Any]:
    """Generate Nixtla-equivalent code from a source library + target engine."""
    src = source_library.lower().strip()
    tgt = target_library.lower().strip()

    template = CODE_TEMPLATES.get((src, tgt))
    if template is None:
        # Try alternate keys (e.g., 'statsmodels' -> first match).
        for (key_src, key_tgt), tmpl in CODE_TEMPLATES.items():
            if src.startswith(key_src.split(".")[0]) and tgt == key_tgt:
                template = tmpl
                break

    if template is None:
        return {
            "status": "error",
            "message": (
                f"No template for source={source_library!r} -> target={target_library!r}. "
                f"Available: {sorted(CODE_TEMPLATES.keys())}"
            ),
            "available_combos": list(CODE_TEMPLATES.keys()),
        }

    rename_pairs = []
    if timestamp_col != "ds":
        rename_pairs.append(f"{timestamp_col!r}: 'ds'")
    if value_col != "y":
        rename_pairs.append(f"{value_col!r}: 'y'")
    if group_col:
        rename_pairs.append(f"{group_col!r}: 'unique_id'")
    rename_map = ", ".join(rename_pairs) if rename_pairs else ""

    if group_col:
        group_by_line = f"# Using {group_col!r} as the unique series identifier"
    else:
        group_by_line = (
            "df['unique_id'] = 'series_0'  # Add default series ID for single-series data"
        )

    code = template.format(
        original_file=original_file,
        migration_date=datetime.utcnow().strftime("%Y-%m-%d"),
        data_path=data_path,
        rename_map=rename_map,
        group_by_line=group_by_line,
        horizon=horizon,
        freq=freq,
        season_length=season_length,
    )

    return {
        "status": "success",
        "source_library": source_library,
        "target_library": target_library,
        "code": code,
        "lines": len(code.splitlines()),
    }


# ---------------------------------------------------------------------------
# Tool: generate_plan
# ---------------------------------------------------------------------------


def generate_plan(analysis: dict[str, Any], target: str = "timegpt") -> dict[str, Any]:
    """Generate a real phased migration plan from analyze_code output."""
    patterns = analysis.get("patterns", [])
    complexity = analysis.get("complexity", "low")
    line_count = int(analysis.get("line_count", 0))
    n_patterns = int(analysis.get("n_patterns", len(patterns)))

    # Phase sizing as a function of code size + pattern count.
    if complexity == "low":
        phase1_hours, phase2_hours, phase3_hours, phase4_hours = (1, 2, 2, 1)
    elif complexity == "medium":
        phase1_hours, phase2_hours, phase3_hours, phase4_hours = (2, 4, 6, 2)
    else:
        phase1_hours, phase2_hours, phase3_hours, phase4_hours = (4, 8, 16, 4)

    phases = [
        {
            "phase": 1,
            "name": "Setup + first dataset",
            "estimated_hours": phase1_hours,
            "tasks": [
                "Install nixtla / statsforecast: pip install nixtla statsforecast",
                "Set NIXTLA_API_KEY in environment (TimeGPT only)",
                "Pick the smallest representative dataset",
                "Run transform_data on it; verify output schema (unique_id, ds, y)",
                "Run compare_accuracy; capture baseline numbers",
            ],
            "validation": [
                "transform_data returns status='success' with no warnings about dropped rows",
                "compare_accuracy returns finite metrics for both engines",
            ],
            "rollback": "Discard pilot results; current production untouched",
        },
        {
            "phase": 2,
            "name": "Pilot on one production series",
            "estimated_hours": phase2_hours,
            "tasks": [
                f"Refactor {max(1, n_patterns)} script(s) using generate_code output",
                "Run pilot on production data with a 14-day shadow period",
                f"Sample size: ~{max(20, line_count // 10)} predictions logged",
                "Compare metrics vs baseline weekly",
            ],
            "validation": [
                "Pilot sMAPE within +/-2% of baseline OR meaningfully better",
                "p95 latency within SLA",
                "No errors in 14 consecutive days of shadow operation",
            ],
            "rollback": "Disable pilot route; production still on legacy engine",
        },
        {
            "phase": 3,
            "name": "Full migration of remaining series",
            "estimated_hours": phase3_hours,
            "tasks": [
                "Migrate all production series in batches of 10-20",
                "Per batch: transform_data + generate_code + smoke test + canary",
                "Document per-series accuracy delta",
            ],
            "validation": [
                "All series transitioned with no SLA breach",
                "Aggregate sMAPE not worse than pre-migration baseline",
            ],
            "rollback": "Per-series rollback via feature flag",
        },
        {
            "phase": 4,
            "name": "Decommission legacy code",
            "estimated_hours": phase4_hours,
            "tasks": [
                "Remove old library imports from codebase",
                "Drop legacy infrastructure (training jobs, model artifacts)",
                "Update runbooks + on-call docs",
            ],
            "validation": [
                "CI green after legacy removal",
                "On-call team trained on new pipeline",
            ],
            "rollback": "git revert; legacy path stays callable for ~30 days",
        },
    ]

    total_hours = sum(p["estimated_hours"] for p in phases)
    risk = "low" if complexity == "low" else "medium" if complexity == "medium" else "high"

    return {
        "target": target,
        "phases": phases,
        "total_estimated_hours": total_hours,
        "complexity": complexity,
        "risk_level": risk,
        "n_patterns": n_patterns,
    }


# ---------------------------------------------------------------------------
# Tool: compare_accuracy
# ---------------------------------------------------------------------------


def compare_accuracy(
    data_path: str,
    horizon: int = 14,
    freq: str = "D",
    source_engine: str = "prophet",
    target_engine: str = "statsforecast",
    timestamp_col: str = "ds",
    value_col: str = "y",
) -> dict[str, Any]:
    """Run real source + target engines on the same train/test split and compare.

    Optional dependencies (prophet, statsmodels, nixtla) are imported lazily
    via try/except — missing deps return a clear "install ..." message rather
    than crashing.
    """
    try:
        import numpy as np
        import pandas as pd
    except ImportError:
        return {"status": "error", "message": "pandas + numpy required"}

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        return {"status": "error", "message": f"File not found: {data_path}"}

    if timestamp_col not in df.columns or value_col not in df.columns:
        return {
            "status": "error",
            "message": (
                f"Required columns missing. Have: {list(df.columns)}; "
                f"need: {timestamp_col}, {value_col}"
            ),
        }

    df = df.rename(columns={timestamp_col: "ds", value_col: "y"})
    df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df = df.dropna(subset=["ds", "y"]).sort_values("ds").reset_index(drop=True)

    if len(df) <= horizon + 10:
        return {
            "status": "error",
            "message": f"Need > {horizon + 10} rows for a meaningful comparison; got {len(df)}",
        }

    train = df.iloc[:-horizon].reset_index(drop=True)
    test = df.iloc[-horizon:].reset_index(drop=True)
    y_test = test["y"].to_numpy()

    def smape(yt, yp):
        denom = np.abs(yt) + np.abs(yp)
        with np.errstate(divide="ignore", invalid="ignore"):
            arr = np.where(denom == 0, 0.0, 2.0 * np.abs(yt - yp) / denom)
        return float(np.mean(arr) * 100.0)

    def mae(yt, yp):
        return float(np.mean(np.abs(yt - yp)))

    results: dict[str, Any] = {
        "source": {"engine": source_engine},
        "target": {"engine": target_engine},
    }

    # Source engine forecast.
    src_forecast = None
    if source_engine.lower() == "prophet":
        try:
            from prophet import Prophet  # type: ignore[import-untyped]

            m = Prophet()
            m.fit(train.rename(columns={"ds": "ds", "y": "y"}))
            future = m.make_future_dataframe(periods=horizon, freq=freq)
            fc = m.predict(future).tail(horizon)
            src_forecast = fc["yhat"].to_numpy()
        except ImportError:
            results["source"]["error"] = "prophet not installed; pip install prophet"
        except Exception as exc:
            results["source"]["error"] = f"Prophet failed: {exc}"
    elif source_engine.lower() in ("statsmodels", "arima"):
        try:
            from statsmodels.tsa.arima.model import ARIMA  # type: ignore[import-untyped]

            model = ARIMA(train["y"].to_numpy(), order=(1, 1, 1)).fit()
            src_forecast = np.asarray(model.forecast(steps=horizon))
        except ImportError:
            results["source"]["error"] = "statsmodels not installed"
        except Exception as exc:
            results["source"]["error"] = f"statsmodels ARIMA failed: {exc}"
    else:
        results["source"]["error"] = f"Unknown source_engine: {source_engine}"

    if src_forecast is not None:
        results["source"]["smape"] = round(smape(y_test, src_forecast), 4)
        results["source"]["mae"] = round(mae(y_test, src_forecast), 4)

    # Target engine forecast.
    tgt_forecast = None
    if target_engine.lower() == "statsforecast":
        try:
            from statsforecast import StatsForecast  # type: ignore[import-untyped]
            from statsforecast.models import AutoETS  # type: ignore[import-untyped]

            sf_train = train.copy()
            sf_train["unique_id"] = "series_0"
            sf = StatsForecast(models=[AutoETS()], freq=freq)
            fc = sf.forecast(df=sf_train[["unique_id", "ds", "y"]], h=horizon)
            tgt_forecast = fc["AutoETS"].to_numpy()
        except ImportError:
            results["target"]["error"] = "statsforecast not installed"
        except Exception as exc:
            results["target"]["error"] = f"StatsForecast failed: {exc}"
    elif target_engine.lower() == "timegpt":
        try:
            import os

            from nixtla import NixtlaClient  # type: ignore[import-untyped]

            if not os.environ.get("NIXTLA_API_KEY"):
                results["target"]["error"] = "NIXTLA_API_KEY not set"
            else:
                client = NixtlaClient()
                tg_train = train.copy()
                tg_train["unique_id"] = "series_0"
                fc = client.forecast(df=tg_train[["unique_id", "ds", "y"]], h=horizon, freq=freq)
                tgt_forecast = fc["TimeGPT"].to_numpy()
        except ImportError:
            results["target"]["error"] = "nixtla not installed"
        except Exception as exc:
            results["target"]["error"] = f"TimeGPT failed: {exc}"
    else:
        results["target"]["error"] = f"Unknown target_engine: {target_engine}"

    if tgt_forecast is not None:
        results["target"]["smape"] = round(smape(y_test, tgt_forecast), 4)
        results["target"]["mae"] = round(mae(y_test, tgt_forecast), 4)

    # Improvement.
    if src_forecast is not None and tgt_forecast is not None:
        src_smape = results["source"]["smape"]
        tgt_smape = results["target"]["smape"]
        if src_smape > 0:
            improvement_pct = round((src_smape - tgt_smape) / src_smape * 100.0, 2)
        else:
            improvement_pct = 0.0
        results["improvement"] = {
            "smape_pct": improvement_pct,
            "winner": target_engine if tgt_smape < src_smape else source_engine,
        }
        if improvement_pct > 5:
            results["recommendation"] = "MIGRATE — meaningful accuracy improvement"
        elif improvement_pct > -5:
            results["recommendation"] = (
                "MAYBE — accuracy similar; weigh cost / latency / maintenance"
            )
        else:
            results["recommendation"] = "HOLD — source engine is more accurate on this data"

    results["status"] = (
        "success" if (src_forecast is not None or tgt_forecast is not None) else "error"
    )
    results["horizon"] = horizon
    results["freq"] = freq
    results["n_train"] = len(train)
    results["n_test"] = len(test)

    return results


# ---------------------------------------------------------------------------
# MCP server surface
# ---------------------------------------------------------------------------


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_code",
            description="AST-based detection of forecasting library usage in Python source.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_path": {"type": "string"},
                    "code": {"type": "string"},
                },
            },
        ),
        Tool(
            name="generate_plan",
            description="Generate a phased migration plan from analyze_code output.",
            inputSchema={
                "type": "object",
                "properties": {
                    "analysis": {"type": "object"},
                    "target": {"type": "string", "enum": ["timegpt", "statsforecast"]},
                },
                "required": ["analysis"],
            },
        ),
        Tool(
            name="transform_data",
            description="Transform a CSV from source schema to Nixtla canonical (unique_id, ds, y).",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_path": {"type": "string"},
                    "timestamp_col": {"type": "string", "default": "ds"},
                    "value_col": {"type": "string", "default": "y"},
                    "group_col": {"type": "string"},
                    "nan_strategy": {
                        "type": "string",
                        "enum": ["interpolate", "drop", "keep"],
                        "default": "interpolate",
                    },
                },
                "required": ["data_path"],
            },
        ),
        Tool(
            name="generate_code",
            description="Generate Nixtla-equivalent code for the source/target combo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_library": {"type": "string"},
                    "target_library": {"type": "string"},
                    "horizon": {"type": "integer", "default": 14},
                    "freq": {"type": "string", "default": "D"},
                    "season_length": {"type": "integer", "default": 7},
                    "data_path": {"type": "string", "default": "data.csv"},
                    "timestamp_col": {"type": "string", "default": "ds"},
                    "value_col": {"type": "string", "default": "y"},
                    "group_col": {"type": "string"},
                },
                "required": ["source_library"],
            },
        ),
        Tool(
            name="compare_accuracy",
            description="Run source + target engines on the same train/test split and compare metrics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_path": {"type": "string"},
                    "horizon": {"type": "integer", "default": 14},
                    "freq": {"type": "string", "default": "D"},
                    "source_engine": {"type": "string", "default": "prophet"},
                    "target_engine": {"type": "string", "default": "statsforecast"},
                    "timestamp_col": {"type": "string", "default": "ds"},
                    "value_col": {"type": "string", "default": "y"},
                },
                "required": ["data_path"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "analyze_code":
        code = arguments.get("code", "")
        if arguments.get("source_path"):
            try:
                with open(arguments["source_path"], "r", encoding="utf-8") as f:
                    code = f.read()
            except FileNotFoundError:
                return [TextContent(type="text", text=json.dumps({"error": "File not found"}))]
        result = analyze_code(code)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "generate_plan":
        result = generate_plan(
            arguments.get("analysis", {}), target=str(arguments.get("target", "timegpt"))
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "transform_data":
        result = transform_data(
            data_path=str(arguments["data_path"]),
            timestamp_col=str(arguments.get("timestamp_col", "ds")),
            value_col=str(arguments.get("value_col", "y")),
            group_col=arguments.get("group_col"),
            nan_strategy=str(arguments.get("nan_strategy", "interpolate")),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

    elif name == "generate_code":
        result = generate_code(
            source_library=str(arguments["source_library"]),
            target_library=str(arguments.get("target_library", "timegpt")),
            horizon=int(arguments.get("horizon", 14)),
            freq=str(arguments.get("freq", "D")),
            season_length=int(arguments.get("season_length", 7)),
            data_path=str(arguments.get("data_path", "data.csv")),
            timestamp_col=str(arguments.get("timestamp_col", "ds")),
            value_col=str(arguments.get("value_col", "y")),
            group_col=arguments.get("group_col"),
            original_file=str(arguments.get("original_file", "original_model.py")),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "compare_accuracy":
        result = compare_accuracy(
            data_path=str(arguments["data_path"]),
            horizon=int(arguments.get("horizon", 14)),
            freq=str(arguments.get("freq", "D")),
            source_engine=str(arguments.get("source_engine", "prophet")),
            target_engine=str(arguments.get("target_engine", "statsforecast")),
            timestamp_col=str(arguments.get("timestamp_col", "ds")),
            value_col=str(arguments.get("value_col", "y")),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
