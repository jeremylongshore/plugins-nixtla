# Forecast Workflow Templates - Technical Specification

**Plugin:** nixtla-forecast-workflow-templates
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Runtime | Python 3.10+ | Nixtla ecosystem |
| MCP Server | FastAPI + MCP SDK | Standard plugin architecture |
| Payments | Stripe | Industry standard |
| Scheduling | APScheduler | Python-native |
| Database | SQLite | Local state management |
| Packaging | pip/setuptools | Standard Python |

---

## API Specification

### MCP Tools

#### 1. `list_templates`
```json
{
  "name": "list_templates",
  "description": "Browse available templates",
  "inputSchema": {
    "type": "object",
    "properties": {
      "category": {
        "type": "string",
        "enum": ["retail", "finance", "energy", "healthcare", "supply_chain", "all"]
      },
      "sort_by": {
        "type": "string",
        "enum": ["popularity", "price", "rating", "newest"],
        "default": "popularity"
      }
    }
  }
}
```

#### 2. `preview_template`
```json
{
  "name": "preview_template",
  "description": "View template details",
  "inputSchema": {
    "type": "object",
    "properties": {
      "template_id": {
        "type": "string"
      }
    },
    "required": ["template_id"]
  }
}
```

#### 3. `install_template`
```json
{
  "name": "install_template",
  "description": "Deploy template to environment",
  "inputSchema": {
    "type": "object",
    "properties": {
      "template_id": {
        "type": "string"
      },
      "install_path": {
        "type": "string",
        "default": "./workflows"
      }
    },
    "required": ["template_id"]
  }
}
```

#### 4. `configure_template`
```json
{
  "name": "configure_template",
  "description": "Set up data sources and outputs",
  "inputSchema": {
    "type": "object",
    "properties": {
      "template_id": {
        "type": "string"
      },
      "config": {
        "type": "object",
        "properties": {
          "data_source": {"type": "object"},
          "forecast_settings": {"type": "object"},
          "output_config": {"type": "object"},
          "schedule": {"type": "object"}
        }
      }
    },
    "required": ["template_id"]
  }
}
```

#### 5. `run_template`
```json
{
  "name": "run_template",
  "description": "Execute workflow",
  "inputSchema": {
    "type": "object",
    "properties": {
      "template_id": {
        "type": "string"
      },
      "dry_run": {
        "type": "boolean",
        "default": false
      }
    },
    "required": ["template_id"]
  }
}
```

#### 6. `schedule_template`
```json
{
  "name": "schedule_template",
  "description": "Set up recurring runs",
  "inputSchema": {
    "type": "object",
    "properties": {
      "template_id": {
        "type": "string"
      },
      "schedule": {
        "type": "object",
        "properties": {
          "frequency": {
            "type": "string",
            "enum": ["hourly", "daily", "weekly", "monthly"]
          },
          "time": {"type": "string"},
          "day": {"type": "integer"},
          "enabled": {"type": "boolean"}
        }
      }
    },
    "required": ["template_id", "schedule"]
  }
}
```

---

## Workflow Base Class

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class WorkflowResult:
    success: bool
    output_path: Optional[str]
    metrics: Dict[str, Any]
    errors: list

class WorkflowTemplate(ABC):
    """Base class for all workflow templates."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = self._setup_logger()

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Load data from configured source."""
        pass

    @abstractmethod
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for forecasting."""
        pass

    @abstractmethod
    def generate_forecasts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate forecasts using TimeGPT."""
        pass

    @abstractmethod
    def post_process(self, forecasts: pd.DataFrame) -> pd.DataFrame:
        """Apply business logic to forecasts."""
        pass

    @abstractmethod
    def export_results(self, results: pd.DataFrame) -> str:
        """Export results to configured destination."""
        pass

    def run(self) -> WorkflowResult:
        """Execute the complete workflow."""
        try:
            data = self.load_data()
            prepared = self.prepare_data(data)
            forecasts = self.generate_forecasts(prepared)
            results = self.post_process(forecasts)
            output_path = self.export_results(results)
            return WorkflowResult(
                success=True,
                output_path=output_path,
                metrics=self._calculate_metrics(results),
                errors=[]
            )
        except Exception as e:
            return WorkflowResult(
                success=False,
                output_path=None,
                metrics={},
                errors=[str(e)]
            )
```

---

## Configuration Schema

```yaml
# config.yaml for retail-demand-planning
data_source:
  type: csv  # csv, postgresql, bigquery, api
  path: /data/sales.csv
  columns:
    date: date
    product_id: sku_id
    quantity: quantity

forecast_settings:
  horizon: 14
  frequency: D
  confidence_levels: [80, 95]
  include_history: 90

business_rules:
  safety_stock_days: 7
  lead_time_days: 14
  service_level: 0.95

output:
  type: excel  # excel, csv, database, sheets
  path: /reports/demand_forecast.xlsx
  include_charts: true
  include_recommendations: true

schedule:
  enabled: true
  frequency: weekly
  day: monday
  time: "06:00"

notifications:
  slack_webhook: ""
  email: ""
  notify_on_success: true
  notify_on_failure: true
```

---

## Dependencies

```txt
# requirements.txt
fastapi>=0.100.0
nixtla>=0.5.0
pandas>=2.0.0
openpyxl>=3.1.0
gspread>=5.0.0
sqlalchemy>=2.0.0
google-cloud-bigquery>=3.0.0
apscheduler>=3.10.0
stripe>=5.0.0
pydantic>=2.0.0
```

---

## Directory Structure

```
nixtla-forecast-workflow-templates/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── workflow-templates.md
├── scripts/
│   ├── mcp_server.py
│   ├── marketplace.py
│   ├── installer.py
│   ├── scheduler.py
│   └── license_manager.py
├── templates/
│   ├── retail-demand-planning/
│   ├── saas-revenue-forecasting/
│   ├── energy-load-forecasting/
│   └── healthcare-capacity/
├── base/
│   ├── workflow.py
│   ├── connectors.py
│   └── outputs.py
├── requirements.txt
└── README.md
```
