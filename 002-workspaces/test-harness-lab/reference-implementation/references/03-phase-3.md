# Phase 3 Reference: Impact Assessment and Risk Analysis

## Context

This phase assesses the business impact and technical risk of removing unused/low-utilization fields identified in Phase 2. You will categorize fields by risk level, estimate downstream dependencies, and provide removal recommendations.

**Building on Phase 2:**
- Phase 2 identified unused fields and storage waste
- Phase 3 evaluates which fields are safe to remove
- Results feed into Phase 4 verification and Phase 5 final recommendations

**This is manual analysis** - Phase 4 will verify field utilization empirically.

## Inputs Available

- `skill_dir`: Absolute path to schema-optimization skill directory
- `session_dir`: Absolute path to this workflow run's session directory
- `phase1_report_path`: Absolute path to Phase 1's report file
- `phase2_report_path`: Absolute path to Phase 2's report file
- `codebase_path`: Optional path to application codebase for dependency analysis

## Step-by-Step Procedure

### Step 1: Review Phase 2 Findings

Read the Phase 2 report to understand field utilization:

```bash
cat <phase2_report_path>
```

Extract:
- List of unused fields (≥90% null)
- List of low utilization fields (70-90% null)
- Storage waste estimates
- Top priority fields for removal

**Create working list:**
```markdown
| Field | Null % | Storage (GB) | Phase 2 Rec | Phase 3 Risk | Final Rec |
|-------|--------|--------------|-------------|--------------|-----------|
| users.legacy_id | 100% | 10.0 | Remove | TBD | TBD |
| orders.notes | 85% | 2.5 | Investigate | TBD | TBD |
```

### Step 2: Analyze Field Dependencies

For each unused/low-util field, check for dependencies:

**Code dependencies (if codebase_path available):**
```bash
# Search for field references in code
grep -r "legacy_id" <codebase_path>/
grep -r "field_name" <codebase_path>/
```

Look for:
- SELECT statements querying the field
- INSERT/UPDATE statements writing to the field
- Application logic reading the field
- API responses including the field

**Schema dependencies:**
- Foreign key constraints
- View definitions
- Stored procedures
- Triggers
- Materialized views

**Downstream dependencies:**
- Data pipelines consuming this field
- Analytics dashboards/reports
- ML models using this field as feature
- ETL processes transforming this field

### Step 3: Categorize Risk Levels

Assign risk level to each field based on dependencies:

**LOW RISK (safe to remove):**
- 100% null AND no code references found
- No foreign key constraints
- No downstream dependencies identified
- Field name suggests deprecation ("legacy_", "old_", "deprecated_")

**MEDIUM RISK (needs investigation):**
- 90-99% null OR code references found but commented out
- Soft dependencies (analytics that could be updated)
- Field used in legacy reports (not critical)
- Recent field (created <6 months ago) - may be planned feature

**HIGH RISK (do not remove without approval):**
- 70-90% null OR active code references
- Foreign key constraints present
- Critical downstream systems depend on it
- Field used in compliance/audit reports
- Financial/legal data fields

### Step 4: Estimate Business Impact

For each field, assess business impact of removal:

**No impact:**
- Field completely unused
- No business process depends on it
- Removing it simplifies schema

**Low impact:**
- Field used by 1-2 teams in non-critical processes
- Easy to notify and migrate affected teams
- Removal improves query performance

**Medium impact:**
- Field used by 3-5 teams
- Some critical processes but workarounds exist
- Requires coordination and migration plan

**High impact:**
- Field used by >5 teams
- Critical business processes depend on it
- Regulatory/compliance requirements
- Removing it breaks core functionality

### Step 5: Calculate Savings vs Risk

For each field, calculate removal value:

**Value score = (storage_gb * 10) + (query_performance_improvement * 5) - (migration_cost * 3)**

Where:
- `storage_gb`: Storage saved by removing field
- `query_performance_improvement`: 0-10 scale (0=no change, 10=major speedup)
- `migration_cost`: 0-10 scale (0=no migration needed, 10=extensive migration)

**Prioritize fields:**
- High value (≥50 points): Remove immediately
- Medium value (20-50 points): Schedule for next sprint
- Low value (<20 points): Low priority or keep

### Step 6: Create Removal Plan

Group fields into removal waves:

**Wave 1: Quick Wins (LOW RISK + HIGH VALUE)**
- 100% null fields with no dependencies
- Large storage impact (>1GB each)
- No migration required

**Wave 2: Medium Effort (LOW RISK + MEDIUM VALUE or MEDIUM RISK + HIGH VALUE)**
- 95-100% null fields with minor dependencies
- Moderate storage impact (100MB-1GB)
- Requires notification but minimal migration

**Wave 3: High Effort (MEDIUM RISK + MEDIUM VALUE)**
- 90-95% null fields with moderate dependencies
- Requires migration scripts and team coordination

**Do Not Remove (HIGH RISK or active use):**
- Fields with <90% null
- Critical dependencies identified
- Compliance/audit fields
- Recent additions (may be planned features)

### Step 7: Write Report

Save to: `{session_dir}/03-impact-assessment.md`

**Required sections:**

```markdown
# Phase 3: Impact Assessment and Risk Analysis

**Session:** <session_id>
**Generated:** <timestamp>
**Input:** Phase 2 report
**Codebase Analyzed:** <codebase_path or "N/A">

---

## Executive Summary

- Analyzed N unused/low-util fields from Phase 2
- Categorized risk: X low, Y medium, Z high
- Recommended removal: W fields (A GB savings)
- Phased approach: 3 waves over B sprints
- Total estimated migration effort: C person-days

---

## Methodology

1. Reviewed Phase 2 field utilization findings
2. Analyzed code dependencies (grep search across codebase)
3. Assessed schema constraints and downstream dependencies
4. Categorized fields by risk level (low/medium/high)
5. Estimated business impact and migration costs
6. Created phased removal plan prioritized by value

---

## Risk Analysis Summary

### Risk Distribution
- **Low Risk:** X fields (Y GB storage)
- **Medium Risk:** A fields (B GB storage)
- **High Risk:** C fields (D GB storage - DO NOT REMOVE)

### Removal Recommendations
- **Wave 1 (Immediate):** W fields (E GB savings, F person-days)
- **Wave 2 (Next Sprint):** G fields (H GB savings, I person-days)
- **Wave 3 (Future):** J fields (K GB savings, L person-days)
- **Do Not Remove:** C fields (high risk or active use)

---

## Detailed Field Analysis

### Wave 1: Quick Wins (LOW RISK + HIGH VALUE)

#### 1. users.legacy_metadata
- **Null Percentage:** 100%
- **Storage:** 10.0 GB
- **Risk Level:** LOW
- **Dependencies Found:** None
- **Code References:** 0 active (2 commented-out in legacy migration scripts)
- **Business Impact:** None (completely unused)
- **Migration Effort:** 0 person-days
- **Recommendation:** Remove immediately
- **Value Score:** 95 points

**Removal steps:**
1. Run ALTER TABLE users DROP COLUMN legacy_metadata
2. Update documentation to reflect schema change
3. No application code changes required

#### 2. orders.internal_notes
- **Null Percentage:** 98.5%
- **Storage:** 2.5 GB
- **Risk Level:** LOW
- **Dependencies Found:** 1 legacy report (not used in 6 months)
- **Code References:** 3 in admin panel (deprecated feature)
- **Business Impact:** Low (legacy admin feature can be removed)
- **Migration Effort:** 0.5 person-days (notify admin team)
- **Recommendation:** Remove after notifying admin team
- **Value Score:** 78 points

**Removal steps:**
1. Notify admin team (1 week notice)
2. Archive 1.5% of non-null rows to separate audit table (if needed)
3. Remove deprecated admin panel code references
4. Run ALTER TABLE orders DROP COLUMN internal_notes

...

### Wave 2: Medium Effort (MEDIUM RISK or MEDIUM VALUE)

#### 1. products.supplier_metadata
- **Null Percentage:** 78%
- **Storage:** 1.56 GB
- **Risk Level:** MEDIUM
- **Dependencies Found:** Used by 2 supplier integration ETL jobs
- **Code References:** 12 in supplier sync codebase
- **Business Impact:** Medium (supplier team uses for 22% of products)
- **Migration Effort:** 3 person-days (refactor ETL to use new supplier_details table)
- **Recommendation:** Migrate to dedicated supplier_details table, then remove
- **Value Score:** 42 points

**Removal steps:**
1. Create new supplier_details table (normalized)
2. Migrate 22% of non-null data to new table
3. Update 12 code references to query new table
4. Test supplier integration ETL jobs
5. Run ALTER TABLE products DROP COLUMN supplier_metadata

...

### Wave 3: High Effort (Requires Coordination)

#### 1. orders.customer_notes
- **Null Percentage:** 85%
- **Storage:** 850 MB
- **Risk Level:** MEDIUM
- **Dependencies Found:** Used by customer support team, CRM exports, analytics dashboard
- **Code References:** 28 in customer support app
- **Business Impact:** Medium (15% of orders have notes - may be critical for those customers)
- **Migration Effort:** 8 person-days (coordinate with support, CRM, analytics teams)
- **Recommendation:** Investigate usage patterns first, then migrate to dedicated notes service
- **Value Score:** 25 points

**Investigation needed:**
1. Which customer segments use notes? (VIP/enterprise customers?)
2. Are notes required for compliance? (financial/healthcare)
3. Can we migrate to dedicated notes microservice?

...

### Do Not Remove (HIGH RISK)

#### 1. users.login_metadata
- **Null Percentage:** 72%
- **Storage:** 500 MB
- **Risk Level:** HIGH
- **Dependencies Found:** Used by security audit system, fraud detection ML model
- **Code References:** 45 in auth system, 12 in fraud detection
- **Business Impact:** HIGH (critical for security/compliance)
- **Recommendation:** DO NOT REMOVE
- **Reason:** Required for PCI compliance audits, fraud detection relies on login patterns

...

---

## Dependency Analysis

### Code References Summary

| Field | Total Refs | Active | Commented | Last Used |
|-------|------------|--------|-----------|-----------|
| users.legacy_id | 2 | 0 | 2 | 2022-03-15 |
| orders.internal_notes | 3 | 3 | 0 | 2023-06-12 |
| products.supplier_metadata | 12 | 12 | 0 | 2025-12-01 |

### Schema Constraints

- **Foreign Keys:** 0 fields have FK constraints
- **Indexes:** 5 fields have indexes (will be automatically dropped)
- **Views:** 2 fields referenced in views (need view updates)
- **Triggers:** 0 fields referenced in triggers

### Downstream Systems

- **Analytics Dashboards:** 8 fields used in dashboards (6 can be removed, 2 need updates)
- **ETL Pipelines:** 12 fields consumed by pipelines (9 unused, 3 active)
- **ML Models:** 3 fields used as features (1 deprecated model, 2 active)

---

## Migration Cost Estimates

### Wave 1: Quick Wins
- **Fields:** 23 fields
- **Storage Savings:** 18.5 GB
- **Person-Days:** 2 days (notifications + documentation)
- **Timeline:** 1 week

### Wave 2: Medium Effort
- **Fields:** 12 fields
- **Storage Savings:** 8.2 GB
- **Person-Days:** 12 days (code refactoring + migration scripts)
- **Timeline:** 1 sprint (2 weeks)

### Wave 3: High Effort
- **Fields:** 5 fields
- **Storage Savings:** 3.1 GB
- **Person-Days:** 25 days (cross-team coordination + testing)
- **Timeline:** 2 sprints (4 weeks)

### Total
- **Fields to Remove:** 40 fields
- **Total Storage Savings:** 29.8 GB
- **Total Person-Days:** 39 days
- **Total Timeline:** 7 weeks

---

## Business Impact Summary

### Affected Teams
- **Engineering:** All waves require schema migrations
- **Data Engineering:** 3 ETL pipelines need updates (Wave 2)
- **Analytics:** 6 dashboards need updates (Wave 1 & 2)
- **Customer Support:** 1 feature deprecation (Wave 3)
- **Supplier Relations:** 2 integrations need migration (Wave 2)

### Notification Plan
1. **Week 1:** Announce Wave 1 removals (email + Slack)
2. **Week 2:** Execute Wave 1 (23 fields removed)
3. **Week 3:** Announce Wave 2, coordinate with affected teams
4. **Week 4-5:** Execute Wave 2 (12 fields removed)
5. **Week 6:** Review Wave 3 requirements, get stakeholder approval
6. **Week 7:** Execute Wave 3 if approved (5 fields removed)

---

## Key Findings (Machine-Readable)

```json
{
  "risk_categories": {
    "low_risk": {
      "count": 23,
      "storage_gb": 18.5,
      "recommendation": "remove_immediately"
    },
    "medium_risk": {
      "count": 17,
      "storage_gb": 11.3,
      "recommendation": "remove_after_migration"
    },
    "high_risk": {
      "count": 11,
      "storage_gb": 6.2,
      "recommendation": "do_not_remove"
    }
  },
  "removal_waves": {
    "wave_1": {
      "fields": 23,
      "storage_gb": 18.5,
      "person_days": 2,
      "timeline_weeks": 1
    },
    "wave_2": {
      "fields": 12,
      "storage_gb": 8.2,
      "person_days": 12,
      "timeline_weeks": 2
    },
    "wave_3": {
      "fields": 5,
      "storage_gb": 3.1,
      "person_days": 25,
      "timeline_weeks": 4
    }
  },
  "total_savings_gb": 29.8,
  "total_effort_days": 39
}
```

---

## Recommendations for Phase 4

- Verify null percentages for Wave 1 fields using actual data queries (not just samples)
- Confirm zero dependencies for high-priority removals
- Run test migrations in staging environment
- Phase 4 should focus on empirically validating top 10 fields from Wave 1

---

## Recommendations for Phase 5

- Prioritize Wave 1 execution (highest value, lowest risk)
- Schedule Wave 2 for next sprint after stakeholder approval
- Defer Wave 3 pending business case review
- Monitor query performance improvements after each wave

---

*Generated by Phase 3 Agent*
*Report Path: 03-impact-assessment.md*
```

### Step 8: Return JSON

Return ONLY the following JSON (no explanatory text):

```json
{
  "status": "complete",
  "report_path": "/absolute/path/to/session_dir/03-impact-assessment.md",
  "impact_summary": {
    "risk_categories": {
      "low_risk": {
        "count": 0,
        "storage_gb": 0.0
      },
      "medium_risk": {
        "count": 0,
        "storage_gb": 0.0
      },
      "high_risk": {
        "count": 0,
        "storage_gb": 0.0
      }
    },
    "removal_waves": {
      "wave_1": {
        "fields": 0,
        "storage_gb": 0.0,
        "person_days": 0
      },
      "wave_2": {
        "fields": 0,
        "storage_gb": 0.0,
        "person_days": 0
      },
      "wave_3": {
        "fields": 0,
        "storage_gb": 0.0,
        "person_days": 0
      }
    },
    "total_savings_gb": 0.0,
    "total_effort_days": 0,
    "top_recommendations": [
      "Recommendation 1: ...",
      "Recommendation 2: ...",
      "Recommendation 3: ..."
    ]
  }
}
```

**CRITICAL:**
- Write report file BEFORE returning JSON
- Use absolute path for report_path
- Include all required keys in impact_summary
- All counts and numbers must be integers or floats (no null)
- status must be "complete" (or "error" if failed)

## Quality Checklist

Before returning JSON, verify:
- [ ] All Phase 2 fields analyzed for dependencies
- [ ] Risk levels assigned with evidence
- [ ] Migration costs estimated realistically
- [ ] Removal waves prioritized by value
- [ ] Business impact documented per team
- [ ] Machine-readable JSON block is valid
- [ ] Report file exists on disk

## Error Handling

If you encounter errors:

**Cannot read Phase 2 report:**
```json
{
  "status": "error",
  "error_message": "Failed to read phase2_report_path: <path>",
  "report_path": null,
  "impact_summary": null
}
```

**Cannot analyze codebase:**
```json
{
  "status": "error",
  "error_message": "Failed to access codebase_path: <path>",
  "report_path": null,
  "impact_summary": null
}
```

**Insufficient data for risk analysis:**
```json
{
  "status": "error",
  "error_message": "Phase 2 report missing required fields: <missing_fields>",
  "report_path": null,
  "impact_summary": null
}
```

---

*This reference doc provides step-by-step instructions for Phase 3 agents.*
