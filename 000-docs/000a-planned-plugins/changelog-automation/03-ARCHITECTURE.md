# Changelog Automation - Architecture

**Plugin:** changelog-automation
**Version:** 0.1.0
**Last Updated:** 2025-12-28

---

## System Context

This plugin sits between Claude Code and external data sources (GitHub, Slack, Git), orchestrating a multi-agent workflow to automate changelog generation.

```
┌─────────────────────────────────────────────────────────────┐
│                      User's Terminal                         │
├─────────────────────────────────────────────────────────────┤
│                      Claude Code CLI                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Slash Commands (/changelog-weekly, /custom, /validate) │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │                                   │
│  ┌───────────────────────▼───────────────────────────────┐  │
│  │         Changelog Orchestrator Skill (SKILL.md)       │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ Phase 1: Initialize & Fetch                     │  │  │
│  │  │ Phase 2: Writer Agent (synthesis)               │  │  │
│  │  │ Phase 3: Formatter Agent (compliance)           │  │  │
│  │  │ Phase 4: Reviewer Agent (quality gate)          │  │  │
│  │  │ Phase 5: PR Writer Agent (repo ops)             │  │  │
│  │  │ Phase 6: User Handoff                           │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                          │                              │  │
│  │                          │ (invokes MCP tools)          │  │
│  │                          ▼                              │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │      MCP Server (changelog_mcp.py)              │  │  │
│  │  │  ┌───────────────────────────────────────────┐  │  │  │
│  │  │  │ Tool 1: fetch_changelog_data              │  │  │  │
│  │  │  │ Tool 2: validate_frontmatter              │  │  │  │
│  │  │  │ Tool 3: write_changelog                   │  │  │  │
│  │  │  │ Tool 4: create_changelog_pr               │  │  │  │
│  │  │  │ Tool 5: validate_changelog_quality        │  │  │  │
│  │  │  │ Tool 6: get_changelog_config              │  │  │  │
│  │  │  └───────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────┬───────────────────────────┘  │  │
│  └────────────────────────┼──────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │              Data Source Plugins                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │  │
│  │  │ GitHub   │  │  Slack   │  │   Git    │            │  │
│  │  │ Source   │  │  Source  │  │  Source  │            │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │  │
│  └───────┼─────────────┼─────────────┼───────────────────┘  │
│          │             │             │                       │
│  ┌───────▼─────────────▼─────────────▼───────────────────┐  │
│  │              External APIs / Services                  │  │
│  │    (GitHub GraphQL, Slack Web API, Local Git)         │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Design

### Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| **Slash Commands** | User entry points (weekly, custom, validate) | `commands/*.md` |
| **Orchestrator Skill** | 6-phase workflow coordination, agent delegation | `skills/.claude/skills/changelog-orchestrator/SKILL.md` |
| **MCP Server** | Deterministic operations (fetch, validate, write, PR) | `scripts/changelog_mcp.py` |
| **Data Sources** | Fetch & normalize data from GitHub/Slack/Git | `scripts/sources/*.py` |
| **Formatters** | Template rendering, frontmatter generation | `scripts/formatters/*.py` |
| **Validators** | JSON Schema validation, quality scoring | `scripts/validators/*.py` |
| **Templates** | Markdown templates with variable placeholders | `skills/.claude/skills/changelog-orchestrator/assets/templates/*.md` |
| **Configuration** | User config, schema validation | `config/.changelog-config.json` |

### Component Interactions

```
User ──▶ Slash Command ──▶ Orchestrator Skill
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         MCP Tool 1      MCP Tool 2      MCP Tool 3
         (fetch_data)    (validate)      (write_file)
              │               │               │
              ▼               ▼               ▼
       Data Sources      Validators      File System
       (GitHub/Slack)    (JSON Schema)   (CHANGELOG.md)
              │               │               │
              └───────────────┴───────────────┘
                              │
                              ▼
                      Formatted Changelog
                              │
                              ▼
                      MCP Tool 4 (create_pr)
                              │
                              ▼
                      GitHub Pull Request
```

---

## Data Flow

### Input

**Sources**:
- GitHub GraphQL API: Merged PRs, closed issues, release tags (date range filter)
- Slack Web API: Channel messages, thread replies (timestamp filter)
- Git Log: Commit history with conventional commit parsing (date range)

**Configuration**: `.changelog-config.json` loaded from project root
```json
{
  "sources": [{"type": "github", "config": {...}}],
  "template": "changelogs/template.md",
  "output_path": "CHANGELOG.md",
  "quality_threshold": 80
}
```

**Format**: JSON Schema-validated configuration object

### Processing

**Phase 1: Data Aggregation**
1. MCP Server fetches data from all configured sources
2. Each source returns normalized items: `{id, title, type, author, labels, url, timestamp}`
3. Items aggregated into unified dataset sorted by timestamp

**Phase 2: AI Synthesis**
1. Writer Agent groups items by type (features, fixes, breaking, other)
2. Generates narrative: summary (2-3 sentences), highlights (top 3-5), detailed sections
3. Applies tone guidelines (user-focused, concise, professional)

**Phase 3: Template Formatting**
1. Formatter Agent loads template with frontmatter schema
2. Generates frontmatter (date, version, authors, categories)
3. Substitutes variables: `{{date}}` → `2025-12-28`, `{{features}}` → feature list
4. Validates structure (required sections, markdown syntax)

**Phase 4: Quality Review**
1. Deterministic checks (MCP): Frontmatter valid, links work, sections present
2. Editorial review (Reviewer Agent): Tone, completeness, accuracy, clarity
3. Combined score (0-100), must be ≥80 to pass
4. Feedback loop: If rejected, return to Writer Agent (max 2 iterations)

**Phase 5: PR Creation**
1. MCP Server writes changelog to file (with SHA256 hash for reproducibility)
2. Creates git branch: `changelog-YYYY-MM-DD`
3. Commits with message: `docs: add changelog for YYYY-MM-DD`
4. Opens PR with description (summary, date range, quality score, reviewer checklist)

### Output

**Primary Artifact**: Pull request with changelog file
- File: `CHANGELOG.md` (or configured path)
- Branch: `changelog-2025-12-28`
- PR URL: `https://github.com/org/repo/pull/1234`

**Metadata**:
- Quality score: 92/100
- Reproducibility bundle: `compat_info.json`, `run_manifest.json`
- Item count: 23 changes (GitHub: 15 PRs, 8 issues; Slack: 0)

---

## Integrations

| System | Type | Direction | Purpose | Auth Method |
|--------|------|-----------|---------|-------------|
| GitHub GraphQL API | API | Outbound | Fetch PRs, issues, releases | Personal Access Token (env var) |
| Slack Web API | API | Outbound | Fetch channel messages, threads | Bot Token (env var) |
| Git (local) | CLI | Outbound | Parse commit log (offline) | None (local filesystem) |
| Claude Code MCP | Protocol | Inbound | Expose 6 tools to Claude | stdio (no auth) |
| GitHub REST API | API | Outbound | Create PR, commit file | Personal Access Token (env var) |

---

## Technical Constraints

- **Python 3.10+**: Required for async/await, type hints, pattern matching
- **Single repository**: No multi-repo aggregation in v1.0 (scoped to one repo per run)
- **Offline mode**: MCP tools must work with fixture data (no live API calls) for testing
- **English only**: AI synthesis in English (no i18n support)
- **No real-time**: Batch mode only (not streaming/live updates)
- **Token limits**: Claude API context limits (plan must fit within token budget)

---

## Security Considerations

### Authentication

**Data Sources**:
- GitHub: Personal Access Token with `repo:read` scope
- Slack: Bot Token with `channels:history`, `channels:read` scopes
- Git: Local filesystem (no auth required)

**Storage**: All tokens stored in environment variables (NEVER in config files or code)

### Authorization

**Minimum Permissions**:
- GitHub: Read-only for PRs/issues, write for PR creation (separate token optional)
- Slack: Read-only for channels (no write permissions needed)
- File system: Write access to configured output path only

### Data Handling

**Sensitive Data**:
- User emails: Extracted from GitHub/Git, included in changelog (public)
- Private repos: Plugin works with private repos (data stays local, never leaves machine)
- API responses: Cached in memory only (not persisted to disk)

**Encryption**: N/A (all processing local, no network transmission of user data)

**Retention**: Temporary data (fetched items) discarded after PR creation

### Secrets Management

**How API keys/credentials are handled**:
1. User sets environment variables: `export GITHUB_TOKEN=ghp_xxx`
2. Config file references env var name: `"token_env": "GITHUB_TOKEN"`
3. MCP Server reads env var at runtime: `os.getenv("GITHUB_TOKEN")`
4. Token never logged, never written to disk, never passed to Claude

**Audit Trail**:
- All MCP tool invocations logged with inputs (minus tokens)
- Reproducibility bundle includes: source versions, fetch timestamps, item counts
- Git commit includes metadata: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`

---

## Scalability

### Current Limits

| Resource | Limit | Mitigation if exceeded |
|----------|-------|----------------------|
| GitHub API rate limit | 5,000 req/hour | Batch requests (GraphQL), cache responses, retry with exponential backoff |
| Slack API rate limit | Tier 3 (50+ req/min) | Pagination with delays, use threads sparingly |
| Changelog file size | <10MB | Warn user if >1MB, suggest date range narrowing |
| Processing time | <90s (golden task) | Parallelize data source fetches, limit item count (series_limit param) |
| Claude context window | 200K tokens | Progressive disclosure (skill loads on-demand), summarize large datasets |

### Future Scaling

**If adopted by large teams (100+ developers)**:
- Add caching layer (Redis) for GitHub/Slack API responses (reduce API calls)
- Implement incremental changelog (only new items since last run)
- Support multi-repo aggregation (parallel fetch across repos)
- Add background job mode (async processing with webhooks)

---

## Error Handling

| Error Type | Detection | Response | Recovery |
|------------|-----------|----------|----------|
| Data fetch failure (GitHub API down) | HTTP 5xx or timeout | Retry 3x with exponential backoff | Fallback to partial sources (Git only), warn user |
| Invalid configuration (missing token) | JSON Schema validation + env var check | Return detailed error message | `/changelog-validate` command helps diagnose |
| Template not found | File existence check at startup | Fail fast with clear error + suggest fix | User fixes path in config |
| Quality gate failure (<80 score) | MCP quality tool + Reviewer Agent | Provide feedback, iterate (max 2 rounds) | User can override threshold in config |
| PR creation failure (branch exists) | GitHub API 422 error | Suggest unique branch name or force flag | User manually deletes branch or renames |
| Frontmatter schema mismatch | JSON Schema validator | List missing/invalid fields | User updates template or config schema |

---

## Observability

### Logging

**What gets logged**:
- MCP tool invocations: Tool name, input params (sanitized), execution time
- Data source fetches: Source type, date range, item count, API response time
- Quality scores: Deterministic checks (pass/fail), editorial review (0-100), final score
- PR creation: Branch name, commit SHA, PR URL, diff summary

**Where**: stderr (console output), structured JSON format

**Log Levels**:
- DEBUG: API request/response details, template variable substitution
- INFO: Workflow progress (phase transitions), item counts, quality scores
- WARNING: Partial failures (source unavailable), quality gate iterations
- ERROR: Fatal errors (config invalid, API auth failure, file write error)

### Metrics

**What metrics are tracked**:
- Execution time per phase (fetch, synthesize, format, review, PR)
- API call counts and latencies (GitHub, Slack)
- Quality score distribution (0-100, histogram)
- Success rate (% of runs that create PR successfully)

**Output**: `run_manifest.json` in reproducibility bundle

### Alerting

**What triggers alerts**:
- Quality score <60 (critical quality failure)
- API rate limit exceeded (pause workflow)
- PR creation failed 3x (user intervention needed)

**Method**: Console output (ERROR level), exit code ≠ 0

---

## Hybrid MCP + Skill Design Rationale

**Why MCP for Deterministic Operations?**
- Data fetching: Same query → same results (reproducible)
- File I/O: Explicit inputs → predictable outputs (testable)
- Validation: Schema-based rules → binary pass/fail (auditable)
- PR creation: Structured inputs → consistent behavior (reliable)

**Why Skill for Editorial Work?**
- Content synthesis: Requires LLM reasoning (grouping, summarization, tone)
- Quality judgment: Subjective criteria (completeness, clarity, user-friendliness)
- Workflow orchestration: Context-aware phase transitions (when to iterate, when to approve)
- Agent delegation: Progressive disclosure pattern (load instructions on-demand)

**Benefits of Separation**:
- MCP tools testable in isolation (unit tests with fixtures)
- Skill focused on high-level workflow (easier to maintain)
- Clear boundary: Deterministic (code) vs. LLM-based (prompts)
