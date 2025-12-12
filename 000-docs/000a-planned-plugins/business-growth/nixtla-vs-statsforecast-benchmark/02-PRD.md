# Nixtla vs StatsForecast Benchmark - Product Requirements Document

**Plugin:** nixtla-vs-statsforecast-benchmark
**Version:** 0.1.0
**Status:** Specified
**Last Updated:** 2025-12-12

---

## Overview

Automated benchmarking tool that runs side-by-side comparisons between TimeGPT (API) and StatsForecast (OSS) on user's actual data. Generates comprehensive accuracy reports with sMAPE, MASE, and other metrics to help users choose the right tool for their use case.

---

## Problem Statement

Free tier trap:
> "Users start with free StatsForecast, get decent results, and never try TimeGPT because 'good enough' feels safe. They don't know TimeGPT might be 20% more accurate on their data."

This plugin provides evidence-based comparison to drive TimeGPT adoption.

---

## Goals

1. Run automated benchmarks comparing StatsForecast vs TimeGPT
2. Generate accuracy comparison reports (sMAPE, MASE, RMSE)
3. Identify use cases where TimeGPT significantly outperforms
4. Quantify the accuracy-cost trade-off
5. Provide data-driven recommendation

## Non-Goals

- Replace comprehensive model evaluation processes
- Guarantee accuracy improvements
- Compare against non-Nixtla libraries
- Provide production-ready model selection

---

## Target Users

| User | Need |
|------|------|
| Data scientists | Evidence-based model selection |
| ML engineers | Accuracy vs cost trade-off analysis |
| Technical evaluators | Vendor comparison data |
| Nixtla sales | Proof points for TimeGPT value |

---

## Functional Requirements

### FR-1: Data Ingestion
- Accept CSV/Parquet files in Nixtla format (unique_id, ds, y)
- Support multiple time series (grouped by unique_id)
- Auto-detect frequency (D, W, M, etc.)
- Handle missing values and data gaps

### FR-2: Benchmark Execution
- Run StatsForecast with multiple models (AutoARIMA, AutoETS, AutoTheta)
- Run TimeGPT with default parameters
- Use cross-validation for robust comparison
- Support configurable holdout periods

### FR-3: Metrics Calculation
- sMAPE (Symmetric Mean Absolute Percentage Error)
- MASE (Mean Absolute Scaled Error)
- RMSE (Root Mean Squared Error)
- Coverage (prediction interval accuracy)
- Execution time comparison

### FR-4: Report Generation
- Summary table with key metrics
- Per-series breakdown showing where each method wins
- Visual comparison charts (matplotlib/plotly)
- Markdown and HTML export options

### FR-5: MCP Server Tools
Expose 4 tools to Claude Code:
1. `run_benchmark` - Execute benchmark comparison
2. `get_metrics` - Retrieve accuracy metrics
3. `generate_report` - Create comparison report
4. `recommend_model` - Get data-driven recommendation

---

## Non-Functional Requirements

### NFR-1: Performance
- Benchmark 1,000 series in < 5 minutes
- StatsForecast runs locally (no API cost)
- TimeGPT uses batch API for efficiency

### NFR-2: Reproducibility
- Seed random states for consistent results
- Log all parameters and versions
- Export full results for audit

### NFR-3: Cost Awareness
- Display TimeGPT API cost during benchmark
- Estimate monthly cost at production scale
- Warn if benchmark exceeds budget threshold

---

## User Stories

### US-1: Model Selection
> "As a data scientist, I want to compare StatsForecast vs TimeGPT on my actual data so I can choose the best tool for my use case."

**Acceptance:**
- Run `/nixtla-benchmark data.csv`
- See accuracy comparison table
- Get clear recommendation based on results

### US-2: Cost-Accuracy Trade-off
> "As an ML engineer, I want to understand the accuracy improvement per dollar spent so I can justify the API cost to management."

**Acceptance:**
- See accuracy improvement percentage
- See cost per forecast
- Calculate ROI of switching to TimeGPT

### US-3: Documentation for Stakeholders
> "As a technical lead, I want a professional benchmark report so I can present findings to the team and leadership."

**Acceptance:**
- Generate HTML report with charts
- Include methodology documentation
- Export to PDF for presentations

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Benchmark execution time (1K series) | < 5 minutes |
| TimeGPT wins rate (on suitable data) | 60-80% |
| Report generation time | < 30 seconds |
| User conversion to TimeGPT (after benchmark) | 40%+ |

---

## Scope

### In Scope
- StatsForecast vs TimeGPT comparison
- Standard accuracy metrics (sMAPE, MASE, RMSE)
- Cross-validation methodology
- HTML/Markdown report generation
- Cost estimation

### Out of Scope
- Comparison with non-Nixtla libraries (Prophet, etc.)
- Fine-tuned TimeGPT comparisons
- Real-time streaming benchmarks
- GPU-accelerated StatsForecast

---

## API Keys Required

```bash
# Required
NIXTLA_API_KEY=nixak-...          # TimeGPT API access

# Optional
BENCHMARK_BUDGET_LIMIT=10.00      # Max API spend for benchmark
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  USER INTERFACE                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │/benchmark    │  │ Agent Skill  │  │  MCP Server     │  │
│  │              │  │ (Auto-invoke)│  │  (4 tools)      │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  BENCHMARK ENGINE (Python)                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - StatsForecast runner (local, free)               │  │
│  │  - TimeGPT runner (API calls)                        │  │
│  │  - Cross-validation framework                        │  │
│  │  - Metrics calculator                                │  │
│  │  - Report generator                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │  Metrics    │  │  Charts     │  │  HTML/PDF        │   │
│  │  CSV        │  │  PNG/HTML   │  │  Report          │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## References

- **Full Specification:** `000-docs/000b-archive-001-096/010-AT-ARCH-plugin-02-nixtla-vs-statsforecast-benchmark.md`
- **Category:** Business Growth
- **Priority:** Tier 1 (Free Tier Conversion)
