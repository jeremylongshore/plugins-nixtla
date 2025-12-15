# Support Deflector - Product Requirements Document

**Plugin:** nixtla-support-deflector
**Version:** 0.1.0
**Status:** Planned
**Last Updated:** 2025-12-15

---

## Overview

A Claude Code plugin that ingests support tickets from GitHub Issues, Intercom, or email, automatically drafts responses using RAG over Nixtla documentation, and surfaces patterns that indicate product gaps versus user education opportunities.

---

## Problem Statement

Engineering teams at small AI companies like Nixtla spend 15-25% of their time on support tickets, many of which are repetitive questions answered in documentation. This creates a costly drain on resources that should be focused on product development.

---

## Goals

1. Ingest tickets from GitHub Issues API, Intercom webhooks, or email parsing
2. Auto-draft contextual replies using Nixtla docs + similar resolved tickets
3. Identify recurring issues and categorize as FAQ vs product bug vs feature request
4. Flag tickets requiring human expertise vs auto-resolvable
5. Generate weekly digest with support themes, resolution rates, and product insights

## Non-Goals

- Replace human support entirely
- Handle billing or account-level issues
- Modify Nixtla's core product

---

## Target Users

| User | Need |
|------|------|
| Engineering teams | Reduce time on repetitive support |
| Support staff | Draft responses faster |
| Product managers | Identify patterns for product improvements |
| Nixtla leadership | Understand support burden |

---

## Functional Requirements

### FR-1: Ticket Ingestion
- Connect to GitHub Issues API
- Support Intercom webhooks
- Optional email parsing integration
- Normalize ticket format across sources

### FR-2: Auto-Draft Responses
- RAG over Nixtla documentation (statsforecast, nixtla, mlforecast)
- Search similar resolved tickets for patterns
- Generate contextual draft responses
- Confidence scoring for drafts

### FR-3: Pattern Detection
- Identify recurring issues automatically
- Categorize as: FAQ, Bug, Feature Request, Documentation Gap
- Track frequency and impact of each category
- Suggest documentation updates for frequent FAQs

### FR-4: Escalation Routing
- Flag tickets requiring human expertise
- Auto-resolve simple questions with high confidence
- Route complex issues to appropriate team member
- Track escalation patterns

### FR-5: Weekly Digest
- Summary report of support themes
- Resolution rates by category
- Product insights from ticket patterns
- Recommended actions for product team

### FR-6: MCP Server Tools
Expose 5 tools to Claude Code:
1. `ingest_tickets` - Import tickets from configured sources
2. `draft_response` - Generate response draft for a ticket
3. `categorize_ticket` - Classify ticket type and priority
4. `get_patterns` - Retrieve recurring issue patterns
5. `generate_digest` - Create weekly summary report

---

## Non-Functional Requirements

### NFR-1: Performance
- Draft generation: <5 seconds per ticket
- Pattern analysis: Real-time updates
- Digest generation: <30 seconds

### NFR-2: Dependencies
- Python 3.10+
- Vector store (ChromaDB or similar)
- GitHub API access
- Optional: Intercom API, email IMAP

### NFR-3: Security
- API tokens stored securely in .env
- No customer PII in logs
- Audit trail for all auto-responses

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Ticket response time reduction | 50%+ |
| Auto-resolved tickets | 30% |
| Engineering hours saved/week | 10+ hours |
| Pattern detection accuracy | 85%+ |

---

## Scope

### In Scope
- GitHub Issues integration
- RAG over Nixtla documentation
- Response drafting
- Pattern detection
- Weekly digests

### Out of Scope
- Billing/account issues
- Real-time chat support
- Phone support
- Multi-language support (Phase 1)

---

## Technical Approach

- **MCP Server**: Exposes tools for ticket search, draft generation, and pattern analysis
- **Vector Store**: Embed Nixtla docs + historical tickets using OpenAI/Cohere embeddings
- **Integrations**: GitHub API, Intercom API, optional Slack notifications

---

## Estimated Effort

4-6 weeks for MVP with GitHub Issues integration. Additional 2 weeks per integration (Intercom, email).

---

## Revenue Impact

Indirect. Frees engineering capacity worth approximately $15-25K/month in recovered productivity for a 5-person team.
