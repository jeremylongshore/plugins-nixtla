"""Pytest fixtures for nixtla-snowflake-adapter."""

from __future__ import annotations

import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"

# Make scripts/snowflake_mcp.py importable.
sys.path.insert(0, str(SCRIPTS_DIR))
