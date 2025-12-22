# 112-AA-PLAN-strategic-skills-roadmap.md

**Document Type**: Planning Document
**Created**: 2025-12-21T21:30:00-06:00 (CST)
**Status**: DRAFT - Strategic Plan
**Purpose**: Identify high-value skills to drive nixtla project success

---

## Executive Summary

**Objective**: Determine which Claude Skills would most accelerate development and showcase value of the nixtla forecasting ecosystem.

**Context**:
- **Current**: 23 production skills (100% L4 quality)
- **Plugins**: 3 working, 11 planned
- **Purpose**: Business showcase for Nixtla CEO demonstrating Claude Code + time-series forecasting

**Recommendation**: Add **8 high-impact skills** across 3 categories to maximize development velocity and business value.

---

## Current Skill Inventory (23 Skills)

### Core Skills (8)
- nixtla-experiment-architect
- nixtla-schema-mapper
- nixtla-timegpt-lab
- nixtla-timegpt-finetune-lab
- nixtla-usage-optimizer
- nixtla-prod-pipeline-generator
- nixtla-skills-bootstrap
- nixtla-skills-index

### Core Forecasting (5)
- nixtla-anomaly-detector
- nixtla-cross-validator
- nixtla-exogenous-integrator
- nixtla-timegpt2-migrator
- nixtla-uncertainty-quantifier

### Prediction Markets (10)
- nixtla-polymarket-analyst
- nixtla-market-risk-analyzer
- nixtla-contract-schema-mapper
- nixtla-correlation-mapper
- nixtla-arbitrage-detector
- nixtla-event-impact-modeler
- nixtla-liquidity-forecaster
- nixtla-batch-forecaster
- nixtla-forecast-validator
- nixtla-model-selector

---

## Gap Analysis: What's Missing?

### Category 1: Plugin Development Acceleration 🚀

**Current gap**: No skills to help BUILD the 11 planned plugins faster.

**Missing skills**:
1. **nixtla-plugin-scaffolder** - Generate plugin structure with all required files
2. **nixtla-prd-to-code** - Transform PRD into implementation checklist
3. **nixtla-mcp-server-builder** - Generate MCP server boilerplate for plugins

**Impact if added**: 3-5x faster plugin development (11 planned plugins → executable).

### Category 2: Code Quality & Testing 🎯

**Current gap**: No skills for systematic testing or quality assurance.

**Missing skills**:
4. **nixtla-test-generator** - Generate pytest tests from function signatures
5. **nixtla-coverage-analyzer** - Identify untested code paths, suggest tests
6. **nixtla-smoke-test-builder** - Create golden task smoke tests (like baseline-lab has)

**Impact if added**: Higher quality plugins, fewer bugs, faster CI/CD.

### Category 3: Business Value Demonstration 💼

**Current gap**: Skills don't help create DEMOS or PRESENTATIONS for Nixtla CEO.

**Missing skills**:
7. **nixtla-demo-generator** - Create Jupyter notebooks showcasing forecasting workflows
8. **nixtla-benchmark-reporter** - Generate markdown reports comparing models (M4, custom datasets)

**Impact if added**: Easier to demo value to Nixtla, faster CEO buy-in.

---

## Priority Matrix

| Skill | Business Value | Dev Velocity | Complexity | Priority |
|-------|---------------|--------------|------------|----------|
| **nixtla-plugin-scaffolder** | HIGH (enables 11 plugins) | VERY HIGH | MEDIUM | **P0** |
| **nixtla-prd-to-code** | HIGH (PRDs → code) | VERY HIGH | LOW | **P0** |
| **nixtla-demo-generator** | VERY HIGH (CEO showcase) | MEDIUM | LOW | **P0** |
| **nixtla-test-generator** | MEDIUM (quality) | HIGH | MEDIUM | **P1** |
| **nixtla-benchmark-reporter** | HIGH (showcase value) | MEDIUM | LOW | **P1** |
| **nixtla-mcp-server-builder** | MEDIUM (plugin quality) | HIGH | MEDIUM | **P1** |
| **nixtla-smoke-test-builder** | MEDIUM (plugin quality) | MEDIUM | MEDIUM | **P2** |
| **nixtla-coverage-analyzer** | LOW (nice to have) | MEDIUM | HIGH | **P2** |

---

## P0 Skills (Critical - Build First)

### 1. nixtla-plugin-scaffolder

**Purpose**: Generate complete plugin structure with all enterprise-compliant files.

**Description**:
```yaml
description: |
  Generate production-ready Claude Code plugin structure with all required files
  (plugin.json, skills/, commands/, agents/, tests/, README). Creates enterprise-compliant
  scaffolding following 6767-c standard. Use when starting a new plugin or converting
  a planned plugin to implementation. Trigger with "scaffold plugin", "create plugin structure",
  "new plugin setup".
```

**Allowed tools**: `Write,Glob,Read,Bash(mkdir:*),Bash(tree:*)`

**What it does**:
1. Reads plugin PRD from `000-docs/planned-plugins/{plugin}/02-PRD.md`
2. Creates directory structure:
   ```
   005-plugins/nixtla-{name}/
   ├── .claude-plugin/plugin.json
   ├── skills/
   ├── commands/
   ├── agents/
   ├── tests/
   ├── README.md
   └── scripts/requirements.txt
   ```
3. Generates `plugin.json` with correct metadata
4. Creates placeholder files with TODOs

**Impact**: Turn 11 PRDs into plugin scaffolds in 1 hour instead of 1 day.

---

### 2. nixtla-prd-to-code

**Purpose**: Transform PRD sections into implementation tasks and code outlines.

**Description**:
```yaml
description: |
  Analyze Product Requirements Documents and generate implementation task lists with code
  outlines. Extracts functional requirements, identifies dependencies, creates step-by-step
  implementation plan. Use when converting PRD to code or planning plugin development.
  Trigger with "implement PRD", "PRD to code", "break down requirements".
```

**Allowed tools**: `Read,Write,Glob,TodoWrite`

**What it does**:
1. Reads PRD from `000-docs/planned-plugins/{plugin}/02-PRD.md`
2. Extracts functional requirements, user stories
3. Generates implementation checklist:
   - Core functionality tasks
   - API integrations needed
   - Test requirements
   - Documentation updates
4. Creates initial code outlines for key functions
5. Uses TodoWrite to track tasks

**Impact**: Clear roadmap from idea to code. No more "where do I start?"

---

### 3. nixtla-demo-generator

**Purpose**: Create Jupyter notebooks demonstrating Nixtla forecasting workflows.

**Description**:
```yaml
description: |
  Generate interactive Jupyter notebooks showcasing Nixtla forecasting workflows with
  TimeGPT, statsforecast, or MLforecast. Creates production-ready demos with data loading,
  model training, evaluation, and visualization. Use when creating demos for stakeholders,
  tutorials, or CEO presentations. Trigger with "create demo", "generate notebook", "showcase forecast".
```

**Allowed tools**: `Write,Read,Glob,Bash(python:*)`

**What it does**:
1. Asks user: which library? (TimeGPT, statsforecast, MLforecast)
2. Which dataset? (M4, custom, sample)
3. Generates notebook with:
   - Data loading and preprocessing
   - Model training with hyperparameters
   - Forecast generation
   - Evaluation metrics (sMAPE, MASE)
   - Visualization (plots with matplotlib/plotly)
   - Markdown explanations
4. Saves to `002-workspaces/{library}-lab/demos/`

**Impact**: Instant high-quality demos for Nixtla CEO. Show, don't tell.

---

## P1 Skills (High Value - Build Soon)

### 4. nixtla-test-generator

**Purpose**: Generate pytest tests from function signatures and docstrings.

**Description**:
```yaml
description: |
  Automatically generate pytest test cases from Python function signatures, type hints,
  and docstrings. Creates unit tests with fixtures, parametrization, and edge cases.
  Use when adding tests to new code or improving test coverage. Trigger with "generate tests",
  "create pytest", "write unit tests".
```

**Allowed tools**: `Read,Write,Glob,Grep,Bash(python:*)`

**What it does**:
1. User provides Python file path
2. Parses file, extracts functions with type hints
3. For each function:
   - Creates test function with fixtures
   - Generates test cases (happy path, edge cases, errors)
   - Uses type hints to create valid test data
4. Writes to `tests/test_{module}.py`
5. Runs pytest to verify tests work

**Impact**: 50%+ test coverage boost. Catch bugs before production.

---

### 5. nixtla-benchmark-reporter

**Purpose**: Generate markdown reports from benchmark metrics CSVs.

**Description**:
```yaml
description: |
  Transform benchmark metrics CSV files into formatted markdown reports with tables,
  comparisons, and insights. Supports M4, custom datasets. Calculates sMAPE, MASE,
  ranks models, highlights best performers. Use when analyzing experiment results or
  creating performance reports. Trigger with "create benchmark report", "format metrics", "compare models".
```

**Allowed tools**: `Read,Write,Glob,Bash(python:*)`

**What it does**:
1. Reads metrics CSV (sMAPE, MASE per model per dataset)
2. Creates markdown report with:
   - Summary table (models ranked by avg sMAPE)
   - Per-dataset breakdown
   - Best/worst performers
   - Statistical comparisons
3. Optionally creates plots (if matplotlib available)
4. Saves to `000-docs/` or outputs to console

**Impact**: Professional reports for stakeholders. Data → insights in 30 seconds.

---

### 6. nixtla-mcp-server-builder

**Purpose**: Generate MCP server boilerplate for plugins.

**Description**:
```yaml
description: |
  Generate Model Context Protocol (MCP) server Python code with tool definitions, handlers,
  and CLI interface. Creates production-ready server following MCP spec. Use when adding
  MCP server to plugin or creating new tools. Trigger with "create MCP server", "generate tools",
  "build protocol server".
```

**Allowed tools**: `Write,Read,Glob,Bash(python:*)`

**What it does**:
1. Asks: which tools to expose? (e.g., run_forecast, validate_data)
2. For each tool:
   - Generates schema (input/output)
   - Creates handler function with TODO comments
   - Adds error handling
3. Generates CLI entry point with argparse
4. Creates requirements.txt with MCP dependencies
5. Writes to `scripts/{plugin}_mcp.py`

**Impact**: MCP servers in 5 minutes instead of 2 hours. Consistent structure.

---

## P2 Skills (Nice to Have - Future)

### 7. nixtla-smoke-test-builder

**Purpose**: Create golden task smoke tests for plugins (like baseline-lab has).

**Allowed tools**: `Write,Read,Glob,Bash(python:*)`

**Impact**: Every plugin has offline verification test.

---

### 8. nixtla-coverage-analyzer

**Purpose**: Analyze pytest coverage reports, identify untested code, suggest test cases.

**Allowed tools**: `Read,Glob,Bash(coverage:*),Bash(pytest:*)`

**Impact**: Systematic path to 80%+ coverage.

---

## Implementation Plan

### Phase 1: P0 Skills (Week 1)

**Day 1-2: nixtla-plugin-scaffolder**
- Create SKILL.md with enterprise compliance
- Write scaffolding script in `scripts/scaffold_plugin.py`
- Test on 1-2 planned plugins
- Validate with `validate_skills_v2.py`

**Day 3-4: nixtla-prd-to-code**
- Create SKILL.md
- Write PRD parser in `scripts/parse_prd.py`
- Test on planned-plugins PRDs
- Integrate with TodoWrite

**Day 5: nixtla-demo-generator**
- Create SKILL.md
- Write notebook generator in `scripts/generate_demo_notebook.py`
- Test with M4 daily dataset
- Validate output notebooks run

### Phase 2: P1 Skills (Week 2)

**Day 1-2: nixtla-test-generator**
**Day 3: nixtla-benchmark-reporter**
**Day 4: nixtla-mcp-server-builder**
**Day 5: Validation + documentation**

### Phase 3: P2 Skills (Future)

**As needed**: nixtla-smoke-test-builder, nixtla-coverage-analyzer

---

## Success Criteria

| Metric | Baseline | Target (After P0+P1) | Measurement |
|--------|----------|---------------------|-------------|
| **Plugin dev time** | 2-3 days/plugin | 4-6 hours/plugin | Time to scaffold → working MCP server |
| **Test coverage** | ~50% | 75%+ | pytest-cov report |
| **PRD → code time** | 1 day planning | 1 hour planning | Time to implementation checklist |
| **Demo creation** | 2 hours/demo | 5 minutes/demo | Time to working Jupyter notebook |
| **Skills count** | 23 | 31 | Production skills in 003-skills/ |
| **Nixtla CEO demos** | 0 | 3+ | Jupyter notebooks ready to show |

---

## Resource Requirements

### Development Time

| Phase | Skills | Est. Time | Developer |
|-------|--------|-----------|-----------|
| P0 | 3 skills | 5 days | 1 developer |
| P1 | 3 skills | 5 days | 1 developer |
| P2 | 2 skills | 3 days | 1 developer (future) |
| **TOTAL** | **8 skills** | **13 days** | - |

### Dependencies

- ✅ No external APIs required (all local processing)
- ✅ No new libraries (use existing pytest, yaml, jinja2)
- ✅ Skills installer already exists (deploy via `nixtla-skills update`)

---

## Business Impact

### For Nixtla CEO

**Before**: "Here's some code that forecasts time series."

**After**: "Here's a Jupyter notebook showing TimeGPT beating baselines on M4 Daily with sMAPE 12.3 vs 15.7. Here's another notebook with your custom sales data showing 18% accuracy improvement. Here's the benchmark report comparing 5 models."

**Result**: Visual proof of value. Data-driven decision making.

### For Development Team

**Before**:
- Plugin development: 2-3 days
- Testing: Manual, incomplete
- Demos: 2 hours each

**After**:
- Plugin development: 4-6 hours (4x faster)
- Testing: Automated, comprehensive
- Demos: 5 minutes each (24x faster)

**Result**: Ship 11 plugins in 1 month instead of 6 months.

---

## Risks & Mitigations

### Risk 1: Skill Activation Conflicts

**Risk**: New skills may overlap with existing skills (e.g., both activate on "create plugin").

**Mitigation**:
- Use specific trigger phrases
- Test activation with diverse prompts
- Document in description when NOT to use

### Risk 2: Generated Code Quality

**Risk**: Scaffolded code may not match project standards.

**Mitigation**:
- Use templates aligned with existing plugins
- Run black/isort on generated code
- Include validation in skill

### Risk 3: Maintenance Burden

**Risk**: 8 new skills = 31 total to maintain.

**Mitigation**:
- P0 skills provide automation that reduces maintenance
- Skills installer makes updates easy
- Focus on high-leverage skills only

---

## Decision: Build P0 Now, P1 Soon

**Recommendation**:
1. Build all 3 P0 skills this week (5 days)
2. Validate impact on plugin development velocity
3. If successful, build P1 skills next week (5 days)
4. P2 skills only if clear need emerges

**Expected outcome**:
- 11 planned plugins → scaffolded in 1 day
- 3+ high-quality demos ready for Nixtla CEO
- Development velocity 3-4x faster

---

## Footer

**intent solutions io — confidential IP**
**Contact**: jeremy@intentsolutions.io
**Repository**: nixtla
**Document**: 112-AA-PLAN-strategic-skills-roadmap.md
**Status**: STRATEGIC PLAN - Awaiting approval
**Next**: User approval to begin P0 skill development
