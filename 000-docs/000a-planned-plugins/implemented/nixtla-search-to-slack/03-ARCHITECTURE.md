# Search-to-Slack - Architecture

**Plugin:** nixtla-search-to-slack
**Version:** 0.1.0 (MVP)
**Last Updated:** 2025-12-12

---

## System Context

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│   SerpAPI    │────▶│                 │────▶│    Slack     │
│   (Web)      │     │  Search-to-     │     │  (Webhook)   │
└──────────────┘     │  Slack Plugin   │     └──────────────┘
                     │                 │
┌──────────────┐     │  - Orchestrator │
│   GitHub     │────▶│  - Aggregator   │
│   API        │     │  - AI Curator   │
└──────────────┘     │  - Publisher    │
                     └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   OpenAI/    │
                     │   Anthropic  │
                     └──────────────┘
```

---

## Component Design

### SearchOrchestrator (`search_orchestrator.py`)

Coordinates search across multiple sources:

| Method | Purpose |
|--------|---------|
| `search_all()` | Execute all configured searches |
| `search_web()` | Query SerpAPI for web results |
| `search_github()` | Query GitHub API for org activity |

### ContentAggregator (`content_aggregator.py`)

Deduplicates and filters content:

| Method | Purpose |
|--------|---------|
| `deduplicate()` | Remove duplicate URLs/titles |
| `filter_relevance()` | Apply relevance threshold |
| `merge_results()` | Combine results from sources |

### AICurator (`ai_curator.py`)

Generates AI summaries:

| Method | Purpose |
|--------|---------|
| `summarize()` | Generate summary for single item |
| `batch_summarize()` | Process multiple items |
| `extract_key_points()` | Pull bullet points |

### SlackPublisher (`slack_publisher.py`)

Formats and posts to Slack:

| Method | Purpose |
|--------|---------|
| `format_digest()` | Create Block Kit message |
| `post()` | Send to Slack channel |
| `format_item()` | Format single content item |

### ConfigLoader (`config_loader.py`)

Loads YAML configuration:

| Method | Purpose |
|--------|---------|
| `load_topics()` | Load topic definitions |
| `load_sources()` | Load source configuration |
| `get_env()` | Get environment variables |

---

## Data Flow

1. **CLI** invokes main entry point with topic name
2. **ConfigLoader** reads topics.yaml and sources.yaml
3. **SearchOrchestrator** queries SerpAPI and GitHub
4. **ContentAggregator** deduplicates and filters results
5. **AICurator** generates summaries via OpenAI/Anthropic
6. **SlackPublisher** formats Block Kit message and posts

---

## File Structure

```
005-plugins/nixtla-search-to-slack/
├── README.md                 # Overview and disclaimers
├── QUICKSTART.md             # Quick setup guide
├── SETUP_GUIDE.md            # Comprehensive setup
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── src/nixtla_search_to_slack/
│   ├── __init__.py
│   ├── main.py               # CLI entry point
│   ├── search_orchestrator.py
│   ├── content_aggregator.py
│   ├── ai_curator.py
│   ├── slack_publisher.py
│   └── config_loader.py
├── config/
│   ├── topics.yaml           # Topic definitions
│   └── sources.yaml          # Source configuration
├── tests/
│   ├── test_config_loader.py
│   ├── test_content_aggregator.py
│   ├── test_search_orchestrator.py
│   ├── test_ai_curator.py
│   └── test_slack_publisher.py
└── skills/
    ├── nixtla-model-benchmarker/
    ├── nixtla-research-assistant/
    └── timegpt-pipeline-builder/
```

---

## Configuration Files

### topics.yaml

```yaml
topics:
  nixtla-core:
    name: "Nixtla Core Updates"
    keywords:
      - TimeGPT
      - StatsForecast
      - MLForecast
    sources: [web, github]
    filters:
      min_relevance: 60
    slack_channel: "#nixtla-updates"
```

### sources.yaml

```yaml
sources:
  web:
    provider: serpapi
    max_results: 10
    time_range: 7d
    exclude_domains: [pinterest.com]
  github:
    organizations: [Nixtla]
    additional_repos: [facebook/prophet]
    max_results: 20
```

---

## Security Model

**Current (MVP):**
- API keys stored in environment variables
- No encryption at rest
- No audit logging
- No rate limiting

**Required for Production:**
- Secret manager integration
- Request signing
- Rate limiting
- Audit trails

---

## Technical Constraints

- **Single-threaded**: No concurrent requests
- **No persistence**: May re-send duplicates
- **No scheduling**: Manual or external cron
- **Memory-based**: All state in memory
- **API costs**: Each run incurs costs
