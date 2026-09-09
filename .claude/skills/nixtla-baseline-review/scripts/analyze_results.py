#!/usr/bin/env python3
"""Validate and summarize one Nixtla Baseline Lab results CSV."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {"series_id", "model", "sMAPE", "MASE"}


def parse_number(raw: str, field: str, row_number: int) -> float:
    """Parse a finite metric value or raise a row-specific error."""
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"row {row_number}: {field} is not numeric: {raw!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"row {row_number}: {field} must be finite")
    if field == "sMAPE" and not 0 <= value <= 200:
        raise ValueError(f"row {row_number}: sMAPE must be between 0 and 200")
    if field == "MASE" and value < 0:
        raise ValueError(f"row {row_number}: MASE must be non-negative")
    return value


def load_rows(path: Path) -> list[dict[str, Any]]:
    """Load rows while enforcing schema, identity, and metric invariants."""
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")

        rows: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for row_number, raw in enumerate(reader, start=2):
            series_id = (raw.get("series_id") or "").strip()
            model = (raw.get("model") or "").strip()
            if not series_id or not model:
                raise ValueError(f"row {row_number}: series_id and model are required")
            identity = (series_id, model)
            if identity in seen:
                raise ValueError(
                    f"row {row_number}: duplicate series/model pair {series_id!r}/{model!r}"
                )
            seen.add(identity)
            rows.append(
                {
                    "series_id": series_id,
                    "model": model,
                    "sMAPE": parse_number(raw.get("sMAPE", ""), "sMAPE", row_number),
                    "MASE": parse_number(raw.get("MASE", ""), "MASE", row_number),
                }
            )
    if not rows:
        raise ValueError("results CSV has no data rows")
    return rows


def rounded(value: float) -> float:
    """Use stable precision without turning the receipt into display prose."""
    return round(value, 6)


def summarize(path: Path) -> dict[str, Any]:
    """Build a deterministic quality and aggregate receipt."""
    rows = load_rows(path)
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_series: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_model[row["model"]].append(row)
        by_series[row["series_id"]].append(row)

    wins = {model: 0 for model in by_model}
    ties: list[dict[str, Any]] = []
    for series_id, series_rows in sorted(by_series.items()):
        best = min(row["sMAPE"] for row in series_rows)
        winners = sorted(row["model"] for row in series_rows if math.isclose(row["sMAPE"], best))
        for model in winners:
            wins[model] += 1
        if len(winners) > 1:
            ties.append({"series_id": series_id, "sMAPE": best, "models": winners})

    models: dict[str, Any] = {}
    for model, model_rows in sorted(by_model.items()):
        smape = [row["sMAPE"] for row in model_rows]
        mase = [row["MASE"] for row in model_rows]
        models[model] = {
            "rows": len(model_rows),
            "coverage_series": sorted(row["series_id"] for row in model_rows),
            "mean_sMAPE": rounded(statistics.fmean(smape)),
            "median_sMAPE": rounded(statistics.median(smape)),
            "population_stddev_sMAPE": rounded(statistics.pstdev(smape)),
            "mean_MASE": rounded(statistics.fmean(mase)),
            "median_MASE": rounded(statistics.median(mase)),
            "sMAPE_wins_including_ties": wins[model],
        }

    all_models = sorted(by_model)
    coverage_gaps = {
        series_id: sorted(set(all_models) - {row["model"] for row in series_rows})
        for series_id, series_rows in sorted(by_series.items())
        if len(series_rows) != len(all_models)
    }
    return {
        "source": str(path.resolve()),
        "status": "valid",
        "row_count": len(rows),
        "series_count": len(by_series),
        "model_count": len(by_model),
        "models": models,
        "coverage_gaps": coverage_gaps,
        "sMAPE_ties": ties,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_csv", type=Path)
    args = parser.parse_args()
    try:
        receipt = summarize(args.results_csv)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
