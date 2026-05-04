# nixtla-forecast-workflow-templates (v0.1.0-wip)

> **WORK IN PROGRESS** — This plugin is scaffolded for the v1.0 build (Epic 4.2).
> Tools currently emit illustrative outputs only. Every response carries a
> `_disclaimer` field flagging the WIP status. Do not use this in
> production until v1.0 ships.

Curated TimeGPT forecasting workflow templates for retail, finance, energy, ops.

## Scope

Library of opinionated forecasting workflow templates — retail demand, financial-revenue, energy-load, ops-capacity. Each template includes data validation, train/test split, NixtlaClient call shape, and result-export hooks.

## Tools (WIP)

| Tool | Description |
|---|---|
| `list_templates` | [WIP] Return the catalog of available workflow templates by industry. |
| `get_template` | [WIP] Fetch a single template's full source by id. |
| `instantiate_template` | [WIP] Generate a customized template with the user's column schema. |
| `validate_template_inputs` | [WIP] Lint a user's data against a template's expected schema. |

## What's real vs roadmap

| Layer | State |
|---|---|
| Plugin manifest + MCP server boot | Real (loads in Claude Code) |
| Tool surface (4 tools listed) | Real (registered, callable) |
| Tool *implementations* | **Stub** — illustrative outputs only, every response carries `_disclaimer` |
| Template catalog is currently 4 illustrative templates | **Roadmap** — see Epic 4.2 for the v1.0 build |

## Production gap

Template catalog is currently 4 illustrative templates. Real industry-domain expert review + tested outputs against real-world datasets are still WIP.

## Honest labels in code

- `plugin.json` version is `0.1.0-wip` (not 0.1.0) so `claude plugin install` surfaces the WIP marker.
- Every tool description in `scripts/nixtla_forecast_workflow_templates_mcp.py` is prefixed with `[WIP]`.
- Every tool response includes a `_disclaimer` field with the WIP notice.

## Roadmap to v1.0

Tracked as Epic 4.2 in beads. Closure criteria documented in
`000-docs/000a-planned-plugins/external-revenue/nixtla-forecast-workflow-templates/02-PRD.md`.
