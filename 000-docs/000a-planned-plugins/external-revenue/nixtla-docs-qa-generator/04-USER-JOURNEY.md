# Docs QA Generator - User Journey

**Plugin:** nixtla-docs-qa-generator
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Persona: DevRel Engineer

**Name:** Maria
**Role:** Developer Relations Engineer at Nixtla
**Pain Point:** Docs constantly drift from SDK, creating support tickets and frustrated users

---

## Journey Map

### Stage 1: Discovery
**Trigger:** Maria notices users complaining "the docs don't work"

**Actions:**
- Reviews recent SDK releases
- Finds docs haven't been updated in 3 weeks
- Identifies 5+ examples that no longer work
- Discovers nixtla-docs-qa-generator plugin

**Outcome:** Decides to implement automated doc QA

---

### Stage 2: Setup
**Trigger:** Maria installs the plugin

**Actions:**
```bash
# Install plugin
claude-code plugins install nixtla-docs-qa-generator

# Configure repositories
export GITHUB_TOKEN=ghp_...

# Initial scan
/docs-qa detect-changes --since v1.0.0
```

**Outcome:** Plugin connected to SDK and docs repos

---

### Stage 3: First Scan
**Trigger:** Maria runs initial drift detection

**Actions:**
```
> /docs-qa detect-changes --since v1.0.0

API Changes Detected (statsforecast v1.0.0 → v1.2.0):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEW:
  + StatsForecast.forecast_fitted_values()
  + AutoETS(seasonal_period=...)  # new parameter

CHANGED:
  ~ StatsForecast.forecast(h) → forecast(h, level=None)
  ~ AutoTheta() → AutoTheta(decomposition_type='multiplicative')

DEPRECATED:
  - StatsForecast.predict()  # use forecast() instead

Affected Documentation:
  - docs/getting-started.md (3 examples)
  - docs/models/autoets.md (2 examples)
  - docs/api-reference.md (5 entries)
```

**Outcome:** Clear visibility into what needs updating

---

### Stage 4: Generate Updates
**Trigger:** Maria generates doc patches

**Actions:**
```
> /docs-qa generate-doc-diff

Generated Patches:
━━━━━━━━━━━━━━━━
1. docs/getting-started.md
   - Line 45: Update forecast() call to include level parameter
   - Line 78: Replace deprecated predict() with forecast()

2. docs/models/autoets.md
   - Line 23: Add seasonal_period parameter documentation
   - Line 56: Update example code

Preview patch for getting-started.md? [y/n]: y

--- a/docs/getting-started.md
+++ b/docs/getting-started.md
@@ -45,7 +45,7 @@ sf = StatsForecast(models=[AutoETS()], freq='D')
 # Generate forecasts
-forecasts = sf.forecast(h=7)
+forecasts = sf.forecast(h=7, level=[80, 95])
```

**Outcome:** Precise patches ready for review

---

### Stage 5: Run Tests
**Trigger:** Maria tests all documentation examples

**Actions:**
```
> /docs-qa run-doc-tests

Executing Documentation Examples:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[PASS] docs/getting-started.md:45 - Basic forecast
[PASS] docs/getting-started.md:78 - Multi-model forecast
[FAIL] docs/models/autoets.md:23 - AutoETS with seasonality
       Error: TypeError: __init__() got an unexpected keyword argument 'season'
       Expected: 'seasonal_period'
[PASS] docs/api-reference.md:12 - StatsForecast init

Results: 18/19 passed (94.7%)
1 failing example needs attention.
```

**Outcome:** Exact failures identified with line numbers

---

### Stage 6: Auto-PR
**Trigger:** Maria creates update PR

**Actions:**
```
> /docs-qa create-update-pr

Creating Pull Request:
━━━━━━━━━━━━━━━━━━━━━
Title: docs: Update examples for statsforecast v1.2.0
Branch: docs/update-statsforecast-v1.2.0

Changes:
- getting-started.md: 2 updates
- models/autoets.md: 2 updates
- api-reference.md: 5 updates

PR created: https://github.com/nixtla/docs/pull/234

Reviewers: @maria, @tech-writer
Labels: documentation, automated
```

**Outcome:** PR ready for review, with full context

---

### Stage 7: CI Integration
**Trigger:** Set up automated drift detection

**Actions:**
```yaml
# Added to .github/workflows/docs-qa.yml
name: Documentation QA
on:
  schedule:
    - cron: '0 6 * * *'

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - name: Check for doc drift
        run: /docs-qa run-doc-tests --fail-on-drift
```

**Outcome:** Docs automatically validated daily

---

## Success Scenario

After 1 month:
- Zero doc drift at release time
- 80% reduction in "docs wrong" tickets
- Doc updates completed within 2 days of SDK release
- All examples execute successfully against current SDK
