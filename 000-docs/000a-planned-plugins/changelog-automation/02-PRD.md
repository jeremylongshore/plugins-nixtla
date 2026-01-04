# Changelog Automation - Product Requirements Document

**Plugin:** changelog-automation
**Version:** 0.1.0
**Status:** Approved
**Last Updated:** 2025-12-28

---

## Overview

Changelog Automation is a Claude Code plugin that automates weekly/monthly changelog generation through a hybrid MCP + Skill architecture. It fetches updates from multiple sources (GitHub, Slack, Git), synthesizes narrative content using AI agents, validates quality and format, and creates pull requests with the final changelog—reducing manual effort from 2.5 hours to 15 minutes per release.

---

## Goals & Non-Goals

### Goals
- [ ] Reduce changelog creation time by 90% (from 2.5 hours to 15 minutes)
- [ ] Achieve 85%+ quality score on AI-generated changelogs (tone, completeness, accuracy)
- [ ] Support 3+ data sources (GitHub PRs/issues, Slack messages, Git commits)
- [ ] Enable template customization (markdown + YAML frontmatter)
- [ ] Provide quality gate with deterministic + editorial review
- [ ] Automate PR creation with changelog file + metadata

### Non-Goals (Explicitly Out of Scope)
- [ ] Multi-language support (English only for v1.0)
- [ ] Custom UI dashboard (CLI-only)
- [ ] Real-time changelog updates (batch mode only)
- [ ] Changelog publishing to external platforms (GitHub Releases, Twitter, etc. - manual for now)
- [ ] Multi-repository aggregation (single repo per run)

---

## User Stories

| ID | As a... | I want to... | So that... | Priority |
|----|---------|--------------|------------|----------|
| US-01 | Engineering Lead | Generate weekly changelogs from GitHub PRs | I save 2 hours/week and ship faster | 🔴 Must |
| US-02 | DevRel Engineer | Synthesize Slack updates into user-friendly changelogs | I communicate clearly to non-technical users | 🔴 Must |
| US-03 | Product Manager | Customize changelog template with custom frontmatter | I match our product docs style (Docusaurus, Hugo) | 🟡 Should |
| US-04 | Technical Writer | Review AI draft before publishing | I ensure accuracy and tone alignment | 🔴 Must |
| US-05 | Open-Source Maintainer | Auto-generate release notes from merged PRs | I spend more time on code, less on docs | 🔴 Must |
| US-06 | DevOps Engineer | Validate changelog config before running | I catch errors early (missing tokens, invalid templates) | 🟡 Should |
| US-07 | Engineering Manager | Track changelog quality scores over time | I improve documentation culture with data | 🟢 Could |

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-01 | Fetch data from GitHub (PRs, issues, releases) via GraphQL API | 🔴 Must | Pagination for >100 items, filter by labels/milestones |
| FR-02 | Fetch data from Slack (channel messages, threads) via Slack API | 🟡 Should | Support multiple channels, thread replies optional |
| FR-03 | Fetch data from Git (commit log with conventional commits parsing) | 🟡 Should | Offline mode, no API required |
| FR-04 | Synthesize AI narrative (summary, highlights, grouped changes) | 🔴 Must | Writer Agent with tone guidelines |
| FR-05 | Validate frontmatter against JSON Schema | 🔴 Must | Required fields: date, version, optional: authors, categories |
| FR-06 | Apply template with variable substitution | 🔴 Must | Support {{date}}, {{version}}, {{features}}, {{fixes}}, etc. |
| FR-07 | Run quality gate (deterministic + editorial review) | 🔴 Must | Min score: 80/100, feedback loop max 2 iterations |
| FR-08 | Create PR with changelog file + description | 🔴 Must | Branch: changelog-YYYY-MM-DD, labels: documentation, changelog |
| FR-09 | Support custom data sources via plugin architecture | 🟢 Could | Base class for extensibility (Jira, Linear, etc.) |
| FR-10 | Provide `/changelog-validate` command for config testing | 🟡 Should | Test sources, template, write permissions before running |

### Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-01 | Performance: Golden task execution time | <90 seconds | Run smoke test with fixture data (offline mode) |
| NFR-02 | Reliability: Success rate for end-to-end workflow | >95% | Track successful PR creation vs. failures (CI metrics) |
| NFR-03 | Usability: Setup time for first-time users | <10 minutes | Time from install to first changelog (with example config) |
| NFR-04 | Quality: AI-generated changelog quality score | ≥85/100 | Deterministic + editorial review score (0-100 scale) |
| NFR-05 | Extensibility: Time to add custom data source | <2 hours | Subclass ChangelogDataSource + register in MCP server |
| NFR-06 | Security: No hardcoded credentials | 100% compliance | All tokens via environment variables (validated by auditor) |

---

## Success Metrics

| Metric | Target | Measurement Method | Timeline |
|--------|--------|-------------------|----------|
| Adoption Rate | 10+ teams in 3 months | GitHub repo stars + plugin installs | Q1 2026 |
| Time Savings | 2+ hours/week saved per team | User survey (before/after comparison) | Monthly |
| Quality Score | 85%+ average across all changelogs | Automated quality gate scores (logged) | Real-time |
| Community Contributions | 3+ custom data sources | GitHub PRs merged (new sources/) | 6 months |
| Test Coverage | 65%+ code coverage | pytest --cov report | Continuous |
| User Satisfaction | 4.5/5 rating | Post-use survey (optional) | Quarterly |

---

## Scope

### MVP (Phase 1 - v1.0.0)
- MCP server with 6 tools (fetch, validate frontmatter, write, create PR, quality check, get config)
- 3 data sources (GitHub, Slack, Git)
- Skill with 6-phase workflow (initialize → write → format → review → PR → handoff)
- Template system with variable substitution + YAML frontmatter
- 3 slash commands (/changelog-weekly, /changelog-custom, /changelog-validate)
- Golden task smoke test (<90s, fixture mode)
- Configuration via .changelog-config.json (JSON Schema validation)

### Phase 2 (Future - v2.0.0)
- Custom data sources from community (Jira, Linear, Notion, etc.)
- Multi-repository aggregation (combined changelog across repos)
- Changelog publishing integrations (GitHub Releases, Twitter, Slack auto-post)
- Quality score tracking dashboard (historical metrics)
- A/B testing for template variants (which generates better quality?)

### Out of Scope (Forever)
- Multi-language AI synthesis (English only)
- Custom web UI (CLI-only by design)
- Automated publishing without human review (always require approval)

---

## Dependencies

| Dependency | Type | Owner | Status |
|------------|------|-------|--------|
| Claude Code CLI | Technical | Anthropic | ✅ Stable |
| GitHub GraphQL API | Technical | GitHub | ✅ Stable |
| Slack Web API | Technical | Slack | ✅ Stable |
| Python 3.10+ | Technical | Python.org | ✅ Stable |
| MCP SDK (mcp.server) | Technical | Anthropic | ✅ Stable |
| JSON Schema validator | Technical | PyPI (jsonschema) | ✅ Stable |
| Nixtla Skills Standard v2.3.0 | Technical | Nixtla repo | ✅ Complete |
| validate_skills_v2.py | Technical | Nixtla repo | ✅ Working |

---

## Open Questions

| Question | Owner | Due Date | Resolution |
|----------|-------|----------|------------|
| Should we support GitLab in MVP or Phase 2? | Product | 2026-01-15 | **Resolved**: Phase 2 (GitHub-first for MVP) |
| What's the default quality threshold (70, 80, or 90)? | UX | 2026-01-10 | **Resolved**: 80 (balanced, configurable) |
| Do we need multi-repo aggregation in MVP? | Engineering | 2026-01-05 | **Resolved**: No (Phase 2, too complex for v1.0) |
| Should Slack be required or optional? | Product | 2026-01-08 | **Resolved**: Optional (GitHub-only is valid config) |
