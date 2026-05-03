"""Pytest fixtures for nixtla-forecast-explainer tests."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def synthetic_seasonal_series():
    """A 60-day daily series with weekly seasonality + trend + noise.

    Constructed so STL can recover trend + seasonality cleanly.
    """
    rng = np.random.default_rng(42)
    n = 60
    period = 7
    t = np.arange(n)
    trend = 0.5 * t + 100.0
    seasonal = 10.0 * np.sin(2.0 * np.pi * t / period)
    noise = rng.normal(0, 1.0, n)
    values = trend + seasonal + noise
    return [{"ds": f"2026-01-{(i % 30) + 1:02d}", "y": float(v)} for i, v in enumerate(values)]


@pytest.fixture
def synthetic_target_and_drivers():
    """A target series + 3 candidate drivers with known correlation properties.

    - 'strong_pos': nearly perfectly correlated with target (correlation ~1).
    - 'noise': pure noise, no relationship.
    - 'inverse': inverted target (correlation ~-1).
    """
    rng = np.random.default_rng(7)
    n = 30
    target = [float(v) for v in rng.normal(100, 10, n)]
    strong_pos = [v + rng.normal(0, 0.1) for v in target]
    noise = [float(v) for v in rng.normal(0, 5, n)]
    inverse = [-v for v in target]
    return {
        "target": target,
        "candidates": {
            "strong_pos": strong_pos,
            "noise": noise,
            "inverse": inverse,
        },
    }
