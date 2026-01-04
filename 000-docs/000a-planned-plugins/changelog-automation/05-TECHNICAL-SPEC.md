# Changelog Automation - Technical Specification

**Plugin:** changelog-automation
**Version:** 0.1.0
**Last Updated:** 2025-12-28

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.10+ | Core implementation, MCP server |
| MCP Framework | mcp.server | Latest | Expose tools to Claude via stdio |
| HTTP Client | aiohttp | 3.9+ | Async GitHub/Slack API calls |
| Git Operations | GitPython | 3.1+ | Local git log parsing |
| Schema Validation | jsonschema | 4.20+ | Config + frontmatter validation |
| YAML Processing | PyYAML | 6.0+ | Frontmatter parsing |
| Testing | pytest | 7.4+ | Unit tests + smoke tests |
| GraphQL | gql | 3.5+ | GitHub GraphQL queries |

---

## Dependencies

### Python Dependencies
```
# requirements.txt
mcp>=0.9.0
aiohttp>=3.9.0
GitPython>=3.1.40
jsonschema>=4.20.0
PyYAML>=6.0.1
gql>=3.5.0
python-dotenv>=1.0.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

### System Dependencies
- Git 2.30+ (for commit log parsing)
- Python 3.10+ with asyncio support

### External Services
| Service | Required | Purpose |
|---------|----------|---------|
| GitHub GraphQL API | Yes | Fetch PRs, issues, releases (primary data source) |
| Slack Web API | No | Fetch channel messages (optional) |
| Git (local) | Yes | Parse commit history (offline, no API) |

---

## File Structure

```
005-plugins/changelog-automation/
├── .claude-plugin/
│   └── plugin.json                     # Plugin manifest
├── .mcp.json                           # MCP server config
├── commands/
│   ├── changelog-weekly.md             # /changelog-weekly command
│   ├── changelog-custom.md             # /changelog-custom command
│   └── changelog-validate.md           # /changelog-validate command
├── skills/
│   └── .claude/skills/changelog-orchestrator/
│       ├── SKILL.md                    # 6-phase workflow orchestration
│       ├── scripts/
│       │   ├── validate_template.py    # Template structure checker
│       │   └── quality_scorer.py       # Deterministic quality checks
│       └── assets/templates/
│           ├── default-changelog.md    # Default template
│           ├── weekly-template.md      # Weekly format
│           └── release-template.md     # Release notes format
├── scripts/
│   ├── changelog_mcp.py                # MCP server (6 async tools)
│   ├── sources/
│   │   ├── base.py                     # Abstract ChangelogDataSource
│   │   ├── github_source.py            # GitHub GraphQL implementation
│   │   ├── slack_source.py             # Slack Web API implementation
│   │   └── git_source.py               # Git log parser
│   ├── formatters/
│   │   ├── frontmatter.py              # YAML frontmatter generator
│   │   └── markdown.py                 # Markdown formatting utilities
│   ├── validators/
│   │   ├── schema_validator.py         # JSON Schema validation
│   │   └── content_validator.py        # Deterministic quality checks
│   └── requirements.txt                # Python dependencies
├── tests/
│   ├── run_changelog_smoke.py          # Golden task smoke test
│   ├── test_sources.py                 # Data source unit tests
│   ├── test_validators.py              # Validation tests
│   ├── test_mcp_tools.py               # MCP tool tests
│   └── fixtures/
│       ├── github_prs.json             # Sample GitHub data
│       ├── slack_messages.json         # Sample Slack data
│       └── git_log.txt                 # Sample git log
├── config/
│   ├── .changelog-config.schema.json   # JSON Schema for validation
│   └── .changelog-config.example.json  # Example configuration
└── README.md                           # Quick start guide
```

---

## API Reference

### MCP Tool 1: `fetch_changelog_data`

**Description:** Fetch structured data from configured sources (GitHub/Slack/Git)

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `source_type` | string | Yes | - | One of: "github", "slack", "git" |
| `start_date` | string | Yes | - | ISO 8601 date (e.g., "2025-12-21") |
| `end_date` | string | Yes | - | ISO 8601 date (e.g., "2025-12-28") |
| `config` | object | Yes | - | Source-specific config (repo, token, etc.) |

**Returns:**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "PR#123",
        "title": "Add dark mode toggle",
        "type": "feature",
        "author": "jane@example.com",
        "labels": ["enhancement", "ui"],
        "url": "https://github.com/org/repo/pull/123",
        "timestamp": "2025-12-27T10:30:00Z"
      }
    ],
    "count": 20,
    "source": "github",
    "date_range": "2025-12-21 to 2025-12-28"
  }
}
```

**Example:**

```python
# Tool invocation
fetch_changelog_data(
    source_type="github",
    start_date="2025-12-21",
    end_date="2025-12-28",
    config={
        "repo": "myorg/myrepo",
        "token_env": "GITHUB_TOKEN"
    }
)
```

---

### MCP Tool 2: `validate_frontmatter`

**Description:** Validate YAML frontmatter against JSON Schema

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `frontmatter` | object | Yes | - | YAML frontmatter as dict |
| `schema_path` | string | No | "config/.changelog-config.schema.json" | Path to JSON Schema |

**Returns:**

```json
{
  "status": "success",
  "valid": true,
  "errors": [],
  "warnings": ["Optional field 'categories' not provided"]
}
```

**Example:**

```python
validate_frontmatter(
    frontmatter={
        "date": "2025-12-28",
        "version": "1.2.0",
        "authors": ["Jane Doe", "John Smith"]
    }
)
```

---

### MCP Tool 3: `write_changelog`

**Description:** Write changelog to file with safety checks (path validation, SHA256 hash)

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content` | string | Yes | - | Full markdown content |
| `output_path` | string | Yes | - | Relative path (e.g., "CHANGELOG.md") |
| `overwrite` | bool | No | false | Allow overwriting existing file |

**Returns:**

```json
{
  "status": "success",
  "file": {
    "path": "CHANGELOG.md",
    "sha256": "a1b2c3d4e5f6...",
    "lines": 42,
    "size_bytes": 3421
  }
}
```

**Example:**

```python
write_changelog(
    content="# Changelog\n\n## 2025-12-28...",
    output_path="CHANGELOG.md",
    overwrite=True
)
```

---

### MCP Tool 4: `create_changelog_pr`

**Description:** Create GitHub PR with changelog changes

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `branch_name` | string | Yes | - | Branch name (e.g., "changelog-2025-12-28") |
| `commit_message` | string | Yes | - | Commit message |
| `pr_title` | string | Yes | - | PR title |
| `pr_body` | string | Yes | - | PR description (markdown) |
| `base_branch` | string | No | "main" | Target branch |

**Returns:**

```json
{
  "status": "success",
  "pr": {
    "url": "https://github.com/org/repo/pull/1234",
    "number": 1234,
    "branch": "changelog-2025-12-28",
    "diff_summary": "+42 lines in CHANGELOG.md"
  }
}
```

**Example:**

```python
create_changelog_pr(
    branch_name="changelog-2025-12-28",
    commit_message="docs: add changelog for 2025-12-28",
    pr_title="Changelog for Week of Dec 21-28",
    pr_body="**Summary**: 20 changes (12 PRs, 8 issues)\n**Quality**: 92/100"
)
```

---

### MCP Tool 5: `validate_changelog_quality`

**Description:** Run deterministic quality checks (frontmatter valid, links work, required sections present)

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content` | string | Yes | - | Full markdown content |
| `template_path` | string | No | null | Template to validate against |

**Returns:**

```json
{
  "status": "success",
  "score": 95,
  "checks": {
    "frontmatter_valid": {"pass": true, "message": "YAML valid"},
    "links_work": {"pass": true, "message": "All 20 links accessible"},
    "sections_present": {"pass": true, "message": "All required sections found"},
    "markdown_valid": {"pass": true, "message": "No syntax errors"}
  },
  "errors": [],
  "warnings": ["Consider adding more detail to 'Breaking Changes' section"]
}
```

**Example:**

```python
validate_changelog_quality(
    content="---\ndate: 2025-12-28\n---\n\n# Changelog\n..."
)
```

---

### MCP Tool 6: `get_changelog_config`

**Description:** Load and validate `.changelog-config.json`

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `config_path` | string | No | ".changelog-config.json" | Path to config file |

**Returns:**

```json
{
  "status": "success",
  "config": {
    "sources": [...],
    "template": "changelogs/weekly-template.md",
    "output_path": "CHANGELOG.md",
    "quality_threshold": 80
  },
  "validation": {
    "valid": true,
    "errors": []
  }
}
```

**Example:**

```python
get_changelog_config()  # Loads .changelog-config.json from current directory
```

---

## Slash Command: `/changelog-weekly`

**Description:** Generate changelog for the last 7 days

**Usage:**
```
/changelog-weekly
```

**Parameters:**
None (uses config from `.changelog-config.json`)

**Returns:**

```
🎉 Changelog PR created successfully!
PR: https://github.com/myorg/myrepo/pull/1234
Quality score: 92/100
```

---

## Slash Command: `/changelog-custom`

**Description:** Generate changelog for custom date range

**Usage:**
```
/changelog-custom start_date=YYYY-MM-DD end_date=YYYY-MM-DD
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_date` | string | Yes | - | ISO 8601 date (e.g., "2025-12-01") |
| `end_date` | string | Yes | - | ISO 8601 date (e.g., "2025-12-15") |

**Example:**

```bash
/changelog-custom start_date=2025-12-01 end_date=2025-12-15

# Output:
# 🎉 Changelog PR created successfully!
# Date range: 2025-12-01 to 2025-12-15
# Changes: 35 items
```

---

## Slash Command: `/changelog-validate`

**Description:** Validate configuration before running

**Usage:**
```
/changelog-validate
```

**Parameters:**
None

**Returns:**

```
✅ All checks passed! Ready to generate changelog.

Checks:
  ✓ Config file found
  ✓ GitHub token valid
  ✓ Template exists
  ✓ Output path writable
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | Yes (for GitHub source) | - | GitHub Personal Access Token with `repo:read` + `repo:write` |
| `SLACK_TOKEN` | No | - | Slack Bot Token with `channels:history` scope |

### Config File

Location: `.changelog-config.json` (project root)

```json
{
  "sources": [
    {
      "type": "github",
      "config": {
        "repo": "myorg/myrepo",
        "token_env": "GITHUB_TOKEN",
        "labels_filter": ["bug", "enhancement"],
        "exclude_labels": ["wontfix", "duplicate"]
      }
    },
    {
      "type": "slack",
      "config": {
        "channel": "changelog",
        "token_env": "SLACK_TOKEN",
        "include_threads": false
      }
    },
    {
      "type": "git",
      "config": {
        "branch": "main",
        "conventional_commits": true
      }
    }
  ],
  "template": "changelogs/weekly-template.md",
  "output_path": "CHANGELOG.md",
  "quality_threshold": 80,
  "pr_config": {
    "base_branch": "main",
    "labels": ["documentation", "changelog"],
    "auto_merge": false
  }
}
```

**Schema Validation**: All configs validated against `config/.changelog-config.schema.json`

---

## Testing

### Run All Tests
```bash
cd 005-plugins/changelog-automation
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_sources.py::test_github_source_fetch -v
```

### Test Coverage
```bash
pytest tests/ --cov=scripts --cov-report=html
```

**Coverage Target:** 65%+

### Golden Task (Smoke Test)

**File:** `tests/run_changelog_smoke.py`

**Criteria:**
- Execution time: <90 seconds
- Uses fixture data (no live APIs)
- Generates changelog with 3 features, 5 fixes
- Validates frontmatter (passes schema)
- Quality score: ≥80
- Output matches expected structure (diff <10 lines)

**Run:**
```bash
python tests/run_changelog_smoke.py

# Expected output:
# ✅ Smoke test passed (87 seconds)
# ✅ Quality score: 92/100
# ✅ Output matches expected structure
```

---

## Deployment

### Local Installation
```bash
# Clone and setup
git clone https://github.com/nixtla/nixtla
cd nixtla/005-plugins/changelog-automation
./scripts/setup.sh

# Or manual
python -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

### Claude Code Installation
```bash
# Add marketplace
/plugin marketplace add nixtla/nixtla

# Install plugin
/plugin install changelog-automation@nixtla
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `ImportError: No module named 'mcp'` | MCP SDK not installed | Run `pip install -r scripts/requirements.txt` |
| `GITHUB_TOKEN not found` | Environment variable not set | Run `export GITHUB_TOKEN="ghp_..."` |
| `Template not found` | Invalid path in config | Check `template` field, ensure file exists |
| `Quality score too low` | Generated content doesn't meet threshold | Lower `quality_threshold` in config or refine template |
| `PR creation failed (403)` | Insufficient GitHub permissions | Verify token has `repo:write` scope |
| `Async runtime error` | Python version <3.10 | Upgrade to Python 3.10+ |

### Debug Mode

```bash
# Enable verbose logging
export CHANGELOG_DEBUG=1
/changelog-weekly

# Output includes:
# - API request/response details
# - Template variable substitution
# - Quality check breakdown
```

### Common Errors

**Error:** `ValueError: Invalid date format`
**Cause:** Date not in ISO 8601 format (YYYY-MM-DD)
**Fix:** Use `/changelog-custom start_date=2025-12-01 end_date=2025-12-15`

**Error:** `JSONDecodeError: Expecting value`
**Cause:** Malformed `.changelog-config.json`
**Fix:** Validate JSON syntax, check for trailing commas

**Error:** `GitCommandError: fatal: not a git repository`
**Cause:** Running outside git repository
**Fix:** Run from git repository root, or remove `git` from sources

---

## Performance Considerations

| Operation | Expected Time | Memory | Notes |
|-----------|--------------|--------|-------|
| GitHub data fetch (100 PRs) | 2-5 seconds | 50 MB | Uses GraphQL pagination, ~10 requests |
| Slack data fetch (200 messages) | 1-3 seconds | 30 MB | Single channel, no threads |
| Git log parsing (500 commits) | <1 second | 20 MB | Local filesystem, no API |
| AI synthesis (Writer Agent) | 10-20 seconds | N/A | Claude API, depends on item count |
| Quality validation | <1 second | 10 MB | Deterministic checks only |
| PR creation | 1-2 seconds | 5 MB | Single GitHub API call |
| **Total (end-to-end)** | **<90 seconds** | **<200 MB** | Golden task target |

**Optimization Notes:**
- Parallel data source fetching (asyncio.gather)
- Cached GitHub API responses (in-memory, session-scoped)
- Lazy template loading (on-demand)

---

## Security Notes

- **Token Storage**: All API tokens stored in environment variables (NEVER in config files or code)
- **Minimum Permissions**: GitHub token requires `repo:read` + `repo:write` only (no admin, no org access)
- **Path Sandboxing**: MCP server validates all file paths (no absolute paths, no parent directory traversal)
- **Audit Trail**: All MCP tool invocations logged with inputs (tokens redacted), Git commits include reproducibility metadata
- **Secret Redaction**: Logs never include full tokens (only last 4 chars for debugging)
- **HTTPS Only**: All API calls over HTTPS (GitHub/Slack APIs enforce TLS 1.2+)
