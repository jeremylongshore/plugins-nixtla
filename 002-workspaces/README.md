# Nixtla Workspaces & Labs

This is the top-level playground and lab layer for the Nixtla plugin showcase. Each workspace is a self-contained area for a specific Nixtla domain (TimeGPT, StatsForecast, MLForecast, NeuralForecast, HierarchicalForecast). Unlike `005-plugins/` and `003-skills/` which hold shipping artifacts, `002-workspaces/` is where we design, prototype, and validate workflows before packaging them for production or external distribution.

## Visual Overview

```
002-workspaces/
├── test-harness-lab/  # 🎓 LEARNING LAB: Multi-phase validated workflow pattern
│   ├── guides/        # Teaching guides (GUIDE-00 through GUIDE-03)
│   ├── reference-implementation/  # Complete 5-phase schema-optimization example
│   ├── skills/        # Nixtla-specific test harness skills
│   ├── scripts/       # Verification scripts (pytest, benchmarks, docs)
│   ├── data/          # Example datasets for exercises
│   ├── reports/       # Session outputs from workflow runs
│   ├── docs/          # Integration guides, quick start, visual maps
│   └── exercises/     # Hands-on practice workflows
│
├── timegpt-lab/
│   ├── skills/        # TimeGPT-specific Claude Skills (prototypes)
│   ├── scripts/       # Python scripts for TimeGPT experiments
│   ├── data/          # Sample datasets, API response caches
│   ├── reports/       # Generated markdown/HTML reports
│   └── docs/          # Internal guides, best practices
│
├── statsforecast-lab/
│   ├── skills/        # StatsForecast Claude Skills (baselines, benchmarks)
│   ├── scripts/       # M4/M5 benchmark runners, model comparisons
│   ├── data/          # Benchmark datasets (M4, M5, custom)
│   ├── reports/       # Benchmark results, model performance
│   └── docs/          # Baselines documentation
│
├── mlforecast-lab/
│   ├── skills/        # MLForecast Claude Skills (ML pipelines)
│   ├── scripts/       # Feature engineering, training, prediction
│   ├── data/          # Training data, feature stores
│   ├── reports/       # ML model evaluations, hyperparameter tuning
│   └── docs/          # ML best practices
│
├── neuralforecast-lab/
│   ├── skills/        # NeuralForecast Claude Skills (deep learning + explainability)
│   ├── scripts/       # NHITS/NBEATS training, IG/SHAP computation
│   ├── data/          # Training datasets, model checkpoints
│   ├── reports/       # Explainability reports, SHAP visualizations
│   └── docs/          # Deep learning + interpretability guides
│
└── hierarchicalforecast-lab/
    ├── skills/        # HierarchicalForecast Claude Skills (reconciliation)
    ├── scripts/       # Hierarchical forecasting, coherence metrics
    ├── data/          # Multi-level hierarchical datasets
    ├── reports/       # Reconciliation results, coherence analysis
    └── docs/          # Hierarchical forecasting documentation
```

## How workspaces relate to plugins & skills-pack

- **005-plugins/**: Shipping artifacts (MCP servers, cloud functions, deployable plugins). These are production-ready code that external users can install and run.
- **003-skills/**: Shared SKILL bundle for external projects. These are stable, well-documented Claude Skills that can be installed via `nixtla-skills init`.
- **002-workspaces/**: Internal labs where prototypes, scripts, and SKILLs are developed and validated before packaging. This is the "research and development" layer.

**Promotion flow**:
1. Develop and test in `002-workspaces/<lab>/skills/` or `002-workspaces/<lab>/scripts/`
2. When stable, promote to:
   - `003-skills/.claude/skills/` (for reusable SKILLs)
   - `005-plugins/` (for deployable MCP servers or cloud functions)
3. Update marketplace metadata and release

## Who uses workspaces

- **CEO / Leadership**: Quick mental model of all 5 Nixtla domains in one place. Visual tree shows breadth of capabilities.
- **DevOps Engineers**: Wiring CI smoke tests, environment bootstrap scripts, per-domain validation. Each lab has consistent structure for automation.
- **Nixtla Engineers**: Domain "home base" for daily work. TimeGPT engineers work in `timegpt-lab/`, StatsForecast engineers in `statsforecast-lab/`, etc.

## Getting Started

Each workspace has its own README explaining:
- Purpose and scope of that domain
- How to set up the environment (API keys, dependencies)
- Example workflows and scripts
- How to promote work from the lab to production

Start by reading the workspace README for your domain of interest.

## Test Harness Lab 🎓

**Special Cross-Cutting Learning Lab**

The `test-harness-lab/` is different from the domain-specific labs. It teaches the **multi-phase validated workflow pattern** for building production-ready agent systems with empirical verification.

**What it is:**
- Teaching system with 60+ pages of guides
- Complete reference implementation (5-phase schema-optimization workflow)
- Hands-on exercises
- Nixtla-specific applications (release validation, benchmark regression, docs sync)

**Use cases for Nixtla:**
1. **Release Validation**: Automated pre-release testing with pytest verification
2. **Benchmark Regression Detection**: Performance validation with baseline comparison
3. **Documentation Sync**: Verify doc examples actually run

**How to use:**
```bash
cd test-harness-lab/
cat README.md                    # Start here
cat docs/QUICK-START.md          # 5-minute introduction
cat guides/GUIDE-00-START-HERE.md  # Deep dive
cat docs/NIXTLA-APPLICATIONS.md  # 3 concrete nixtla use cases
```

**Learning path:**
- Beginner (1 hour): Read GUIDE-00, explore reference implementation
- Intermediate (3 hours): Run Exercise 1, adapt for nixtla releases
- Advanced (1 day): Build custom workflow, deploy to 003-skills/

**Promotion:** Skills graduate from test-harness-lab → 003-skills/ when validated.

## Standards

All workspaces follow the same structure and standards defined in `.directory-standards.md`. This ensures consistency across all labs and makes it easy to onboard new engineers or add new domains in the future.
