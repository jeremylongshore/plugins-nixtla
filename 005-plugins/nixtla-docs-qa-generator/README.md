# nixtla-docs-qa-generator (v0.1.0-wip)

> **WORK IN PROGRESS** — This plugin is scaffolded for the v1.0 build (Epic 5.2).
> Tools currently emit illustrative outputs only. Every response carries a
> `_disclaimer` field flagging the WIP status. Do not use this in
> production until v1.0 ships.

Auto-generate Q&A pairs from the Nixtla docs corpus for support training and FAQ pages.

## Scope

Docs ingestion -> Q&A generator. Crawls the Nixtla docs site, extracts canonical sections, and produces high-quality Q&A pairs for use in support training, FAQ pages, and search-index seed data.

## Tools (WIP)

| Tool | Description |
|---|---|
| `crawl_docs` | [WIP] Walk the Nixtla docs sitemap and pull canonical content. |
| `extract_qa_pairs` | [WIP] Generate Q&A pairs from a crawled section. |
| `dedupe_qa_pairs` | [WIP] Collapse near-duplicate questions into a single canonical entry. |
| `export_faq_html` | [WIP] Emit the Q&A set as embeddable FAQ HTML. |

## What's real vs roadmap

| Layer | State |
|---|---|
| Plugin manifest + MCP server boot | Real (loads in Claude Code) |
| Tool surface (4 tools listed) | Real (registered, callable) |
| Tool *implementations* | **Stub** — illustrative outputs only, every response carries `_disclaimer` |
| Crawler respects robots | **Roadmap** — see Epic 5.2 for the v1.0 build |

## Production gap

Crawler respects robots.txt but the QA-generation step uses heuristic extraction, not LLM-grade rewriting. Output quality is rough draft-tier until the pipeline lands.

## Honest labels in code

- `plugin.json` version is `0.1.0-wip` (not 0.1.0) so `claude plugin install` surfaces the WIP marker.
- Every tool description in `scripts/nixtla_docs_qa_generator_mcp.py` is prefixed with `[WIP]`.
- Every tool response includes a `_disclaimer` field with the WIP notice.

## Roadmap to v1.0

Tracked as Epic 5.2 in beads. Closure criteria documented in
`000-docs/000a-planned-plugins/external-revenue/nixtla-docs-qa-generator/02-PRD.md`.
