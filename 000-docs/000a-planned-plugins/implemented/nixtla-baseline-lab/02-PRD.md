# Baseline Lab - Product Requirements Document

**Plugin:** nixtla-baseline-lab
**Version:** 0.8.0
**Status:** Implemented
**Last Updated:** 2025-12-12

---

## Overview

Statistical forecasting benchmark plugin for Claude Code. Runs AutoETS, AutoTheta, and SeasonalNaive models on M4 competition data and returns sMAPE and MASE metrics.

---

## Goals

1. Run statistical baselines on M4 benchmark data
2. Calculate industry-standard metrics (sMAPE, MASE)
3. Generate reproducible benchmark reports
4. Integrate with Claude Code via MCP server

## Non-Goals

- Not a replacement for TimeGPT
- Not for production forecasting workloads
- Not for real-time predictions

---

## Functional Requirements

### FR-1: Model Execution
- Run AutoETS, AutoTheta, SeasonalNaive on time series data
- Support configurable forecast horizon
- Accept M4 data or custom CSV input

### FR-2: Metric Calculation
- Calculate sMAPE (Symmetric Mean Absolute Percentage Error)
- Calculate MASE (Mean Absolute Scaled Error)
- Report per-series and aggregated metrics

### FR-3: Report Generation
- Generate markdown benchmark reports
- Include model comparison tables
- Support GitHub issue draft generation

### FR-4: Claude Code Integration
- Expose MCP server with 4 tools
- Support slash commands (`/nixtla-baseline-m4`)
- Provide skill for result interpretation

---

## Non-Functional Requirements

### NFR-1: Performance
- Smoke test completes in <90 seconds
- Handles 4,000+ series (M4 Daily) without memory issues

### NFR-2: Dependencies
- No API keys required (uses open-source statsforecast)
- Python 3.10+ required
- ~2GB RAM recommended

### NFR-3: Testing
- Golden task smoke test validates expected output
- CI/CD pipeline validates on push

---

## User Stories

### US-1: Data Scientist
> "As a data scientist, I want to quickly establish baseline accuracy on M4 data so I can compare against TimeGPT."

**Acceptance:** Run `/nixtla-baseline-m4 demo_preset=m4_daily_small` and receive sMAPE/MASE metrics.

### US-2: ML Engineer
> "As an ML engineer, I want reproducible benchmark results so I can validate model improvements."

**Acceptance:** Same inputs always produce identical metrics (deterministic).

---

## Scope

### In Scope
- M4 Daily, Hourly, Monthly, Weekly datasets
- AutoETS, AutoTheta, SeasonalNaive models
- sMAPE and MASE metrics
- Markdown report generation

### Out of Scope
- TimeGPT comparison (requires API key)
- Custom model support
- Real-time forecasting
- Production deployment patterns
