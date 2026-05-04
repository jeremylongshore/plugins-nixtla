# nixtla-sales-demo-builder (v0.1.0-wip)

> **WORK IN PROGRESS** — This plugin is scaffolded for the v1.0 build (Epic 4.1).
> Tools currently emit illustrative outputs only. Every response carries a
> `_disclaimer` field flagging the WIP status. Do not use this in
> production until v1.0 ships.

Generate enterprise-ready Nixtla TimeGPT sales demos from a customer's data shape.

## Scope

Sales engineering tool. Takes a description of a customer's industry / data structure / forecasting goal and assembles a runnable TimeGPT demo (synthetic data + script + slides outline) that the AE can walk through in a 30-minute call.

## Tools (WIP)

| Tool | Description |
|---|---|
| `scaffold_demo` | [WIP] Build a TimeGPT demo project for the given industry + data shape. |
| `generate_synthetic_data` | [WIP] Emit a CSV that matches the customer's described schema. |
| `write_demo_script` | [WIP] Produce a runnable Python script that calls NixtlaClient.forecast() against the synthetic data. |
| `draft_slide_outline` | [WIP] Write a 5-7 slide outline narrating the demo for a 30-minute pitch. |

## What's real vs roadmap

| Layer | State |
|---|---|
| Plugin manifest + MCP server boot | Real (loads in Claude Code) |
| Tool surface (4 tools listed) | Real (registered, callable) |
| Tool *implementations* | **Stub** — illustrative outputs only, every response carries `_disclaimer` |
| Real TimeGPT API access + real customer-data schemas + slide | **Roadmap** — see Epic 4.1 for the v1.0 build |

## Production gap

Real TimeGPT API access + real customer-data schemas + slide-deck rendering library are still scaffolding. The current emit is illustrative.

## Honest labels in code

- `plugin.json` version is `0.1.0-wip` (not 0.1.0) so `claude plugin install` surfaces the WIP marker.
- Every tool description in `scripts/nixtla_sales_demo_builder_mcp.py` is prefixed with `[WIP]`.
- Every tool response includes a `_disclaimer` field with the WIP notice.

## Roadmap to v1.0

Tracked as Epic 4.1 in beads. Closure criteria documented in
`000-docs/000a-planned-plugins/external-revenue/nixtla-sales-demo-builder/02-PRD.md`.
