# Forecast Workflow Templates - User Journey

**Plugin:** nixtla-forecast-workflow-templates
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Persona: Business Analyst

**Name:** Lisa
**Role:** Demand Planning Analyst at a mid-size retailer
**Pain Point:** Has TimeGPT API access but doesn't know how to operationalize forecasts

---

## Journey Map

### Stage 1: Discovery
**Trigger:** Lisa's trial is expiring and she hasn't built anything useful

**Actions:**
- Has run a few API calls successfully
- Doesn't know how to turn forecasts into actionable outputs
- About to churn when she discovers workflow templates

**Outcome:** Finds the retail demand planning template

---

### Stage 2: Browse Templates
**Trigger:** Lisa browses the template marketplace

**Actions:**
```
> /workflow-templates list --category=retail

Available Templates (Retail):
━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. retail-demand-planning ($299)
   SKU-level forecasting → inventory recommendations → PO suggestions
   ⭐ 4.8 (47 reviews) | 120+ installs

2. retail-markdown-optimizer ($199)
   Predict optimal markdown timing for clearance items
   ⭐ 4.6 (23 reviews) | 45+ installs

3. retail-store-traffic ($249)
   Foot traffic predictions for staffing optimization
   ⭐ 4.7 (31 reviews) | 67+ installs

Use: /workflow-templates preview <template-id>
```

**Outcome:** Interested in demand planning template

---

### Stage 3: Preview Template
**Trigger:** Lisa previews the template

**Actions:**
```
> /workflow-templates preview retail-demand-planning

Retail Demand Planning Template
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Price: $299 (one-time)

What You Get:
✓ Multi-SKU demand forecasting with TimeGPT
✓ Safety stock calculations
✓ Reorder point recommendations
✓ Purchase order suggestions
✓ Excel report generation
✓ Automated scheduling

Data Requirements:
- Historical sales data (daily/weekly)
- SKU/product identifiers
- Optional: promotions calendar, holidays

Output Options:
- Excel workbook with forecasts + recommendations
- CSV export for ERP import
- Direct database write (PostgreSQL, BigQuery)

Includes:
- Full source code
- Setup wizard
- Email support for 30 days
- Free updates for 1 year

[Purchase $299] [Request Demo]
```

**Outcome:** Decides to purchase

---

### Stage 4: Installation
**Trigger:** Lisa purchases and installs

**Actions:**
```
> /workflow-templates install retail-demand-planning

Installing Retail Demand Planning...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Validating license
✓ Creating directory structure
✓ Installing dependencies
✓ Configuring environment

Installation complete!

Next: Run the setup wizard
> /workflow-templates configure retail-demand-planning
```

**Outcome:** Template installed

---

### Stage 5: Configuration
**Trigger:** Lisa runs the setup wizard

**Actions:**
```
> /workflow-templates configure retail-demand-planning

Setup Wizard: Retail Demand Planning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1/4: Data Source
Where is your sales data?
[1] CSV file
[2] PostgreSQL database
[3] BigQuery
[4] API endpoint

> 1

CSV file path: /data/sales_history.csv

Detecting columns...
Found: date, sku_id, store_id, quantity, revenue

Map columns:
- Date column: date ✓
- Product ID: sku_id ✓
- Sales quantity: quantity ✓

Step 2/4: Forecast Settings
Forecast horizon: 14 days
Confidence levels: [80, 95]
Include seasonality: yes

Step 3/4: Output Configuration
Output format: Excel
Output path: /reports/demand_forecast.xlsx
Include charts: yes

Step 4/4: Schedule (Optional)
Run automatically?
[1] Daily at 6 AM
[2] Weekly on Monday
[3] Monthly on 1st
[4] Manual only

> 2

Configuration saved!
Test run? [y/n]: y
```

**Outcome:** Template configured for Lisa's data

---

### Stage 6: First Run
**Trigger:** Lisa runs the workflow

**Actions:**
```
> /workflow-templates run retail-demand-planning

Running Retail Demand Planning...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1/5] Loading data... 15,234 rows loaded
[2/5] Preparing data... 847 SKUs identified
[3/5] Generating forecasts... (TimeGPT API)
[4/5] Calculating recommendations...
[5/5] Generating Excel report...

✓ Complete!

Report: /reports/demand_forecast.xlsx

Summary:
- SKUs forecasted: 847
- Reorder alerts: 23 (immediate)
- Stock-out risk: 12 SKUs
- Overstock risk: 45 SKUs

Open report? [y/n]: y
```

**Outcome:** First actionable forecasts in 10 minutes

---

### Stage 7: Ongoing Use
**Trigger:** Lisa uses the template weekly

**Actions:**
- Workflow runs automatically every Monday
- Lisa reviews the Excel report
- Sends PO recommendations to procurement
- Tracks forecast accuracy over time

**Outcome:**
- Lisa converts to paid TimeGPT plan
- API usage: 50 calls/week → 1,500 calls/week
- Inventory costs down 18%

---

## Success Scenario

- Time to value: 2 weeks → 10 minutes
- Trial conversion: Yes (was about to churn)
- API consumption: 30x increase
- Business impact: $50K/year inventory savings
