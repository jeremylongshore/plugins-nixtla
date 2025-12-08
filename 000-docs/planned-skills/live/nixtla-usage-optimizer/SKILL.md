---
name: nixtla-usage-optimizer
description: |
  Audits Nixtla API usage and recommends cost-effective routing.
  Use when optimizing TimeGPT API costs, understanding API usage patterns, or reducing expenses.
  Trigger with "optimize Nixtla costs", "analyze TimeGPT usage", "reduce API expenses".
allowed-tools: "Read,Glob,Grep"
version: "1.0.0"
---

# Nixtla Usage Optimizer

Analyzes Nixtla API usage to provide cost optimization recommendations.

## Overview

This skill audits your TimeGPT API usage by analyzing API logs and configurations. It identifies potential areas for cost savings, such as inefficient routing or unnecessary API calls. The skill recommends alternative configurations or routing strategies to minimize expenses. The output includes a detailed report of your current usage and actionable suggestions for optimization.

## Prerequisites

**Tools**: Read, Glob, Grep

**Environment**: `NIXTLA_API_LOG_PATH`, `NIXTLA_API_CONFIG_PATH`

**Packages**:
```bash
pip install pandas
```

## Instructions

### Step 1: Gather data

Read API logs from `{NIXTLA_API_LOG_PATH}` and configuration from `{NIXTLA_API_CONFIG_PATH}`.

### Step 2: Analyze usage

Identify usage patterns: frequency, region, and API endpoint.

### Step 3: Generate recommendations

Based on the analysis, suggest cost-effective routing and configuration changes.

### Step 4: Output report

Create a report with current usage statistics and optimization recommendations.

## Output

- **usage_report.txt**: Detailed usage statistics and analysis.
- **optimization_recommendations.txt**: Specific recommendations for cost optimization.
- **potential_savings.txt**: Estimated cost savings from implementing the recommendations.

## Error Handling

1. **Error**: `NIXTLA_API_LOG_PATH not set`
   **Solution**: `export NIXTLA_API_LOG_PATH=/path/to/your/api_logs.log`

2. **Error**: `NIXTLA_API_CONFIG_PATH not set`
   **Solution**: `export NIXTLA_API_CONFIG_PATH=/path/to/your/api_config.json`

3. **Error**: `Invalid log format`
   **Solution**: Ensure logs are in a readable format (e.g., JSON or CSV).

4. **Error**: `Insufficient data for analysis`
   **Solution**: Ensure API logs cover a reasonable time period.

## Examples

### Example 1: High latency routing

**Input**:
API logs showing high latency from US region to EU server.

**Output**:
Recommends routing US requests to US-based server to reduce latency and cost.

### Example 2: Unnecessary API calls

**Input**:
API logs showing redundant calls to the same TimeGPT endpoint.

**Output**:
Recommends caching results or optimizing API call frequency to reduce unnecessary usage.

## Resources

- Scripts: `{baseDir}/scripts/optimize.py`
- Configuration examples: `{baseDir}/config/`
