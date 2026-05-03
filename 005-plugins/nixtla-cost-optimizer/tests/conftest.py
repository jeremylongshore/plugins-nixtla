"""Pytest fixtures for nixtla-cost-optimizer tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def small_batch_calls():
    """100 calls, 70% with <10 series — strong batching signal."""
    calls = []
    for i in range(100):
        n = 5 if i < 70 else 50
        calls.append(
            {
                "series_count": n,
                "horizon": 30,
                "freq": "D",
                "input_hash": f"unique_{i}",
            }
        )
    return calls


@pytest.fixture
def redundant_calls():
    """100 calls with only 5 unique payload signatures — strong cache signal."""
    calls = []
    for i in range(100):
        sig = i % 5  # Only 5 unique signatures.
        calls.append(
            {
                "series_count": 20,
                "horizon": 14,
                "freq": "D",
                "input_hash": f"sig_{sig}",
            }
        )
    return calls


@pytest.fixture
def short_horizon_calls():
    """100 calls, 50% with horizon<=3 — strong hybrid-routing signal."""
    calls = []
    for i in range(100):
        h = 1 if i < 50 else 30
        calls.append(
            {
                "series_count": 20,
                "horizon": h,
                "freq": "D",
                "input_hash": f"unique_{i}",
            }
        )
    return calls
