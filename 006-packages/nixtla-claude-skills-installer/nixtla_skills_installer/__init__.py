"""
Nixtla Claude Skills Installer

Per-project installation and update utility for Nixtla Claude Code skills.

This package provides a CLI tool (`nixtla-skills`) to install and update
Nixtla forecasting skills in your Claude Code projects.

Usage:
    nixtla-skills init    # First-time install in current project
    nixtla-skills update  # Refresh installed skills
"""

__version__ = "0.4.0"
__author__ = "Intent Solutions (Jeremy Longshore)"
__email__ = "jeremy@intentsolutions.io"

from .cli import main
from .core import (
    copy_skills_to_project,
    ensure_skills_directory,
    list_installed_skills,
    locate_skills_source,
)

__all__ = [
    "locate_skills_source",
    "ensure_skills_directory",
    "copy_skills_to_project",
    "list_installed_skills",
    "main",
]
