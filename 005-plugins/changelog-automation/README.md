# Changelog Automation Plugin

Automate changelog generation with AI-powered synthesis, multi-source data fetching, and quality validation.

## Features

- **Multi-Source Data Fetching**: GitHub PRs/issues, Slack messages, Git commits
- **AI-Powered Synthesis**: Writer Agent groups changes, generates narrative
- **Quality Gate**: Two-layer validation (deterministic + editorial)
- **Template System**: Customizable markdown templates with YAML frontmatter
- **PR Automation**: Automatically creates pull request with changelog

## Quick Start

### 1. Install Plugin

```bash
cd your-project
/plugin install changelog-automation
```

### 2. Configure

Copy example config:
```bash
cp .claude/plugins/changelog-automation/config/.changelog-config.example.json .changelog-config.json
```

Set environment variables:
```bash
export GITHUB_TOKEN="ghp_..."
export SLACK_TOKEN="xoxb-..."  # Optional
```

### 3. Validate Setup

```bash
/changelog-validate
```

### 4. Generate Changelog

```bash
# Weekly changelog (last 7 days)
/changelog-weekly

# Custom date range
/changelog-custom start_date=2025-12-01 end_date=2025-12-15
```

## Commands

- `/changelog-weekly` - Generate changelog for last 7 days
- `/changelog-custom` - Generate changelog for custom date range
- `/changelog-validate` - Validate configuration and setup

## Configuration

Edit `.changelog-config.json`:

```json
{
  "sources": [
    {
      "type": "github",
      "config": {
        "repo": "myorg/myrepo",
        "token_env": "GITHUB_TOKEN"
      }
    }
  ],
  "template": "changelogs/weekly-template.md",
  "output_path": "CHANGELOG.md",
  "quality_threshold": 80
}
```

## Requirements

- Python 3.10+
- GitHub Personal Access Token (for GitHub source)
- Slack Bot Token (optional, for Slack source)

## Documentation

Full documentation in `000-docs/000a-planned-plugins/changelog-automation/`:
- [Business Case](../../../000-docs/000a-planned-plugins/changelog-automation/01-BUSINESS-CASE.md)
- [PRD](../../../000-docs/000a-planned-plugins/changelog-automation/02-PRD.md)
- [Architecture](../../../000-docs/000a-planned-plugins/changelog-automation/03-ARCHITECTURE.md)
- [User Journey](../../../000-docs/000a-planned-plugins/changelog-automation/04-USER-JOURNEY.md)
- [Technical Spec](../../../000-docs/000a-planned-plugins/changelog-automation/05-TECHNICAL-SPEC.md)

## Development

```bash
cd 005-plugins/changelog-automation

# Install dependencies
pip install -r scripts/requirements.txt

# Run tests
pytest tests/ -v

# Run smoke test
python tests/run_changelog_smoke.py
```

## License

MIT - See [LICENSE](../../LICENSE)

## Author

Jeremy Longshore <jeremy@intentsolutions.io>
