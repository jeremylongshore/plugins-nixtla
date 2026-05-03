# 130-AA-VISN — Strategic Vision v2.0: Flagship Curation

| | |
|---|---|
| **Status** | Decided |
| **Date** | 2026-05-02 (CST) |
| **Decision owner** | Jeremy Longshore |
| **Authors** | Jeremy Longshore, with Claude (Opus 4.7) acting as lead-tech / CTO |
| **Supersedes** | The implicit "build everything" trajectory that produced 14 plugin directories from a 3-plugin marketplace |
| **Anchors** | `.claude-plugin/marketplace.json`, `README.md`, `005-plugins/README.md`, `CHANGELOG.md`, beads `nixtla-*` |

---

## TL;DR

**This repository ships *three* flagship plugins to the world, not fourteen.** Everything else is either the next-six-months revenue roadmap, deferred Y2 work, or scaffolding that gets explicitly demarcated as experimental and removed from the public-facing surface. The goal is not coverage; the goal is a globally-elite Nixtla showcase that any prospect, partner, or hiring manager can land on and immediately understand: this is what production-grade time-series forecasting with Claude Code looks like.

---

## What we decided

1. **The marketplace is the truth.** The three plugins listed in `.claude-plugin/marketplace.json` (`nixtla-baseline-lab`, `nixtla-bigquery-forecaster`, `nixtla-search-to-slack`) are the v2.0 flagship — call this **The Trinity**. Everything else either earns its way onto the marketplace via the v3.0 roadmap or gets demarcated as experimental.
2. **The Trinity ships at globally-elite quality before anything else gets attention.** That means: parameterized BigQuery, retry/backoff, real CI per plugin, formal pytest with coverage, screencasts, deployment guide for self-hosting, observability hooks. The bar is "a Fortune 500 user installs this, runs it on their data, and trusts the result enough to build downstream automation on it."
3. **The v3.0 expansion is the three highest-revenue PRDs**, in order: `nixtla-sales-demo-builder` (3wk, sales acceleration), `nixtla-forecast-workflow-templates` (6wk, $50–100K ARR, flywheel), `nixtla-forecast-audit-report` (8wk, $100–200K ARR, regulated verticals). Each lands as its own minor release.
4. **The Y2 flagship is `nixtla-embedded-forecast-widget`** (10–12wk, $200–500K Y2). Built only after Trinity + v3.0 are battle-tested with paying customers. Building this earlier is premature optimization.
5. **Everything else is archived or marked experimental.** Eight PRD-missing plugins, two pure-internal tools (support-deflector, docs-qa-generator), one streaming greenfield (anomaly-streaming-monitor), and one warehouse SCAFFOLD (dbt-package) — all moved to an explicit experimental tier, not advertised to the world, not blocking the flagship release.

---

## Why we decided this

### The three-identities problem

Walking the repo today, three different versions of "what this is" are simultaneously visible:

| Identity | Where it lives | Plugin count |
|---|---|---|
| **Original tight showcase** | `.claude-plugin/marketplace.json`, original README narrative | 3 |
| **Organic drift** | `005-plugins/` directory | 14 |
| **Aspirational roadmap** | `000-docs/000a-planned-plugins/` | 7 |

The marketplace is the artifact users actually install from. It listed three plugins on the day the repo was made public, and it lists three plugins today. The 11 extra directories in `005-plugins/` are not products — they are early scaffolds that grew faster than they were finished, with stub READMEs (32–65 lines) and `.mcp.json` shells around thin handlers. Of the 10 PARTIAL plugins, only **two** have any meaningful product documentation (`changelog-automation` and `nixtla-bigquery-forecaster`). The rest were never intended to be public; they leaked through because nothing forced a tier distinction.

### The "global elite" criterion

The owner's question is: what would we present to the world? Not what could we present, what *would* we. The right answer is small, polished, narratively coherent, and verifiable. The wrong answer is "everything we've ever started." Quality is the thing that compounds; sprawl is the thing that decays. This decision optimizes for the compounding direction.

### The revenue picture

A read of all seven PRDs reveals three different value mechanisms:

| Plugin | Value | Y1 projection |
|---|---|---|
| `nixtla-sales-demo-builder` | Direct sales acceleration | 20% cycle reduction, 10% win-rate lift |
| `nixtla-forecast-audit-report` | Regulated-vertical unlock | $100–200K ARR + influenced revenue |
| `nixtla-forecast-workflow-templates` | Flywheel (3× API consumption, 40% churn reduction) | $50–100K ARR |
| `nixtla-embedded-forecast-widget` | Partner distribution / platform play | $200–500K Y2 |
| `nixtla-support-deflector` | Internal cost reduction | $0 customer revenue |
| `nixtla-docs-qa-generator` | Internal cost reduction | $0 customer revenue |
| `changelog-automation` | Internal cost reduction | $0 customer revenue |

Three of seven move the business; four don't. Building the four would be a service to ourselves, not to Nixtla or the world. They get explicit "deferred indefinitely" status — not because they're bad ideas, but because they aren't *this repo's job*. They could be re-spun as standalone Intent Solutions repos if internal demand materializes.

### What the audit told us about quality

State audits dispatched against the partial set returned a consistent signal: most "PARTIAL" plugins are actually closer to scaffolds than to working software.

- `nixtla-search-to-slack`: misclassified — actually working (1.5K LOC, 5 pytest suites at 70–85% coverage, 24K SETUP_GUIDE, real integrations, existing PRD). Belongs in The Trinity, which is exactly where the marketplace already had it.
- `nixtla-baseline-lab`: WORKING, grade A-. MCP server is 1925 lines with full type hints and real schemas; README is grade A. Gaps to elite: no CI per plugin, no formal pytest, no performance benchmarks, no screencast.
- `nixtla-bigquery-forecaster`: demo-grade. Has Workload Identity auth (modern, good) and a real CI/CD pipeline. SQL-injection risk via f-string column names, no retry logic, no caching, no enterprise auth/deploy guide. ~2–3wk to elite.
- `nixtla-dbt-package`: SCAFFOLD. Adapters all empty. 2–3wk with warehouse access.
- `nixtla-anomaly-streaming-monitor`: pure scaffold; closer to greenfield than fix.
- 8 PRD-missing partial plugins: thin MCP handlers + stub READMEs. None are "almost done."

The audit confirmed what marketplace.json already implied: there are three real plugins here. The other eleven directories are unfinished thoughts.

---

## The four tiers

### Tier 1 — The Trinity (v2.0 ship target)

Three plugins, hardened to elite quality, shipped together as v2.0.

| Plugin | Current grade | Hardening required |
|---|---|---|
| `nixtla-baseline-lab` | A− | Add per-plugin CI workflow; migrate homegrown smoke test to pytest with coverage; commit golden output CSVs + plots; record a 60-second screencast; add `examples/` with a runnable demo |
| `nixtla-bigquery-forecaster` | demo-grade | Parameterize all column names in BigQuery queries (security); add exponential backoff for BQ quota errors; add Cloud Function timeout config; ship a Terraform/gcloud "deploy to your project" guide; add response-cache layer; surface query cost estimate in response |
| `nixtla-search-to-slack` | working | Verify `claude plugin install` loads cleanly; wire skills as Claude Code skills; add optional Claude WebSearch fallback to drop SerpAPI cost; one real Slack-bot smoke test; close out the existing PRD's MVP checklist |

**v2.0 acceptance criteria** (every Trinity plugin must pass):

1. Loads via `claude plugin install` from a fresh clone of `jeremylongshore/plugins-nixtla` with zero local state.
2. Per-plugin CI workflow runs on every PR, gates merge, and produces a coverage report.
3. Formal pytest test suite with ≥80% line coverage on plugin code.
4. README starts with a 30-second elevator + a copy-paste quickstart that produces a real result on a fresh machine in under 5 minutes.
5. At least one runnable demo committed to `examples/` with a sample input and expected output.
6. Security review passes (no f-string SQL, no plaintext secrets, retry logic on external APIs, timeouts on every blocking call).
7. A 60–90 second screencast linked from the plugin README.
8. Deploy / self-host guide if the plugin requires external infrastructure (BigQuery, Slack workspace).
9. Listed in `.claude-plugin/marketplace.json` with version synced to plugin manifest.
10. Linked from the root README's flagship section.

### Tier 2 — Revenue plays (v3.0 expansion, sequenced)

Three plugins, each shipped as its own minor release.

| Plugin | Effort | Why this priority |
|---|---|---|
| `nixtla-sales-demo-builder` | 3 wk | Quick-win, smallest of the three, validates v2.0 build template under real load. Direct sales acceleration multiplier for Nixtla. |
| `nixtla-forecast-workflow-templates` | 6 wk | Flywheel: 3× API consumption + 40% churn reduction. Converts demo users into sticky paying customers. $50–100K ARR. |
| `nixtla-forecast-audit-report` | 8 wk | Unlocks regulated verticals (finance, healthcare, pharma). $100–200K ARR + unlocks $200–500K of currently-blocked deals. |

Each lands as its own release (`v2.1.0`, `v2.2.0`, `v2.3.0`). Each must meet the v2.0 acceptance criteria (above) on its own before merging.

### Tier 3 — Y2 flagship

`nixtla-embedded-forecast-widget` — 10–12 wk, $200–500K Y2 ARR. Building this in 2026 instead of waiting for Trinity + v3.0 customer signal is premature optimization. Revisit in 2027 once we have at least three paying enterprise customers on Tier 2 plugins.

### Tier 4 — Experimental / archived

Eleven plugin directories get demarcated and pulled off the public-facing surface:

| Plugin | Disposition | Rationale |
|---|---|---|
| `nixtla-roi-calculator` | Experimental | PRD missing, partial code, valuable concept but not core showcase |
| `nixtla-migration-assistant` | Experimental | Useful sales tool but better as a hosted utility than a plugin |
| `nixtla-snowflake-adapter` | Experimental | Wait until Snowflake Native App story stabilizes |
| `nixtla-airflow-operator` | Experimental | Reasonable concept but no committed customer |
| `nixtla-cost-optimizer` | Experimental | Marketing for an internal optimization, not a product |
| `nixtla-defi-sentinel` | Experimental | Off-mission for a Nixtla showcase |
| `nixtla-forecast-explainer` | Experimental | Could fold into other plugins; not standalone |
| `nixtla-vs-statsforecast-benchmark` | Experimental | Useful blog post / internal benchmark, not a plugin |
| `nixtla-dbt-package` | Deferred | Real value but needs warehouse customer commitment first |
| `nixtla-anomaly-streaming-monitor` | Archived | Closer to greenfield than fix; streaming complexity not worth it without committed customer |
| `changelog-automation` | Deferred indefinitely | Internal-only, $0 customer revenue, distracts from showcase |
| `nixtla-docs-qa-generator` | Removed from roadmap | Internal-only, $0 customer revenue |
| `nixtla-support-deflector` | Removed from roadmap | Internal-only, $0 customer revenue |

**Experimental status means**: the directory stays in the repo, but it gets a banner in its README, it's NOT listed in `.claude-plugin/marketplace.json`, NOT linked from the root README's flagship section, and explicitly tagged in `005-plugins/README.md` as "experimental — not for public install."

**Removed-from-roadmap status means**: the planned-plugins PRD gets archived under `000-docs/000a-planned-plugins/99-removed-from-roadmap/` with a one-line reason. The decision is durable; revisit only if a paying customer asks.

---

## What "globally elite" means concretely

Every Trinity plugin must hit each of these gates before v2.0 ships. This is the "no questions about what we're presenting to the world" bar.

| Dimension | Gate |
|---|---|
| **Install** | Fresh clone → `claude plugin install` → working in <5 minutes with zero hand-holding. |
| **Tests** | Per-plugin CI workflow gates merge. Pytest. ≥80% coverage. Tests run on push and PR. |
| **Security** | No SQL injection vectors. No plaintext secrets. Retry/timeout/circuit-breaker on every external call. Documented threat model. |
| **Docs** | README opens with a 30s pitch and a 5-minute quickstart. Setup guide for self-hosting. Troubleshooting section. Architecture overview. |
| **Demo** | Screencast (60–90s). Runnable `examples/` directory with sample inputs and expected outputs. Sample outputs committed to repo. |
| **Observability** | Structured logs. If it makes external API calls, surface cost/latency in the response. |
| **Versioning** | Semver-pinned. Plugin manifest version matches marketplace listing. Changelog entry per release. |
| **Audit harness** | Repo-wide `audit-harness` install passes. Coverage and CRAP gates green. |

---

## What this means for beads

**Closing**: F1 (`nixtla-48n` — already closed). F2 (`nixtla-788` — already closed). B1 (`nixtla-9vz` — closed, search-to-slack reclassified into The Trinity). B2 (`nixtla-o6p` — close, dbt-package moves to deferred). B3 (`nixtla-v6n` — close, streaming-monitor archived). C0 (`nixtla-xha` — close, replaced by this VISN doc). A4 (`nixtla-scv` embedded-widget — close, deferred to Y2). A5 (`nixtla-qtl` support-deflector — close, removed from roadmap). A6 (`nixtla-l25` docs-qa-generator — close, removed from roadmap).

**Keeping open and re-priming**: A1 (`nixtla-1ku` sales-demo-builder), A2 (`nixtla-4xx` workflow-templates), A3 (`nixtla-r5u` audit-report). These become the v3.0 expansion sequence. Per-plugin epics keep their existing 13-story templates per the original plan.

**New epic**: `Epic: v2.0 release — The Trinity hardened to globally-elite quality`. Three children, one per Trinity plugin, each carrying the v2.0 acceptance criteria as its definition of done. This is the most important epic in the repo until v2.0 ships.

**New epic**: `Epic: experimental tier demarcation`. Walks every Tier 4 plugin directory, adds the experimental banner to README, removes from any public listing, archives PRDs as appropriate. Single sweep.

**Re-priming D1 (`nixtla-q8j`)**: the pre-public-launch health audit becomes the v2.0 release gate, scoped to the Trinity only.

---

## What we're explicitly NOT deciding here

1. Whether the repo itself eventually splits — keeping plugins-nixtla as a meta-marketplace and spinning Trinity plugins into their own repos under `jeremylongshore/`. That is a future-decision worth revisiting once Trinity has shipped and we see how external contributors interact with it. For now: monorepo.
2. Whether to cut a `v2.0.0` release or follow the existing minor-version cadence. v2.0 is the simpler narrative ("we cut the sprawl, we shipped the showcase") and aligns with semver's signal of intentional breaking change (we are removing 11 plugin directories from the public marketplace presentation, even if they remain in-tree).
3. Pricing and licensing for Tier 2 revenue plugins. Their PRDs propose price points; final pricing is a separate decision after Trinity ships and we have customer conversations.
4. Whether to physically move Tier 4 directories to `99-experimental/`. That's a large-blast-radius restructure. Phase 1 is *demarcation* (banners, README, marketplace exclusion). Phase 2 is *physical move* once we're sure no external clones depend on the current paths.

---

## How we will remember why we did this

This document is the anchor. Every future change that proposes adding to the public marketplace, building a new plugin, or undoing the experimental demarcation must be reconciled against the four-tier structure here. If the change can't articulate which tier it lands in and why, the change isn't ready.

Specifically:
- New plugin idea? Default Tier 4 unless it hits the Tier 1/2/3 criteria explicitly.
- Existing Tier 4 plugin gets resurrected? Requires evidence of a paying customer ask, then promotion via this doc's amendment.
- Trinity plugin proposed for removal? Requires evidence of structural failure (security, abandonment, fundamental mis-fit). High bar.
- The "build all 14" instinct returns? Re-read the three-identities section. The drift will not stop on its own.

---

## Approval and execution

This vision is approved by Jeremy Longshore (owner, sole admin of `jeremylongshore/plugins-nixtla`). Execution begins immediately:

1. ~~v1.9.0 tagged~~ ✓ done (`efdc964`)
2. Strategic vision document filed (this file)
3. README rewrite reflecting the Trinity narrative + post-transfer URLs
4. `marketplace.json` owner update + transfer-aware source URLs
5. v1.9.0 GitHub Release published with proper notes (the tag exists; the public release artifact does not)
6. Beads re-decomposed against the four-tier structure
7. New v2.0 release epic created with Trinity hardening children
8. Experimental tier demarcation epic created
9. CHANGELOG `[Unreleased]` section updated with v2.0 plan

Items 2–9 land in this session. Items beyond that are tracked in beads.
