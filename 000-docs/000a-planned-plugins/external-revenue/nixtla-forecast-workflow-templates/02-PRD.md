# Forecast Workflow Templates - Product Requirements Document

**Plugin:** nixtla-forecast-workflow-templates
**Version:** 0.1.0
**Status:** Planned
**Last Updated:** 2025-12-15

---

## Overview

A marketplace of pre-built forecasting workflow templates that users purchase. Each template includes data connectors, forecasting logic, output formatting, and integration patterns for specific use cases like demand planning, capacity planning, or financial forecasting.

---

## Problem Statement

Most TimeGPT users go from API call to... nothing. They don't know how to operationalize forecasts into business workflows. This results in churn after trial periods. Users need structured paths from "cool demo" to "production value."

---

## Goals

1. Create 10+ workflow templates for common forecasting use cases
2. One-click deployment with guided setup
3. Claude skill for adapting template to user's specific data schema
4. Push forecasts to Excel, Google Sheets, databases, or dashboards
5. Built-in scheduling for recurring forecast runs

## Non-Goals

- Build a full workflow orchestration platform
- Compete with Airflow/Prefect
- Handle non-forecasting workflows

---

## Target Users

| User | Need |
|------|------|
| Data engineers | Production-ready pipelines |
| Business analysts | Operational workflows |
| FinOps teams | Financial forecasting |
| Operations managers | Demand/capacity planning |

---

## Functional Requirements

### FR-1: Template Library
- 10+ workflow templates covering common use cases
- Categorized by vertical and use case
- Searchable and filterable
- Preview before purchase

### FR-2: One-Click Deploy
- Install template into user's environment
- Guided setup wizard
- Environment variable configuration
- Dependency installation

### FR-3: Customization Layer
- Claude skill for adapting to user's data schema
- Column mapping interface
- Parameter configuration
- Custom business logic hooks

### FR-4: Output Integrations
- Excel export (xlsx)
- Google Sheets sync
- Database write (PostgreSQL, MySQL, BigQuery)
- Dashboard integration (Tableau, PowerBI)
- Slack/email notifications

### FR-5: Scheduling
- Cron-based scheduling
- Event-triggered runs
- Manual trigger option
- Run history and logs

### FR-6: MCP Server Tools
Expose 6 tools to Claude Code:
1. `list_templates` - Browse available templates
2. `preview_template` - View template details
3. `install_template` - Deploy template to environment
4. `configure_template` - Set up data sources and outputs
5. `run_template` - Execute workflow
6. `schedule_template` - Set up recurring runs

---

## Template Examples

### Retail Demand Planning
- **Input**: SKU sales history (CSV, database, or API)
- **Process**: TimeGPT forecast → inventory recommendations
- **Output**: PO suggestions → Excel or ERP system
- **Price**: $299

### SaaS Revenue Forecasting
- **Input**: MRR/ARR history, cohort data
- **Process**: Revenue predictions → cohort analysis
- **Output**: Board deck exports, Sheets sync
- **Price**: $199

### Energy Load Forecasting
- **Input**: Historical load data, weather API
- **Process**: Load predictions with exogenous variables
- **Output**: Peak shaving alerts, cost optimization report
- **Price**: $399

### Healthcare Capacity
- **Input**: Patient volume history
- **Process**: Volume forecasts → staffing recommendations
- **Output**: Resource allocation report, shift scheduling
- **Price**: $249

---

## Non-Functional Requirements

### NFR-1: Performance
- Template installation: <2 minutes
- Workflow execution: Scales with data size
- Scheduling: <1 minute latency

### NFR-2: Security
- API keys stored securely
- No data leaves user's environment
- Audit logging for all runs

### NFR-3: Reliability
- Retry logic for failed runs
- Error notifications
- Rollback capability

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Template purchases (Y1) | 100+ |
| API consumption increase | 3x for template users |
| Churn reduction | 40% |
| Template satisfaction | 4.5/5 stars |

---

## Pricing Model

| Tier | Price | Features |
|------|-------|----------|
| Individual Template | $99-499 | Single use case |
| Bundle (5 templates) | $499 | Choose any 5 |
| Enterprise Package | $999 | All templates + support |

---

## Scope

### In Scope
- 10 workflow templates
- Installation and configuration
- Scheduling and execution
- Output integrations
- Basic support

### Out of Scope
- Custom template development
- On-premise deployment support
- Real-time streaming workflows
- Non-TimeGPT forecasting

---

## Estimated Effort

6 weeks for marketplace infrastructure + 3 templates. Additional 2 weeks per template.

---

## Revenue Impact

Direct. Template sales + increased API consumption.
- Template revenue: $30-50K Y1
- API uplift: $20-50K Y1
- **Total projected**: $50-100K ARR
