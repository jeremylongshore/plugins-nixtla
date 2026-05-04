# nixtla-embedded-forecast-widget (v0.1.0-wip)

> **WORK IN PROGRESS** — This plugin is scaffolded for the v1.0 build (Epic 5.3).
> Tools currently emit illustrative outputs only. Every response carries a
> `_disclaimer` field flagging the WIP status. Do not use this in
> production until v1.0 ships.

Embeddable JS widget that renders a TimeGPT forecast inline in any web page.

## Scope

Browser-side widget for embedding TimeGPT forecasts in customer-facing pages. Ships as a small JS bundle that calls a thin proxy backend (to keep the API key server-side) and renders the forecast + uncertainty band via a Canvas chart.

## Tools (WIP)

| Tool | Description |
|---|---|
| `generate_widget_html` | [WIP] Produce the <script>+<div> snippet for embedding. |
| `scaffold_proxy_backend` | [WIP] Emit a Cloud Run / Cloud Functions backend that hides the TimeGPT API key. |
| `preview_forecast` | [WIP] Render a static SVG preview of the forecast for design review. |
| `export_widget_bundle` | [WIP] Emit a versioned JS bundle for CDN deploy. |

## What's real vs roadmap

| Layer | State |
|---|---|
| Plugin manifest + MCP server boot | Real (loads in Claude Code) |
| Tool surface (4 tools listed) | Real (registered, callable) |
| Tool *implementations* | **Stub** — illustrative outputs only, every response carries `_disclaimer` |
| Widget renderer is stub HTML — production requires a real Ca | **Roadmap** — see Epic 5.3 for the v1.0 build |

## Production gap

Widget renderer is stub HTML — production requires a real Canvas / D3 chart, server-side rate limiting on the proxy, and a tested CDN deploy pipeline. This is the Y2 flagship; expect 10-12 weeks to v1.0.

## Honest labels in code

- `plugin.json` version is `0.1.0-wip` (not 0.1.0) so `claude plugin install` surfaces the WIP marker.
- Every tool description in `scripts/nixtla_embedded_forecast_widget_mcp.py` is prefixed with `[WIP]`.
- Every tool response includes a `_disclaimer` field with the WIP notice.

## Roadmap to v1.0

Tracked as Epic 5.3 in beads. Closure criteria documented in
`000-docs/000a-planned-plugins/external-revenue/nixtla-embedded-forecast-widget/02-PRD.md`.
