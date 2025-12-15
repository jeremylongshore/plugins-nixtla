# Sales Demo Builder - Technical Specification

**Plugin:** nixtla-sales-demo-builder
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Runtime | Python 3.10+ | Nixtla ecosystem |
| Templating | Jinja2 | Flexible notebook generation |
| Notebooks | nbformat | Native Jupyter format |
| Visualization | matplotlib, plotly | Charts and graphs |
| Forecasting | nixtla, statsforecast, prophet | Model comparison |
| Export | nbconvert | HTML/PDF generation |

---

## API Specification

### MCP Tools

#### 1. `list_verticals`
```json
{
  "name": "list_verticals",
  "description": "Get available industry templates",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

#### 2. `generate_demo`
```json
{
  "name": "generate_demo",
  "description": "Create customized demo notebook",
  "inputSchema": {
    "type": "object",
    "properties": {
      "vertical": {
        "type": "string",
        "enum": ["retail", "energy", "finance", "healthcare", "supply_chain"]
      },
      "prospect": {
        "type": "string",
        "description": "Company name"
      },
      "contact": {
        "type": "string",
        "description": "Contact name and title"
      },
      "use_case": {
        "type": "string",
        "description": "Specific use case description"
      },
      "include_comparison": {
        "type": "boolean",
        "default": true
      }
    },
    "required": ["vertical", "prospect"]
  }
}
```

#### 3. `list_datasets`
```json
{
  "name": "list_datasets",
  "description": "Browse available public datasets",
  "inputSchema": {
    "type": "object",
    "properties": {
      "vertical": {
        "type": "string",
        "description": "Filter by vertical"
      }
    }
  }
}
```

#### 4. `add_comparison`
```json
{
  "name": "add_comparison",
  "description": "Add model comparison section",
  "inputSchema": {
    "type": "object",
    "properties": {
      "notebook": {
        "type": "string",
        "description": "Path to notebook"
      },
      "models": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": ["prophet", "arima", "ets", "naive", "seasonal_naive"]
        }
      }
    },
    "required": ["notebook"]
  }
}
```

#### 5. `export_notebook`
```json
{
  "name": "export_notebook",
  "description": "Export to .ipynb or HTML",
  "inputSchema": {
    "type": "object",
    "properties": {
      "notebook": {
        "type": "string"
      },
      "format": {
        "type": "string",
        "enum": ["ipynb", "html", "pdf"],
        "default": "html"
      },
      "execute": {
        "type": "boolean",
        "default": true,
        "description": "Execute cells before export"
      }
    },
    "required": ["notebook"]
  }
}
```

---

## Data Models

### Demo Configuration
```python
@dataclass
class DemoConfig:
    vertical: str
    prospect: str
    contact: Optional[str]
    use_case: Optional[str]
    dataset_id: str
    include_comparison: bool
    comparison_models: List[str]
    output_path: str
```

### Dataset Metadata
```python
@dataclass
class Dataset:
    id: str
    name: str
    vertical: str
    url: str
    format: str
    size_mb: int
    columns: List[str]
    frequency: str
    license: str
    description: str
```

---

## Template Variables

```python
# Variables available in Jinja2 templates
template_vars = {
    # Prospect info
    "prospect_name": "Target Corporation",
    "contact_name": "Sarah Chen",
    "contact_title": "VP Supply Chain",
    "use_case": "SKU-level demand forecasting",

    # Dataset info
    "dataset_name": "M5 Forecasting Competition",
    "dataset_description": "Walmart sales data",
    "n_series": 30490,
    "frequency": "daily",

    # Generated content
    "executive_summary": "...",  # LLM-generated
    "talking_points": ["...", "..."],  # LLM-generated
    "roi_estimate": "$50M+",

    # Comparison results (if included)
    "comparison_results": {...}
}
```

---

## Notebook Structure

```python
notebook_structure = [
    # Section 1: Title and Executive Summary
    {"type": "markdown", "template": "01_title.md.j2"},
    {"type": "markdown", "template": "02_executive_summary.md.j2"},

    # Section 2: Data Loading
    {"type": "code", "template": "03_imports.py.j2"},
    {"type": "code", "template": "04_load_data.py.j2"},
    {"type": "markdown", "template": "05_data_overview.md.j2"},

    # Section 3: Forecasting
    {"type": "markdown", "template": "06_timegpt_intro.md.j2"},
    {"type": "code", "template": "07_timegpt_forecast.py.j2"},
    {"type": "code", "template": "08_visualize_forecast.py.j2"},

    # Section 4: Analysis
    {"type": "markdown", "template": "09_accuracy_analysis.md.j2"},
    {"type": "code", "template": "10_calculate_metrics.py.j2"},

    # Section 5: Comparison (optional)
    {"type": "markdown", "template": "11_comparison_intro.md.j2"},
    {"type": "code", "template": "12_run_comparison.py.j2"},
    {"type": "code", "template": "13_comparison_chart.py.j2"},

    # Section 6: ROI and Next Steps
    {"type": "markdown", "template": "14_roi_calculator.md.j2"},
    {"type": "markdown", "template": "15_next_steps.md.j2"},
]
```

---

## Performance Requirements

| Metric | Target |
|--------|--------|
| Notebook generation | <30 seconds |
| Dataset download | <60 seconds (cached) |
| Comparison execution | <2 minutes |
| HTML export | <10 seconds |

---

## Dependencies

```txt
# requirements.txt
fastapi>=0.100.0
jinja2>=3.0.0
nbformat>=5.0.0
nbconvert>=7.0.0
matplotlib>=3.5.0
plotly>=5.0.0
nixtla>=0.5.0
statsforecast>=1.0.0
prophet>=1.1.0
pandas>=2.0.0
requests>=2.28.0
```

---

## Directory Structure

```
nixtla-sales-demo-builder/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── sales-demo.md
├── scripts/
│   ├── mcp_server.py
│   ├── template_engine.py
│   ├── dataset_manager.py
│   ├── comparison_engine.py
│   └── export_handler.py
├── templates/
│   ├── retail/
│   ├── energy/
│   ├── finance/
│   ├── healthcare/
│   └── supply_chain/
├── datasets/
│   └── registry.json
├── requirements.txt
└── README.md
```
