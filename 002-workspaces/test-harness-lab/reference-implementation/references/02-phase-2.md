# Phase 2 Reference: Field Utilization Analysis

## Context

This phase analyzes actual field usage patterns to identify unused and underutilized fields. You will query data samples to calculate null percentages and categorize fields by utilization level.

**Building on Phase 1:**
- Phase 1 identified schema structure and potential issues
- Phase 2 measures actual field usage through data sampling
- Results feed into Phase 3 impact assessment

**This is manual analysis** - Phase 4 will verify your conclusions empirically.

## Inputs Available

- `skill_dir`: Absolute path to schema-optimization skill directory
- `session_dir`: Absolute path to this workflow run's session directory
- `input_folder`: Path to directory containing BigQuery schema export files
- `phase1_report_path`: Absolute path to Phase 1's report file
- `sample_size`: Number of rows to analyze per table (e.g., 1000)

## Step-by-Step Procedure

### Step 1: Review Phase 1 Findings

Read the Phase 1 report to understand schema structure:

```bash
cat <phase1_report_path>
```

Extract:
- Total tables and fields
- Naming patterns identified
- Potential issues flagged
- Fields with "legacy", "deprecated", "old" in names

**Focus areas from Phase 1:**
- Tables with highest field counts (likely have unused fields)
- Fields flagged as potentially deprecated
- NULLABLE fields (candidates for utilization analysis)

### Step 2: Query Field Utilization

For each table, analyze field null percentages.

**If using BigQuery:**
```sql
SELECT
  COUNT(*) as total_rows,
  SUM(CASE WHEN field_name IS NULL THEN 1 ELSE 0 END) as null_count,
  ROUND((SUM(CASE WHEN field_name IS NULL THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as null_pct
FROM `project.dataset.table`
LIMIT <sample_size>
```

**If using CSV/local data:**
- Load sample rows (first 1000 or random sample)
- Count NULL/empty values per field
- Calculate null_pct = (null_count / total_rows) * 100

**For each field, record:**
```
{
  "table": "users",
  "field": "legacy_id",
  "total_rows": 1000,
  "null_count": 1000,
  "null_pct": 100.0,
  "data_type": "STRING",
  "mode": "NULLABLE"
}
```

### Step 3: Categorize Fields by Utilization

**Unused fields (≥90% null):**
- Null percentage ≥ 90%
- Likely safe to remove
- High priority for cleanup

**Low utilization fields (70-90% null):**
- Null percentage between 70-90%
- May be used by specific processes
- Medium priority for investigation

**High utilization fields (<70% null):**
- Null percentage < 70%
- Actively used
- Keep unless business rule changes

### Step 4: Identify Patterns

Look for patterns in unused/low-util fields:

**By naming:**
- Fields with "legacy", "old", "deprecated" prefixes
- Fields with "temp", "backup", "archive" in name
- Misspelled or outdated naming conventions

**By data type:**
- Large STRING fields that are unused (high storage cost)
- Complex STRUCT/RECORD fields with all NULL children

**By table:**
- Tables with many unused fields (schema bloat)
- Staging tables with leftover fields

### Step 5: Calculate Storage Impact

Estimate storage consumed by unused fields:

**For each unused field:**
```
storage_bytes = row_count * avg_field_size

Where:
- STRING: avg_field_size ≈ avg_string_length (or max_length if fixed)
- INTEGER: 8 bytes
- FLOAT: 8 bytes
- TIMESTAMP: 8 bytes
- BOOLEAN: 1 byte
- STRUCT/RECORD: sum of child field sizes
```

**Aggregate by category:**
```
total_unused_storage_gb = sum(storage_bytes for all unused fields) / (1024^3)
total_low_util_storage_gb = sum(storage_bytes for all low-util fields) / (1024^3)
```

### Step 6: Flag High-Impact Fields

Prioritize fields for removal based on:

**High impact (remove first):**
- 100% null AND large storage footprint
- Example: unused STRING(10000) field with 1M rows = 10GB

**Medium impact:**
- 90-99% null OR moderate storage
- Example: 95% null INTEGER field

**Low impact:**
- 70-89% null OR small storage
- Example: 75% null BOOLEAN field (negligible storage)

### Step 7: Write Report

Save to: `{session_dir}/02-field-utilization-analysis.md`

**Required sections:**

```markdown
# Phase 2: Field Utilization Analysis

**Session:** <session_id>
**Generated:** <timestamp>
**Sample Size:** <sample_size> rows per table
**Data Source:** <input_folder>

---

## Executive Summary

- Analyzed N tables with M total fields
- Found X unused fields (≥90% null)
- Found Y low utilization fields (70-90% null)
- Estimated storage waste: Z GB from unused fields
- Top priority: Remove W high-impact unused fields

---

## Methodology

Sampled <sample_size> rows from each table to calculate null percentages.
Categorized fields as unused (≥90% null), low-util (70-90% null), or high-util (<70% null).
Estimated storage impact using field data types and row counts.

---

## Field Utilization Summary

### Overall Statistics
- **Total fields analyzed:** M
- **Unused fields (≥90% null):** X (Y% of total)
- **Low utilization (70-90% null):** A (B% of total)
- **High utilization (<70% null):** C (D% of total)

### Storage Impact
- **Storage in unused fields:** Z GB
- **Storage in low-util fields:** W GB
- **Total reclaimable storage:** (Z + W) GB

---

## Unused Fields (≥90% null)

### High-Impact Removals (>1GB each)

1. **users.legacy_metadata** - 100% null
   - Data type: STRING(10000)
   - Rows: 1,000,000
   - Storage waste: 10 GB
   - Recommendation: Remove immediately
   - Risk: LOW (completely unused)

2. **orders.internal_notes** - 98.5% null
   - Data type: STRING(5000)
   - Rows: 500,000
   - Storage waste: 2.5 GB
   - Recommendation: Remove or archive remaining 1.5%
   - Risk: MEDIUM (check if 1.5% are critical records)

...

### Medium-Impact Removals (100MB - 1GB each)

1. **products.old_sku** - 95% null
   - Data type: STRING(100)
   - Rows: 2,000,000
   - Storage waste: 190 MB
   - Recommendation: Remove
   - Risk: LOW

...

### Low-Impact Removals (<100MB each)

1. **sessions.deprecated_flag** - 100% null
   - Data type: BOOLEAN
   - Rows: 10,000,000
   - Storage waste: 10 MB
   - Recommendation: Remove (low priority)
   - Risk: LOW

...

---

## Low Utilization Fields (70-90% null)

### Fields to Investigate

1. **orders.customer_notes** - 85% null
   - Data type: STRING(2000)
   - Rows: 500,000
   - Storage waste: 850 MB
   - Used in: 15% of rows (75,000 orders)
   - Recommendation: Investigate which customers/processes use this
   - Risk: MEDIUM (used by 15% - may be critical subset)

2. **products.supplier_metadata** - 78% null
   - Data type: STRING(1000)
   - Rows: 2,000,000
   - Storage waste: 1.56 GB
   - Used in: 22% of rows (440,000 products)
   - Recommendation: Check if specific product categories need this
   - Risk: MEDIUM

...

---

## Fields by Table

### Tables with Most Unused Fields

| Table | Total Fields | Unused | Low-Util | Waste (GB) |
|-------|--------------|--------|----------|------------|
| users | 87 | 23 | 12 | 15.3 |
| orders | 65 | 18 | 8 | 8.7 |
| products | 42 | 9 | 5 | 3.2 |
| sessions | 31 | 15 | 4 | 0.8 |

### Tables with Highest Storage Waste

1. **users**: 15.3 GB reclaimable (23 unused fields)
2. **orders**: 8.7 GB reclaimable (18 unused fields)
3. **products**: 3.2 GB reclaimable (9 unused fields)

---

## Patterns Identified

### By Naming Convention
- **"legacy_" prefix:** 15 fields, all 100% null
- **"old_" prefix:** 8 fields, 95-100% null
- **"deprecated_" prefix:** 5 fields, 100% null
- **"temp_" prefix:** 3 fields, 100% null

**Recommendation:** Enforce naming policy - deprecate fields before removing.

### By Data Type
- **Large STRING fields:** 12 unused, 18.5 GB waste
- **STRUCT/RECORD fields:** 5 unused, 2.3 GB waste
- **Integer/Boolean fields:** 23 unused, 0.2 GB waste

**Recommendation:** Prioritize large STRING field removals.

### By Table Pattern
- **Staging tables:** 8 tables with 30%+ unused fields
- **Dimension tables:** 5 tables with 20%+ unused fields
- **Fact tables:** 3 tables with 10%+ unused fields

**Recommendation:** Review ETL processes - may be copying unused fields.

---

## Key Findings (Machine-Readable)

```json
{
  "total_fields": 367,
  "unused_fields_count": 51,
  "low_util_fields_count": 29,
  "high_util_fields_count": 287,
  "unused_storage_gb": 28.7,
  "low_util_storage_gb": 7.3,
  "total_reclaimable_gb": 36.0,
  "top_priorities": [
    {
      "field": "users.legacy_metadata",
      "null_pct": 100.0,
      "storage_gb": 10.0,
      "recommendation": "remove"
    },
    {
      "field": "orders.internal_notes",
      "null_pct": 98.5,
      "storage_gb": 2.5,
      "recommendation": "remove_or_archive"
    }
  ]
}
```

---

## Recommendations for Phase 3

- Assess business impact of removing 51 unused fields (28.7 GB savings)
- Investigate 29 low-util fields (7.3 GB savings) - may be critical for specific use cases
- Prioritize large STRING field removals (highest storage impact)
- Review ETL processes to prevent future schema bloat
- Enforce naming convention for deprecated fields

---

*Generated by Phase 2 Agent*
*Report Path: 02-field-utilization-analysis.md*
```

### Step 8: Return JSON

Return ONLY the following JSON (no explanatory text):

```json
{
  "status": "complete",
  "report_path": "/absolute/path/to/session_dir/02-field-utilization-analysis.md",
  "utilization_summary": {
    "total_fields": 0,
    "unused_fields_count": 0,
    "low_util_fields_count": 0,
    "high_util_fields_count": 0,
    "unused_storage_gb": 0.0,
    "low_util_storage_gb": 0.0,
    "total_reclaimable_gb": 0.0,
    "top_priorities": [
      {
        "field": "table.field_name",
        "null_pct": 100.0,
        "storage_gb": 0.0,
        "recommendation": "remove"
      }
    ]
  }
}
```

**CRITICAL:**
- Write report file BEFORE returning JSON
- Use absolute path for report_path
- Include all required keys in utilization_summary
- top_priorities array should have 3-5 items (highest impact fields)
- status must be "complete" (or "error" if failed)

## Quality Checklist

Before returning JSON, verify:
- [ ] Sampled data from all tables
- [ ] Null percentages calculated accurately
- [ ] Storage estimates use correct data type sizes
- [ ] High-impact fields identified (prioritized by storage waste)
- [ ] Patterns documented with specific examples
- [ ] Machine-readable JSON block is valid
- [ ] Report file exists on disk

## Error Handling

If you encounter errors:

**Cannot access data:**
```json
{
  "status": "error",
  "error_message": "Failed to query data: <details>",
  "report_path": null,
  "utilization_summary": null
}
```

**Insufficient sample size:**
```json
{
  "status": "error",
  "error_message": "Sample size too small (<sample_size> rows): need at least 100 rows per table",
  "report_path": null,
  "utilization_summary": null
}
```

**Cannot read Phase 1 report:**
```json
{
  "status": "error",
  "error_message": "Failed to read phase1_report_path: <path>",
  "report_path": null,
  "utilization_summary": null
}
```

---

*This reference doc provides step-by-step instructions for Phase 2 agents.*
