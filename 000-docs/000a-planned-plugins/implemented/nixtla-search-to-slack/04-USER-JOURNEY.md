# Search-to-Slack - User Journey

**Plugin:** nixtla-search-to-slack
**Last Updated:** 2025-12-12

---

## Setup Journey

### Step 1: Clone and Setup Environment

```bash
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd plugins-nixtla/005-plugins/nixtla-search-to-slack

python -m venv venv
source venv/bin/activate
pip install python-dotenv pyyaml requests slack-sdk openai
```

### Step 2: Configure API Keys

Copy template and edit:

```bash
cp .env.example .env
```

Required keys:

```bash
# .env
SLACK_BOT_TOKEN=xoxb-your-token
SERP_API_KEY=your-serpapi-key
GITHUB_TOKEN=ghp_your-github-token
OPENAI_API_KEY=sk-your-key  # or ANTHROPIC_API_KEY
SLACK_CHANNEL=#nixtla-updates
```

### Step 3: Configure Slack Bot

1. Create app at https://api.slack.com/apps
2. Add OAuth scopes: `chat:write`, `channels:read`
3. Install to workspace
4. Copy bot token to `.env`
5. Add bot to target channel

### Step 4: Test Run

```bash
# Dry run (no Slack posting)
python -m nixtla_search_to_slack --topic nixtla-core --dry-run

# Real run
python -m nixtla_search_to_slack --topic nixtla-core
```

---

## Usage Journey

### List Available Topics

```bash
python -m nixtla_search_to_slack --list-topics
```

Output:
```
Available topics:
  nixtla-core: Nixtla Core Updates
  forecasting-news: Time Series Forecasting News
```

### Run Digest for Topic

```bash
python -m nixtla_search_to_slack --topic nixtla-core
```

### Dry Run (No Slack Posting)

```bash
python -m nixtla_search_to_slack --topic nixtla-core --dry-run
```

Output shows what would be posted without actually posting.

---

## Example Output

Slack message format:

```
📊 Nixtla & Time Series Digest
Generated: Dec 12, 2025 at 9:00 AM CST | Items: 5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. TimeGPT 2.0 Released with Multivariate Support
Source: GitHub • Relevance: 95%

> TimeGPT now supports multivariate time series forecasting
> with automatic feature selection and improved accuracy.

Key Points:
• Handles up to 100 variables simultaneously
• 15% accuracy improvement on M5 data
• New Python SDK with async support

Why this matters: Enables enterprise forecasting scenarios
previously requiring custom solutions.

[View Source →]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Customization

### Add New Topic

Edit `config/topics.yaml`:

```yaml
topics:
  my-topic:
    name: "My Custom Topic"
    keywords:
      - keyword1
      - keyword2
    sources: [web, github]
    filters:
      min_relevance: 50
    slack_channel: "#my-channel"
```

### Change Search Sources

Edit `config/sources.yaml`:

```yaml
sources:
  web:
    max_results: 20  # Increase results
    time_range: 14d  # Two weeks instead of one
```

---

## Scheduling (External)

### Cron Example

```bash
# Daily at 9 AM
0 9 * * * /path/to/venv/bin/python -m nixtla_search_to_slack --topic nixtla-core
```

### GitHub Actions Example

```yaml
name: Daily Digest
on:
  schedule:
    - cron: '0 14 * * *'  # 2 PM UTC
jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install -e 005-plugins/nixtla-search-to-slack
      - run: python -m nixtla_search_to_slack --topic nixtla-core
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
          SERP_API_KEY: ${{ secrets.SERP_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

---

## Error Scenarios

### "Missing API key"

Check `.env` file has all required keys.

### "Slack posting failed"

- Verify bot token is valid
- Check bot is added to channel
- Confirm OAuth scopes include `chat:write`

### "No results found"

- Check keywords in topics.yaml
- Verify SerpAPI has remaining credits
- Try broader search terms

### "Rate limit exceeded"

- SerpAPI: Check monthly quota
- GitHub: Use token for higher limits
- OpenAI: Check usage dashboard
