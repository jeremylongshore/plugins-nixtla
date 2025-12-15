# Sales Demo Builder - User Journey

**Plugin:** nixtla-sales-demo-builder
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Persona: Solutions Engineer

**Name:** Jake
**Role:** Solutions Engineer at Nixtla
**Pain Point:** Spends 4+ hours customizing demos for each enterprise prospect

---

## Journey Map

### Stage 1: Discovery
**Trigger:** Jake has a demo call with Target's supply chain team tomorrow

**Actions:**
- Realizes he needs a retail-specific demo
- Looks for existing demos - none match Target's use case
- Would normally spend 4 hours customizing
- Discovers nixtla-sales-demo-builder plugin

**Outcome:** Decides to use the plugin

---

### Stage 2: Setup
**Trigger:** Jake installs the plugin

**Actions:**
```bash
# Install plugin
claude-code plugins install nixtla-sales-demo-builder

# Check available verticals
/sales-demo list-verticals
```

**Output:**
```
Available Demo Verticals:
━━━━━━━━━━━━━━━━━━━━━━━━
1. retail       - Demand planning, inventory optimization
2. energy       - Load forecasting, grid optimization
3. finance      - Revenue forecasting, price prediction
4. healthcare   - Patient volume, capacity planning
5. supply_chain - Logistics, shipping optimization

Use: /sales-demo generate --vertical=<name>
```

**Outcome:** Plugin ready to use

---

### Stage 3: Generate Demo
**Trigger:** Jake generates a demo for Target

**Actions:**
```
> /sales-demo generate \
    --vertical=retail \
    --prospect="Target Corporation" \
    --contact="Sarah Chen, VP Supply Chain" \
    --use-case="SKU-level demand forecasting for 2,000 stores"

Generating Demo Notebook...
━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Loading retail template
✓ Downloading M5 dataset (120MB)
✓ Customizing narrative for Target
✓ Generating code cells
✓ Adding comparison section
✓ Validating notebook execution

Demo Generated: target_demand_forecasting_demo.ipynb

Notebook Sections:
1. Introduction (customized for Target)
2. Data Overview (M5 - similar to Target's scale)
3. TimeGPT Forecasting
4. Accuracy Analysis
5. Model Comparison (TimeGPT vs Prophet vs ARIMA)
6. ROI Calculator
7. Next Steps & Call-to-Action
```

**Outcome:** Complete demo in 30 seconds

---

### Stage 4: Review Demo
**Trigger:** Jake opens the notebook

**Notebook Contents:**
```markdown
# Demand Forecasting for Target Corporation

Prepared for: Sarah Chen, VP Supply Chain
Prepared by: Nixtla Solutions Engineering
Date: December 15, 2025

---

## Executive Summary

Target manages inventory for 2,000+ stores across diverse product
categories. Accurate demand forecasting directly impacts:

- **Stockout reduction**: Estimated 30% improvement
- **Overstock reduction**: Estimated 25% improvement
- **Working capital**: $50M+ annual savings potential

This demo uses the M5 Competition dataset (Walmart) to demonstrate
TimeGPT's forecasting capabilities on retail data similar to Target's.

---

## Why TimeGPT for Target?

1. **Scale**: Handles 10,000+ SKUs across 2,000 stores
2. **Speed**: Forecasts generated in seconds, not hours
3. **Accuracy**: State-of-the-art performance on retail benchmarks
4. **Simplicity**: No ML expertise required

---
```

**Outcome:** Professional, customized demo ready for presentation

---

### Stage 5: Add Comparison
**Trigger:** Jake wants to emphasize TimeGPT's advantage

**Actions:**
```
> /sales-demo add-comparison \
    --notebook=target_demand_forecasting_demo.ipynb \
    --models="prophet,arima,naive"

Adding Model Comparison...
━━━━━━━━━━━━━━━━━━━━━━━━
✓ Running Prophet forecast
✓ Running ARIMA forecast
✓ Running Naive baseline
✓ Calculating metrics
✓ Generating comparison chart

Comparison Results:
┌─────────────┬────────┬────────┬────────┐
│ Model       │ MAPE   │ RMSE   │ Time   │
├─────────────┼────────┼────────┼────────┤
│ TimeGPT     │ 12.3%  │ 145.2  │ 2.1s   │
│ Prophet     │ 18.7%  │ 201.4  │ 45.3s  │
│ ARIMA       │ 21.2%  │ 234.1  │ 12.7s  │
│ Naive       │ 28.4%  │ 312.8  │ 0.1s   │
└─────────────┴────────┴────────┴────────┘

TimeGPT: 34% more accurate than Prophet, 22x faster
```

**Outcome:** Compelling competitive comparison added

---

### Stage 6: Export & Present
**Trigger:** Jake exports for the call

**Actions:**
```
> /sales-demo export \
    --notebook=target_demand_forecasting_demo.ipynb \
    --format=html

Exporting...
✓ Rendered: target_demand_forecasting_demo.html

Files ready:
- target_demand_forecasting_demo.ipynb (interactive)
- target_demand_forecasting_demo.html (presentation)
```

**Outcome:** Ready for tomorrow's demo call

---

## Success Scenario

- Demo prep: 4 hours → 15 minutes
- Customization: Fully tailored to Target
- Comparison: Quantified TimeGPT advantage
- Jake: Hero to the sales team
