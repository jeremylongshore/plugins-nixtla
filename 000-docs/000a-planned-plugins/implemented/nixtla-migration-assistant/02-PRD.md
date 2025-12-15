# Migration Assistant - Product Requirements Document

**Plugin:** nixtla-migration-assistant
**Version:** 0.1.0
**Status:** Specified
**Last Updated:** 2025-12-12

---

## Overview

Automated migration tool that converts existing forecasting code (pandas/scikit-learn/Prophet/statsmodels) to Nixtla's TimeGPT or StatsForecast. Generates migration plans, transforms data pipelines, and provides accuracy comparison to prove migration value.

---

## Problem Statement

Integration tax friction:
> "Users see how easy the TimeGPT demo is, but panic when they realize they need to integrate with 50,000 lines of existing forecasting infrastructure. Migration feels like a 6-month project."

This plugin reduces migration from weeks to hours.

---

## Goals

1. Analyze existing forecasting code and identify migration patterns
2. Generate migration plan with effort estimates
3. Transform data from legacy formats to Nixtla format
4. Provide side-by-side accuracy comparison
5. Generate drop-in replacement code

## Non-Goals

- Migrate non-forecasting ML code
- Support custom deep learning models
- Provide production deployment automation
- Handle infrastructure migration (just code)

---

## Target Users

| User | Need |
|------|------|
| Data scientists | Quick migration of existing models |
| ML engineers | Integration with existing pipelines |
| Technical leads | Migration effort estimation |
| Architects | Compatibility assessment |

---

## Functional Requirements

### FR-1: Code Analysis
- Parse existing Python forecasting code
- Detect library usage (Prophet, statsmodels, sklearn, pandas)
- Identify data pipeline patterns
- Estimate migration complexity (Low/Med/High)

### FR-2: Data Transformation
- Convert dataframes to Nixtla format (unique_id, ds, y)
- Handle various datetime formats
- Support wide-to-long format conversion
- Validate data quality pre-migration

### FR-3: Code Generation
- Generate equivalent Nixtla code
- Preserve existing function signatures
- Create adapter classes for legacy APIs
- Include error handling and logging

### FR-4: Accuracy Comparison
- Run original model vs Nixtla model
- Calculate accuracy metrics (sMAPE, MASE, RMSE)
- Generate comparison report
- Highlight accuracy improvements

### FR-5: Migration Report
- Document all code changes required
- Estimate effort in developer-hours
- Identify risk areas
- Provide rollback strategy

---

## Non-Functional Requirements

### NFR-1: Performance
- Code analysis: < 60 seconds per file
- Data transformation: 10,000 rows/second
- Comparison run: < 5 minutes

### NFR-2: Compatibility
- Python 3.8+ source code
- Support async code patterns
- Handle Jupyter notebooks

### NFR-3: Safety
- Never modify original code without approval
- Create backup before changes
- Dry-run mode by default

---

## User Stories

### US-1: Prophet Migration
> "As a data scientist, I want to migrate 20 Prophet models to TimeGPT so I can improve accuracy and reduce infrastructure costs."

**Acceptance:**
- Run `/nixtla-migrate --source prophet_models/`
- Get migration plan with effort estimate
- Execute migration with single command
- Verify accuracy improvement

### US-2: Pandas Pipeline Migration
> "As an ML engineer, I want to convert our custom pandas forecasting code to StatsForecast so we can use maintained libraries."

**Acceptance:**
- Analyze existing pandas code
- Identify forecasting patterns
- Generate equivalent StatsForecast code
- Test with existing data

### US-3: Migration Effort Estimation
> "As a technical lead, I want to estimate migration effort before committing resources so I can plan the project timeline."

**Acceptance:**
- Run `/nixtla-migrate --analyze-only`
- Get complexity rating per component
- See estimated hours per migration
- Identify high-risk areas

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Migration time reduction | 80-90% |
| Accuracy improvement (vs original) | 10-30% typical |
| Code generation accuracy | 95%+ |
| User satisfaction | 4.5+/5.0 |

---

## Scope

### In Scope
- Prophet migrations
- statsmodels migrations
- scikit-learn time series migrations
- pandas rolling/expanding window forecasts
- Data format transformations
- Accuracy comparison reports

### Out of Scope
- Custom deep learning models (PyTorch, TensorFlow)
- Non-Python code (R, MATLAB)
- Infrastructure migration
- Production deployment automation

---

## Supported Migration Patterns

| Source | Target | Support Level |
|--------|--------|---------------|
| Prophet | TimeGPT | Full |
| Prophet | StatsForecast | Full |
| statsmodels.tsa.arima | StatsForecast | Full |
| statsmodels.tsa.exponential_smoothing | StatsForecast | Full |
| sklearn time series | StatsForecast | Partial |
| pandas rolling | StatsForecast | Partial |
| Custom Python | TimeGPT | Analysis only |

---

## API Keys Required

```bash
# Required for TimeGPT comparison
NIXTLA_API_KEY=nixak-...

# Optional
MIGRATION_BACKUP_DIR=/path/to/backups
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  EXISTING CODE                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  from prophet import Prophet                          │  │
│  │  model = Prophet()                                    │  │
│  │  model.fit(df)                                        │  │
│  │  forecast = model.predict(future_df)                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  MIGRATION ASSISTANT                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Phase 1: Code Analysis                              │  │
│  │  - Parse AST, detect patterns                        │  │
│  │  - Identify library calls                            │  │
│  │                                                        │  │
│  │  Phase 2: Data Transformation                        │  │
│  │  - Convert to Nixtla format                          │  │
│  │  - Validate data quality                              │  │
│  │                                                        │  │
│  │  Phase 3: Code Generation                            │  │
│  │  - Generate equivalent Nixtla code                   │  │
│  │  - Preserve function signatures                       │  │
│  │                                                        │  │
│  │  Phase 4: Accuracy Comparison                        │  │
│  │  - Run both models                                    │  │
│  │  - Compare metrics                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  MIGRATED CODE                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  from nixtla import NixtlaClient                     │  │
│  │  client = NixtlaClient()                             │  │
│  │  forecast = client.forecast(df, h=30, freq='D')     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Example Migration Output

```
Migration Analysis Report
========================

Source: prophet_models/demand_forecast.py
Library: Prophet 1.1.5
Complexity: Medium

Detected Patterns:
- Prophet model with custom seasonality
- Holiday effects (US holidays)
- Regressor variables (2 external variables)

Migration Plan:
1. Convert dataframe format (30 min)
2. Replace Prophet with TimeGPT (15 min)
3. Handle holiday effects via TimeGPT (15 min)
4. Convert regressors to exogenous variables (45 min)

Total Estimated Effort: 1.75 hours

Accuracy Comparison:
| Metric | Prophet | TimeGPT | Change |
|--------|---------|---------|--------|
| sMAPE  | 8.2%    | 6.1%    | -25.6% |
| MASE   | 0.92    | 0.71    | -22.8% |
| RMSE   | 145.3   | 112.8   | -22.4% |

Recommendation: MIGRATE (significant accuracy improvement)
```

---

## References

- **Full Specification:** `000-docs/000b-archive-001-096/016-AT-ARCH-plugin-08-nixtla-migration-assistant.md`
- **Category:** Internal Efficiency
- **Priority:** Tier 1 (Onboarding Acceleration)
