# Search-to-Slack - Business Case

**Plugin:** nixtla-search-to-slack
**Category:** Internal Efficiency
**Status:** MVP / Reference Implementation
**Last Updated:** 2025-12-12

---

## Problem Statement

Time-series forecasting practitioners need to stay updated on:
- Nixtla product releases and updates
- statsforecast/TimeGPT GitHub activity
- Industry news and research
- Community discussions

Manually monitoring these sources is time-consuming and inconsistent.

## Solution

An automated content discovery pipeline that:
1. Searches web and GitHub for Nixtla-related content
2. Uses AI to summarize and filter relevant items
3. Posts curated digests to Slack channels

---

## Important Disclaimers

This is explicitly **NOT**:
- A Nixtla product or service
- A production-ready system
- A managed service
- Enterprise-grade software

This **IS**:
- A reference implementation
- A construction kit for learning
- An MVP demonstration
- An educational example

---

## Target Users

1. **Nixtla Team**: Stay updated on product mentions and community activity
2. **Developers**: Learn how to build search → AI → Slack workflows
3. **Internal Teams**: Automate content curation for any topic

---

## Value Proposition

| Without Plugin | With Plugin |
|---------------|-------------|
| Manual source monitoring | Automated search |
| Read full articles | AI-generated summaries |
| Scattered updates | Consolidated Slack digest |
| Hours per week | Minutes per week |

---

## Current Capabilities

### Implemented
- Web search via SerpAPI
- GitHub search (Nixtla org + allowlist)
- Basic URL/title deduplication
- AI summaries (OpenAI or Anthropic)
- Slack Block Kit formatting
- YAML configuration
- CLI execution

### Not Implemented
- Reddit, Twitter/X, arXiv, YouTube, RSS
- Semantic deduplication
- User personalization
- Database persistence
- Queue system
- Monitoring/alerting

---

## Cost Structure

| Service | Approximate Cost |
|---------|-----------------|
| SerpAPI | $50/month (100 searches/day) |
| GitHub API | Free |
| OpenAI | ~$0.01-0.10 per digest |
| Slack | Free |

---

## Recommendation

**Status: MVP** - Working reference implementation suitable for learning and adaptation. Not designed for production use without significant hardening.
