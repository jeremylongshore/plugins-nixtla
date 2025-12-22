# Test Harness Lab

**Version**: 1.0.0
**Status**: Learning Environment
**Owner**: intent solutions io

## Purpose

The Test Harness Lab teaches the **multi-phase validated workflow pattern** for building production-ready agent systems. Instead of one massive LLM call, workflows are decomposed into isolated phases with strict validation gates and empirical verification. Each phase produces evidence (files) + structured outputs (JSON), with Phase 4 running deterministic scripts to validate LLM conclusions against ground truth.

This workspace provides: 60+ pages of teaching guides, complete reference implementation (schema-optimization 5-phase workflow), working verification scripts, hands-on exercises, and nixtla-specific adaptations (release validation, benchmark regression detection).

## Structure

```
test-harness-lab/
├── README.md                     # This file
├── guides/                       # Learning guides (GUIDE-00 through GUIDE-03)
│   ├── GUIDE-00-START-HERE.md    # Mental model (5 min)
│   ├── GUIDE-01-PATTERN-EXPLAINED.md  # Architecture deep dive (15 min)
│   ├── GUIDE-02-BUILDING-YOUR-OWN.md  # Adaptation guide (30 min)
│   └── GUIDE-03-DEBUGGING-TIPS.md     # Troubleshooting (15 min)
├── reference-implementation/     # Schema-optimization (educational example)
│   ├── SKILL.md                  # Orchestrator
│   ├── agents/                   # 5 phase subagents
│   ├── references/               # Step-by-step procedures
│   ├── scripts/                  # Verification scripts
│   └── reports/                  # Session outputs
├── skills/                       # Nixtla-specific test harness skills
│   └── nixtla-release-validation/  # 5-phase release workflow
├── scripts/                      # Verification scripts for nixtla
│   ├── analyze_test_results.sh   # pytest verification
│   └── analyze_benchmark_results.sh  # Performance regression
├── exercises/                    # Hands-on practice
│   ├── exercise-1-run-workflow.md    # Execute reference implementation
│   ├── exercise-2-nixtla-release.md  # Adapt for nixtla releases
│   └── exercise-3-add-phase.md       # Extend workflows
├── data/                         # Example datasets (gitignored)
├── reports/                      # Generated verification reports
└── docs/                         # Integration guides
    ├── INTEGRATION-GUIDE.md      # How to deploy to nixtla .claude/skills/
    ├── VISUAL-MAP.md             # ASCII diagrams
    ├── QUICK-START.md            # 5-minute version
    └── NIXTLA-APPLICATIONS.md    # 3 concrete use cases
```

## Example Future Flows

1. **Learn the Pattern** (1 hour)
   - Read GUIDE-00-START-HERE.md to understand mental model
   - Read GUIDE-01-PATTERN-EXPLAINED.md for architecture
   - Explore reference-implementation/ to see working code

2. **Run Reference Implementation** (30 min)
   - Follow exercise-1-run-workflow.md
   - Create test data, run verification script standalone
   - Execute phases manually to understand validation gates

3. **Adapt for Nixtla Release Validation** (2 hours)
   - Follow exercise-2-nixtla-release.md
   - Build 5-phase workflow: git diff → test prediction → risk scoring → pytest verification → go/no-go
   - Run on last nixtla release (v1.6.0 → v1.7.0)

4. **Deploy to Production** (1 hour)
   - Move from test-harness-lab/skills/ to ../../003-skills/.claude/skills/
   - Follow INTEGRATION-GUIDE.md for deployment checklist
   - Create beads issue for production monitoring

5. **Build Custom Workflow** (Half day)
   - Use GUIDE-02-BUILDING-YOUR-OWN.md
   - Design 3-7 phase workflow for your use case
   - Implement verification script (Phase 4 critical)
   - Test end-to-end, deploy when ready

6. **Benchmark Regression Detection** (3 hours)
   - Adapt test harness for performance validation
   - Phase 1: Identify benchmark targets
   - Phase 2: Predict performance impact
   - Phase 3: Risk scoring
   - Phase 4: Run actual benchmarks, compare predictions vs results
   - Phase 5: Performance report with go/no-go

7. **Documentation Sync Validation** (2 hours)
   - Build workflow to verify docs match code reality
   - Phase 1: Scan code for public APIs
   - Phase 2: Extract documented APIs
   - Phase 3: Gap analysis
   - Phase 4: Run doc tests (verify examples work)
   - Phase 5: Documentation update plan

## Environment Setup

### Prerequisites
```bash
# Python 3.10+ with nixtla packages
cd /home/jeremy/000-projects/nixtla
source 005-plugins/nixtla-baseline-lab/.venv-nixtla-baseline/bin/activate

# Or create new venv
python3 -m venv .venv-test-harness
source .venv-test-harness/bin/activate
pip install pytest jq
```

### Optional Tools
```bash
# For visualization
pip install matplotlib seaborn

# For verification scripts
sudo apt-get install jq  # JSON parsing in bash
```

### No API Keys Required
Test harness pattern works offline - verification scripts use deterministic computation (no LLM calls).

## Promotion Path

**This is a learning workspace.** Skills and scripts graduate to production when:

1. ✅ **Validated** - End-to-end testing passed
2. ✅ **Documented** - Complete README, integration guide, examples
3. ✅ **Stable** - Used successfully in 3+ workflows
4. ✅ **Aligned** - Conforms to SKILLS-STANDARD-COMPLETE.md

**Promotion targets:**
- **Skills** → `../../003-skills/.claude/skills/nixtla-{workflow-name}/`
- **Scripts** → `../../005-plugins/nixtla-{plugin}/scripts/`
- **Docs** → `../../000-docs/` with NNN-CC-ABCD naming

**Promotion checklist:**
1. Create beads issue: `bd create "Promote {skill} to production"`
2. Follow INTEGRATION-GUIDE.md
3. Update marketplace metadata
4. Create release AAR in `../../000-docs/`
5. Tag version, deploy

## Learning Path

**Beginner (1 hour):**
1. Read guides/GUIDE-00-START-HERE.md
2. Explore reference-implementation/
3. Run exercises/exercise-1-run-workflow.md

**Intermediate (3 hours):**
1. Read guides/GUIDE-01-PATTERN-EXPLAINED.md
2. Run exercises/exercise-2-nixtla-release.md
3. Adapt for your own use case

**Advanced (1 day):**
1. Read guides/GUIDE-02-BUILDING-YOUR-OWN.md
2. Build custom workflow from scratch
3. Deploy to production (../../003-skills/)

## Quick Start (5 Minutes)

```bash
cd /home/jeremy/000-projects/nixtla/002-workspaces/test-harness-lab/

# Read the introduction
cat guides/GUIDE-00-START-HERE.md

# See the visual map
cat docs/VISUAL-MAP.md

# Explore reference implementation
cd reference-implementation/
cat SKILL.md  # Orchestrator logic
cat agents/phase_4.md  # Verification contract
./scripts/analyze_field_utilization.sh --help
```

## Contact

**Owner**: intent solutions io
**Email**: jeremy@intentsolutions.io
**Nixtla Repo**: /home/jeremy/000-projects/nixtla
**Created**: 2025-12-21

---

*This workspace teaches production-ready agent workflow patterns through hands-on learning.*
