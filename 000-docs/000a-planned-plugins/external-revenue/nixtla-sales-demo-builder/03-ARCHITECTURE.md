# Sales Demo Builder - Architecture

**Plugin:** nixtla-sales-demo-builder
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  USER INPUT                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Vertical     │  │ Prospect     │  │ Customization   │   │
│  │ Selection    │  │ Details      │  │ Options         │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  TEMPLATE ENGINE                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Vertical Templates (Jinja2)                         │   │
│  │  - Retail, Energy, Finance, Healthcare, Supply Chain │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Narrative Generator                                 │   │
│  │  - LLM-powered sales copy                            │   │
│  │  - Industry-specific talking points                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Dataset      │  │ Download     │  │ Validation      │   │
│  │ Registry     │  │ Manager      │  │ Engine          │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  NOTEBOOK GENERATOR                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Code Cells   │  │ Markdown     │  │ Visualization   │   │
│  │ Generator    │  │ Cells        │  │ Cells           │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  MCP SERVER (5 tools)                                       │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────────┐  │
│  │ list_      │ │ generate_  │ │ list_datasets          │  │
│  │ verticals  │ │ demo       │ │                        │  │
│  └────────────┘ └────────────┘ └────────────────────────┘  │
│  ┌────────────┐ ┌────────────────────────────────────────┐ │
│  │ add_       │ │ export_notebook                        │ │
│  │ comparison │ │                                        │ │
│  └────────────┘ └────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Jupyter      │  │ HTML         │  │ PDF             │   │
│  │ Notebook     │  │ Export       │  │ Export          │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Template Engine
- **Vertical Templates**: Jinja2 notebooks per industry
- **Variable Injection**: Prospect name, company, use case
- **Narrative Generator**: LLM-powered sales copy

### 2. Dataset Registry
- **Manifest**: JSON file with dataset metadata
- **Download Manager**: Fetch and cache datasets
- **Validation**: Ensure data quality before use

### 3. Notebook Generator
- **nbformat**: Create Jupyter notebook structure
- **Code Cells**: Forecasting code with proper imports
- **Markdown Cells**: Narrative and talking points
- **Visualization Cells**: Charts and graphs

### 4. Comparison Engine
- **Model Runner**: Execute TimeGPT, Prophet, ARIMA
- **Metrics Calculator**: MAPE, RMSE, MAE
- **Comparison Chart**: Side-by-side visualization

---

## Dataset Registry Schema

```json
{
  "datasets": [
    {
      "id": "m5_sales",
      "name": "M5 Forecasting Competition",
      "vertical": "retail",
      "url": "https://...",
      "format": "csv",
      "size_mb": 120,
      "columns": ["date", "item_id", "store_id", "sales"],
      "frequency": "daily",
      "license": "CC BY-NC 4.0",
      "description": "Walmart sales data for 3,049 products"
    }
  ]
}
```

---

## Template Structure

```
templates/
├── retail/
│   ├── notebook.ipynb.j2
│   ├── narrative.md.j2
│   └── comparison.ipynb.j2
├── energy/
│   ├── notebook.ipynb.j2
│   └── narrative.md.j2
├── finance/
│   ├── notebook.ipynb.j2
│   └── narrative.md.j2
├── healthcare/
│   ├── notebook.ipynb.j2
│   └── narrative.md.j2
└── supply_chain/
    ├── notebook.ipynb.j2
    └── narrative.md.j2
```

---

## Integration Points

| System | Integration Type | Purpose |
|--------|------------------|---------|
| Dataset sources | HTTP download | Public data |
| TimeGPT API | API call | Forecasting |
| Prophet | Local library | Comparison |
| statsforecast | Local library | Comparison |
| nbformat | Library | Notebook generation |

---

## Deployment Model

- **Local Development**: Run from Claude Code
- **Output**: Generated notebooks saved locally
- **Caching**: Datasets cached in `~/.nixtla-demos/`
