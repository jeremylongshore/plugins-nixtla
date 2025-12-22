# Test Harness Pattern - Quick Start (5 Minutes)

**Goal:** Understand the pattern and see it in action immediately.

---

## The 30-Second Pitch

Traditional LLM workflow:
```
Agent: "I analyzed your database and found 23 unused fields"
You: "How do I verify this?"
Agent: "You could manually check..." 🤷
```

Test Harness Pattern:
```
Phase 2 (Agent): "Found 23 unused fields" [writes report]
Phase 4 (Script): Runs analyze_field_utilization.sh
Phase 4 (Agent): "Script confirmed 21/23, revised 2" [writes verification report]
You: "I can inspect reports. Script verified. Trust established." ✅
```

**Key insight:** Empirical validation via deterministic scripts (Phase 4) turns LLM text into verifiable work.

---

## The 5-Phase Pattern

```
Phase 1: Initial Analysis  → Establishes baseline
Phase 2: Deep Analysis     → Identifies patterns
Phase 3: Risk Assessment   → Evaluates impact
Phase 4: VERIFICATION ★    → RUNS REAL SCRIPT, compares vs manual
Phase 5: Recommendations   → Synthesizes validated findings
```

**Phase 4 is the "money shot"** - where manual LLM analysis meets deterministic computation.

---

## See It In Action (2 Minutes)

```bash
cd /home/jeremy/000-projects/nixtla/002-workspaces/test-harness-lab/

# 1. Look at the orchestrator (how phases chain)
head -50 reference-implementation/SKILL.md

# 2. Look at a phase contract (what it must return)
cat reference-implementation/agents/phase_4.md

# 3. Run the verification script (the "make it real" component)
cd reference-implementation/
echo '{"table":"users","schema":[{"name":"id","type":"INTEGER","mode":"REQUIRED"},{"name":"legacy_id","type":"STRING","mode":"NULLABLE"}]}' > test.json
./scripts/analyze_field_utilization.sh . test-output
cat test-output/field_utilization_report.json | jq .
rm -rf test.json test-output
```

**What you just saw:**
- Script runs deterministically (no LLM)
- Produces structured JSON output
- Can be compared against manual predictions
- This is how Phase 4 validates Phase 2-3 conclusions

---

## Real-World Applications

**For Nixtla:**
1. **Release Validation** - Run tests, compare predictions vs actual failures
2. **Benchmark Regression** - Run benchmarks, verify performance claims
3. **Doc Sync** - Run doc tests, verify examples actually work

**General:**
- Code review (lint → test → verify)
- Security audits (scan → verify with SAST tools)
- API documentation (extract → verify with endpoint tests)

---

## Next Steps (Choose Your Path)

**Path 1: Learn Deeply (1 hour)**
```bash
cat guides/GUIDE-00-START-HERE.md      # Mental model
cat guides/GUIDE-01-PATTERN-EXPLAINED.md  # Architecture
```

**Path 2: Hands-On (30 min)**
```bash
cat exercises/exercise-1-run-workflow.md  # Step-by-step walkthrough
```

**Path 3: Adapt for Nixtla (2 hours)**
```bash
cat docs/NIXTLA-APPLICATIONS.md  # 3 concrete use cases
# Then build your own 5-phase workflow
```

---

## The Core Innovation

**Before (traditional):**
- LLM analyzes
- LLM concludes
- LLM recommends
- **Trust based on vibes**

**After (test harness):**
- LLM analyzes [Phase 1-3]
- **SCRIPT verifies [Phase 4]**
- LLM synthesizes validated findings [Phase 5]
- **Trust based on evidence**

---

## Questions?

**Q: Does this work for non-data workflows?**
A: Yes! Any workflow where you can run deterministic checks. Examples: code review (run linter), security (run scanner), docs (run tests).

**Q: Is Phase 4 always a script?**
A: Usually. Can be any deterministic tool: pytest, eslint, curl, diff, etc. Key: reproducible, no LLM calls.

**Q: How long to build a custom workflow?**
A: Simple 3-phase: 2 hours. Complex 7-phase: 1 day. Nixtla release validation: ~3 hours.

---

**Ready to dive deeper?** Read `guides/GUIDE-00-START-HERE.md`

**Want hands-on practice?** Follow `exercises/exercise-1-run-workflow.md`

**Need nixtla examples?** Read `docs/NIXTLA-APPLICATIONS.md`

---

*5-minute introduction to production-ready agent workflows*
