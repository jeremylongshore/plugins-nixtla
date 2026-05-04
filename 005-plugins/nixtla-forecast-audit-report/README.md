# nixtla-forecast-audit-report (v0.1.0-wip)

> **WORK IN PROGRESS** — This plugin is scaffolded for the v1.0 build (Epic 4.3).
> Tools currently emit illustrative outputs only. Every response carries a
> `_disclaimer` field flagging the WIP status. Do not use this in
> production until v1.0 ships.

Generate an audit-grade report from a TimeGPT forecast for compliance + governance review.

## Scope

Audit reporting tool for forecasting workflows under regulatory scrutiny (SOX / Basel / model-risk). Takes a TimeGPT forecast run + its inputs and emits a markdown report covering inputs, model card, residual diagnostics, calibration, and reproducibility checklist.

## Tools (WIP)

| Tool | Description |
|---|---|
| `ingest_forecast_run` | [WIP] Load a TimeGPT forecast manifest + outputs into the audit context. |
| `generate_audit_report` | [WIP] Emit the full audit-grade markdown report. |
| `compute_residual_diagnostics` | [WIP] Calculate Ljung-Box, Jarque-Bera, and ACF on residuals. |
| `export_model_card` | [WIP] Generate a TimeGPT model-card section conforming to Google's Model Cards spec. |

## What's real vs roadmap

| Layer | State |
|---|---|
| Plugin manifest + MCP server boot | Real (loads in Claude Code) |
| Tool surface (4 tools listed) | Real (registered, callable) |
| Tool *implementations* | **Stub** — illustrative outputs only, every response carries `_disclaimer` |
| Residual diagnostics are stub calculations | **Roadmap** — see Epic 4.3 for the v1.0 build |

## Production gap

Residual diagnostics are stub calculations. Real audit-grade output requires statsmodels integration + reviewed model-card schemas + signed reproducibility hashes.

## Honest labels in code

- `plugin.json` version is `0.1.0-wip` (not 0.1.0) so `claude plugin install` surfaces the WIP marker.
- Every tool description in `scripts/nixtla_forecast_audit_report_mcp.py` is prefixed with `[WIP]`.
- Every tool response includes a `_disclaimer` field with the WIP notice.

## Roadmap to v1.0

Tracked as Epic 4.3 in beads. Closure criteria documented in
`000-docs/000a-planned-plugins/external-revenue/nixtla-forecast-audit-report/02-PRD.md`.
