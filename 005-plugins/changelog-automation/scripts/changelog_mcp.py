#!/usr/bin/env python3
"""
Changelog Automation MCP Server.

Real implementations for:
  - fetch_changelog_data: GitHub via `gh` CLI subprocess, git log via `git`
    subprocess, optional Slack via slack-sdk (lazy import).
  - validate_frontmatter: jsonschema Draft7Validator against a defined
    CHANGELOG_FRONTMATTER_SCHEMA.
  - get_changelog_config: load + validate .changelog-config.json (real).

Slack integration follows the canonical patterns in
~/000-projects/claude-code-slack-channel/ (CCS repo) per principal direction.
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# Frontmatter schema (jsonschema Draft 7)
# ---------------------------------------------------------------------------


CHANGELOG_FRONTMATTER_SCHEMA: Dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Changelog Entry Frontmatter",
    "type": "object",
    "required": ["version", "date"],
    "properties": {
        "version": {
            "type": "string",
            "pattern": r"^\d+\.\d+\.\d+(-[A-Za-z0-9.-]+)?$",
            "description": "Semantic version, e.g. 1.2.3 or 1.2.3-rc.1",
        },
        "date": {
            "type": "string",
            "format": "date",
            "description": "ISO 8601 date (YYYY-MM-DD)",
        },
        "type": {
            "type": "string",
            "enum": ["feature", "fix", "docs", "chore", "breaking", "release"],
        },
        "categories": {
            "type": "array",
            "items": {"type": "string"},
        },
        "audience": {
            "type": "string",
            "enum": ["internal", "public", "both"],
        },
        "breaking_changes": {"type": "boolean"},
        "authors": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "additionalProperties": True,
}


# ---------------------------------------------------------------------------
# Source fetchers
# ---------------------------------------------------------------------------


def _fetch_github(start_date: str, end_date: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch closed PRs from a repo via `gh` CLI subprocess.

    Required config: `repo` (owner/name).
    Optional: `state` (default "merged"), `limit` (default 100), `labels` (list).
    """
    repo = config.get("repo")
    if not repo:
        return {"status": "error", "error": "github source requires config.repo (owner/name)"}

    state = config.get("state", "merged")
    limit = int(config.get("limit", 100))
    labels = config.get("labels", [])

    cmd = [
        "gh",
        "pr",
        "list",
        "--repo",
        str(repo),
        "--state",
        str(state),
        "--limit",
        str(limit),
        "--search",
        f"merged:{start_date}..{end_date}",
        "--json",
        "number,title,body,author,mergedAt,labels,url",
    ]
    if labels:
        cmd[-1] = "number,title,body,author,mergedAt,labels,url"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        return {"status": "error", "error": "gh CLI not installed"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "gh CLI timed out after 60s"}

    if result.returncode != 0:
        return {
            "status": "error",
            "error": f"gh CLI failed (exit {result.returncode}): {result.stderr.strip()}",
        }

    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {"status": "error", "error": f"failed to parse gh output: {exc}"}

    items = []
    for pr in prs:
        if labels:
            pr_label_names = {lbl.get("name", "") for lbl in pr.get("labels", [])}
            if not pr_label_names.intersection(labels):
                continue
        items.append(
            {
                "id": f"github-pr-{pr.get('number')}",
                "title": pr.get("title", ""),
                "body": pr.get("body", "") or "",
                "author": (
                    pr.get("author", {}).get("login", "")
                    if isinstance(pr.get("author"), dict)
                    else str(pr.get("author", ""))
                ),
                "labels": [lbl.get("name", "") for lbl in pr.get("labels", [])],
                "url": pr.get("url", ""),
                "timestamp": pr.get("mergedAt", ""),
                "type": "feature",  # could be inferred from labels
            }
        )

    return {
        "status": "success",
        "data": {
            "items": items,
            "count": len(items),
            "source": "github",
            "date_range": f"{start_date} to {end_date}",
        },
    }


def _fetch_git(start_date: str, end_date: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch commits via `git log` subprocess.

    Optional config: `path` (default current dir), `pattern` (commit msg
    grep, e.g. "feat\\|fix\\|docs"), `limit` (default 200).
    """
    path = config.get("path", ".")
    limit = int(config.get("limit", 200))

    cmd = [
        "git",
        "-C",
        str(path),
        "log",
        f"--since={start_date}",
        f"--until={end_date} 23:59:59",
        f"--max-count={limit}",
        "--pretty=format:%H|%an|%ae|%aI|%s",
    ]
    pattern = config.get("pattern")
    if pattern:
        cmd.append(f"--grep={pattern}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except FileNotFoundError:
        return {"status": "error", "error": "git not installed"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "git log timed out after 30s"}

    if result.returncode != 0:
        return {
            "status": "error",
            "error": f"git log failed (exit {result.returncode}): {result.stderr.strip()}",
        }

    items = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 4)
        if len(parts) != 5:
            continue
        sha, author_name, author_email, timestamp, subject = parts
        items.append(
            {
                "id": f"git-{sha[:8]}",
                "title": subject,
                "body": "",
                "author": author_name,
                "author_email": author_email,
                "labels": [],
                "url": "",
                "timestamp": timestamp,
                "type": _infer_type_from_subject(subject),
            }
        )

    return {
        "status": "success",
        "data": {
            "items": items,
            "count": len(items),
            "source": "git",
            "date_range": f"{start_date} to {end_date}",
        },
    }


def _infer_type_from_subject(subject: str) -> str:
    """Infer changelog type from a Conventional Commits-style subject."""
    s = subject.lower().strip()
    for prefix, kind in [
        ("feat", "feature"),
        ("fix", "fix"),
        ("docs", "docs"),
        ("chore", "chore"),
        ("refactor", "chore"),
        ("perf", "feature"),
        ("breaking", "breaking"),
    ]:
        if s.startswith(prefix + ":") or s.startswith(prefix + "("):
            return kind
    return "chore"


def _fetch_slack(start_date: str, end_date: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch messages from a Slack channel via slack-sdk (CCS repo pattern).

    Required: NIXTLA_SLACK_TOKEN env var; config.channel (channel ID or name).
    Optional: config.pattern (substring filter on message text).

    Per principal direction: this uses the canonical pattern from
    ~/000-projects/claude-code-slack-channel/ — slack-sdk is lazy-imported.
    """
    token = os.environ.get("NIXTLA_SLACK_TOKEN")
    if not token:
        return {
            "status": "error",
            "error": "NIXTLA_SLACK_TOKEN env var not set",
            "data": {"items": [], "count": 0, "source": "slack"},
        }

    channel = config.get("channel")
    if not channel:
        return {"status": "error", "error": "slack source requires config.channel"}

    try:
        from slack_sdk import WebClient  # type: ignore[import-untyped]
        from slack_sdk.errors import SlackApiError  # type: ignore[import-untyped]
    except ImportError:
        return {"status": "error", "error": "slack-sdk not installed"}

    pattern = config.get("pattern", "")
    client = WebClient(token=token)

    # Convert dates to unix timestamps for Slack API.
    try:
        start_ts = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
        end_ts = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59).timestamp()
    except ValueError as exc:
        return {"status": "error", "error": f"invalid date format: {exc}"}

    items: List[Dict[str, Any]] = []
    try:
        cursor: Optional[str] = None
        while True:
            kwargs: Dict[str, Any] = {
                "channel": channel,
                "oldest": str(start_ts),
                "latest": str(end_ts),
                "limit": 200,
            }
            if cursor:
                kwargs["cursor"] = cursor
            resp = client.conversations_history(**kwargs)
            for msg in resp.get("messages", []):
                text = msg.get("text", "")
                if pattern and pattern.lower() not in text.lower():
                    continue
                items.append(
                    {
                        "id": f"slack-{msg.get('ts')}",
                        "title": text[:120],
                        "body": text,
                        "author": msg.get("user", ""),
                        "labels": [],
                        "url": "",
                        "timestamp": datetime.fromtimestamp(float(msg.get("ts", 0))).isoformat(),
                        "type": "chore",
                    }
                )
            cursor = (resp.get("response_metadata") or {}).get("next_cursor")
            if not cursor:
                break
    except SlackApiError as exc:
        return {"status": "error", "error": f"Slack API error: {exc.response.get('error', exc)}"}

    return {
        "status": "success",
        "data": {
            "items": items,
            "count": len(items),
            "source": "slack",
            "date_range": f"{start_date} to {end_date}",
        },
    }


# ---------------------------------------------------------------------------
# MCP server class
# ---------------------------------------------------------------------------


class ChangelogMCPServer:
    """MCP server for changelog automation tools."""

    def __init__(self):
        self.server = Server("changelog-mcp")
        self.setup_tools()

    def setup_tools(self):
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="fetch_changelog_data",
                    description=(
                        "Fetch real data from GitHub (via gh CLI), git log, "
                        "or optional Slack (slack-sdk + NIXTLA_SLACK_TOKEN)."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source_type": {"type": "string", "enum": ["github", "slack", "git"]},
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                            "config": {"type": "object"},
                        },
                        "required": ["source_type", "start_date", "end_date", "config"],
                    },
                ),
                Tool(
                    name="validate_frontmatter",
                    description="Validate YAML frontmatter against the CHANGELOG_FRONTMATTER_SCHEMA via jsonschema Draft7Validator.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "frontmatter": {"type": "object"},
                            "schema_path": {"type": "string"},
                        },
                        "required": ["frontmatter"],
                    },
                ),
                Tool(
                    name="get_changelog_config",
                    description="Load and validate .changelog-config.json",
                    inputSchema={
                        "type": "object",
                        "properties": {"config_path": {"type": "string"}},
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            try:
                if name == "fetch_changelog_data":
                    result = await self.fetch_changelog_data(**arguments)
                elif name == "validate_frontmatter":
                    result = await self.validate_frontmatter(**arguments)
                elif name == "get_changelog_config":
                    result = await self.get_changelog_config(**arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as exc:
                err = {"status": "error", "error": str(exc), "tool": name}
                return [TextContent(type="text", text=json.dumps(err, indent=2))]

    async def fetch_changelog_data(
        self,
        source_type: str,
        start_date: str,
        end_date: str,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Fetch real data from the configured source."""
        src = source_type.lower()
        if src == "github":
            base = _fetch_github(start_date, end_date, config)
        elif src == "git":
            base = _fetch_git(start_date, end_date, config)
        elif src == "slack":
            base = _fetch_slack(start_date, end_date, config)
        else:
            return {
                "status": "error",
                "error": f"unknown source_type: {source_type}",
            }

        base["version"] = VERSION
        base["timestamp"] = datetime.utcnow().isoformat()
        return base

    async def validate_frontmatter(
        self, frontmatter: Dict[str, Any], schema_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Validate frontmatter against jsonschema."""
        try:
            from jsonschema import Draft7Validator  # type: ignore[import-untyped]
        except ImportError:
            return {
                "status": "error",
                "error": "jsonschema not installed; pip install jsonschema",
                "version": VERSION,
            }

        # Load schema (custom path or default).
        if schema_path:
            try:
                with open(schema_path, "r", encoding="utf-8") as f:
                    schema = json.load(f)
            except FileNotFoundError:
                return {
                    "status": "error",
                    "error": f"schema_path not found: {schema_path}",
                    "version": VERSION,
                }
            except json.JSONDecodeError as exc:
                return {
                    "status": "error",
                    "error": f"invalid JSON in schema_path: {exc}",
                    "version": VERSION,
                }
        else:
            schema = CHANGELOG_FRONTMATTER_SCHEMA

        validator = Draft7Validator(schema)
        errors: List[Dict[str, Any]] = []
        for err in validator.iter_errors(frontmatter):
            errors.append(
                {
                    "path": ".".join(str(p) for p in err.absolute_path) or "(root)",
                    "message": err.message,
                    "validator": err.validator,
                }
            )

        # Optional warnings (non-blocking missing fields).
        warnings: List[str] = []
        for opt in ("authors", "categories", "audience"):
            if opt not in frontmatter:
                warnings.append(f"optional field '{opt}' not provided")

        return {
            "status": "success",
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "schema_version": "1.0",
            "version": VERSION,
        }

    async def get_changelog_config(
        self, config_path: str = ".changelog-config.json"
    ) -> Dict[str, Any]:
        """Load and validate the changelog config file."""
        config_file = Path(config_path)
        if not config_file.exists():
            return {
                "status": "error",
                "error": f"Config file not found: {config_path}",
                "suggestion": "Run /changelog-validate to create example config",
            }
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as exc:
            return {
                "status": "error",
                "error": f"Invalid JSON in config file: {exc}",
                "config_path": config_path,
            }

        required_fields = ["sources", "template", "output_path"]
        errors = [f"Missing required field: {f}" for f in required_fields if f not in config]

        return {
            "status": "success",
            "config": config,
            "validation": {"valid": len(errors) == 0, "errors": errors},
            "version": VERSION,
            "config_path": str(config_file.absolute()),
        }


def main():
    server = ChangelogMCPServer()

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.server.run(
                read_stream, write_stream, server.server.create_initialization_options()
            )

    asyncio.run(run())


if __name__ == "__main__":
    main()
