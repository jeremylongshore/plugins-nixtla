# Search-to-Slack - Product Requirements Document

**Plugin:** nixtla-search-to-slack
**Version:** 0.1.0 (MVP)
**Status:** Reference Implementation
**Last Updated:** 2025-12-12

---

## Overview

A construction kit and reference implementation for automated content discovery. Searches web and GitHub for Nixtla-related content, generates AI summaries, and posts curated digests to Slack.

---

## Goals

1. Demonstrate search → AI → Slack workflow pattern
2. Provide example code for content curation
3. Automate Nixtla-focused content discovery
4. Serve as educational reference

## Non-Goals

- Production-ready service
- Comprehensive source coverage
- Enterprise features (auth, multi-tenant, monitoring)
- Real-time alerting

---

## Functional Requirements

### FR-1: Content Search
- Search web via SerpAPI for configurable keywords
- Search GitHub for Nixtla org activity
- Support time-range filtering (last 7 days)
- Exclude configurable domains

### FR-2: Content Processing
- Deduplicate by URL and title (basic string matching)
- Score relevance (configurable threshold)
- Extract key metadata (title, source, date)

### FR-3: AI Summarization
- Generate concise summaries using OpenAI or Anthropic
- Extract key points as bullet list
- Add "why this matters" context
- Configurable LLM provider

### FR-4: Slack Publishing
- Format as Block Kit message
- Include source links
- Show relevance scores
- Support configurable channel

### FR-5: Configuration
- YAML-based topic definitions
- YAML-based source configuration
- Environment variables for secrets
- CLI for manual execution

---

## Non-Functional Requirements

### NFR-1: Limitations (By Design)
- Single-threaded execution
- No persistence between runs
- No rate limiting
- No automatic scheduling

### NFR-2: Dependencies
- Python 3.8+
- SerpAPI account ($50/month)
- GitHub token (free)
- OpenAI or Anthropic API key
- Slack workspace with bot permissions

---

## User Stories

### US-1: Nixtla Team Member
> "As a Nixtla team member, I want automated weekly digests of product mentions so I can track community engagement."

**Acceptance:** Run CLI command and receive Slack digest with relevant content.

### US-2: Developer Learning
> "As a developer, I want example code for search → AI → Slack so I can build my own workflow."

**Acceptance:** Code is readable, documented, and demonstrates the pattern clearly.

---

## Scope

### In Scope
- Web search (SerpAPI)
- GitHub search (Nixtla org)
- AI summarization
- Slack posting
- YAML configuration
- CLI execution
- Example code

### Out of Scope
- Reddit, Twitter/X, arXiv, YouTube, RSS
- Semantic deduplication
- User preferences
- Database storage
- Automatic scheduling
- Production hardening
- Multi-tenant support
- Monitoring/alerting
