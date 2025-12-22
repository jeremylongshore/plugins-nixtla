# Root Directory Cleanup Plan

**Created**: 2025-12-21
**Status**: PROPOSAL - Awaiting Approval
**Goal**: Organize 30+ root files into clean structure without breaking foundational architecture

---

## Current State Analysis

### Root Directory Inventory (30 files + 13 loose directories)

**Files by Category:**

#### 1. KEEP IN ROOT (Critical - Must Stay)
- `README.md` - Primary entry point
- `CLAUDE.md` - AI assistant instructions
- `CHANGELOG.md` - Version history
- `VERSION` - Current version number
- `LICENSE` - Legal requirement
- `pyproject.toml` - Python project config (PEP 517 standard)
- `pytest.ini` - Test configuration
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies
- `.gitignore`, `.gitattributes` - Git configuration
- `.editorconfig` - Editor configuration
- `.flake8` - Linter configuration

#### 2. MOVE TO 000-docs/ (Documentation)
- `CODE_OF_CONDUCT.md` → `000-docs/CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md` → `000-docs/CONTRIBUTING.md`
- `SECURITY.md` → `000-docs/SECURITY.md`
- `FOR-MAX-QUICKSTART.md` → `000-docs/FOR-MAX-QUICKSTART.md`
- `GEMINI.md` → `000-docs/GEMINI.md`
- `AGENTS.md` → `000-docs/AGENTS.md`
- `@AGENTS.md` → **DELETE** (duplicate of AGENTS.md)
- `PLUGIN_TREE.md` → `000-docs/PLUGIN_TREE.md`

#### 3. MOVE TO 008-build-artifacts/ (NEW - Build Outputs)
- `htmlcov/` → `008-build-artifacts/htmlcov/` (coverage HTML reports)
- `coverage.xml` → `008-build-artifacts/coverage.xml`
- `.coverage` → `008-build-artifacts/.coverage`
- `001-htmlcov/` → **DELETE or MERGE** (older coverage, redundant with htmlcov/)

#### 4. MOVE TO 009-temp-data/ (NEW - Temporary/Generated Data)
- `analysis_report.txt` → `009-temp-data/analysis_report.txt`
- `kalshi_data.json` → `009-temp-data/kalshi_data.json` (appears empty/stale)
- `compliance-report.json` → `009-temp-data/compliance-report.json`
- `plugins_inventory.csv` → `009-temp-data/plugins_inventory.csv`
- `skills_inventory.csv` → `009-temp-data/skills_inventory.csv`

#### 5. MOVE TO 004-scripts/ (Consolidate Scripts)
- `scripts/` directory contents → merge into `004-scripts/`
- `emailer/` → `004-scripts/emailer/` (utility script)
- **DELETE** `scripts/` after merge (duplicate of 004-scripts/)

#### 6. MOVE TO 000-docs/plugin-reference/ (Plugin Documentation)
- `plugin-docs/` → `000-docs/plugin-reference/`

#### 7. CONFIGURATION FILES - REVIEW
- `nixtla-playground-config.env` → `004-scripts/configs/nixtla-playground-config.env` (or .gitignore if secrets)
- `timegpt2_config.yaml` → `004-scripts/configs/timegpt2_config.yaml`

---

## Proposed New Structure

### Root Directory (After Cleanup - 12 essential files only)

```
nixtla/
├── .editorconfig               # Editor config
├── .flake8                     # Linter config
├── .gitattributes              # Git config
├── .gitignore                  # Git config
├── CHANGELOG.md                # Version history
├── CLAUDE.md                   # AI instructions
├── LICENSE                     # Legal
├── README.md                   # Entry point
├── VERSION                     # Current version
├── pyproject.toml              # Python project
├── pytest.ini                  # Test config
├── requirements.txt            # Dependencies
└── requirements-dev.txt        # Dev dependencies
```

### Numbered Directories (Preserved + Enhanced)

```
000-docs/                       # ALL documentation
├── AGENTS.md                   # (moved from root)
├── CODE_OF_CONDUCT.md         # (moved from root)
├── CONTRIBUTING.md            # (moved from root)
├── FOR-MAX-QUICKSTART.md      # (moved from root)
├── GEMINI.md                  # (moved from root)
├── PLUGIN_TREE.md             # (moved from root)
├── SECURITY.md                # (moved from root)
├── plugin-reference/          # (moved from root plugin-docs/)
└── [existing 000-docs content]

001-htmlcov/                    # (DEPRECATED - merge to 008-build-artifacts)

002-workspaces/                 # (unchanged)

003-skills/                     # (unchanged)

004-scripts/                    # Consolidated automation
├── configs/                    # (NEW - config files)
│   ├── nixtla-playground-config.env
│   └── timegpt2_config.yaml
├── emailer/                    # (moved from root)
└── [existing 004-scripts content]

005-plugins/                    # (unchanged)

006-packages/                   # (unchanged)

007-tests/                      # (unchanged)

008-build-artifacts/            # NEW - Build outputs
├── htmlcov/                    # Current coverage HTML
├── coverage.xml                # Coverage XML
└── .coverage                   # Coverage data

009-temp-data/                  # NEW - Temporary/generated data
├── analysis_report.txt
├── compliance-report.json
├── kalshi_data.json
├── plugins_inventory.csv
└── skills_inventory.csv

010-archive/                    # (unchanged)
```

---

## Migration Steps (Safe Execution Plan)

### Phase 1: Create New Directories
```bash
mkdir -p 008-build-artifacts
mkdir -p 009-temp-data
mkdir -p 004-scripts/configs
mkdir -p 000-docs/plugin-reference
```

### Phase 2: Move Documentation (Safe - No Breaking Changes)
```bash
# Move docs to 000-docs/
git mv CODE_OF_CONDUCT.md 000-docs/
git mv CONTRIBUTING.md 000-docs/
git mv SECURITY.md 000-docs/
git mv FOR-MAX-QUICKSTART.md 000-docs/
git mv GEMINI.md 000-docs/
git mv AGENTS.md 000-docs/
git mv PLUGIN_TREE.md 000-docs/
git mv plugin-docs 000-docs/plugin-reference

# Delete duplicate
rm @AGENTS.md
```

### Phase 3: Move Build Artifacts
```bash
# Move to 008-build-artifacts/
git mv htmlcov 008-build-artifacts/
mv coverage.xml 008-build-artifacts/
mv .coverage 008-build-artifacts/

# Handle 001-htmlcov (check if needed)
# If 001-htmlcov is obsolete:
git rm -rf 001-htmlcov
# If needed, rename:
# git mv 001-htmlcov 008-build-artifacts/htmlcov-archive
```

### Phase 4: Move Temporary Data
```bash
# Move to 009-temp-data/
mv analysis_report.txt 009-temp-data/
mv kalshi_data.json 009-temp-data/
mv compliance-report.json 009-temp-data/
mv plugins_inventory.csv 009-temp-data/
mv skills_inventory.csv 009-temp-data/
```

### Phase 5: Consolidate Scripts
```bash
# Move config files
git mv nixtla-playground-config.env 004-scripts/configs/
git mv timegpt2_config.yaml 004-scripts/configs/

# Move emailer
git mv emailer 004-scripts/

# Merge scripts/ into 004-scripts/ (if scripts/ exists and differs)
# Manual review needed - compare contents first
```

### Phase 6: Update .gitignore
```bash
# Add new directories to .gitignore
echo "008-build-artifacts/" >> .gitignore
echo "009-temp-data/" >> .gitignore
```

### Phase 7: Update CI/CD Paths
```bash
# Files to update:
# - .github/workflows/ci.yml (coverage paths)
# - pytest.ini (htmlcov path if hardcoded)
# - Any scripts referencing moved files
```

---

## Required Updates After Move

### 1. GitHub Workflows (.github/workflows/ci.yml)
```yaml
# Update coverage report paths
--cov-report=html:008-build-artifacts/htmlcov
--cov-report=xml:008-build-artifacts/coverage.xml
```

### 2. pytest.ini
```ini
# If hardcoded paths exist, update:
--cov-report=html:008-build-artifacts/htmlcov
```

### 3. Documentation Links
- Update any README.md links to moved docs
- Update CLAUDE.md references to moved files
- Update CONTRIBUTING.md if it references paths

### 4. Scripts Referencing Moved Files
- `004-scripts/` scripts that read configs
- Any automation that generates inventories

---

## Risks & Mitigation

### Risk 1: Breaking CI/CD
**Mitigation**: Test locally with pytest before committing
```bash
pytest -v --cov=005-plugins --cov-report=html:008-build-artifacts/htmlcov
```

### Risk 2: Breaking Import Paths
**Mitigation**: No Python imports affected - only data files moved

### Risk 3: Breaking External References
**Mitigation**:
- GitHub "Community Standards" expects CODE_OF_CONDUCT.md, CONTRIBUTING.md, SECURITY.md in root or .github/
- **Decision**: Keep symlinks in root for GitHub compliance OR update .github/

### Risk 4: Lost History
**Mitigation**: Use `git mv` for all tracked files to preserve history

---

## Alternative: Minimal Cleanup (Low Risk)

If full cleanup is too risky, do minimal version:

### Keep Root Clean - Just Remove Obvious Junk
```bash
# Delete clearly temporary/stale files
rm analysis_report.txt          # Stale (Dec 10)
rm kalshi_data.json             # Empty
rm @AGENTS.md                   # Duplicate

# Move just documentation
git mv CODE_OF_CONDUCT.md 000-docs/
git mv CONTRIBUTING.md 000-docs/
git mv SECURITY.md 000-docs/
git mv GEMINI.md 000-docs/

# Consolidate coverage (move newer to 001-htmlcov, delete loose htmlcov)
rm -rf htmlcov/
mv coverage.xml 001-htmlcov/
mv .coverage 001-htmlcov/

# Add to .gitignore
echo "analysis_report.txt" >> .gitignore
echo "kalshi_data.json" >> .gitignore
echo "compliance-report.json" >> .gitignore
```

This reduces root from 30 files to ~22 files with minimal risk.

---

## Recommendation: Phased Approach

**Recommended Execution:**

1. **Phase A (Zero Risk)**: Delete obvious junk + duplicates
   - `rm @AGENTS.md analysis_report.txt kalshi_data.json`

2. **Phase B (Low Risk)**: Move documentation to 000-docs/
   - Standard practice, no code impact

3. **Phase C (Medium Risk)**: Create 008-build-artifacts/, update CI
   - Test locally first

4. **Phase D (Optional)**: Create 009-temp-data/ for generated files
   - Add to .gitignore, low priority

5. **Phase E (Review Needed)**: Consolidate scripts/ and 004-scripts/
   - Requires manual comparison

---

## GitHub Community Standards Compatibility

GitHub looks for these files in root OR .github/:
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `LICENSE`

**Options:**
1. **Symlink approach**: Create symlinks in root pointing to 000-docs/
2. **GitHub standard**: Move to `.github/` instead of `000-docs/`
3. **Accept yellow badge**: Move to 000-docs/, accept "missing" badge

**Recommendation**: Use symlinks to keep root clean AND satisfy GitHub.

---

## Next Steps

**Awaiting User Decision:**

1. **Full cleanup** (proposed above)?
2. **Minimal cleanup** (delete junk only)?
3. **Phased approach** (A → B → C → D)?
4. **Different strategy**?

**After approval, I will:**
1. Execute chosen plan
2. Test CI/CD locally
3. Update all references
4. Create summary AAR document in 000-docs/
5. Update CLAUDE.md with new structure

---

**Questions for User:**

1. Is 001-htmlcov/ still needed, or can we delete/archive it?
2. Are `scripts/` and `004-scripts/` truly different, or can we consolidate?
3. Do you want GitHub "Community Standards" badges (requires root or .github/ docs)?
4. Should temp data files go in .gitignore or tracked in 009-temp-data/?
