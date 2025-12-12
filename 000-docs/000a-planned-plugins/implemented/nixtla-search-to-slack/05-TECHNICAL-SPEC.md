# Search-to-Slack - Technical Specification

**Plugin:** nixtla-search-to-slack
**Version:** 0.1.0 (MVP)
**Last Updated:** 2025-12-12

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Runtime | Python | 3.8+ |
| HTTP | requests | latest |
| Config | pyyaml | latest |
| Environment | python-dotenv | latest |
| Slack | slack-sdk | latest |
| LLM (option 1) | openai | latest |
| LLM (option 2) | anthropic | latest |

---

## API Integrations

### SerpAPI (Web Search)

**Endpoint:** `https://serpapi.com/search`

**Parameters:**
```python
{
    "q": "TimeGPT OR StatsForecast",
    "tbm": "nws",  # news search
    "num": 10,
    "api_key": SERP_API_KEY
}
```

**Cost:** ~$50/month for 100 searches/day

### GitHub API

**Endpoint:** `https://api.github.com/search/repositories`

**Headers:**
```python
{
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
```

**Rate Limit:** 30 requests/minute (authenticated)

### OpenAI API

**Endpoint:** `https://api.openai.com/v1/chat/completions`

**Model:** gpt-3.5-turbo (default) or gpt-4

**Cost:** ~$0.01-0.10 per digest

### Slack Web API

**Endpoint:** `https://slack.com/api/chat.postMessage`

**Required Scopes:** `chat:write`, `channels:read`

---

## File Structure

```
005-plugins/nixtla-search-to-slack/
├── README.md                     # Full documentation
├── QUICKSTART.md                 # Quick setup
├── SETUP_GUIDE.md                # Comprehensive guide
├── requirements.txt
├── .env.example
├── src/nixtla_search_to_slack/
│   ├── __init__.py
│   ├── main.py                   # CLI entry point
│   ├── search_orchestrator.py    # Search coordination
│   ├── content_aggregator.py     # Deduplication
│   ├── ai_curator.py             # AI summaries
│   ├── slack_publisher.py        # Slack posting
│   └── config_loader.py          # YAML loading
├── config/
│   ├── topics.yaml               # Topic definitions
│   └── sources.yaml              # Source config
├── tests/
│   ├── conftest.py
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

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Slack bot OAuth token |
| `SERP_API_KEY` | Yes | SerpAPI key for web search |
| `GITHUB_TOKEN` | Yes | GitHub personal access token |
| `OPENAI_API_KEY` | Either | OpenAI API key |
| `ANTHROPIC_API_KEY` | Either | Anthropic API key |
| `SLACK_CHANNEL` | No | Default channel (default: #nixtla-updates) |
| `MAX_ITEMS_PER_DIGEST` | No | Max items (default: 10) |
| `DEBUG` | No | Enable debug logging |

---

## CLI Interface

### Usage

```bash
python -m nixtla_search_to_slack [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--topic TOPIC` | Run digest for specified topic |
| `--list-topics` | List available topics |
| `--dry-run` | Preview without posting |
| `--debug` | Enable debug output |

---

## Configuration Schema

### topics.yaml

```yaml
topics:
  <topic-id>:
    name: string           # Display name
    keywords: list         # Search keywords
    sources: list          # [web, github]
    filters:
      min_relevance: int   # 0-100 threshold
    slack_channel: string  # Channel to post to
```

### sources.yaml

```yaml
sources:
  web:
    provider: serpapi
    max_results: int
    time_range: string     # 7d, 14d, 30d
    exclude_domains: list
  github:
    organizations: list
    additional_repos: list
    max_results: int
```

---

## Testing

### Run All Tests

```bash
pytest
```

### With Coverage

```bash
pytest --cov=nixtla_search_to_slack --cov-report=term-missing
```

### Individual Test File

```bash
pytest tests/test_content_aggregator.py
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Import error | Missing deps | `pip install -r requirements.txt` |
| API key error | Invalid/missing key | Check `.env` file |
| Slack 403 | Missing scope | Add `chat:write` scope |
| Empty results | No matches | Broaden keywords |
| Rate limit | Too many requests | Wait and retry |

---

## Limitations (By Design)

| Limitation | Reason |
|------------|--------|
| No persistence | MVP simplicity |
| No scheduling | External cron preferred |
| Basic dedup | String matching only |
| Single-threaded | Simplicity over performance |
| No auth | Reference implementation |
