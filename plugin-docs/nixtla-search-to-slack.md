# Nixtla Search-to-Slack Plugin

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           📢 NIXTLA SEARCH-TO-SLACK PLUGIN                   ║
║       AI-Powered Content Curation & Team Notifications        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## Plugin Structure

```
📢 nixtla-search-to-slack/
│
├── 📖 README.md
├── 📘 SETUP_GUIDE.md
├── 📦 requirements.txt
│
├── ⚙️  config/
│   ├── 📄 sources.yaml
│   └── 📄 topics.yaml
│
├── 🎯 skills/
│   ├── 📊 nixtla-model-benchmarker/
│   │   ├── 📄 SKILL.md
│   │   └── 🖼️  assets/
│   │
│   ├── 🔍 nixtla-research-assistant/
│   │   └── 📄 SKILL.md
│   │
│   └── 🔨 timegpt-pipeline-builder/
│       ├── 📄 SKILL.md
│       └── 🖼️  assets/
│
├── 💻 src/
│   └── 🐍 nixtla_search_to_slack/
│       ├── 🤖 ai_curator.py
│       ├── 📡 content_aggregator.py
│       ├── ⚙️  config_loader.py
│       ├── 🎯 search_orchestrator.py
│       └── 💬 slack_publisher.py
│
└── 🧪 tests/
    ├── ⚙️  conftest.py
    ├── 🧪 test_ai_curator.py
    ├── 🧪 test_config_loader.py
    ├── 🧪 test_content_aggregator.py
    ├── 🧪 test_search_orchestrator.py
    └── 🧪 test_slack_publisher.py
```

---

## What It Does

**Nixtla Search-to-Slack** is an AI-powered content aggregation and curation plugin that automatically searches multiple sources for Nixtla-related content, filters it through AI quality checks, and publishes relevant findings to Slack channels for team knowledge sharing.

**Who It Helps**:
- 📚 Research teams tracking Nixtla developments
- 🏢 Organizations monitoring time-series ML trends
- 👥 Teams wanting automated knowledge sharing
- 🔍 Analysts staying current with forecasting research

**Key Value**: Automate research aggregation with AI quality filtering - save hours of manual searching and curation.

---

## Branch-by-Branch Description

### ⚙️ config/

**Purpose**: Configuration files for sources and topics

#### `sources.yaml`

**What it does**:
- Defines content sources to search
- API endpoints and authentication
- Search frequency and limits

**Example configuration**:
```yaml
sources:
  - name: arxiv
    type: api
    endpoint: http://export.arxiv.org/api/query
    search_fields: [title, abstract]
    rate_limit: 3/second

  - name: github
    type: api
    endpoint: https://api.github.com/search/repositories
    auth: token
    search_fields: [name, description, readme]

  - name: reddit
    type: api
    endpoint: https://oauth.reddit.com
    subreddits: [MachineLearning, datascience, statistics]
```

**Supported sources**:
- arXiv (research papers)
- GitHub (code repositories)
- Reddit (discussions)
- Twitter/X (social media)
- RSS feeds (blogs, news)

#### `topics.yaml`

**What it does**:
- Defines search topics and keywords
- Relevance scoring criteria
- Quality filters

**Example configuration**:
```yaml
topics:
  nixtla_releases:
    keywords: [nixtla, timegpt, statsforecast, mlforecast]
    priority: high
    min_relevance: 0.7

  forecasting_research:
    keywords: [time series, forecasting, ARIMA, prophet]
    priority: medium
    min_relevance: 0.6

  competition_tracking:
    keywords: [M5 competition, M4 competition, kaggle forecasting]
    priority: low
    min_relevance: 0.5
```

---

### 🎯 skills/

**Purpose**: Embedded Claude Code skills

#### 📊 nixtla-model-benchmarker/

**What it does**:
- Activates when user mentions model comparison
- Provides benchmarking guidance
- Suggests evaluation metrics
- Helps interpret results

**Triggers**: "compare models", "benchmark nixtla", "model performance"

#### 🔍 nixtla-research-assistant/

**What it does**:
- Activates during research tasks
- Helps find relevant papers
- Summarizes research findings
- Suggests related topics

**Triggers**: "research nixtla", "find papers", "literature review"

#### 🔨 timegpt-pipeline-builder/

**What it does**:
- Activates when building pipelines
- Guides pipeline architecture
- Suggests best practices
- Provides code templates

**Triggers**: "build pipeline", "create workflow", "timegpt production"

---

### 💻 src/nixtla_search_to_slack/

**Purpose**: Core plugin source code (5 modules)

#### `config_loader.py` ⚙️

**What it does**:
- Loads and validates YAML configuration
- Environment variable substitution
- Configuration schema validation
- Default value management

**Key Functions**:
- `load_config(path)` - Load YAML config file
- `validate_schema(config)` - Validate against JSON schema
- `merge_defaults(config)` - Apply default values
- `get_env_vars()` - Load environment variables

**Example Usage**:
```python
from nixtla_search_to_slack import config_loader

config = config_loader.load_config("config/sources.yaml")
sources = config["sources"]
```

---

#### `content_aggregator.py` 📡

**What it does**:
- Searches multiple content sources
- Rate limiting and retry logic
- Data normalization across sources
- Caching and deduplication

**Supported Sources**:
- **arXiv API**: Academic papers
- **GitHub API**: Code repositories
- **Reddit API**: Subreddit discussions
- **Twitter API**: Social media mentions
- **RSS feeds**: Blog posts and news

**Key Functions**:
- `search_all_sources(query)` - Search all configured sources
- `search_arxiv(query)` - Search arXiv papers
- `search_github(query)` - Search GitHub repos
- `search_reddit(query)` - Search Reddit discussions
- `normalize_results(raw_data)` - Convert to common format

**Rate Limiting**:
- Respects API rate limits
- Exponential backoff on errors
- Concurrent requests with limits

**Example Usage**:
```python
from nixtla_search_to_slack import content_aggregator

aggregator = content_aggregator.ContentAggregator(config)
results = aggregator.search_all_sources("timegpt forecasting")
# Returns: [{source, title, url, content, timestamp}, ...]
```

---

#### `ai_curator.py` 🤖

**What it does**:
- AI-powered content quality filtering
- Relevance scoring (0.0 to 1.0)
- Duplicate detection
- Sentiment analysis
- Topic classification

**AI Models Used**:
- Sentence transformers for embeddings
- BERT for relevance scoring
- Custom trained Nixtla topic classifier

**Key Functions**:
- `score_relevance(content, topic)` - Calculate relevance score
- `is_duplicate(content, existing)` - Check for duplicates
- `classify_quality(content)` - Quality assessment
- `extract_key_points(content)` - Summarization

**Scoring Criteria**:
- **0.9-1.0**: Highly relevant (official Nixtla announcements)
- **0.7-0.9**: Very relevant (direct mentions, benchmarks)
- **0.5-0.7**: Moderately relevant (time-series general)
- **0.0-0.5**: Low relevance (filtered out)

**Example Usage**:
```python
from nixtla_search_to_slack import ai_curator

curator = ai_curator.AICurator()
for item in results:
    score = curator.score_relevance(item, "nixtla")
    if score >= 0.7:
        print(f"✅ {item['title']} (score: {score})")
```

---

#### `search_orchestrator.py` 🎯

**What it does**:
- Orchestrates the entire pipeline
- Workflow management
- Error handling and recovery
- Scheduling and automation
- Progress tracking

**Workflow Steps**:
1. Load configuration
2. Execute searches across sources
3. Aggregate results
4. AI curation and filtering
5. Prepare Slack messages
6. Publish to Slack
7. Log results and metrics

**Key Functions**:
- `run_pipeline()` - Execute full pipeline
- `schedule_recurring(cron)` - Set up scheduled runs
- `handle_error(error)` - Error recovery
- `generate_report()` - Create summary report

**Scheduling**:
- Cron-style scheduling
- One-time runs
- Continuous monitoring mode

**Example Usage**:
```python
from nixtla_search_to_slack import search_orchestrator

orchestrator = search_orchestrator.SearchOrchestrator(config)

# One-time run
orchestrator.run_pipeline()

# Scheduled run (daily at 9 AM)
orchestrator.schedule_recurring("0 9 * * *")
```

---

#### `slack_publisher.py` 💬

**What it does**:
- Publishes curated content to Slack
- Formatted message creation
- Channel management
- Thread conversations
- Reaction/emoji support
- Error notifications

**Slack Features**:
- Rich message formatting (markdown)
- Interactive buttons
- Threaded discussions
- File attachments
- @mentions and notifications

**Key Functions**:
- `publish_message(channel, content)` - Send message
- `create_thread(parent, reply)` - Create thread
- `add_reaction(message, emoji)` - Add emoji reaction
- `upload_file(channel, file)` - Upload file
- `format_message(content)` - Format for Slack

**Message Format**:
```
🔍 *New Nixtla Content Found*

*[Paper] TimeGPT: The First Foundation Model for Time Series*
📊 Relevance Score: 0.95
🔗 https://arxiv.org/abs/2310.xxxxx

Summary: TimeGPT introduces a pre-trained transformer model for...

---
Found 3 similar items | Last updated: 2025-12-09 14:30 UTC
```

**Example Usage**:
```python
from nixtla_search_to_slack import slack_publisher

publisher = slack_publisher.SlackPublisher(token=SLACK_TOKEN)
publisher.publish_message(
    channel="#research",
    content=curated_results
)
```

---

### 🧪 tests/

**Purpose**: Comprehensive test suite (6 test files)

#### `conftest.py`

**What it does**:
- Pytest configuration
- Shared fixtures
- Test environment setup
- Mock data generation

#### `test_config_loader.py`

**What it tests**:
- YAML parsing
- Schema validation
- Environment variable substitution
- Error handling

#### `test_content_aggregator.py`

**What it tests**:
- API integration
- Rate limiting
- Data normalization
- Caching logic

#### `test_ai_curator.py`

**What it tests**:
- Relevance scoring accuracy
- Duplicate detection
- Quality classification
- Edge cases

#### `test_search_orchestrator.py`

**What it tests**:
- Pipeline execution
- Error recovery
- Scheduling logic
- Reporting

#### `test_slack_publisher.py`

**What it tests**:
- Message formatting
- Slack API integration
- Thread creation
- Error handling

---

## Terminal How-To Guide

### Initial Setup

```bash
# Navigate to plugin directory
cd /home/jeremy/000-projects/nixtla/005-plugins/nixtla-search-to-slack

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "slack|pyyaml|requests"
```

**Expected packages**:
- slack-sdk
- pyyaml
- requests
- beautifulsoup4
- sentence-transformers

---

### Configuration Setup

#### Step 1: Create Slack App

```bash
# 1. Go to https://api.slack.com/apps
# 2. Create New App → "From scratch"
# 3. Name it "Nixtla Research Bot"
# 4. Select your workspace
# 5. Add Bot Token Scopes:
#    - chat:write
#    - chat:write.public
#    - files:write
#    - reactions:write
# 6. Install App to Workspace
# 7. Copy "Bot User OAuth Token" (starts with xoxb-)
```

#### Step 2: Set Environment Variables

```bash
# Create .env file
cat > .env <<EOF
SLACK_BOT_TOKEN=xoxb-your-token-here
GITHUB_TOKEN=ghp_your-token-here
REDDIT_CLIENT_ID=your-client-id
REDDIT_CLIENT_SECRET=your-client-secret
EOF

# Load environment variables
export $(cat .env | xargs)

# Verify
echo $SLACK_BOT_TOKEN
```

#### Step 3: Configure Sources

```bash
# Edit config/sources.yaml
nano config/sources.yaml

# Add your sources (example below)
```

Example `sources.yaml`:
```yaml
sources:
  - name: arxiv
    enabled: true
    search_terms: ["timegpt", "nixtla", "time series forecasting"]

  - name: github
    enabled: true
    auth_token: ${GITHUB_TOKEN}
    search_terms: ["nixtla", "statsforecast", "mlforecast"]

  - name: reddit
    enabled: true
    client_id: ${REDDIT_CLIENT_ID}
    client_secret: ${REDDIT_CLIENT_SECRET}
    subreddits: ["MachineLearning", "datascience"]
```

---

### Running the Plugin

#### One-Time Search

```bash
# Run once and exit
python -m nixtla_search_to_slack.search_orchestrator

# With specific topic
python -m nixtla_search_to_slack.search_orchestrator --topic "timegpt"

# Dry run (no Slack publishing)
python -m nixtla_search_to_slack.search_orchestrator --dry-run
```

#### Scheduled Execution

```bash
# Run daily at 9 AM using cron
crontab -e

# Add this line:
0 9 * * * cd /home/jeremy/000-projects/nixtla/005-plugins/nixtla-search-to-slack && python -m nixtla_search_to_slack.search_orchestrator

# Or use the built-in scheduler
python -m nixtla_search_to_slack.search_orchestrator --schedule "0 9 * * *"
```

#### Continuous Monitoring

```bash
# Run in background, check every hour
nohup python -m nixtla_search_to_slack.search_orchestrator \
  --continuous \
  --interval 3600 \
  > logs/search_to_slack.log 2>&1 &

# Check process
ps aux | grep search_orchestrator

# View logs
tail -f logs/search_to_slack.log
```

---

### Testing Individual Components

#### Test Configuration Loading

```bash
# Validate YAML syntax
python -c "from src.nixtla_search_to_slack.config_loader import load_config; load_config('config/sources.yaml')"

# Expected output: No errors = valid config
```

#### Test Content Aggregation

```bash
# Test arXiv search
python -c "
from src.nixtla_search_to_slack.content_aggregator import ContentAggregator
agg = ContentAggregator()
results = agg.search_arxiv('timegpt')
print(f'Found {len(results)} papers')
"

# Test GitHub search
python -c "
from src.nixtla_search_to_slack.content_aggregator import ContentAggregator
agg = ContentAggregator()
results = agg.search_github('nixtla')
print(f'Found {len(results)} repos')
"
```

#### Test AI Curation

```bash
# Test relevance scoring
python -c "
from src.nixtla_search_to_slack.ai_curator import AICurator
curator = AICurator()
score = curator.score_relevance(
    'TimeGPT: First foundation model for time series',
    'nixtla'
)
print(f'Relevance score: {score:.2f}')
"
```

#### Test Slack Publishing

```bash
# Send test message
python -c "
from src.nixtla_search_to_slack.slack_publisher import SlackPublisher
publisher = SlackPublisher(token='$SLACK_BOT_TOKEN')
publisher.publish_message(
    channel='#research',
    content='🧪 Test message from Nixtla Search-to-Slack'
)
"
```

---

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_ai_curator.py

# Run with coverage
pytest --cov=src/nixtla_search_to_slack tests/

# Run with verbose output
pytest -v tests/

# Run only fast tests (skip slow integration tests)
pytest -m "not slow" tests/
```

**Expected output**:
```
============================= test session starts ==============================
collected 42 items

tests/test_config_loader.py ........                                    [ 19%]
tests/test_content_aggregator.py ..........                             [ 42%]
tests/test_ai_curator.py .......                                        [ 59%]
tests/test_search_orchestrator.py .....                                 [ 71%]
tests/test_slack_publisher.py ......                                    [ 85%]
tests/conftest.py ......                                                [100%]

============================== 42 passed in 12.34s =============================
```

---

### Monitoring and Debugging

#### View Logs

```bash
# Real-time log viewing
tail -f logs/search_to_slack.log

# Search logs for errors
grep -i error logs/search_to_slack.log

# Count successful runs
grep -c "Pipeline completed successfully" logs/search_to_slack.log
```

#### Check Metrics

```bash
# View summary statistics
python -m nixtla_search_to_slack.search_orchestrator --report

# Example output:
# Total searches: 156
# Items found: 1,234
# Items curated: 342
# Published to Slack: 89
# Average relevance: 0.78
# Success rate: 98.7%
```

---

### Troubleshooting

#### Error: "Slack API: invalid_auth"

```bash
# Solution: Check Slack token
echo $SLACK_BOT_TOKEN

# Regenerate token if needed (Slack App settings)
# Update .env file
# Reload environment
export $(cat .env | xargs)
```

#### Error: "GitHub API rate limit exceeded"

```bash
# Solution 1: Check rate limit status
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit

# Solution 2: Reduce search frequency in config/sources.yaml
# Change: rate_limit: 10/minute  →  rate_limit: 5/minute

# Solution 3: Use authenticated requests (higher limit)
# Add GITHUB_TOKEN to .env
```

#### Error: "Reddit API: 401 Unauthorized"

```bash
# Solution: Verify Reddit credentials
python -c "
import requests
auth = requests.auth.HTTPBasicAuth('$REDDIT_CLIENT_ID', '$REDDIT_CLIENT_SECRET')
response = requests.post('https://www.reddit.com/api/v1/access_token',
    auth=auth,
    data={'grant_type': 'client_credentials'},
    headers={'User-Agent': 'nixtla-search-bot/1.0'}
)
print(response.json())
"

# Should return access_token, not error
```

#### Error: "No results found"

```bash
# Solution 1: Check search terms
cat config/sources.yaml | grep search_terms

# Solution 2: Verify sources are enabled
cat config/sources.yaml | grep enabled

# Solution 3: Lower relevance threshold
# Edit config/topics.yaml
# Change: min_relevance: 0.7  →  min_relevance: 0.5
```

---

## Performance Benchmarks

| Sources | Search Frequency | Runtime | API Calls | Slack Messages |
|---------|-----------------|---------|-----------|----------------|
| 3 sources | Daily | ~2 min | ~50 | ~5-10 |
| 5 sources | Daily | ~5 min | ~120 | ~15-20 |
| 7 sources | Hourly | ~10 min | ~800/day | ~100-150/day |

---

## Common Use Cases

### Use Case 1: Daily Research Digest

```bash
# Schedule daily at 9 AM
crontab -e

# Add:
0 9 * * * cd /path/to/plugin && python -m nixtla_search_to_slack.search_orchestrator
```

**Result**: Team receives daily digest of Nixtla-related research in #research channel.

---

### Use Case 2: Real-Time Monitoring

```bash
# Continuous monitoring, check every 15 minutes
python -m nixtla_search_to_slack.search_orchestrator \
  --continuous \
  --interval 900 \
  --priority high
```

**Result**: Instant notifications for high-priority content (new releases, breaking news).

---

### Use Case 3: Custom Topic Tracking

```bash
# Track specific topic
python -m nixtla_search_to_slack.search_orchestrator \
  --topic "M5 competition" \
  --channel "#forecasting-competitions"
```

**Result**: Focused tracking of M5 competition discussions.

---

## Integration with Other Plugins

**Works with**:
- `nixtla-baseline-lab` - Share benchmark results with team
- `nixtla-bigquery-forecaster` - Alert when new forecasts complete
- Research skills - Embedded skills enhance search quality

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              SEARCH-TO-SLACK PIPELINE FLOW                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  arXiv   │  │  GitHub  │  │  Reddit  │  │   RSS    │   │
│  │   API    │  │   API    │  │   API    │  │  Feeds   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │             │          │
│       └─────────────┴──────────────┴─────────────┘          │
│                          │                                   │
│                ┌─────────▼──────────┐                        │
│                │  Content           │                        │
│                │  Aggregator        │                        │
│                └─────────┬──────────┘                        │
│                          │                                   │
│                ┌─────────▼──────────┐                        │
│                │  AI Curator        │◄── ML Models          │
│                │  (Relevance Filter)│                        │
│                └─────────┬──────────┘                        │
│                          │                                   │
│                ┌─────────▼──────────┐                        │
│                │  Slack Publisher   │                        │
│                └─────────┬──────────┘                        │
│                          │                                   │
│                  ┌───────▼────────┐                          │
│                  │  #research     │                          │
│                  │  Slack Channel │                          │
│                  └────────────────┘                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Support & Resources

- **Setup Guide**: `005-plugins/nixtla-search-to-slack/SETUP_GUIDE.md`
- **Source Code**: `005-plugins/nixtla-search-to-slack/src/`
- **Tests**: `005-plugins/nixtla-search-to-slack/tests/`

---

**Version**: 1.7.0
**Status**: ✅ Production Ready
**Last Updated**: 2025-12-09
