# Forecast Workflow Templates - Architecture

**Plugin:** nixtla-forecast-workflow-templates
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TEMPLATE MARKETPLACE                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Template     │  │ Purchase     │  │ License         │   │
│  │ Catalog      │  │ Flow         │  │ Management      │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  DEPLOYMENT ENGINE                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Template Installer                                  │   │
│  │  - Clone template structure                          │   │
│  │  - Install dependencies                              │   │
│  │  - Configure environment                             │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Setup Wizard                                        │   │
│  │  - Data source configuration                         │   │
│  │  - Output destination setup                          │   │
│  │  - Schedule configuration                            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  WORKFLOW RUNTIME                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Data         │  │ Forecast     │  │ Output          │   │
│  │ Connectors   │  │ Engine       │  │ Handlers        │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Scheduler    │  │ Logger       │  │ Notifier        │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  MCP SERVER (6 tools)                                       │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────────┐  │
│  │ list_      │ │ preview_   │ │ install_template       │  │
│  │ templates  │ │ template   │ │                        │  │
│  └────────────┘ └────────────┘ └────────────────────────┘  │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────────┐  │
│  │ configure_ │ │ run_       │ │ schedule_template      │  │
│  │ template   │ │ template   │ │                        │  │
│  └────────────┘ └────────────┘ └────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Template Marketplace
- **Catalog Service**: List, search, filter templates
- **Purchase Flow**: Stripe integration for payments
- **License Manager**: Validate purchases, manage entitlements

### 2. Deployment Engine
- **Template Installer**: Clone, configure, validate
- **Setup Wizard**: Interactive configuration
- **Dependency Manager**: pip/conda installation

### 3. Workflow Runtime
- **Data Connectors**: CSV, databases, APIs
- **Forecast Engine**: TimeGPT API wrapper
- **Output Handlers**: Excel, Sheets, databases, dashboards
- **Scheduler**: Cron-based execution
- **Logger**: Execution history
- **Notifier**: Slack, email alerts

---

## Template Structure

```
templates/
├── retail-demand-planning/
│   ├── manifest.json           # Template metadata
│   ├── requirements.txt        # Python dependencies
│   ├── config.yaml.template    # Configuration template
│   ├── workflow.py             # Main workflow logic
│   ├── connectors/
│   │   ├── csv_loader.py
│   │   ├── database_loader.py
│   │   └── api_loader.py
│   ├── processors/
│   │   ├── data_prep.py
│   │   ├── forecast.py
│   │   └── post_process.py
│   ├── outputs/
│   │   ├── excel_export.py
│   │   ├── sheets_sync.py
│   │   └── database_write.py
│   └── README.md
```

---

## Template Manifest

```json
{
  "id": "retail-demand-planning",
  "name": "Retail Demand Planning",
  "version": "1.0.0",
  "description": "SKU-level demand forecasting with inventory recommendations",
  "category": "retail",
  "price_usd": 299,
  "features": [
    "Multi-SKU forecasting",
    "Safety stock calculation",
    "PO recommendations",
    "Excel export"
  ],
  "requirements": {
    "python": ">=3.10",
    "nixtla_api_key": true,
    "data_format": ["csv", "postgresql", "bigquery"]
  },
  "outputs": ["excel", "csv", "database"],
  "schedule_options": ["daily", "weekly", "monthly"]
}
```

---

## Data Flow

1. **Install**: User purchases and installs template
2. **Configure**: Setup wizard collects data source, output, schedule
3. **Validate**: Test data connection and API access
4. **Run**: Execute workflow (manual or scheduled)
5. **Output**: Write results to configured destinations
6. **Notify**: Send alerts on completion/failure

---

## Integration Points

| System | Integration Type | Purpose |
|--------|------------------|---------|
| Stripe | API | Payments |
| TimeGPT | API | Forecasting |
| PostgreSQL | Driver | Data source/output |
| BigQuery | Client | Data source/output |
| Google Sheets | API | Output |
| Excel | openpyxl | Output |
| Slack | Webhooks | Notifications |

---

## Deployment Model

- **Template Storage**: GitHub private repo or S3
- **Installation**: Local to user's environment
- **Execution**: User's machine or cloud
- **Scheduling**: Local cron or cloud scheduler
