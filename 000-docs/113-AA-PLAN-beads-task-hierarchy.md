# 113-AA-PLAN-beads-task-hierarchy.md

**Document Type**: Planning Document - Beads Task Breakdown
**Created**: 2025-12-21T22:00:00-06:00 (CST)
**Status**: ACTIVE - Ready to Execute
**Purpose**: Complete Beads task hierarchy for enterprise compliance + skills acceleration

---

## Executive Summary

**Created**: 1 Master Epic, 4 Epics, 46 tasks with full dependency graph

**Total Work**:
- **46 tasks** across 4 epics
- **10 ready tasks** (no blockers - can start immediately)
- **P0 tasks**: 27 (critical)
- **P1 tasks**: 16 (high value)
- **P2 tasks**: 3 (nice to have)

**Estimated Timeline**:
- Epic 1 (Enterprise Compliance): 3-4 days
- Epic 2 (P0 Skills): 5 days
- Epic 3 (P1 Skills): 5 days
- Epic 4 (Documentation): 2 days
- **Total**: ~15 days (3 weeks with buffer)

---

## Master Epic

**ID**: nixtla-bi6
**Title**: MASTER: Nixtla Enterprise Compliance + Skills Acceleration
**Priority**: P0
**Status**: open

**Depends on** (blocks until complete):
- Epic 1: Enterprise Compliance
- Epic 2: P0 Skills Development
- Epic 3: P1 Skills Development
- Epic 4: Documentation & Integration

**Outcome**: 100% enterprise compliance + 6 acceleration skills + 3-4x dev velocity

---

## Epic 1: Enterprise Compliance (Validator + Skills Update)

**ID**: nixtla-lmn
**Priority**: P0
**Timeline**: 3-4 days

### Tasks

| ID | Priority | Task | Dependencies | Est. Time |
|----|----------|------|--------------|-----------|
| **nixtla-qtj** | P0 | Update 23 production skills | 4 subtasks | 2 days |
| nixtla-9l9 | P0 | → Update 8 core skills | none | 4 hours |
| nixtla-2cb | P0 | → Update 5 core-forecasting skills | none | 2 hours |
| nixtla-t1u | P0 | → Update 10 prediction-markets skills | none | 4 hours |
| nixtla-e0m | P0 | → Run validator verification | none | 30 min |
| **nixtla-0d8** | P0 | Fix unscoped Bash (~12 skills) | none | 1 day |
| **nixtla-0r6** | P1 | Update 31 plugin-bundled skills | none | 1 day |
| **nixtla-g81** | P1 | Fix 2 root-level skills | none | 1 hour |
| **nixtla-zpv** | P0 | Update CI/CD to validator v2 | none | 30 min |
| **nixtla-qbj** | P2 | Create bulk update script | none | 2 hours |

### Ready Work (Can Start Now)

✅ **nixtla-0d8**: Fix unscoped Bash
✅ **nixtla-zpv**: Update CI/CD workflows
✅ **nixtla-9l9**: Update 8 core skills
✅ **nixtla-2cb**: Update 5 core-forecasting skills
✅ **nixtla-t1u**: Update 10 prediction-markets skills
✅ **nixtla-e0m**: Run validator verification

### Success Criteria

- [ ] All 56 SKILL.md files have `author` and `license` fields
- [ ] No unscoped Bash in `allowed-tools`
- [ ] `validate_skills_v2.py` reports 0 errors
- [ ] CI/CD uses validator v2
- [ ] Compliance rate: 100% (from 0%)

---

## Epic 2: P0 Skills Development (Critical - Week 1)

**ID**: nixtla-er8
**Priority**: P0
**Timeline**: 5 days

### Skills to Build

#### 1. nixtla-plugin-scaffolder (nixtla-jr6)

**Purpose**: Generate plugin structure from PRDs
**Impact**: 11 planned plugins → scaffolded in 1 day

| ID | Task | Est. Time |
|----|------|-----------|
| nixtla-0fz | Create SKILL.md | 2 hours |
| nixtla-aro | Write scaffold_plugin.py script | 4 hours |
| nixtla-aii | Create plugin.json template | 1 hour |
| nixtla-5pc | Test on 2 planned plugins | 2 hours |
| nixtla-e9b | Validate with validator v2 | 30 min |
| **Total** | | **10 hours** |

#### 2. nixtla-prd-to-code (nixtla-6ql)

**Purpose**: Transform PRDs into implementation checklists
**Impact**: Clear roadmap from idea → code

| ID | Task | Est. Time |
|----|------|-----------|
| nixtla-7r1 | Create SKILL.md | 2 hours |
| nixtla-82v | Write parse_prd.py script | 4 hours |
| nixtla-abg | Integrate with TodoWrite | 2 hours |
| nixtla-9r7 | Test on nixtla-roi-calculator PRD | 1 hour |
| nixtla-uqn | Validate with validator v2 | 30 min |
| **Total** | | **9.5 hours** |

#### 3. nixtla-demo-generator (nixtla-99s)

**Purpose**: Generate Jupyter notebooks for CEO demos
**Impact**: Professional demos in 5 minutes

| ID | Task | Est. Time |
|----|------|-----------|
| nixtla-uyq | Create SKILL.md | 2 hours |
| nixtla-k3b | Write generate_demo_notebook.py | 4 hours |
| nixtla-2f2 | Create 3 Jupyter notebook templates | 3 hours |
| nixtla-t6y | Test for all 3 libraries | 2 hours |
| nixtla-7p3 | Validate with validator v2 | 30 min |
| **Total** | | **11.5 hours** |

### Ready Work (Can Start Now)

✅ **nixtla-0fz**: Create SKILL.md for plugin-scaffolder
✅ **nixtla-aro**: Write scaffold_plugin.py script
✅ **nixtla-aii**: Create plugin.json template
✅ **nixtla-5pc**: Test on 2 planned plugins

### Success Criteria

- [ ] 3 skills created with 100% validator v2 compliance
- [ ] plugin-scaffolder can scaffold all 11 planned plugins
- [ ] prd-to-code creates TodoWrite tasks from PRDs
- [ ] demo-generator creates working Jupyter notebooks for TimeGPT/statsforecast/MLforecast

---

## Epic 3: P1 Skills Development (High Value - Week 2)

**ID**: nixtla-x7d
**Priority**: P1
**Timeline**: 5 days

### Skills to Build

#### 1. nixtla-test-generator (nixtla-x9w)

| ID | Task | Est. Time |
|----|------|-----------|
| nixtla-mq2 | Create SKILL.md + script + test | 8 hours |

**Impact**: 50%+ test coverage boost

#### 2. nixtla-benchmark-reporter (nixtla-yty)

| ID | Task | Est. Time |
|----|------|-----------|
| nixtla-tpk | Create SKILL.md + script + test | 6 hours |

**Impact**: Professional reports in 30 seconds

#### 3. nixtla-mcp-server-builder (nixtla-3c5)

| ID | Task | Est. Time |
|----|------|-----------|
| nixtla-y0j | Create SKILL.md + script + template + test | 8 hours |

**Impact**: MCP servers in 5 minutes

### Success Criteria

- [ ] 3 skills created with 100% validator v2 compliance
- [ ] test-generator creates pytest tests from function signatures
- [ ] benchmark-reporter transforms CSVs into markdown reports
- [ ] mcp-server-builder generates working MCP server boilerplate

---

## Epic 4: Documentation & Integration

**ID**: nixtla-ia3
**Priority**: P1
**Timeline**: 2 days

### Tasks

| ID | Priority | Task | Dependencies | Est. Time |
|----|----------|------|--------------|-----------|
| **nixtla-ooi** | P1 | Update SKILLS-STANDARD-COMPLETE.md | none | 2 hours |
| **nixtla-oza** | P1 | Update CLAUDE.md | none | 1 hour |
| **nixtla-piu** | P1 | Create AAR for Epic 1 | nixtla-lmn | 2 hours |
| **nixtla-irs** | P1 | Create AAR for Epic 2 | nixtla-er8 | 2 hours |

### Success Criteria

- [ ] SKILLS-STANDARD updated with enterprise fields documentation
- [ ] CLAUDE.md reflects validator v2 and new skills
- [ ] 2 comprehensive AARs documenting Epic 1 and Epic 2 completion

---

## Dependency Graph

```
MASTER (nixtla-bi6)
  │
  ├─ Epic 1 (nixtla-lmn) ◄─────────────┐
  │   ├─ Update 23 skills (nixtla-qtj)  │
  │   │   ├─ 8 core (nixtla-9l9)       │
  │   │   ├─ 5 forecasting (nixtla-2cb) │
  │   │   ├─ 10 markets (nixtla-t1u)   │
  │   │   └─ Verify (nixtla-e0m)       │
  │   ├─ Fix Bash (nixtla-0d8)         │
  │   ├─ 31 plugins (nixtla-0r6)       │
  │   ├─ 2 root (nixtla-g81)           │
  │   └─ CI/CD (nixtla-zpv)            │
  │                                     │
  ├─ Epic 2 (nixtla-er8) ◄─────────────┤
  │   ├─ plugin-scaffolder (nixtla-jr6) │
  │   ├─ prd-to-code (nixtla-6ql)      │
  │   └─ demo-generator (nixtla-99s)   │
  │                                     │
  ├─ Epic 3 (nixtla-x7d)               │
  │   ├─ test-generator (nixtla-x9w)   │
  │   ├─ benchmark-reporter (nixtla-yty)│
  │   └─ mcp-server-builder (nixtla-3c5)│
  │                                     │
  └─ Epic 4 (nixtla-ia3)               │
      ├─ Update SKILLS-STANDARD        │
      ├─ Update CLAUDE.md              │
      ├─ AAR Epic 1 ────────────────────┘
      └─ AAR Epic 2 ────────────────────┘
```

---

## Ready Work (Start Immediately)

**10 tasks ready** (no dependencies blocking):

### Epic 1 Tasks (6 ready)
1. **nixtla-0d8** [P0]: Fix unscoped Bash in skills
2. **nixtla-zpv** [P0]: Update CI/CD workflows to validator v2
3. **nixtla-9l9** [P0]: Update 8 core skills (author/license)
4. **nixtla-2cb** [P0]: Update 5 core-forecasting skills
5. **nixtla-t1u** [P0]: Update 10 prediction-markets skills
6. **nixtla-e0m** [P0]: Run validator verification

### Epic 2 Tasks (4 ready)
7. **nixtla-0fz** [P0]: Create SKILL.md for nixtla-plugin-scaffolder
8. **nixtla-aro** [P0]: Write scaffold_plugin.py script
9. **nixtla-aii** [P0]: Create plugin.json template
10. **nixtla-5pc** [P0]: Test nixtla-plugin-scaffolder on 2 plugins

---

## Execution Strategy

### Week 1: Epic 1 + Epic 2 P0 Skills

**Days 1-2**: Enterprise Compliance (Epic 1)
- Update 23 production skills (parallel work)
- Fix unscoped Bash
- Update CI/CD
- Verify with validator v2

**Days 3-5**: P0 Skills Development (Epic 2)
- Build nixtla-plugin-scaffolder (Day 3)
- Build nixtla-prd-to-code (Day 4)
- Build nixtla-demo-generator (Day 5)

### Week 2: Epic 3 P1 Skills

**Days 6-8**: P1 Skills Development
- Build nixtla-test-generator (Days 6-7)
- Build nixtla-benchmark-reporter (Day 7)
- Build nixtla-mcp-server-builder (Day 8)

### Week 3: Epic 4 + Buffer

**Days 9-10**: Documentation & Integration
- Update SKILLS-STANDARD (Day 9)
- Update CLAUDE.md (Day 9)
- Create AARs (Day 10)

**Days 11-15**: Buffer for issues, testing, polish

---

## Metrics to Track

| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| **Skills compliance** | 0% (0/56) | 100% (56/56) | `validate_skills_v2.py` |
| **Validator errors** | 189 | 0 | Validator output |
| **Skills count** | 23 | 31 (23+6+2) | Count in 003-skills/ |
| **Plugin dev time** | 2-3 days | 4-6 hours | Time to scaffold → working plugin |
| **Demo creation time** | 2 hours | 5 minutes | Time to working Jupyter notebook |
| **Test coverage** | ~50% | 75%+ | pytest-cov report |

---

## Risk Management

### Risk 1: Bulk Updates Break Skills

**Probability**: Medium
**Impact**: High

**Mitigation**:
- Use bulk script (nixtla-qbj) for mechanical changes
- Test validator after each batch
- Git commit after each skill category

### Risk 2: New Skills Don't Activate Properly

**Probability**: Medium
**Impact**: Medium

**Mitigation**:
- Test each skill with diverse prompts
- Use specific trigger phrases
- Document activation patterns in Examples

### Risk 3: Timeline Slippage

**Probability**: High
**Impact**: Medium

**Mitigation**:
- 15-day timeline includes 5-day buffer
- P0 tasks prioritized (can defer P1/P2)
- Can parallelize Epic 1 tasks

---

## Beads Commands Reference

```bash
# Start session
bd ready

# Start work on a task
bd update nixtla-9l9 --status in_progress

# Complete task
bd close nixtla-9l9 --reason "Updated all 8 core skills with author/license"

# View dependency graph for task
bd graph nixtla-lmn

# End session
bd sync
```

---

## Next Steps

### Immediate (Today)

1. **Start Epic 1**: Pick from 6 ready tasks
2. **Recommended order**:
   - nixtla-9l9: Update 8 core skills (4 hours)
   - nixtla-2cb: Update 5 core-forecasting (2 hours)
   - nixtla-t1u: Update 10 prediction-markets (4 hours)
   - nixtla-e0m: Run validator verification (30 min)
   - nixtla-0d8: Fix unscoped Bash (1 day)
   - nixtla-zpv: Update CI/CD (30 min)

### This Week

- Complete Epic 1 (enterprise compliance)
- Start Epic 2 (P0 skills)

### Next Week

- Complete Epic 2
- Start Epic 3 (P1 skills)

---

## Success Definition

**Project complete when**:
- ✅ MASTER epic (nixtla-bi6) closed
- ✅ All 4 epics closed
- ✅ 56 skills 100% compliant
- ✅ 6 new skills in production
- ✅ Validator v2 in CI
- ✅ Documentation updated
- ✅ AARs created

**Expected outcome**:
- Enterprise compliance achieved
- 3-4x development velocity
- Professional demos ready for Nixtla CEO
- Systematic plugin development workflow

---

## Footer

**intent solutions io — confidential IP**
**Contact**: jeremy@intentsolutions.io
**Repository**: nixtla
**Document**: 113-AA-PLAN-beads-task-hierarchy.md
**Beads Database**: `.beads/` (synced to git)
**Master Epic**: nixtla-bi6
**Total Tasks**: 46
**Ready Work**: 10 tasks
