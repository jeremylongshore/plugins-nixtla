# Forecast Audit Report - User Journey

**Plugin:** nixtla-forecast-audit-report
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Persona: Compliance Officer

**Name:** Rachel
**Role:** Chief Compliance Officer at a regional bank
**Pain Point:** Auditors require documentation for every AI model used in financial decisions

---

## Journey Map

### Stage 1: Discovery
**Trigger:** External auditors flag insufficient documentation for forecasting models

**Actions:**
- Receives audit finding: "AI forecasting model lacks documentation"
- Data science team has no model documentation process
- Manual documentation would take weeks per model
- Discovers Nixtla audit report plugin

**Outcome:** Decides to evaluate automated documentation

---

### Stage 2: Setup
**Trigger:** Rachel's team implements the plugin

**Actions:**
```bash
# Install plugin
claude-code plugins install nixtla-forecast-audit-report

# Check available compliance templates
/audit-report list-templates
```

**Output:**
```
Available Compliance Templates:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. sox            - Sarbanes-Oxley (financial controls)
2. fda_21_cfr_11  - FDA healthcare/pharma
3. basel_iii     - Banking risk models
4. ifrs_9        - Financial reporting (ECL)
5. custom        - Build your own template

Each template includes:
- Executive summary
- Methodology explanation
- Data governance
- Results and accuracy
- Limitations and assumptions
- Approval chain

Use: /audit-report generate --template=<name>
```

**Outcome:** Plugin ready, Basel III template selected

---

### Stage 3: Generate Report
**Trigger:** Rachel generates documentation for quarterly loan loss forecast

**Actions:**
```
> /audit-report generate \
    --forecast-id=fc_2024q4_loan_loss \
    --template=basel_iii \
    --purpose="Quarterly Expected Credit Loss (ECL) forecast" \
    --approvers="rachel@bank.com,cfo@bank.com"

Generating Basel III Compliance Report...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Loading forecast metadata
✓ Calculating accuracy metrics
✓ Generating methodology explanation
✓ Creating data lineage documentation
✓ Building model card
✓ Assembling report sections

Report Generated: audit_report_fc_2024q4_loan_loss_v1.json

Sections:
1. Executive Summary
2. Methodology (TimeGPT architecture explained for auditors)
3. Data Governance (sources, transformations, quality checks)
4. Results (forecasts, confidence intervals, backtesting)
5. Model Limitations
6. Approval Chain (pending: rachel@bank.com, cfo@bank.com)

Preview report? [y/n]: y
```

**Outcome:** Comprehensive report generated in 30 seconds

---

### Stage 4: Review Report
**Trigger:** Rachel reviews the generated report

**Report Preview:**
```markdown
# Basel III Model Risk Documentation
## Expected Credit Loss Forecast - Q4 2024

**Report ID:** RPT-2024-12-001
**Version:** 1.0
**Generated:** 2024-12-15 14:32:00 CST
**Template:** Basel III Risk Model

---

## 1. Executive Summary

This document provides comprehensive model risk documentation for the
Expected Credit Loss (ECL) forecasting model deployed for Q4 2024
quarterly reporting. The model utilizes Nixtla TimeGPT, a foundation
model for time series forecasting, to predict loan default rates and
associated credit losses.

**Key Findings:**
- Model accuracy (MAPE): 4.2% on 12-month backtesting
- Forecast horizon: 4 quarters
- Confidence level: 95%
- Data coverage: 36 months historical

**Risk Assessment:** Low model risk based on backtesting performance
and methodology transparency.

---

## 2. Methodology

### 2.1 Model Architecture
TimeGPT is a transformer-based foundation model pre-trained on over
100 billion time series data points. Unlike traditional statistical
models (ARIMA, ETS), TimeGPT learns temporal patterns through
self-attention mechanisms, enabling:

- Zero-shot forecasting without task-specific training
- Automatic seasonality and trend detection
- Probabilistic forecasts with confidence intervals

### 2.2 Model Selection Rationale
TimeGPT was selected based on:
1. Superior accuracy vs. baseline models (34% MAPE improvement)
2. Reduced operational complexity (no manual parameter tuning)
3. Consistent methodology across forecast types

[Continues with detailed technical documentation...]
```

**Outcome:** Auditor-friendly documentation ready for review

---

### Stage 5: Approval Workflow
**Trigger:** Rachel routes report for approval

**Actions:**
```
> /audit-report approve \
    --report-id=RPT-2024-12-001 \
    --approver=rachel@bank.com \
    --comment="Reviewed methodology, approved for external audit"

Approval recorded:
━━━━━━━━━━━━━━━━━━
Approver: Rachel Martinez (CCO)
Timestamp: 2024-12-15 15:45:00 CST
Status: Approved
Comment: Reviewed methodology, approved for external audit

Remaining approvals: 1 (cfo@bank.com)
```

**Outcome:** Approval chain progressing

---

### Stage 6: Export & Audit
**Trigger:** External auditors request documentation

**Actions:**
```
> /audit-report export \
    --report-id=RPT-2024-12-001 \
    --format=pdf \
    --include-signatures=true

Exporting to PDF...
✓ Including digital signatures
✓ Embedding approval chain
✓ Adding audit trail
✓ Generating PDF

Exported: audit_report_fc_2024q4_loan_loss_v1_signed.pdf

File ready for external distribution.
```

**Auditor Response:**
> "This is the most comprehensive model documentation we've seen.
> No follow-up questions required."

**Outcome:** Audit passed, finding closed

---

## Success Scenario

- Documentation time: 40+ hours → 30 minutes
- Audit finding: Closed
- Auditor satisfaction: Exceptional
- Future audits: Repeatable process
- Rachel: Compliance hero
