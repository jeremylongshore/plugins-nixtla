"""Unit tests for changelog-automation MCP server."""

from __future__ import annotations

import asyncio
import json
import subprocess
from unittest.mock import patch

import changelog_mcp as mod
import pytest

# ---------------------------------------------------------------------------
# _fetch_github
# ---------------------------------------------------------------------------


class TestFetchGithub:
    def test_missing_repo_returns_error(self):
        result = mod._fetch_github("2026-01-01", "2026-01-31", {})
        assert result["status"] == "error"
        assert "repo" in result["error"]

    def test_gh_not_installed_returns_error(self):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = mod._fetch_github("2026-01-01", "2026-01-31", {"repo": "owner/name"})
        assert result["status"] == "error"
        assert "gh CLI not installed" in result["error"]

    def test_gh_timeout_returns_error(self):
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gh", 60)):
            result = mod._fetch_github("2026-01-01", "2026-01-31", {"repo": "owner/name"})
        assert result["status"] == "error"
        assert "timed out" in result["error"]

    def test_successful_fetch(self):
        fake_prs = [
            {
                "number": 123,
                "title": "Add feature",
                "body": "Description",
                "author": {"login": "alice"},
                "mergedAt": "2026-01-15T10:00:00Z",
                "labels": [{"name": "feature"}],
                "url": "https://github.com/x/y/pull/123",
            }
        ]
        fake_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=json.dumps(fake_prs), stderr=""
        )
        with patch("subprocess.run", return_value=fake_result):
            result = mod._fetch_github("2026-01-01", "2026-01-31", {"repo": "owner/name"})
        assert result["status"] == "success"
        assert result["data"]["count"] == 1
        assert result["data"]["items"][0]["author"] == "alice"

    def test_label_filter(self):
        fake_prs = [
            {
                "number": 1,
                "title": "no",
                "body": "",
                "author": {"login": "x"},
                "mergedAt": "",
                "labels": [{"name": "chore"}],
                "url": "",
            },
            {
                "number": 2,
                "title": "yes",
                "body": "",
                "author": {"login": "x"},
                "mergedAt": "",
                "labels": [{"name": "feature"}],
                "url": "",
            },
        ]
        fake_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=json.dumps(fake_prs), stderr=""
        )
        with patch("subprocess.run", return_value=fake_result):
            result = mod._fetch_github(
                "2026-01-01",
                "2026-01-31",
                {"repo": "owner/name", "labels": ["feature"]},
            )
        assert result["data"]["count"] == 1
        assert result["data"]["items"][0]["title"] == "yes"


# ---------------------------------------------------------------------------
# _fetch_git
# ---------------------------------------------------------------------------


class TestFetchGit:
    def test_git_not_installed(self):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = mod._fetch_git("2026-01-01", "2026-01-31", {})
        assert result["status"] == "error"
        assert "git not installed" in result["error"]

    def test_successful_fetch(self):
        fake_log = (
            "abc123def|alice|alice@example.com|2026-01-15T10:00:00+00:00|feat: add thing\n"
            "def456789|bob|bob@example.com|2026-01-16T11:00:00+00:00|fix: a bug\n"
        )
        fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout=fake_log, stderr="")
        with patch("subprocess.run", return_value=fake_result):
            result = mod._fetch_git("2026-01-01", "2026-01-31", {})
        assert result["status"] == "success"
        assert result["data"]["count"] == 2
        assert result["data"]["items"][0]["author"] == "alice"
        assert result["data"]["items"][0]["type"] == "feature"
        assert result["data"]["items"][1]["type"] == "fix"

    def test_empty_log(self):
        fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with patch("subprocess.run", return_value=fake_result):
            result = mod._fetch_git("2026-01-01", "2026-01-31", {})
        assert result["data"]["count"] == 0


# ---------------------------------------------------------------------------
# _infer_type_from_subject
# ---------------------------------------------------------------------------


class TestInferType:
    @pytest.mark.parametrize(
        "subject,expected",
        [
            ("feat: add x", "feature"),
            ("feat(scope): add x", "feature"),
            ("fix: bug", "fix"),
            ("docs: readme", "docs"),
            ("chore: bump deps", "chore"),
            ("refactor: cleanup", "chore"),
            ("perf: faster", "feature"),
            ("BREAKING: drop py39", "breaking"),
            ("random commit message", "chore"),
        ],
    )
    def test_classifications(self, subject, expected):
        assert mod._infer_type_from_subject(subject) == expected


# ---------------------------------------------------------------------------
# _fetch_slack
# ---------------------------------------------------------------------------


class TestFetchSlack:
    def test_missing_token(self, monkeypatch):
        monkeypatch.delenv("NIXTLA_SLACK_TOKEN", raising=False)
        result = mod._fetch_slack("2026-01-01", "2026-01-31", {"channel": "C123"})
        assert result["status"] == "error"
        assert "NIXTLA_SLACK_TOKEN" in result["error"]

    def test_missing_channel(self, monkeypatch):
        monkeypatch.setenv("NIXTLA_SLACK_TOKEN", "test")
        result = mod._fetch_slack("2026-01-01", "2026-01-31", {})
        assert result["status"] == "error"
        assert "channel" in result["error"]


# ---------------------------------------------------------------------------
# validate_frontmatter
# ---------------------------------------------------------------------------


class TestValidateFrontmatter:
    @pytest.fixture
    def server(self):
        return mod.ChangelogMCPServer()

    def test_valid_frontmatter(self, server):
        fm = {"version": "1.0.0", "date": "2026-01-15", "type": "feature"}
        result = asyncio.run(server.validate_frontmatter(frontmatter=fm))
        assert result["status"] == "success"
        assert result["valid"] is True
        assert result["errors"] == []

    def test_missing_required_field(self, server):
        fm = {"version": "1.0.0"}  # missing date
        result = asyncio.run(server.validate_frontmatter(frontmatter=fm))
        assert result["valid"] is False
        assert any("date" in e["path"] or "date" in e["message"] for e in result["errors"])

    def test_invalid_version_pattern(self, server):
        fm = {"version": "not-a-version", "date": "2026-01-15"}
        result = asyncio.run(server.validate_frontmatter(frontmatter=fm))
        assert result["valid"] is False

    def test_invalid_type_enum(self, server):
        fm = {"version": "1.0.0", "date": "2026-01-15", "type": "not_a_real_type"}
        result = asyncio.run(server.validate_frontmatter(frontmatter=fm))
        assert result["valid"] is False

    def test_warnings_for_optional_fields(self, server):
        fm = {"version": "1.0.0", "date": "2026-01-15"}
        result = asyncio.run(server.validate_frontmatter(frontmatter=fm))
        assert any("authors" in w for w in result["warnings"])
        assert any("audience" in w for w in result["warnings"])

    def test_external_schema_path_not_found(self, server):
        result = asyncio.run(
            server.validate_frontmatter(
                frontmatter={"version": "1.0.0"}, schema_path="/nonexistent.json"
            )
        )
        assert result["status"] == "error"


# ---------------------------------------------------------------------------
# get_changelog_config
# ---------------------------------------------------------------------------


class TestGetChangelogConfig:
    @pytest.fixture
    def server(self):
        return mod.ChangelogMCPServer()

    def test_missing_config(self, server, tmp_path):
        path = tmp_path / "missing.json"
        result = asyncio.run(server.get_changelog_config(config_path=str(path)))
        assert result["status"] == "error"
        assert "not found" in result["error"]

    def test_valid_config(self, server, tmp_path):
        path = tmp_path / "config.json"
        path.write_text(
            json.dumps(
                {
                    "sources": {"github": {"repo": "owner/name"}},
                    "template": "{date}",
                    "output_path": "CHANGELOG.md",
                }
            )
        )
        result = asyncio.run(server.get_changelog_config(config_path=str(path)))
        assert result["status"] == "success"
        assert result["validation"]["valid"] is True

    def test_missing_required_fields(self, server, tmp_path):
        path = tmp_path / "config.json"
        path.write_text(json.dumps({"sources": {}}))
        result = asyncio.run(server.get_changelog_config(config_path=str(path)))
        assert result["validation"]["valid"] is False
        assert len(result["validation"]["errors"]) >= 2  # missing template + output_path

    def test_invalid_json(self, server, tmp_path):
        path = tmp_path / "config.json"
        path.write_text("not valid json {")
        result = asyncio.run(server.get_changelog_config(config_path=str(path)))
        assert result["status"] == "error"
        assert "Invalid JSON" in result["error"]


# ---------------------------------------------------------------------------
# fetch_changelog_data dispatch
# ---------------------------------------------------------------------------


class TestFetchChangelogData:
    @pytest.fixture
    def server(self):
        return mod.ChangelogMCPServer()

    def test_dispatch_to_git(self, server):
        fake_log = "abc|alice|alice@example.com|2026-01-15T10:00:00|chore: x\n"
        fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout=fake_log, stderr="")
        with patch("subprocess.run", return_value=fake_result):
            result = asyncio.run(
                server.fetch_changelog_data(
                    source_type="git",
                    start_date="2026-01-01",
                    end_date="2026-01-31",
                    config={},
                )
            )
        assert result["status"] == "success"
        assert result["data"]["source"] == "git"

    def test_unknown_source(self, server):
        result = asyncio.run(
            server.fetch_changelog_data(
                source_type="oracle",
                start_date="2026-01-01",
                end_date="2026-01-31",
                config={},
            )
        )
        assert result["status"] == "error"
        assert "unknown" in result["error"].lower()
