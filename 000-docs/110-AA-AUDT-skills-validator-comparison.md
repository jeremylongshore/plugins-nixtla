# 110-AA-AUDT-skills-validator-comparison.md

**Document Type**: Audit Report
**Created**: 2025-12-21T20:30:00-06:00 (CST)
**Status**: COMPLETE
**Purpose**: Compare nixtla skills validator with claude-code-plugins source of truth

---

## Executive Summary

**Audit Scope**: Compare `/home/jeremy/000-projects/nixtla/004-scripts/validate_skills.py` against source of truth validators in `/home/jeremy/000-projects/claude-code-plugins/`

**Finding**: nixtla validator is STRICTER in quality checks but MISSING enterprise required fields and optional field support.

**Verdict**: UPDATE REQUIRED - Add enterprise fields while preserving nixtla's strict quality standards.

---

## Source of Truth References

| File | Location | Purpose |
|------|----------|---------|
| **validate-skills-schema.py** | claude-code-plugins/scripts/ | Anthropic 2025 spec + enterprise validator |
| **6767-b-SPEC-MASTER-claude-skills-standard.md** | claude-code-plugins/000-docs/ | Complete skills specification v2.0.0 |
| **6767-c-DR-STND-claude-code-extensions-standard.md** | claude-code-plugins/000-docs/ | Enterprise standard v3.0.0 |

**Anthropic Sources**:
- https://code.claude.com/docs/en/skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills
- https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/

---

## Comparison Matrix

### Required Fields

| Field | Anthropic Spec | Enterprise Standard | nixtla Current | Status |
|-------|---------------|-------------------|---------------|--------|
| `name` | ✅ REQUIRED | ✅ REQUIRED | ✅ REQUIRED | MATCH |
| `description` | ✅ REQUIRED | ✅ REQUIRED | ✅ REQUIRED | MATCH |
| `allowed-tools` | ⚠️ OPTIONAL | ✅ REQUIRED | ✅ REQUIRED | MATCH |
| `version` | ⚠️ OPTIONAL | ✅ REQUIRED | ✅ REQUIRED | MATCH |
| `author` | ⚠️ OPTIONAL | ✅ REQUIRED | ❌ NOT REQUIRED | **MISSING** |
| `license` | ⚠️ OPTIONAL | ✅ REQUIRED | ❌ NOT REQUIRED | **MISSING** |

### Optional Fields

| Field | Anthropic Spec | Enterprise Standard | nixtla Current | Status |
|-------|---------------|-------------------|---------------|--------|
| `model` | ✅ OPTIONAL | ✅ OPTIONAL | ❌ NOT VALIDATED | **MISSING** |
| `disable-model-invocation` | ✅ OPTIONAL | ✅ OPTIONAL | ❌ NOT VALIDATED | **MISSING** |
| `mode` | ✅ OPTIONAL | ✅ OPTIONAL | ❌ NOT VALIDATED | **MISSING** |
| `tags` | ✅ OPTIONAL | ✅ OPTIONAL | ❌ NOT VALIDATED | **MISSING** |
| `metadata` | ✅ OPTIONAL | ✅ OPTIONAL | ❌ NOT VALIDATED | **MISSING** |

### Deprecated Fields

| Field | Anthropic Spec | Enterprise Standard | nixtla Current | Status |
|-------|---------------|-------------------|---------------|--------|
| `when_to_use` | ⚠️ UNDOCUMENTED | ⚠️ WARN | ❌ NOT CHECKED | **MISSING** |

### Description Quality Checks

| Check | Source of Truth | nixtla Current | Status |
|-------|----------------|---------------|--------|
| Length ≤ 1024 chars | ✅ ERROR | ✅ ERROR | MATCH |
| "Use when" phrase | ⚠️ INFO | ✅ ERROR (strict) | **STRICTER** |
| "Trigger with" phrase | ⚠️ INFO | ✅ ERROR (strict) | **STRICTER** |
| No first person | ⚠️ INFO | ✅ ERROR (strict) | **STRICTER** |
| No second person | ⚠️ INFO | ✅ ERROR (strict) | **STRICTER** |
| No reserved words | ✅ ERROR | ✅ ERROR | MATCH |
| Imperative language | ⚠️ INFO | ❌ NOT CHECKED | MISSING |

### Tool Validation

| Check | Source of Truth | nixtla Current | Status |
|-------|----------------|---------------|--------|
| Valid tools list | 13 tools (Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, Task, TodoWrite, NotebookEdit, AskUserQuestion, Skill) | ❌ Partial | **INCOMPLETE** |
| Bash scoping | ✅ Validates wildcards `Bash(git:*)` | ✅ Forbids unscoped | MATCH (stricter) |
| Wildcard syntax | ✅ Validates `(cmd:*)` | ❌ NOT VALIDATED | **MISSING** |

### Content Checks

| Check | Source of Truth | nixtla Current | Status |
|-------|----------------|---------------|--------|
| Word count limit | 5000 words (WARN at 3500) | 500 lines (ERROR) | **DIFFERENT METRIC** |
| Hardcoded paths | ✅ ERROR | ✅ ERROR | MATCH |
| Required sections | ❌ NOT CHECKED | ✅ ERROR (8 sections) | **STRICTER** |
| Scripts exist | ❌ NOT CHECKED | ✅ ERROR | **STRICTER** |

### Severity Levels

| Level | Source of Truth | nixtla Current | Status |
|-------|----------------|---------------|--------|
| ERRORS | ✅ Fatal issues | ✅ All issues | MATCH |
| WARNINGS | ✅ Best practices | ❌ NONE (zero tolerance) | **STRICTER** |
| INFO | ✅ Suggestions | ❌ NONE | **STRICTER** |

---

## Key Discrepancies

### 1. Missing Enterprise Required Fields ❌ CRITICAL

**nixtla is missing**:
```yaml
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: "MIT"
```

**Impact**: Skills not compliant with enterprise marketplace standard.

**Fix**: Add to required fields in validator.

### 2. Missing Optional Field Validation ⚠️ HIGH

**nixtla doesn't validate**:
- `model` (allows model override per skill)
- `disable-model-invocation` (manual-only invocation)
- `mode` (categorizes as mode command)
- `tags` (categorization for marketplace)
- `metadata` (custom metadata)

**Impact**: Users can't use these Anthropic-spec features. Invalid values go unchecked.

**Fix**: Add optional field validation.

### 3. No Deprecated Field Warning ⚠️ MEDIUM

**Missing**: Warning for `when_to_use` (undocumented, possibly deprecated)

**Impact**: Users may use deprecated field unknowingly.

**Fix**: Add warning when `when_to_use` detected.

### 4. Incomplete Tool Validation ⚠️ MEDIUM

**Source of truth validates 13 tools**:
Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, Task, TodoWrite, NotebookEdit, AskUserQuestion, Skill

**nixtla missing**: WebFetch, WebSearch, Task, TodoWrite, NotebookEdit, AskUserQuestion, Skill

**Impact**: Invalid tools not caught.

**Fix**: Add complete valid tools list.

### 5. Word Count vs Line Count ⚠️ LOW

**Source of truth**: 5000 word limit (with 3500 warning)
**nixtla**: 500 line limit

**Impact**: Different metrics make comparison difficult. A 5000-word document could be 300-700 lines depending on formatting.

**Decision**: KEEP both checks. Lines are easier to check and more deterministic.

---

## What nixtla Does BETTER (Keep These)

### 1. Strict Description Quality ✅

**nixtla enforces as ERRORS**:
- "Use when" phrase REQUIRED
- "Trigger with" phrase REQUIRED
- No first person ("I can", "I will")
- No second person ("You can")

**Source of truth**: These are INFO-level suggestions.

**Verdict**: KEEP strict enforcement. This ensures high-quality skill activation.

### 2. Required Sections ✅

**nixtla enforces 8 sections**:
- Title (`# `)
- Overview
- Prerequisites
- Instructions
- Output
- Error Handling
- Examples
- Resources

**Source of truth**: Not checked.

**Verdict**: KEEP. Ensures consistent, complete skill documentation.

### 3. Unscoped Bash Forbidden ✅

**nixtla**: FORBIDS `allowed-tools: "Bash"` (unscoped)
**Source of truth**: VALIDATES but allows unscoped Bash

**Verdict**: KEEP strict enforcement. Security best practice.

### 4. Scripts Existence Validation ✅

**nixtla**: Validates every `{baseDir}/scripts/...` reference points to real file
**Source of truth**: Not checked

**Verdict**: KEEP. Prevents broken references.

### 5. Zero Tolerance Mode ✅

**nixtla**: All violations are ERRORS (CI fails)
**Source of truth**: Errors/Warnings/Info levels

**Verdict**: KEEP for nixtla. This is a quality-first project.

---

## Recommended Updates

### Phase 1: Add Enterprise Required Fields (CRITICAL)

```python
# In validate_frontmatter()
required_keys = ["name", "description", "allowed-tools", "version", "author", "license"]
```

### Phase 2: Add Optional Field Validation (HIGH)

```python
# Add validation for:
# - model: "inherit" | "sonnet" | "haiku" | "claude-*"
# - disable-model-invocation: boolean
# - mode: boolean
# - tags: array of strings
# - metadata: object (any structure)
```

### Phase 3: Add Deprecated Field Warning (MEDIUM)

```python
# Check for when_to_use and warn
if 'when_to_use' in fm:
    warnings.append("[frontmatter] 'when_to_use' is undocumented/deprecated; use detailed 'description' instead")
```

### Phase 4: Complete Tool Validation (MEDIUM)

```python
VALID_TOOLS = {
    'Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep',
    'WebFetch', 'WebSearch', 'Task', 'TodoWrite',
    'NotebookEdit', 'AskUserQuestion', 'Skill'
}
```

### Phase 5: Add Severity Levels (LOW - Optional)

```python
# For better UX, separate errors/warnings/info
# But keep zero tolerance mode as default
```

---

## Implementation Plan

### Step 1: Update Validator (Immediate)

Create `004-scripts/validate_skills_v2.py` with:
- Enterprise required fields (author, license)
- Optional field validation (model, mode, tags, etc.)
- Deprecated field warnings (when_to_use)
- Complete tool validation (13 tools)
- KEEP all strict quality checks

### Step 2: Update All Skills (Immediate)

Add to all 23 skills:
```yaml
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: "MIT"
```

### Step 3: CI Integration (Immediate)

Update `.github/workflows/skills-validation.yml`:
```yaml
- name: Validate skills
  run: python 004-scripts/validate_skills_v2.py
```

### Step 4: Documentation (Short-term)

Update `000-docs/000a-skills-schema/SKILLS-STANDARD-COMPLETE.md` to reflect:
- Enterprise required fields
- Optional field usage
- nixtla-specific strict quality requirements

---

## Compliance Summary

| Category | Status | Action Required |
|----------|--------|-----------------|
| **Anthropic Spec (name, description)** | ✅ COMPLIANT | None |
| **Enterprise Fields (author, license)** | ❌ NON-COMPLIANT | Add to all 23 skills |
| **Optional Fields Support** | ❌ NOT VALIDATED | Add validation |
| **Tool Validation** | ⚠️ PARTIAL | Add missing tools |
| **Quality Checks** | ✅ EXCEEDS STANDARD | Maintain strict mode |
| **Security (Bash scoping, paths)** | ✅ EXCEEDS STANDARD | Maintain strict mode |

---

## Decision: Keep Strict Quality, Add Enterprise Compliance

**Recommendation**: Update validator to include enterprise required fields and optional field validation, while KEEPING all strict quality checks that make nixtla skills high-quality.

**Result**: nixtla skills will be:
- ✅ Anthropic-spec compliant
- ✅ Enterprise marketplace compliant
- ✅ Higher quality than source of truth requires (stricter checks)

---

## Footer

**intent solutions io — confidential IP**
**Contact**: jeremy@intentsolutions.io
**Repository**: nixtla
**Document**: 110-AA-AUDT-skills-validator-comparison.md
**Status**: AUDIT COMPLETE
**Next**: Implement validator v2 with enterprise compliance
