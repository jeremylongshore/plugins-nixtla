# Documentation Quality Audit

**Audit Date**: 2025-12-11
**Scope**: 355 markdown files across repo
**Auditor**: Claude Opus 4.5
**Source of Truth Confirmed By**: User (Jeremy)

---

## Executive Summary

| Category | Count | Severity |
|----------|-------|----------|
| Version mismatches (1.6.0 instead of 1.7.0) | 12 | Medium |
| Skill count mismatches (8/21 instead of 23) | 10 | Medium |
| Wrong directory paths (plugins/, skills-pack/) | 15+ | High |

**Root Cause**: Documentation was written before repo restructure from flat directories (`plugins/`, `skills-pack/`) to numbered prefixes (`005-plugins/`, `003-skills/`).

---

## Source of Truth (Confirmed)

| Fact | Correct Value | Source |
|------|---------------|--------|
| Version | `1.7.0` | `VERSION` file |
| Skills count | `23` | `003-skills/.claude/skills/nixtla-*` |
| Skills directory | `003-skills/` | Actual filesystem |
| Plugins directory | `005-plugins/` | Actual filesystem |
| Packages directory | `006-packages/` | Actual filesystem |

---

## Critical Issues (Code/Workflow Breaking)

### 1. `plugin-validator.yml` Uses Wrong Paths
**File**: `.github/workflows/plugin-validator.yml`
**Lines**: 72, 81, 90, 103, 130, 151, 172, 215, 284, 357

**Current** (WRONG):
```yaml
plugin_json="plugins/${{ matrix.plugin }}/.claude-plugin/plugin.json"
```

**Should Be**:
```yaml
plugin_json="005-plugins/${{ matrix.plugin }}/.claude-plugin/plugin.json"
```

**Impact**: Workflow fails to find any plugins, validates nothing.

### 2. `007-tests/basic_validator.py` Uses Wrong Paths
**File**: `007-tests/basic_validator.py`
**Lines**: 13, 57

**Current** (WRONG):
```python
required = ["plugins", "000-docs", "skills-pack"]
```

**Should Be**:
```python
required = ["005-plugins", "000-docs", "003-skills"]
```

**Impact**: Test always fails - looks for non-existent directories.

---

## High Priority (Misleading Documentation)

### 3. Version 1.6.0 References (Should be 1.7.0)

| File | Line | Content |
|------|------|---------|
| `097-AA-AUDT-appaudit-devops-playbook.md` | 54 | "Version 1.6.0" |
| `097-AA-AUDT-appaudit-devops-playbook.md` | 175 | "VERSION # 1.6.0" |
| `097-AA-AUDT-appaudit-devops-playbook.md` | 185 | "Current version (1.6.0)" |
| `097-AA-AUDT-appaudit-devops-playbook.md` | 1056 | "Repository Version: 1.6.0" |
| `098-AA-AUDT-global-reality-check-audit.md` | 5 | "Repository Version: 1.6.0" |
| `098-AA-AUDT-global-reality-check-audit.md` | 41 | "Current Version: 1.6.0" |
| `098-AA-AUDT-global-reality-check-audit.md` | 68 | "VERSION # 1.6.0" |
| `098-AA-AUDT-global-reality-check-audit.md` | 503 | "VERSION (1.6.0)" |
| `105-AA-AAR-complete-skills-and-bigquery-delivery.md` | 43 | "Version: 1.6.0" |
| `105-AA-AAR-complete-skills-and-bigquery-delivery.md` | 370 | "Version: 1.6.0" |

### 4. Skill Count Mismatches (Should be 23)

| File | Line | Claims | Correct |
|------|------|--------|---------|
| `097-AA-AUDT-appaudit-devops-playbook.md` | 99 | "21 skills" | 23 |
| `097-AA-AUDT-appaudit-devops-playbook.md` | 155 | "8 skills" | 23 |
| `098-AA-AUDT-global-reality-check-audit.md` | 261 | "8 skills" | 10 (prediction markets) |
| `098-AA-AUDT-global-reality-check-audit.md` | 275 | "21 skills" | 23 |
| `098-AA-AUDT-global-reality-check-audit.md` | 367 | "21 skills" | 23 |
| `098-AA-AUDT-global-reality-check-audit.md` | 528 | "8 skills" | 10 |

---

## Medium Priority (Historical Documentation Drift)

### 5. `skills-pack/` References (Should be `003-skills/`)

These files correctly identify the bug but are now historical records:

| File | Line | Context |
|------|------|---------|
| `098-AA-AUDT-global-reality-check-audit.md` | 19 | Documents the bug being fixed |
| `098-AA-AUDT-global-reality-check-audit.md` | 206 | Shows wrong path in code |
| `098-AA-AUDT-global-reality-check-audit.md` | 307 | Recommends fix |
| `100-OD-RELS-v1-7-0-release.md` | 58 | Documents fix was applied |

**Note**: These are AAR/audit documents describing past bugs. They're historically accurate but may confuse future readers.

---

## Recommended Fixes

### Immediate (Breaking)

```bash
# Fix 1: plugin-validator.yml
sed -i 's|plugins/\$|005-plugins/$|g' .github/workflows/plugin-validator.yml

# Fix 2: basic_validator.py
sed -i 's/"plugins"/"005-plugins"/g; s/"skills-pack"/"003-skills"/g' 007-tests/basic_validator.py
```

### High Priority (Version/Count Updates)

These documents are historical (AAR/audits from Dec 8-10) and could be left as-is with a note, OR updated with "[Updated 2025-12-11: Now 1.7.0 with 23 skills]" annotations.

**Recommended Approach**: Leave historical AARs as-is (they document what was true at that time), but add header note:

```markdown
> **Historical Note**: This document was written when repo was at v1.6.0 with 21 skills.
> Current state: v1.7.0 with 23 skills. See `108-AA-AUDT-docs-code-consistency.md`.
```

### Prevention Strategy

1. **Dynamic References**: Never hardcode skill counts or version numbers in docs
   - Use: "See `VERSION` file for current version"
   - Use: "Run `ls 003-skills/.claude/skills/nixtla-* | wc -l` for current count"

2. **CI Check**: Add workflow that greps for hardcoded values and warns:
   ```bash
   # Detect hardcoded skill counts (not in code blocks)
   grep -rn "[0-9]+ skills" 000-docs/*.md | grep -v "^#\|^\`"
   ```

3. **Doc Update Checklist**: Before releases, run:
   ```bash
   VERSION=$(cat VERSION)
   SKILLS=$(ls -d 003-skills/.claude/skills/nixtla-* | wc -l)
   echo "Verify all docs reference: v$VERSION with $SKILLS skills"
   ```

---

## Files Requiring Updates

### Priority 1 (Code - Will Break CI)
- [ ] `.github/workflows/plugin-validator.yml` (10 path fixes)
- [ ] `007-tests/basic_validator.py` (2 path fixes)

### Priority 2 (Optional - Historical Accuracy)
- [ ] `097-AA-AUDT-appaudit-devops-playbook.md` (add historical note)
- [ ] `098-AA-AUDT-global-reality-check-audit.md` (add historical note)
- [ ] `105-AA-AAR-complete-skills-and-bigquery-delivery.md` (update version refs)

---

## Audit Complete

**Total Issues Found**: 37
- Critical (breaks code): 12
- High (misleading): 15
- Medium (drift): 10

**Next Steps**:
1. Fix `plugin-validator.yml` and `basic_validator.py` immediately
2. Decide on historical doc approach (leave as-is or annotate)
3. Implement prevention strategy before next release

---

*Audit completed: 2025-12-11T07:30:00Z*
*Auditor: Claude Opus 4.5*
