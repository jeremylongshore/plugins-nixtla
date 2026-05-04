"""Pytest fixtures for nixtla-docs-qa-generator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def plugin_root():
    return PLUGIN_ROOT


@pytest.fixture
def plugin_manifest():
    return json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))


@pytest.fixture
def readme_source():
    return (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")


@pytest.fixture
def mcp_source():
    return (SCRIPTS_DIR / "nixtla_docs_qa_generator_mcp.py").read_text(encoding="utf-8")
