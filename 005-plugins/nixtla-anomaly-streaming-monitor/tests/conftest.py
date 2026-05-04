"""Pytest fixtures for nixtla-anomaly-streaming-monitor tests."""

from __future__ import annotations

from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def plugin_root():
    return PLUGIN_ROOT


@pytest.fixture
def ts_server_source(plugin_root):
    return (plugin_root / "src" / "mcp-server" / "index.ts").read_text(encoding="utf-8")


@pytest.fixture
def readme_source(plugin_root):
    return (plugin_root / "README.md").read_text(encoding="utf-8")


@pytest.fixture
def plugin_manifest(plugin_root):
    import json

    return json.loads((plugin_root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
