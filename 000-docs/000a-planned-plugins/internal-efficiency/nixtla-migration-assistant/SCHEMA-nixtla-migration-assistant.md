# Schema: nixtla-migration-assistant

**Generated:** 2025-12-12
**Plugin Version:** 0.1.0
**Status:** Planned (Internal Efficiency)

---

## Directory Tree (Planned)

```
nixtla-migration-assistant/
├── .claude-plugin/
│   └── plugin.json                # Plugin manifest (Anthropic spec)
├── .mcp.json                      # MCP server configuration
├── commands/
│   ├── nixtla-migrate.md          # Slash command: Run migration
│   └── nixtla-migrate-analyze.md  # Slash command: Analysis only
├── scripts/
│   ├── migration_mcp.py           # MCP server (5 tools exposed)
│   ├── code_analyzer.py           # AST-based code parsing
│   ├── pattern_detector.py        # Library detection (Prophet, statsmodels)
│   ├── data_transformer.py        # Format conversion to Nixtla
│   ├── code_generator.py          # Nixtla code generation
│   ├── accuracy_comparator.py     # Side-by-side accuracy test
│   └── requirements.txt           # Python dependencies
├── templates/
│   ├── prophet_to_timegpt.py      # Prophet → TimeGPT template
│   ├── statsmodels_to_sf.py       # statsmodels → StatsForecast template
│   └── sklearn_to_nixtla.py       # sklearn → Nixtla template
├── tests/
│   ├── test_prophet_migration.py
│   └── test_statsmodels_migration.py
├── QUICKSTART.md                  # Quick start guide
└── README.md                      # Full documentation
```

---

## Plugin Manifest (Planned plugin.json)

| Field | Value | Status |
|-------|-------|--------|
| name | nixtla-migration-assistant | Required |
| description | Automated migration from legacy forecasting code... | Required |
| version | 0.1.0 | Required |
| author.name | Intent Solutions | Required |

---

## MCP Tools (5 planned)

| Tool Name | Purpose |
|-----------|---------|
| analyze_code | Parse and detect forecasting patterns |
| generate_plan | Create migration plan with estimates |
| transform_data | Convert data to Nixtla format |
| generate_code | Generate equivalent Nixtla code |
| compare_accuracy | Run side-by-side accuracy test |

---

## Slash Commands (2 planned)

| Command | Purpose |
|---------|---------|
| /nixtla-migrate | Full migration workflow |
| /nixtla-migrate --analyze-only | Analysis and planning only |

---

## Migration Patterns Supported

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

## Migration Phases

| Phase | Description |
|-------|-------------|
| Phase 1: Code Analysis | Parse AST, detect library usage |
| Phase 2: Data Transformation | Convert to Nixtla format (unique_id, ds, y) |
| Phase 3: Code Generation | Generate equivalent Nixtla code |
| Phase 4: Accuracy Comparison | Run both models, compare metrics |

---

## Example Output

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

## Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Code analysis | <60 seconds per file |
| Data transformation | 10,000 rows/second |
| Comparison run | <5 minutes |
| Code generation accuracy | 95%+ |
| Migration time reduction | 80-90% |

---

## Safety Requirements

| Requirement | Implementation |
|-------------|----------------|
| Never modify original code | Read-only analysis |
| Create backup before changes | Automatic backup |
| Dry-run mode by default | --execute flag required |
| Rollback strategy | Documented in every plan |

---

## CSV Inventory Reference

From `plugins_inventory.csv`:

- **Who:** Organizations migrating from other tools
- **What:** Guided migration from legacy forecasting systems to TimeGPT
- **When:** Simplify conversion process
- **Target Goal:** Convert Prophet/SARIMA code to TimeGPT equivalent
- **Production:** false (planned-internal-efficiency)
