"""
Nixtla Search-to-Slack Plugin
A construction kit for building time-series content discovery and curation workflows.

This is an MVP implementation and example, not a production service.
Not endorsed or operated by Nixtla.
"""

__version__ = "1.0.0"
__author__ = "Jeremy Longshore"

from .main import run_digest

__all__ = ["run_digest"]
