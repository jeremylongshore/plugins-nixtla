# Forecast Audit Report - Technical Specification

**Plugin:** nixtla-forecast-audit-report
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Runtime | Python 3.10+ | Nixtla ecosystem |
| MCP Server | FastAPI + MCP SDK | Standard plugin architecture |
| Templates | Jinja2 | Flexible document generation |
| PDF | WeasyPrint | High-quality PDF output |
| Word | python-docx | Editable documents |
| Storage | SQLite | Local report database |
| LLM | Claude/GPT-4 | Methodology explanations |

---

## API Specification

### MCP Tools

#### 1. `generate_report`
```json
{
  "name": "generate_report",
  "description": "Create audit report for forecast",
  "inputSchema": {
    "type": "object",
    "properties": {
      "forecast_id": {
        "type": "string",
        "description": "ID of the forecast to document"
      },
      "template": {
        "type": "string",
        "enum": ["sox", "fda_21_cfr_11", "basel_iii", "ifrs_9", "custom"]
      },
      "purpose": {
        "type": "string",
        "description": "Business purpose of the forecast"
      },
      "approvers": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Email addresses of approvers"
      },
      "custom_sections": {
        "type": "object",
        "description": "Additional custom content"
      }
    },
    "required": ["forecast_id", "template"]
  }
}
```

#### 2. `list_templates`
```json
{
  "name": "list_templates",
  "description": "Get available compliance templates",
  "inputSchema": {
    "type": "object",
    "properties": {
      "industry": {
        "type": "string",
        "enum": ["finance", "healthcare", "all"]
      }
    }
  }
}
```

#### 3. `customize_template`
```json
{
  "name": "customize_template",
  "description": "Modify template for specific needs",
  "inputSchema": {
    "type": "object",
    "properties": {
      "base_template": {"type": "string"},
      "name": {"type": "string"},
      "sections": {
        "type": "object",
        "description": "Section overrides and additions"
      }
    },
    "required": ["base_template", "name"]
  }
}
```

#### 4. `export_report`
```json
{
  "name": "export_report",
  "description": "Export to PDF/Word/HTML",
  "inputSchema": {
    "type": "object",
    "properties": {
      "report_id": {"type": "string"},
      "format": {
        "type": "string",
        "enum": ["pdf", "docx", "html", "json"]
      },
      "include_signatures": {
        "type": "boolean",
        "default": true
      }
    },
    "required": ["report_id", "format"]
  }
}
```

#### 5. `get_report_history`
```json
{
  "name": "get_report_history",
  "description": "Retrieve past reports",
  "inputSchema": {
    "type": "object",
    "properties": {
      "forecast_id": {"type": "string"},
      "start_date": {"type": "string"},
      "end_date": {"type": "string"},
      "template": {"type": "string"}
    }
  }
}
```

---

## Data Models

### Report Model
```python
@dataclass
class AuditReport:
    id: str
    version: str
    template: str
    created_at: datetime
    updated_at: datetime

    # Forecast reference
    forecast_id: str
    forecast_metadata: ForecastMetadata

    # Content
    executive_summary: str
    methodology: MethodologySection
    data_section: DataSection
    results: ResultsSection
    limitations: LimitationsSection
    model_card: ModelCard

    # Approval
    approvers: List[str]
    approvals: List[Approval]

    # Export
    exports: List[ExportRecord]
```

### Forecast Metadata
```python
@dataclass
class ForecastMetadata:
    forecast_id: str
    timestamp: datetime
    horizon: int
    frequency: str
    confidence_levels: List[int]

    # Data summary (no raw data)
    n_observations: int
    date_range: Tuple[str, str]
    missing_values: int
    outliers_detected: int

    # Results
    predictions: List[float]
    confidence_intervals: Dict[int, Tuple[List, List]]

    # Accuracy
    backtesting_mape: float
    backtesting_rmse: float

    # Environment
    api_version: str
    request_timestamp: datetime
```

### Model Card
```python
@dataclass
class ModelCard:
    model_name: str
    model_version: str
    model_type: str

    # Purpose
    intended_use: str
    out_of_scope_use: str

    # Performance
    metrics: Dict[str, float]
    performance_by_segment: Dict[str, Dict[str, float]]

    # Limitations
    known_limitations: List[str]
    failure_modes: List[str]

    # Ethical considerations
    fairness_considerations: str
    bias_assessment: str
```

---

## Template Sections

```python
BASEL_III_SECTIONS = [
    Section(
        id="executive_summary",
        title="Executive Summary",
        template="executive_summary.md.j2",
        required=True
    ),
    Section(
        id="model_identification",
        title="Model Identification",
        template="model_identification.md.j2",
        required=True
    ),
    Section(
        id="methodology",
        title="Methodology",
        template="methodology.md.j2",
        required=True
    ),
    Section(
        id="data_governance",
        title="Data Governance",
        template="data_governance.md.j2",
        required=True
    ),
    Section(
        id="validation",
        title="Model Validation",
        template="validation.md.j2",
        required=True
    ),
    Section(
        id="results",
        title="Results and Analysis",
        template="results.md.j2",
        required=True
    ),
    Section(
        id="limitations",
        title="Limitations and Assumptions",
        template="limitations.md.j2",
        required=True
    ),
    Section(
        id="model_card",
        title="Model Card",
        template="model_card.md.j2",
        required=True
    ),
    Section(
        id="approval",
        title="Approval Chain",
        template="approval.md.j2",
        required=True
    ),
]
```

---

## Performance Requirements

| Metric | Target |
|--------|--------|
| Report generation | <30 seconds |
| PDF export | <10 seconds |
| Word export | <5 seconds |
| Version retrieval | <2 seconds |

---

## Dependencies

```txt
# requirements.txt
fastapi>=0.100.0
jinja2>=3.0.0
weasyprint>=60.0
python-docx>=1.0.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
anthropic>=0.5.0
matplotlib>=3.5.0
```

---

## Directory Structure

```
nixtla-forecast-audit-report/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── audit-report.md
├── scripts/
│   ├── mcp_server.py
│   ├── report_generator.py
│   ├── template_engine.py
│   ├── model_card_generator.py
│   └── export_handler.py
├── templates/
│   ├── sox/
│   ├── fda_21_cfr_11/
│   ├── basel_iii/
│   └── ifrs_9/
├── data/
│   └── reports.db
├── requirements.txt
└── README.md
```
