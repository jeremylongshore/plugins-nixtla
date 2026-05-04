# nixtla-support-deflector (v0.1.0-wip)

> **WORK IN PROGRESS** — This plugin is scaffolded for the v1.0 build (Epic 5.1).
> Tools currently emit illustrative outputs only. Every response carries a
> `_disclaimer` field flagging the WIP status. Do not use this in
> production until v1.0 ships.

Triage Nixtla support questions against the public docs + answer in-thread.

## Scope

Support automation. Watches an inbound queue (Slack / Zendesk / GitHub Discussions), classifies questions against the Nixtla docs corpus, and either auto-answers from canonical docs or escalates with context-rich handoff.

## Tools (WIP)

| Tool | Description |
|---|---|
| `classify_question` | [WIP] Tag an inbound question as docs / bug / feature-request / billing. |
| `answer_from_docs` | [WIP] Search the indexed Nixtla docs and emit an answer with cited sources. |
| `escalate_to_human` | [WIP] Emit a structured handoff payload for the on-call support engineer. |
| `learn_from_resolution` | [WIP] Record a resolved question's final answer for future retrieval. |

## What's real vs roadmap

| Layer | State |
|---|---|
| Plugin manifest + MCP server boot | Real (loads in Claude Code) |
| Tool surface (4 tools listed) | Real (registered, callable) |
| Tool *implementations* | **Stub** — illustrative outputs only, every response carries `_disclaimer` |
| Docs corpus indexing + RAG pipeline + Slack/Zendesk webhook | **Roadmap** — see Epic 5.1 for the v1.0 build |

## Production gap

Docs corpus indexing + RAG pipeline + Slack/Zendesk webhook adapters are still WIP. Current responses are illustrative.

## Honest labels in code

- `plugin.json` version is `0.1.0-wip` (not 0.1.0) so `claude plugin install` surfaces the WIP marker.
- Every tool description in `scripts/nixtla_support_deflector_mcp.py` is prefixed with `[WIP]`.
- Every tool response includes a `_disclaimer` field with the WIP notice.

## Roadmap to v1.0

Tracked as Epic 5.1 in beads. Closure criteria documented in
`000-docs/000a-planned-plugins/external-revenue/nixtla-support-deflector/02-PRD.md`.
