# Schema: nixtla-search-to-slack

**Generated:** 2025-12-12
**Plugin Version:** 0.2.0
**Status:** Development (Live)

---

## Directory Tree

```
nixtla-search-to-slack/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── config/
│   ├── sources.yaml               # Data source configuration
│   └── topics.yaml                # Topic/keyword configuration
├── skills/
│   ├── nixtla-model-benchmarker/
│   │   ├── SKILL.md               # Skill definition
│   │   └── assets/templates/      # Benchmark templates
│   ├── nixtla-research-assistant/
│   │   └── SKILL.md               # Skill definition
│   └── timegpt-pipeline-builder/
│       ├── SKILL.md               # Skill definition
│       └── assets/templates/      # Pipeline templates
├── src/
│   └── nixtla_search_to_slack/
│       ├── __init__.py            # Package init
│       ├── ai_curator.py          # AI-powered content curation
│       ├── config_loader.py       # YAML config loader
│       ├── content_aggregator.py  # Content aggregation logic
│       ├── main.py                # Main entry point
│       ├── search_orchestrator.py # Search orchestration
│       ├── slack_publisher.py     # Slack message formatting/posting
│       └── web_search_providers.py # Web search provider integrations
├── tests/
│   ├── conftest.py                # Pytest fixtures
│   ├── test_ai_curator.py         # AI curator tests
│   ├── test_config_loader.py      # Config loader tests
│   ├── test_content_aggregator.py # Aggregator tests
│   ├── test_search_orchestrator.py # Orchestrator tests
│   └── test_slack_publisher.py    # Publisher tests
├── .env.example                   # Environment variable template
├── requirements.txt               # Python dependencies
├── QUICKSTART.md                  # Quick start guide
├── README.md                      # Full documentation
└── SETUP_GUIDE.md                 # Setup instructions
```

---

## Plugin Manifest (plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-search-to-slack | Required |
| description | Automated content discovery and curation... | Required |
| version | 0.2.0 | Required |
| author.name | Jeremy Longshore | Required |
| homepage | https://github.com/intent-solutions-io/plugins-nixtla | Optional |
| repository | https://github.com/intent-solutions-io/plugins-nixtla | Optional |
| license | MIT | Optional |

---

## Skills (3)

| Skill | Purpose |
|-------|---------|
| nixtla-model-benchmarker | Model benchmarking automation |
| nixtla-research-assistant | Research assistance for Nixtla content |
| timegpt-pipeline-builder | TimeGPT pipeline generation |

---

## Source Modules (7)

| Module | Purpose |
|--------|---------|
| main.py | Entry point and orchestration |
| ai_curator.py | AI-powered content curation/summarization |
| config_loader.py | YAML configuration loading |
| content_aggregator.py | Content deduplication and aggregation |
| search_orchestrator.py | Multi-source search coordination |
| slack_publisher.py | Slack message formatting and posting |
| web_search_providers.py | SerpAPI, GitHub API integrations |

---

## Configuration Files

| File | Purpose |
|------|---------|
| config/sources.yaml | Data source URLs and APIs |
| config/topics.yaml | Search keywords and topics |
| .env.example | Required environment variables |

---

## Test Coverage (5 test files)

| Test File | Coverage |
|-----------|----------|
| test_ai_curator.py | AI curation logic |
| test_config_loader.py | YAML loading |
| test_content_aggregator.py | Deduplication |
| test_search_orchestrator.py | Search coordination |
| test_slack_publisher.py | Slack formatting |

---

## Key Files

| File | Lines | Purpose |
|------|-------|---------|
| src/.../main.py | ~200 | Main orchestration |
| src/.../ai_curator.py | ~300 | LLM-powered summarization |
| src/.../slack_publisher.py | ~150 | Slack SDK integration |
| src/.../search_orchestrator.py | ~250 | Multi-provider search |

---

## Environment Variables Required

```bash
SERPAPI_KEY=...           # Web search API
GITHUB_TOKEN=...          # GitHub API access
SLACK_WEBHOOK_URL=...     # Slack posting
OPENAI_API_KEY=...        # AI summarization (optional)
```

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Content curators, teams wanting Nixtla content discovery
- **What:** Search web and GitHub for Nixtla content, deduplicate, post to Slack
- **When:** Content discovery, Slack team updates
- **Target Goal:** Post curated digest to Slack channel without errors
- **Production:** false (development)
