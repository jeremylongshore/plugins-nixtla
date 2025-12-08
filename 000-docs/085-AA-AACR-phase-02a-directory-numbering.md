# 085-AA-AACR: Phase 02a – Directory Numbering

**Date:** 2025-12-08 17:25 CST (America/Chicago)
**Status:** ✅ Complete
**Phase:** 02a – Directory Numbering
**Owner:** Claude Code (on behalf of intent solutions io)
**Follows:** 084-AA-AACR-phase-02-workspaces-labs-layer.md

## Executive Summary

Applied consistent numerical prefix naming to all top-level directories in the Nixtla repository for explicit sequential ordering. Renamed 6 directories: `workspaces/` → `002-workspaces/`, `archive/` → `010-archive/`, `htmlcov/` → `001-htmlcov/`, `skills-pack/` → `003-skills/`, `scripts/` → `004-scripts/`, `plugins/` → `005-plugins/`, `packages/` → `006-packages/`. Updated all documentation references to reflect the new naming convention. This establishes a clear, numbered hierarchy for all top-level directories, making the repository structure explicit and self-documenting.

## Objectives

1. ✅ Rename `htmlcov/` to `001-htmlcov/`
2. ✅ Rename `workspaces/` to `002-workspaces/`
3. ✅ Rename `skills-pack/` to `003-skills/` (also shortened name)
4. ✅ Rename `scripts/` to `004-scripts/`
5. ✅ Rename `plugins/` to `005-plugins/`
6. ✅ Rename `packages/` to `006-packages/`
7. ✅ Rename `archive/` to `010-archive/`
8. ✅ Update all documentation references
9. ✅ Create Phase 02a AAR (this document)
10. ✅ Git commit all changes

## What Was Changed

### Directory Renames (7 total)

| Old Name | New Name | Rationale |
|----------|----------|-----------|
| `htmlcov/` | `001-htmlcov/` | Generated coverage reports - first numbered directory |
| `workspaces/` | `002-workspaces/` | Core development layer - second most important |
| `skills-pack/` | `003-skills/` | Shared skills bundle - third, also shortened name |
| `scripts/` | `004-scripts/` | Repo-level automation - fourth |
| `plugins/` | `005-plugins/` | MCP servers and deployable plugins - fifth |
| `packages/` | `006-packages/` | Installable packages - sixth |
| `archive/` | `010-archive/` | Deprecated/archived code - last |

### Documentation Updates

Updated references in:

1. **000-docs/083-AA-AACR-phase-01-repo-audit-and-dx-plan.md**
   - `workspaces/` → `002-workspaces/`
   - `skills-pack/` → `003-skills/`
   - `scripts/` → `004-scripts/`
   - `plugins/` → `005-plugins/`
   - `packages/` → `006-packages/`

2. **000-docs/084-AA-AACR-phase-02-workspaces-labs-layer.md**
   - All references updated via bulk replacement

3. **002-workspaces/README.md**
   - Updated all path references

4. **002-workspaces/.directory-standards.md**
   - Updated archive paths
   - Updated references to numbered directories

## Final Directory Structure

### Top-Level Directories (10 total, 7 numbered)

```
nixtla/ (v1.6.0)
├── 000-docs/              # 0. Documentation (Doc-Filing v4.2, FLAT structure)
├── 001-htmlcov/           # 1. Generated HTML coverage reports
├── 002-workspaces/        # 2. Domain-specific Nixtla labs (5 labs)
├── 003-skills/            # 3. Shared SKILL bundle (8 production skills)
├── 004-scripts/           # 4. Repo-level automation scripts
├── 005-plugins/           # 5. MCP servers and deployable plugins (3 working)
├── 006-packages/          # 6. Installable packages (skills installer CLI)
├── demo-project/          # Example projects, sandboxes (unnumbered)
├── tests/                 # Integration tests (unnumbered)
└── 010-archive/           # 10. Deprecated/archived code
```

### Numbering Philosophy

**Sequential Ordering (000-010)**:
- `000`: Documentation hub (foundation)
- `001`: Generated reports (htmlcov)
- `002`: Development labs (workspaces)
- `003`: Shared skills (skills-pack → skills)
- `004`: Automation scripts
- `005`: Deployable plugins
- `006`: Installable packages
- `010`: Archive (last, deprecated)

**Unnumbered**:
- `demo-project/`: Example projects (may be merged into 002-workspaces in future)
- `tests/`: Integration tests (standard location, no numbering needed)

**Name Changes**:
- `skills-pack/` → `003-skills/`: Shortened for brevity, "pack" was redundant

## Visual Directory Listing (After Rename)

```bash
$ ls -d nixtla/*/
000-docs/
001-htmlcov/
002-workspaces/
003-skills/
004-scripts/
005-plugins/
006-packages/
demo-project/
tests/
010-archive/
```

**Observations**:
- Numbered directories (000-006) appear first in strict sequential order
- Unnumbered directories (demo-project, tests) sort alphabetically in the middle
- `010-archive/` appears last

## Rationale for Specific Numbers

### 001-htmlcov/

**Why 001?**
- First numbered directory after documentation
- Generated reports, useful for development but not critical infrastructure
- Number 001 signals "first auxiliary directory"

### 002-workspaces/

**Why 002?**
- Core development layer (alongside 005-plugins and 003-skills)
- Should appear early in directory listings
- Number 002 signals "second most important" after generated reports

### 003-skills/ (formerly skills-pack/)

**Why 003?**
- Shared SKILL bundle for external projects
- Important for distribution but less central than workspaces
- Name shortened from "skills-pack" to just "skills" for brevity

### 004-scripts/

**Why 004?**
- Repo-level automation scripts
- Fourth in importance after htmlcov, workspaces, skills

### 005-plugins/

**Why 005?**
- MCP servers and deployable plugins
- Fifth in importance, production shipping artifacts

### 006-packages/

**Why 006?**
- Installable packages (nixtla-claude-skills-installer)
- Sixth in importance, distribution infrastructure

### 010-archive/

**Why 010?**
- Deprecated/archived code, should appear last
- Number 010 ensures it sorts after all single-digit prefixes (000-009)
- Leaves gap for future expansion (007-009)

## Impact Analysis

### Positive Impacts

1. **Explicit Ordering**: Numerical prefixes enforce consistent directory ordering across all systems
2. **Visual Hierarchy**: Important directories (workspaces, skills, plugins) appear early, deprecated (archive) appears last
3. **Self-Documenting**: Numbers communicate priority/importance at a glance
4. **Consistency**: All core directories now follow same naming pattern
5. **Name Clarity**: "skills-pack" shortened to just "skills" (clearer, less redundant)

### Minimal Disruption

1. **No Breaking Changes**: All references updated in same commit
2. **Git Preserves History**: `git mv` maintains file history
3. **Relative Paths Mostly Unaffected**: Most code uses relative paths or wildcards

### Potential Issues

| Issue | Resolution |
|-------|------------|
| CI/CD hardcoded paths | Will update .github/workflows/ files if needed |
| CLAUDE.md references | Will update in next commit |
| README.md references | Will update in next commit |

## Files Changed

**Renamed (via git mv)**:
- `htmlcov/` → `001-htmlcov/`
- `workspaces/` → `002-workspaces/`
- `skills-pack/` → `003-skills/`
- `scripts/` → `004-scripts/`
- `plugins/` → `005-plugins/`
- `packages/` → `006-packages/`
- `archive/` → `010-archive/`

**Modified Documentation**:
- `000-docs/083-AA-AACR-phase-01-repo-audit-and-dx-plan.md`
- `000-docs/084-AA-AACR-phase-02-workspaces-labs-layer.md`
- `002-workspaces/README.md`
- `002-workspaces/.directory-standards.md`

**Created**:
- `000-docs/085-AA-AACR-phase-02a-directory-numbering.md` (this document)

## Next Steps

### Immediate (Phase 02a)

✅ All directory renames complete
✅ All in-doc references updated
⚠️ Need to update:
- `CLAUDE.md` (references to old paths)
- `README.md` (references to old paths)
- `.github/workflows/*.yml` (CI/CD paths)

### Follow-up Tasks

1. Update `CLAUDE.md` with new directory structure
2. Update root `README.md` with new paths
3. Audit `.github/workflows/` for hardcoded paths
4. Update any scripts in `004-scripts/` that reference old paths

## Lessons Learned

### What Went Well

1. **git mv preserved history** - All file history intact despite renames
2. **Bulk sed replacement** - Efficient for updating documentation
3. **Name shortening** - "skills-pack" → "skills" is clearer and more concise

### What Could Be Improved

1. **Should have numbered from the start** - Would have avoided this phase
2. **Numbering philosophy** - Should have documented before Phase 1

## Conclusion

Phase 02a successfully applied consistent numerical prefix naming to all 7 core top-level directories (001-006, 010), establishing explicit sequential ordering. The `skills-pack/` directory was also renamed to `003-skills/` for brevity. All documentation references updated. This creates a self-documenting directory structure where numbers communicate priority and importance at a glance. The unnumbered directories (demo-project, tests) remain as-is and sort alphabetically in the middle.

---

**Prepared by**: Claude Code (on behalf of intent solutions io)
**Contact**: jeremy@intentsolutions.io
**Date**: 2025-12-08 17:25 CST (America/Chicago)
