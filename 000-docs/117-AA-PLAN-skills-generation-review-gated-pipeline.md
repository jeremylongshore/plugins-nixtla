# Skills Generation Pipeline - Review-Gated Process

## 🎯 Pipeline Overview (6 Stages + Review Gate)

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: GENERATION (GitHub Actions + Vertex AI)           │
│                                                             │
│ Trigger: Manual workflow dispatch                          │
│ Action:  Generate 25 SKILL.md files via Gemini             │
│ Output:  workspace/gemini-testing/output/batch-NNN/raw/    │
│ Time:    ~3-5 minutes (with 6s pauses)                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: SCHEMA VALIDATION (Automated)                     │
│                                                             │
│ Script:  scripts/validate-skills-schema.py                 │
│ Checks:  YAML syntax, required fields, CSV format          │
│ Pass →   workspace/.../validated/                          │
│ Fail →   workspace/.../failed/                             │
│ Gate:    BLOCKS if > 20% failure rate                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: AUTO-FIX (Automated)                              │
│                                                             │
│ Script:  scripts/auto-fix-yaml.js                          │
│ Fixes:   Common YAML errors, CSV formatting                │
│ Retry:   Re-validate after fixes                           │
│ Pass →   workspace/.../fixed/                              │
│ Fail →   workspace/.../manual-review/                      │
│ Gate:    BLOCKS if > 5% still failing after auto-fix       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: QUALITY VALIDATION (Automated)                    │
│                                                             │
│ Script:  scripts/validate-skill-quality.py                 │
│ Checks:  Trigger phrases, examples, use cases              │
│ Output:  quality-report.json (scores per skill)            │
│ Pass →   workspace/.../quality-passed/                     │
│ Gate:    BLOCKS if avg quality score < 80%                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 5: STAGING (Pre-Production Review Area)              │
│                                                             │
│ Script:  scripts/stage-for-review.sh batch-NNN             │
│ Action:  Copy quality-passed/ → REVIEW-STAGING/            │
│ Output:  workspace/gemini-testing/REVIEW-STAGING/batch-NNN/│
│         ├── skills/ (25 SKILL.md files)                    │
│         ├── quality-report.json                            │
│         ├── validation-summary.json                        │
│         └── README.md (review checklist)                   │
│                                                             │
│ ⚠️  HUMAN REVIEW GATE - YOU REVIEW HERE                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
                  [APPROVAL DECISION]
                          ↓
        ┌─────────────────┴──────────────────┐
        │                                     │
        ▼ APPROVED                            ▼ REJECTED
┌──────────────────┐              ┌──────────────────────┐
│ STAGE 6: DEPLOY  │              │ STAGE R: REWORK      │
│                  │              │                      │
│ Script: deploy   │              │ Action: Move to      │
│ Target: /skills/ │              │   rework/ folder     │
│ Update: INDEX    │              │ Notify: Create issue │
└──────────────────┘              └──────────────────────┘
```

---

## 📂 Directory Structure (Where Everything Lives)

```
workspace/gemini-testing/
│
├── output/                              # Working directory (per-batch)
│   ├── batch-001/
│   │   ├── raw/                        # Stage 1: Gemini output (25 files)
│   │   ├── validated/                  # Stage 2: Schema pass
│   │   ├── failed/                     # Stage 2: Schema fail
│   │   ├── fixed/                      # Stage 3: Auto-fixed
│   │   ├── manual-review/              # Stage 3: Needs human fix
│   │   ├── quality-passed/             # Stage 4: Quality pass
│   │   └── metadata.json               # Pipeline status
│   ├── batch-002/
│   └── ... (20 batches total)
│
├── REVIEW-STAGING/                      # ← YOU REVIEW HERE (Stage 5)
│   ├── batch-001/
│   │   ├── skills/
│   │   │   ├── docker-container-debugger/
│   │   │   │   └── SKILL.md
│   │   │   ├── git-workflow-manager/
│   │   │   │   └── SKILL.md
│   │   │   └── ... (25 total)
│   │   ├── quality-report.json         # Quality scores
│   │   ├── validation-summary.json     # Schema validation results
│   │   ├── sample-test-results.json    # Test run results
│   │   └── README.md                   # Review checklist
│   └── batch-002/
│
├── APPROVED/                            # Post-review approved batches
│   └── batch-001/                      # Ready for deployment
│
├── REJECTED/                            # Needs rework
│   └── batch-003/                      # Failed review
│
└── DEPLOYED/                            # Production archive
    └── batch-001/                      # Deployed to /skills/
        └── deployment-log.json
```

---

## 🔍 Stage 5: YOUR REVIEW PROCESS

### Location
```
workspace/gemini-testing/REVIEW-STAGING/batch-NNN/
```

### What You Review

**1. Quality Report** (`quality-report.json`)
```json
{
  "batch_id": "batch-001",
  "total_skills": 25,
  "quality_scores": {
    "docker-container-debugger": {
      "overall": 92,
      "has_trigger_phrases": true,
      "has_examples": true,
      "has_use_cases": true,
      "description_quality": 90,
      "instruction_clarity": 95
    }
  },
  "batch_average": 87,
  "passing_threshold": 80,
  "status": "PASS"
}
```

**2. Validation Summary** (`validation-summary.json`)
```json
{
  "batch_id": "batch-001",
  "schema_validation": {
    "total": 25,
    "passed_first_try": 22,
    "auto_fixed": 3,
    "manual_review": 0,
    "success_rate": "100%"
  },
  "common_fixes": [
    "CSV format conversion: 3 skills",
    "Version format: 0 skills"
  ]
}
```

**3. Sample Skills** (Spot-check 10%)
```bash
# Review 2-3 random skills from the batch
cat REVIEW-STAGING/batch-001/skills/docker-container-debugger/SKILL.md
cat REVIEW-STAGING/batch-001/skills/kubernetes-pod-debugger/SKILL.md
```

**4. Review Checklist** (`README.md`)
```markdown
# Batch 001 Review Checklist

## Automated Checks (✅ Already Passed)
- [x] Schema validation: 100% pass rate
- [x] CSV format: All skills use "Read,Write,Grep" format
- [x] Quality score: 87% average (threshold: 80%)
- [x] No secrets detected
- [x] No hardcoded paths

## Manual Review (Your Tasks)
- [ ] Spot-check 3 random skills for accuracy
- [ ] Verify trigger phrases make sense
- [ ] Check instructions are clear and actionable
- [ ] Confirm tool permissions are appropriate
- [ ] Review overall batch coherence

## Approval Decision
**Approve:** `./scripts/approve-batch.sh batch-001`
**Reject:**  `./scripts/reject-batch.sh batch-001 "reason here"`
```

---

## ✅ Approval Workflow

### Option 1: Command Line
```bash
# Review the batch
cd workspace/gemini-testing/REVIEW-STAGING/batch-001/
cat README.md
cat quality-report.json

# Spot-check skills
less skills/docker-container-debugger/SKILL.md
less skills/git-workflow-manager/SKILL.md

# Approve
./scripts/approve-batch.sh batch-001

# → Moves to APPROVED/ folder
# → Creates deployment PR
# → Ready for Stage 6 (Deploy to /skills/)
```

### Option 2: Beads Task
```bash
# Batch ready for review
bd create "Review Batch 001 - 25 DevOps Skills" -p 1 \
  --description "Review batch-001 in REVIEW-STAGING/
  
Location: workspace/gemini-testing/REVIEW-STAGING/batch-001/

Tasks:
- [ ] Check quality-report.json (target: 80%+ avg)
- [ ] Review validation-summary.json (target: 100% pass)
- [ ] Spot-check 3 random skills
- [ ] Verify trigger phrases
- [ ] Approve or reject

Approve: ./scripts/approve-batch.sh batch-001
Reject:  ./scripts/reject-batch.sh batch-001 'reason'"

# When done reviewing
bd close <task-id> --reason "Batch 001 approved, ready for deploy"
```

### Option 3: GitHub PR Review
```bash
# Auto-creates PR when batch reaches REVIEW-STAGING
# Title: "Batch 001: 25 DevOps Skills for Review"
# Files changed: Shows all 25 SKILL.md files
# PR description: Quality report + validation summary
# You: Approve PR → triggers deployment
```

---

## 🚀 Stage 6: Deployment (After Your Approval)

### Trigger
```bash
./scripts/approve-batch.sh batch-001
# OR merge the review PR
```

### Actions
```bash
# 1. Deploy skills to production
scripts/deploy-skills.js --batch batch-001 --target /skills/

# 2. Update search index
scripts/generate-skills-index.js

# 3. Update category READMEs
scripts/generate-category-readmes.js

# 4. Create deployment log
# Output: workspace/gemini-testing/DEPLOYED/batch-001/deployment-log.json

# 5. Commit to main
git add skills/
git commit -m "deploy: batch-001 - 25 DevOps skills"
git push
```

### Result
```
/skills/
├── devops-basics/
│   ├── docker-container-debugger/
│   │   └── SKILL.md                    # ← NOW IN PRODUCTION
│   ├── git-workflow-manager/
│   │   └── SKILL.md
│   └── ... (25 total from batch-001)
└── SKILLS-INDEX.json                    # Updated with new skills
```

---

## 🔒 Quality Gates (Automatic Blocks)

### Gate 1: Schema Validation
**Threshold:** < 20% failure rate  
**Blocks if:** More than 5 skills fail schema validation after auto-fix  
**Action:** Pipeline stops, creates issue, notifies you

### Gate 2: Quality Score
**Threshold:** 80% average  
**Blocks if:** Batch average quality score < 80%  
**Action:** Pipeline stops, skills moved to manual-review/

### Gate 3: Security Scan
**Threshold:** 0 secrets detected  
**Blocks if:** Any hardcoded API keys, passwords, or .env files found  
**Action:** Pipeline stops immediately, critical alert

### Gate 4: Human Review (Stage 5)
**Threshold:** Your approval  
**Blocks if:** You reject the batch or don't approve  
**Action:** Batch moves to REJECTED/, issue created with your feedback

---

## 📊 Review Dashboard (Coming in Phase 5.5)

```bash
# View all batches awaiting review
./scripts/review-dashboard.sh

# Output:
┌──────────┬────────┬─────────┬──────────────┬────────┐
│ Batch    │ Skills │ Quality │ Status       │ Age    │
├──────────┼────────┼─────────┼──────────────┼────────┤
│ batch-001│   25   │  87%    │ READY        │ 2h ago │
│ batch-002│   25   │  91%    │ READY        │ 1h ago │
│ batch-003│   25   │  76%    │ BLOCKED (Q)  │ 30m    │
└──────────┴────────┴─────────┴──────────────┴────────┘

Actions:
- Review batch-001: cd workspace/gemini-testing/REVIEW-STAGING/batch-001/
- Approve batch-001: ./scripts/approve-batch.sh batch-001
- Reject batch-003: ./scripts/reject-batch.sh batch-003 "Quality too low"
```

---

## 🎯 Complete Example Flow

### Step 1: Trigger Generation
```bash
# Via GitHub Actions UI
# Workflow: "Generate Skills Batch"
# Input: batch_id = "001"
# Click: "Run workflow"
```

### Step 2: Wait for Pipeline (~10 min)
```bash
# Monitor progress
tail -f workspace/gemini-testing/output/batch-001/pipeline.log

# Stages complete automatically:
# ✓ Generation (3 min)
# ✓ Validation (30 sec)
# ✓ Auto-fix (1 min)
# ✓ Quality check (2 min)
# ✓ Staging (1 min)
```

### Step 3: Review Notification
```bash
# GitHub notification: PR created "Batch 001: Review 25 Skills"
# Slack message: "Batch 001 ready for review"
# Email: "25 skills in REVIEW-STAGING/batch-001/"
```

### Step 4: Your Review (10-15 min)
```bash
cd workspace/gemini-testing/REVIEW-STAGING/batch-001/

# Check quality
cat quality-report.json | jq '.batch_average'
# → 87

# Spot-check 3 skills
less skills/docker-container-debugger/SKILL.md  # Looks good
less skills/git-workflow-manager/SKILL.md       # Looks good
less skills/ci-cd-pipeline-builder/SKILL.md     # Looks good

# Approve
./scripts/approve-batch.sh batch-001
```

### Step 5: Deployment (Automatic)
```bash
# Script deploys to /skills/
# Updates SKILLS-INDEX.json
# Creates git commit
# Pushes to main
# ✓ Batch 001 deployed to production
```

### Step 6: Verify Production
```bash
# Check deployed skills
ls /skills/devops-basics/ | wc -l
# → 25 new skills

# Test search
node scripts/search-skills.js "docker debug"
# → docker-container-debugger found
```

---

## 📋 Scripts Reference

### Review Scripts
```bash
./scripts/review-dashboard.sh              # View all batches
./scripts/approve-batch.sh batch-001       # Approve for deployment
./scripts/reject-batch.sh batch-001 "msg"  # Reject with reason
./scripts/spot-check.sh batch-001 3        # Random sample 3 skills
```

### Deployment Scripts
```bash
./scripts/deploy-skills.js --batch 001     # Deploy to /skills/
./scripts/rollback-batch.sh batch-001      # Undo deployment
./scripts/deployment-report.sh             # View deployment history
```

### Quality Scripts
```bash
./scripts/quality-report.sh batch-001      # Detailed quality analysis
./scripts/compare-batches.sh 001 002       # Compare batch quality
./scripts/reprocess-batch.sh batch-003     # Re-run failed batch
```

---

## 🎓 Training: Your First Review

**Checklist for Batch 001:**

1. **Navigate to staging:**
   ```bash
   cd workspace/gemini-testing/REVIEW-STAGING/batch-001/
   ```

2. **Check quality score:**
   ```bash
   cat quality-report.json | jq '.batch_average'
   # Expect: 80% or higher
   ```

3. **Review validation:**
   ```bash
   cat validation-summary.json | jq '.schema_validation.success_rate'
   # Expect: "100%"
   ```

4. **Spot-check 3 skills:**
   ```bash
   ./scripts/spot-check.sh batch-001 3
   # Opens 3 random skills in $EDITOR
   ```

5. **Verify CSV format:**
   ```bash
   grep "allowed-tools:" skills/*/SKILL.md | head -5
   # Expect: allowed-tools: "Read,Write,Grep"
   # NOT: allowed-tools: [Read, Write]
   ```

6. **Check trigger phrases:**
   ```bash
   grep -A 2 "Trigger:" skills/*/SKILL.md | head -10
   # Expect: Clear, actionable trigger phrases
   ```

7. **Approve or reject:**
   ```bash
   # If all looks good:
   ./scripts/approve-batch.sh batch-001
   
   # If issues found:
   ./scripts/reject-batch.sh batch-001 "Missing trigger phrases in 3 skills"
   ```

---

**YOUR REVIEW GATE:** Stage 5 (REVIEW-STAGING/)  
**FINAL DESTINATION:** /skills/ (after your approval)  
**SAFETY:** Can rollback any deployed batch within 24 hours

