---
name: nixtla-arbitrage-detector
description: |
  Detects arbitrage opportunities between Polymarket and Kalshi prediction markets.
  Use when a user wants to find price discrepancies for the same event on different platforms.
  Trigger with "find arbitrage", "detect market inefficiencies", "compare Polymarket and Kalshi prices".
allowed-tools: "Read,Write,Bash,Glob,Grep,WebFetch"
version: "1.0.0"
---

# Arbitrage Detector

Identifies potential arbitrage opportunities across Polymarket and Kalshi.

## Purpose

Finds discrepancies in contract prices for the same event across Polymarket and Kalshi prediction markets.

## Overview

Scans Polymarket and Kalshi for matching events.  Fetches current prices for each event.  Calculates the potential profit from buying on one platform and selling on the other, factoring in fees. Outputs a list of arbitrage opportunities ranked by potential profit.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep, WebFetch

**Environment**: None

**Packages**:
```bash
pip install requests
```

## Instructions

### Step 1: Fetch data

Run the data fetching script: `python {baseDir}/scripts/fetch_data.py`

### Step 2: Analyze data

Run the analysis script: `python {baseDir}/scripts/analyze_data.py`

### Step 3: Generate report

Run the report generation script: `python {baseDir}/scripts/generate_report.py`

### Step 4: Write output

Save the arbitrage opportunities report to a file.

## Output

- **arbitrage_opportunities.csv**: A list of arbitrage opportunities with potential profit.
- **polymarket_data.json**: Raw data fetched from Polymarket.
- **kalshi_data.json**: Raw data fetched from Kalshi.

## Error Handling

1. **Error**: `Polymarket API Error`
   **Solution**: Check Polymarket API status and retry.

2. **Error**: `Kalshi API Error`
   **Solution**: Check Kalshi API status and retry.

3. **Error**: `No matching events found`
   **Solution**: Expand search criteria or check event names for discrepancies.

4. **Error**: `Insufficient data to calculate arbitrage`
   **Solution**: Ensure both Polymarket and Kalshi have data for the event.

## Examples

### Example 1: Basic Arbitrage

**Input**:
(Polymarket: Event A - Yes: 0.4, No: 0.6; Kalshi: Event A - Yes: 0.5, No: 0.5)

**Output**:
```
Event,Platform Buy,Platform Sell,Profit
Event A,Polymarket Yes,Kalshi Yes,0.09
```

### Example 2: No Arbitrage

**Input**:
(Polymarket: Event B - Yes: 0.5, No: 0.5; Kalshi: Event B - Yes: 0.5, No: 0.5)

**Output**:
```
No arbitrage opportunities found.
```

## Resources

- Scripts: `{baseDir}/scripts/`
- Data: `{baseDir}/data/`