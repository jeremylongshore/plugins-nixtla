---
name: nixtla-timegpt2-migrator
description: |
  Assists users in migrating their codebase and data pipelines from TimeGPT-1 to TimeGPT-2.
  Use when upgrading to the latest version of TimeGPT, ensuring compatibility, and optimizing performance.
  Trigger with "migrate to TimeGPT-2", "upgrade TimeGPT", "TimeGPT compatibility".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla TimeGPT-2 Migrator

Facilitates a smooth transition from TimeGPT-1 to TimeGPT-2.

## Overview

Evaluates existing TimeGPT-1 workflows for compatibility with TimeGPT-2.  Identifies potential breaking changes and suggests necessary code modifications.  Employs API checks and data schema validation. Provides updated code snippets and configuration examples for TimeGPT-2. Generates a migration report summarizing the changes required.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas
```

## Instructions

### Step 1: Analyze codebase

Read the existing codebase and TimeGPT-1 API usage using `Glob` and `Grep`.

### Step 2: Compatibility check

Run the compatibility checker script: `python {baseDir}/scripts/compatibility_check.py`.

### Step 3: Generate migration plan

Edit necessary files based on compatibility check results using `Edit`.

### Step 4: Update configuration

Write the updated configuration files for TimeGPT-2 using `Write`.

## Output

- **migration_report.txt**: Summary of necessary code and configuration changes.
- **updated_codebase/**: Modified source code with TimeGPT-2 compatible calls.
- **timegpt2_config.yaml**: Configuration file for TimeGPT-2.

## Error Handling

1. **Error**: `TimeGPT-1 API endpoint not found`
   **Solution**: Ensure TimeGPT-1 API is accessible.

2. **Error**: `Incompatible data schema`
   **Solution**:  Update data input format to match TimeGPT-2 requirements.

3. **Error**: `Missing API Key`
   **Solution**: Set the `NIXTLA_TIMEGPT_API_KEY` environment variable.

4. **Error**: `Unsupported TimeGPT-1 feature`
   **Solution**: Refactor code to use equivalent TimeGPT-2 functionality, or use alternative approaches.

## Examples

### Example 1: Basic Migration

**Input**: Existing TimeGPT-1 code using `timegpt.forecast()`

**Output**: Modified code using TimeGPT-2's equivalent function, along with updated data schema conversion if needed.

### Example 2: Configuration Update

**Input**: TimeGPT-1 configuration file `config.json`

**Output**: Updated TimeGPT-2 configuration file `timegpt2_config.yaml` with relevant parameters.

## Resources

- Scripts: `{baseDir}/scripts/`
- Documentation: `{baseDir}/docs/`
- Examples: `{baseDir}/examples/`