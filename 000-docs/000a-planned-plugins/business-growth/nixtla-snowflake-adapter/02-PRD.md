# Snowflake Native Adapter - Product Requirements Document

**Plugin:** nixtla-snowflake-adapter
**Version:** 0.1.0
**Status:** Specified
**Last Updated:** 2025-12-12

---

## Overview

Claude Code plugin that wraps Nixtla's existing Snowflake Native App integration, providing one-command SQL-native forecasting with automatic setup, error handling, and result formatting. Enables SQL analysts to use TimeGPT without writing Python.

---

## Problem Statement

Integration tax friction:
> "Marketing copy attacks Python infrastructure requirements. This plugin makes the native Snowflake integration discoverable and easy to use from Claude Code."

This plugin is a wrapper/helper for the existing Nixtla Snowflake integration.

---

## Goals

1. Simplify Snowflake Native App usage via Claude Code
2. Generate correct SQL for CALL NIXTLA_FORECAST(...)
3. Validate Snowflake connections and permissions
4. Format results for BI tools (Looker, Tableau)
5. Provide clear error messages and troubleshooting

## Non-Goals

- Replace the Nixtla Snowflake Native App
- Handle non-Snowflake data warehouses
- Provide Python-based forecasting
- Manage Snowflake infrastructure

---

## Target Users

| User | Need |
|------|------|
| SQL analysts | Forecasting without Python |
| BI developers | Forecasts for dashboards |
| Data teams | Snowflake-native forecasting |
| Snowflake admins | Easy TimeGPT setup |

---

## Functional Requirements

### FR-1: Connection Validation
- Test Snowflake connection credentials
- Verify Nixtla Native App installation
- Check user permissions for forecasting
- Provide setup instructions if not installed

### FR-2: SQL Generation
- Generate CALL NIXTLA_FORECAST(...) SQL
- Support all forecast parameters (horizon, freq, level)
- Handle grouped forecasting (by product, region, etc.)
- Generate anomaly detection SQL

### FR-3: Result Formatting
- Parse forecast results into readable format
- Generate SQL for querying forecast tables
- Export to CSV/Parquet for BI tools
- Create Looker/Tableau-ready views

### FR-4: Error Handling
- Parse Snowflake error messages
- Provide actionable troubleshooting steps
- Suggest permission fixes
- Validate data format before forecasting

---

## Non-Functional Requirements

### NFR-1: Simplicity
- Pure Python helpers (no MCP server)
- No additional infrastructure required
- Works with existing Snowflake setup

### NFR-2: Compatibility
- Snowflake connector 3.0+
- Python 3.10+
- All Snowflake editions (Standard, Enterprise)

### NFR-3: Security
- Credentials via environment variables only
- No credential logging
- Support Snowflake key-pair authentication

---

## User Stories

### US-1: SQL Analyst Uses Forecasting
> "As a SQL analyst, I want to generate forecasts in Snowflake so I can add them to my Looker dashboard without learning Python."

**Acceptance:**
- Run `/nixtla-snowflake-forecast --table SALES`
- Get SQL to copy-paste into Snowflake
- Query results in Looker SQL Runner

### US-2: Setup Validation
> "As a Snowflake admin, I want to verify the Nixtla Native App is correctly installed so my team can start forecasting."

**Acceptance:**
- Run `/nixtla-snowflake-setup`
- See installation status
- Get fix instructions if needed

### US-3: Grouped Forecasting
> "As a data analyst, I want to forecast sales by region so I can create regional performance dashboards."

**Acceptance:**
- Specify GROUP_BY_COL in command
- Get per-region forecasts
- Results grouped in output table

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Time to first forecast | < 10 minutes |
| SQL generation accuracy | 100% |
| Setup validation success | 99%+ |
| User adoption (Snowflake customers) | 30%+ |

---

## Scope

### In Scope
- Snowflake connection validation
- SQL generation for Nixtla Native App
- Result formatting and export
- Error handling and troubleshooting

### Out of Scope
- Nixtla Native App installation (done by admin)
- Snowflake infrastructure management
- Non-Snowflake data warehouses
- Custom model training

---

## API Keys Required

```bash
# Snowflake connection
SNOWFLAKE_ACCOUNT=myorg.snowflakecomputing.com
SNOWFLAKE_USER=analytics_user
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ANALYTICS
SNOWFLAKE_SCHEMA=FORECASTS

# Nixtla Snowflake app must be installed (done once by admin)
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  CLAUDE CODE INTERFACE                                      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │Slash Command │  │ Agent Skill  │                        │
│  │/snowflake    │  │(Auto-invoke) │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  PLUGIN HELPERS (Python)                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - SQL generator (CALL NIXTLA_FORECAST(...))        │  │
│  │  - Connection validator                              │  │
│  │  - Error parser                                      │  │
│  │  - Result formatter                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  SNOWFLAKE NATIVE APP (Existing Nixtla Integration)        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Nixtla functions available in Snowflake:            │  │
│  │  - CALL NIXTLA_FORECAST(...)                         │  │
│  │  - CALL NIXTLA_DETECT_ANOMALIES(...)                │  │
│  │  - CALL NIXTLA_CROSS_VALIDATE(...)                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Example Usage

```python
# User runs slash command
/nixtla-snowflake-forecast --table SALES_HISTORY --horizon 30

# Claude generates SQL:
"""
-- Generated Nixtla Snowflake forecast SQL
CALL NIXTLA.FORECAST(
    INPUT_TABLE => 'SALES_HISTORY',
    TIMESTAMP_COL => 'DATE',
    VALUE_COL => 'REVENUE',
    GROUP_BY_COL => 'PRODUCT_ID',
    HORIZON => 30,
    FREQUENCY => 'D',
    LEVEL => ARRAY_CONSTRUCT(80, 90, 95)
);

-- View results
SELECT * FROM NIXTLA.FORECAST_RESULTS
WHERE FORECAST_DATE > CURRENT_DATE
ORDER BY PRODUCT_ID, FORECAST_DATE;
"""
```

---

## References

- **Full Specification:** `000-docs/000b-archive-001-096/014-AT-ARCH-plugin-06-nixtla-snowflake-adapter.md`
- **Category:** Business Growth
- **Priority:** Tier 2 (Integration Win)
