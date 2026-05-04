"""Pytest fixtures for nixtla-bigquery-forecaster."""

from __future__ import annotations

import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

# src/ is a proper Python package (has __init__.py with relative imports).
# Add the plugin root to sys.path so tests can do `from src.<module> import ...`.
sys.path.insert(0, str(PLUGIN_ROOT))
