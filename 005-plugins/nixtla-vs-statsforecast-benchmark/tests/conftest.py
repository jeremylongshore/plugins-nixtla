"""Pytest fixtures for nixtla-vs-statsforecast-benchmark tests."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def sample_long_df():
    """Three series, 60 observations each, daily frequency, with seasonality."""
    rng = np.random.default_rng(0)
    rows = []
    for uid in ["s1", "s2", "s3"]:
        for i in range(60):
            ds = pd.Timestamp("2026-01-01") + pd.Timedelta(days=i)
            t = i
            base = {"s1": 100.0, "s2": 50.0, "s3": 200.0}[uid]
            seasonal = 10.0 * np.sin(2.0 * np.pi * t / 7.0)
            noise = rng.normal(0, 1.0)
            rows.append({"unique_id": uid, "ds": ds, "y": base + seasonal + noise + 0.5 * t})
    return pd.DataFrame(rows)


@pytest.fixture
def sample_csv_path(tmp_path, sample_long_df):
    """Write the sample DataFrame to a CSV and return the path."""
    p = tmp_path / "sample.csv"
    sample_long_df.to_csv(p, index=False)
    return str(p)
