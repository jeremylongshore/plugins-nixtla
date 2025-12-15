# Forecast Audit Report - Architecture

**Plugin:** nixtla-forecast-audit-report
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  FORECAST INPUT                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ TimeGPT      │  │ Forecast     │  │ Data            │   │
│  │ Response     │  │ Metadata     │  │ Statistics      │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  REPORT ENGINE                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Template Selector                                   │   │
│  │  - SOX, FDA, Basel III, IFRS 9                       │   │
│  │  - Custom templates                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Content Generator                                   │   │
│  │  - Methodology explanations (LLM)                    │   │
│  │  - Data lineage documentation                        │   │
│  │  - Metrics calculation                               │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Model Card Generator                                │   │
│  │  - Intended use                                      │   │
│  │  - Limitations                                       │   │
│  │  - Ethical considerations                            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  DOCUMENT ASSEMBLY                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Section      │  │ Chart        │  │ Signature       │   │
│  │ Builder      │  │ Generator    │  │ Fields          │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  MCP SERVER (5 tools)                                       │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────────┐  │
│  │ generate_  │ │ list_      │ │ customize_template     │  │
│  │ report     │ │ templates  │ │                        │  │
│  └────────────┘ └────────────┘ └────────────────────────┘  │
│  ┌────────────┐ ┌────────────────────────────────────────┐ │
│  │ export_    │ │ get_report_history                     │ │
│  │ report     │ │                                        │ │
│  └────────────┘ └────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  EXPORT LAYER                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ PDF          │  │ Word         │  │ HTML            │   │
│  │ (WeasyPrint) │  │ (python-docx)│  │ (Jinja2)        │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Metadata Capture
- **Forecast Response Parser**: Extract predictions, confidence intervals
- **Data Statistics Calculator**: Input data summary (no raw data)
- **Environment Recorder**: Python version, library versions, timestamps

### 2. Report Engine
- **Template Selector**: Match compliance framework to template
- **Content Generator**: LLM-powered explanations
- **Model Card Generator**: Standardized model documentation
- **Metrics Calculator**: MAPE, RMSE, MAE, backtesting

### 3. Document Assembly
- **Section Builder**: Assemble sections in correct order
- **Chart Generator**: Matplotlib/Plotly charts for embedding
- **Signature Fields**: Digital signature placeholders

### 4. Export System
- **PDF Generator**: WeasyPrint for professional output
- **Word Generator**: python-docx for editable documents
- **HTML Generator**: Jinja2 templates for web viewing

---

## Template Structure

```
templates/
├── sox/
│   ├── template.html.j2
│   ├── sections/
│   │   ├── executive_summary.md.j2
│   │   ├── methodology.md.j2
│   │   ├── data_governance.md.j2
│   │   ├── results.md.j2
│   │   └── controls.md.j2
│   └── styles/
│       └── sox.css
├── fda_21_cfr_11/
│   ├── template.html.j2
│   ├── sections/
│   └── styles/
├── basel_iii/
│   ├── template.html.j2
│   └── ...
└── ifrs_9/
    ├── template.html.j2
    └── ...
```

---

## Report Schema

```python
@dataclass
class AuditReport:
    # Identification
    report_id: str
    version: str
    created_at: datetime
    template: str

    # Forecast reference
    forecast_id: str
    forecast_timestamp: datetime

    # Content sections
    executive_summary: str
    methodology: MethodologySection
    data_section: DataSection
    results: ResultsSection
    limitations: LimitationsSection
    model_card: ModelCard

    # Approval
    approval_chain: List[Approval]
    digital_signatures: List[Signature]

    # Metadata
    generator_version: str
    template_version: str
```

---

## Data Flow

1. **Capture**: Extract forecast metadata at generation time
2. **Store**: Save metadata in report database
3. **Generate**: On-demand report generation
4. **Review**: Optional approval workflow
5. **Export**: PDF/Word/HTML output
6. **Archive**: Version-controlled storage

---

## Compliance Framework Mapping

| Framework | Key Requirements | Report Sections |
|-----------|------------------|-----------------|
| SOX | Internal controls, data integrity | Controls, audit trail |
| FDA 21 CFR 11 | Electronic signatures, validation | Validation, signatures |
| Basel III | Model risk, validation | Risk assessment, backtesting |
| IFRS 9 | Expected credit loss | Methodology, assumptions |

---

## Integration Points

| System | Integration Type | Purpose |
|--------|------------------|---------|
| TimeGPT API | Extended response | Metadata capture |
| WeasyPrint | Library | PDF generation |
| python-docx | Library | Word generation |
| S3/GCS | Storage | Report archival |
| DocuSign | API (optional) | Digital signatures |

---

## Deployment Model

- **Plugin**: Local execution via Claude Code
- **Storage**: User's cloud storage
- **Templates**: Bundled with plugin, updateable
