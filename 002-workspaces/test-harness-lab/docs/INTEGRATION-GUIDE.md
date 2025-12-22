# Integration Guide: Test Harness Pattern → Nixtla Production

**How to promote test harness workflows from lab → production**

---

## Overview

This guide shows how to take validated test harness workflows from `002-workspaces/test-harness-lab/` and deploy them to nixtla's production skill system at `../../003-skills/.claude/skills/`.

**Promotion path:**
```
002-workspaces/test-harness-lab/skills/nixtla-release-validation/
                ↓
../../003-skills/.claude/skills/nixtla-release-validation/
                ↓
Used in CI/CD, pre-release validation, production workflows
```

---

## Prerequisites

Before promoting a workflow to production:

1. ✅ **End-to-end tested** - Ran Exercise 1, verified all phases work
2. ✅ **Nixtla-specific** - Adapted for nixtla use case (release, benchmarks, docs)
3. ✅ **Verification script works** - Phase 4 script runs successfully with real nixtla data
4. ✅ **Documentation complete** - README, reference docs, examples
5. ✅ **Standards compliant** - Conforms to `../../000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md`

---

## Step 1: Prepare Skill for Promotion

### Update Skill Metadata

Edit your skill's `SKILL.md` frontmatter to conform to nixtla standards:

```yaml
---
name: nixtla-release-validation
description: |
  5-phase release validation workflow with empirical test verification.
  Analyzes git changes, predicts test impact, runs pytest suite, compares
  predictions vs actual results, produces go/no-go recommendation.

  Trigger: "validate release", "run release checks", "pre-release validation"
allowed-tools: Read, Write, Bash, Task, Grep
version: 1.0.0
license: MIT
author: intent solutions io <jeremy@intentsolutions.io>
tags:
  - testing
  - validation
  - release-engineering
  - nixtla
---
```

**Key requirements:**
- Use `{baseDir}/` for all file paths (not absolute paths)
- Description must be third-person, imperative voice
- Include trigger phrases users might say
- `allowed-tools` must list only tools used by orchestrator

### Update File Paths

**Replace absolute paths with {baseDir}:**

```markdown
# BEFORE (test-harness-lab version)
script_path: /home/jeremy/000-projects/nixtla/.../scripts/analyze_test_results.sh

# AFTER (production version)
script_path: {baseDir}/scripts/analyze_test_results.sh
```

**Why:** `{baseDir}` resolves to skill directory at runtime, making skill portable.

---

## Step 2: Create Production Structure

```bash
cd /home/jeremy/000-projects/nixtla/

# Create production skill directory
mkdir -p 003-skills/.claude/skills/nixtla-release-validation/{agents,references,scripts,reports}

# Copy from lab
cp -r 002-workspaces/test-harness-lab/skills/nixtla-release-validation/* \
      003-skills/.claude/skills/nixtla-release-validation/

# Verify structure
tree 003-skills/.claude/skills/nixtla-release-validation/
```

**Expected structure:**
```
003-skills/.claude/skills/nixtla-release-validation/
├── SKILL.md                  # Orchestrator (updated paths)
├── agents/
│   ├── phase_1.md
│   ├── phase_2.md
│   ├── phase_3.md
│   ├── phase_4.md
│   └── phase_5.md
├── references/
│   ├── 01-phase-1.md
│   ├── 02-phase-2.md
│   ├── 03-phase-3.md
│   ├── 04-verify-with-script.md
│   └── 05-phase-5.md
├── scripts/
│   └── analyze_test_results.sh  # Make executable!
└── reports/
    ├── runs/                 # Created at runtime
    └── _samples/             # Example outputs
```

---

## Step 3: Test in Production Location

```bash
cd 003-skills/.claude/skills/nixtla-release-validation/

# Verify script is executable
chmod +x scripts/*.sh
./scripts/analyze_test_results.sh --help || echo "Add help text"

# Test with nixtla repo
./scripts/analyze_test_results.sh \
  /home/jeremy/000-projects/nixtla \
  ./test-output

# Verify output
cat ./test-output/verification_report.json | jq .
rm -rf ./test-output
```

---

## Step 4: Integrate with Nixtla Hooks

Nixtla has `.claude/hooks/` for automation. You can trigger test harness on events:

### Pre-Commit Hook (Optional)

```bash
# .claude/hooks/pre-commit
#!/bin/bash

# Run release validation before commit
if [ -n "$(git diff --name-only | grep -E 'src/|tests/')" ]; then
  echo "Running release validation..."
  # Trigger nixtla-release-validation skill
  # (Implementation depends on how you invoke skills)
fi
```

### CI Integration

Add to `.github/workflows/`:

```yaml
name: Test Harness Validation

on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run release validation
        run: |
          # Execute test harness workflow
          # Phase 1-5 run sequentially
          # Fail PR if Phase 4 verification finds issues
```

---

## Step 5: Update Metadata

### Update Nixtla CLAUDE.md

Add reference to new skill:

```bash
cd /home/jeremy/000-projects/nixtla/

# Add to CLAUDE.md
cat >> CLAUDE.md << 'EOF'

## Test Harness Workflows

Production-ready validated workflows using multi-phase pattern:

### nixtla-release-validation
**Location:** `003-skills/.claude/skills/nixtla-release-validation/`
**Use:** Pre-release validation with empirical test verification
**Trigger:** "validate release", "run release checks"
**Output:** Go/no-go recommendation with evidence

**How to use:**
```bash
# Option 1: Manual invocation
# (Invoke via Claude Code, provide inputs)

# Option 2: Script invocation
cd 003-skills/.claude/skills/nixtla-release-validation/
# Create session directory
# Run phases 1-5 sequentially
# Review reports in session directory
```
EOF
```

### Create Beads Issue for Monitoring

```bash
cd /home/jeremy/000-projects/nixtla/

# Create production monitoring issue
bd create "Monitor nixtla-release-validation skill usage" \
  -t task \
  -p 2 \
  --description "Track: usage frequency, failure modes, false positives, user feedback. Update workflow based on real-world usage. Review after 5 releases."
```

---

## Step 6: Create Release AAR

Document the promotion in `000-docs/`:

```bash
cd /home/jeremy/000-projects/nixtla/

# Create AAR using nixtla's template
cp 000-docs/6767-b-AA-TMPL-after-action-report-template.md \
   000-docs/NNN-AA-RELT-nixtla-release-validation-v1.0.0.md

# Fill in:
# - What changed (skill promoted to production)
# - Why (automated release validation)
# - How to verify (run on last release)
# - Risks (false positives, script dependencies)
# - Next actions (monitor usage, iterate)
```

---

## Compatibility with Nixtla Standards

### SKILLS-STANDARD-COMPLETE.md Compliance

**Checklist:**
- ✅ Frontmatter includes all required fields (name, description, allowed-tools, version, license, author)
- ✅ Description is third-person, imperative, includes trigger phrases
- ✅ Uses `{baseDir}/` for all file paths
- ✅ Tags include domain-specific keywords (nixtla, time-series, validation)
- ✅ Version follows semver (1.0.0)
- ✅ License specified (MIT)

### Directory Standards Compliance

**From `002-workspaces/.directory-standards.md`:**
- ✅ Skill promoted from `002-workspaces/test-harness-lab/skills/` (prototype)
- ✅ To `003-skills/.claude/skills/` (production)
- ✅ Validated, documented, stable
- ✅ Metadata updated (CLAUDE.md, AAR created)

---

## Production Deployment Checklist

**Before marking skill as "production-ready":**

1. **Validation**
   - [ ] End-to-end test passed with real nixtla data
   - [ ] Verification script (Phase 4) works reliably
   - [ ] All reference docs tested for accuracy
   - [ ] No hardcoded paths or API keys

2. **Documentation**
   - [ ] README.md in skill directory
   - [ ] All 5 reference docs complete
   - [ ] Example session outputs in `reports/_samples/`
   - [ ] Integration examples in docs/

3. **Standards**
   - [ ] SKILL.md conforms to SKILLS-STANDARD-COMPLETE.md
   - [ ] Uses `{baseDir}/` for paths
   - [ ] Frontmatter includes all required fields
   - [ ] Tags are relevant and searchable

4. **Metadata**
   - [ ] CLAUDE.md updated with skill reference
   - [ ] Beads issue created for monitoring
   - [ ] AAR created in `000-docs/`
   - [ ] CHANGELOG.md updated

5. **Integration**
   - [ ] Scripts are executable (`chmod +x`)
   - [ ] No external dependencies (or documented)
   - [ ] Works in nixtla's CI environment
   - [ ] Hooks configured (if applicable)

---

## Rollback Plan

If skill causes issues in production:

```bash
cd /home/jeremy/000-projects/nixtla/

# 1. Remove from production
rm -rf 003-skills/.claude/skills/nixtla-release-validation/

# 2. Revert CLAUDE.md changes
git checkout CLAUDE.md

# 3. Close beads issue
bd close <issue-id> --reason "Skill rollback - needs iteration"

# 4. Return to lab for fixes
cd 002-workspaces/test-harness-lab/
# Iterate, fix issues, test again
```

---

## Post-Deployment Monitoring

**Week 1:**
- [ ] Monitor first 3 uses
- [ ] Collect feedback on false positives
- [ ] Check script runtime (should be <5 min)

**Month 1:**
- [ ] Review 10+ workflow executions
- [ ] Identify common failure patterns
- [ ] Update reference docs based on learnings

**Quarter 1:**
- [ ] Evaluate ROI (time saved vs maintenance cost)
- [ ] Consider automating more phases
- [ ] Plan v2.0 features

---

## Next Steps

**Option 1: Deploy nixtla-release-validation**
1. Build skill in `002-workspaces/test-harness-lab/skills/`
2. Test with last release (v1.6.0 → v1.7.0)
3. Follow this guide to promote
4. Monitor first 5 uses

**Option 2: Build custom workflow**
1. Use `NIXTLA-APPLICATIONS.md` for ideas
2. Follow `GUIDE-02-BUILDING-YOUR-OWN.md`
3. Test in lab, then promote

**Option 3: Contribute back**
1. Document your workflow
2. Share with nixtla team
3. Add to marketplace

---

*Complete guide for deploying test harness workflows from lab to nixtla production*
