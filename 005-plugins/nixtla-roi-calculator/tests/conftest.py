"""Pytest fixtures for nixtla-roi-calculator tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make the plugin's scripts/ importable as a top-level package
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def sample_roi_inputs():
    """A representative ROI scenario with positive savings."""
    import roi_calculator_mcp as mcp

    return mcp.ROIInputs(
        current_tool_cost=2000.0,
        fte_hours_per_week=20.0,
        fte_hourly_rate=80.0,
        infrastructure_cost=500.0,
        forecast_volume_monthly=10000,
        timegpt_price_per_1k=0.10,
    )


@pytest.fixture
def sample_roi_result(sample_roi_inputs):
    """A pre-computed ROI result dict (the schema generate_pdf_report expects)."""
    import roi_calculator_mcp as mcp

    return mcp.calculate_roi_internal(sample_roi_inputs)


@pytest.fixture
def clean_sf_env(monkeypatch):
    """Ensure Salesforce env vars are unset for dry-run tests."""
    monkeypatch.delenv("NIXTLA_SF_INSTANCE_URL", raising=False)
    monkeypatch.delenv("NIXTLA_SF_ACCESS_TOKEN", raising=False)
    return monkeypatch
