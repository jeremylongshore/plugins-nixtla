# Support Deflector - User Journey

**Plugin:** nixtla-support-deflector
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Persona: Engineering Lead

**Name:** Alex
**Role:** Engineering Lead at Nixtla
**Pain Point:** Spending 20% of team's time on support tickets instead of product development

---

## Journey Map

### Stage 1: Discovery
**Trigger:** Alex notices engineering velocity dropping due to support burden

**Actions:**
- Reviews time spent on support tickets
- Identifies repetitive questions that could be automated
- Discovers nixtla-support-deflector plugin

**Outcome:** Decides to try the plugin

---

### Stage 2: Setup
**Trigger:** Alex installs the plugin

**Actions:**
```bash
# Install plugin
claude-code plugins install nixtla-support-deflector

# Configure GitHub integration
export GITHUB_TOKEN=ghp_...
export GITHUB_REPO=nixtla/nixtla

# Index Nixtla documentation
/support-deflector index-docs
```

**Outcome:** Plugin connected to GitHub Issues and docs indexed

---

### Stage 3: First Use
**Trigger:** New GitHub issue arrives

**Actions:**
- Plugin automatically ingests the ticket
- RAG engine finds relevant documentation
- Draft response generated with confidence score

**Claude Code Session:**
```
> /support-deflector draft-response --issue 1234

Draft Response (Confidence: 92%):
---
Thank you for your question about TimeGPT confidence intervals.

You can access confidence intervals by setting `level` parameter:

```python
forecast = client.forecast(df, h=12, level=[80, 95])
```

This will return columns for each confidence level.

See: https://docs.nixtla.io/docs/timegpt-confidence-intervals
---

[Auto-respond] [Edit] [Escalate]
```

**Outcome:** Response drafted in seconds instead of 30+ minutes

---

### Stage 4: Pattern Recognition
**Trigger:** After 2 weeks of usage

**Actions:**
```
> /support-deflector get-patterns

Top Support Patterns (Last 14 Days):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Confidence intervals (23 tickets) → FAQ
   Recommendation: Add to getting started guide

2. API rate limits (15 tickets) → Documentation Gap
   Recommendation: Create rate limit documentation

3. Windows installation (12 tickets) → Bug
   Recommendation: Create GitHub issue for engineering

4. Exogenous variables (8 tickets) → Feature Request
   Recommendation: Add to roadmap discussion
```

**Outcome:** Product insights surfaced automatically

---

### Stage 5: Weekly Review
**Trigger:** Monday morning

**Actions:**
```
> /support-deflector generate-digest

Weekly Support Digest (Dec 9-15, 2025)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tickets Processed: 47
Auto-Resolved: 14 (30%)
Avg Response Time: 42 minutes (was 4.2 hours)
Engineering Hours Saved: 12.5

Top Categories:
- FAQ: 28 (60%)
- Bug Reports: 8 (17%)
- Feature Requests: 7 (15%)
- Documentation Gaps: 4 (8%)

Recommended Actions:
1. Update confidence interval docs (would resolve 23% of tickets)
2. Add rate limit page to docs
3. Investigate Windows installation issue
```

**Outcome:** Clear visibility into support burden and actionable improvements

---

## Success Scenario

After 1 month:
- 50% reduction in ticket response time
- 30% of tickets auto-resolved
- Engineering team reclaims 10+ hours/week
- Product roadmap informed by support patterns
