---
name: nixtla-event-impact-modeler
description: |
  Models the impact of exogenous events on contract prices using TimeGPT.
  Use when needing to quantify the effect of events on time series, analyze pricing anomalies, or forecast with event considerations.
  Trigger with "event impact analysis", "model event effects", "quantify event impact".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebSearch"
version: "1.0.0"
---

# Nixtla Event Impact Modeler

Quantifies the impact of exogenous events on contract prices using TimeGPT.

## Purpose

Analyzes and models the impact of specified events on contract prices over time.

## Overview

This skill assesses how external events (e.g., promotions, natural disasters, policy changes) affect contract prices. It takes historical price data and event details as input, uses TimeGPT to model the time series, and quantifies the causal impact of events. The skill is useful for understanding event effects and improving forecasting accuracy. Outputs include event impact estimates, adjusted forecasts, and visualizations.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep, WebSearch

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas causalimpact
```

## Instructions

### Step 1: Prepare data

Read contract price data and event details from CSV files.

### Step 2: Configure model

Define the event periods and causal model parameters (e.g., prior).

### Step 3: Execute analysis

Run the analysis script: `python {baseDir}/scripts/event_impact.py --prices prices.csv --events events.csv`

### Step 4: Generate output

Save the event impact results and create visualizations.

## Output

- **impact_results.csv**: Quantified impact of each event on contract prices.
- **adjusted_forecast.csv**: Forecast of contract prices with event effects removed.
- **impact_plot.png**: Visualization of event impact over time.

## Error Handling

1. **Error**: `Event dates outside price range`
   **Solution**: Adjust event dates to fall within the available price data.

2. **Error**: `Missing event descriptions`
   **Solution**: Ensure 'event' column exists and is populated in the events CSV.

3. **Error**: `TimeGPT API request failed`
   **Solution**: Verify `NIXTLA_TIMEGPT_API_KEY` and internet connection.

4. **Error**: `CausalImpact failed to converge`
   **Solution**: Adjust model parameters or increase the `niter` parameter.

## Examples

### Example 1: Promotion impact

**Input**: `prices.csv` contains daily prices; `events.csv` marks promotion periods.

**Output**: `impact_results.csv` shows the average price increase during promotion periods.

### Example 2: Natural disaster impact

**Input**: `prices.csv` contains weekly prices; `events.csv` marks a natural disaster.

**Output**: `impact_results.csv` shows the price drop following the disaster.

## Resources

- Scripts: `{baseDir}/scripts/`
- Documentation: `{baseDir}/references/`
