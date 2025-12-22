# 120-AA-AUDT: Validator Parity Review (claude-code-plugins vs nixtla)

**Date**: 2025-12-21 23:16 CST (America/Chicago)  
**Purpose**: Compare upstream `claude-code-plugins` validators with this repo’s `validate_skills_v2.py` and document gaps/merges.

---

## Executive Summary

This repo’s `004-scripts/validate_skills_v2.py` is a strict, repo-scoped fork of upstream `claude-code-plugins/scripts/validate-skills-schema.py`, with additional Nixtla quality requirements (required sections, trigger phrases, reserved words, scoped Bash enforcement). Upstream also provides a separate validator for command/agent markdown frontmatter (`validate-frontmatter.py`) that this repo does not currently run.

Key outcome: align on a “two-layer” approach:
1) **Upstream parity** for structural/spec checks (low false positives)  
2) **Nixtla strict mode** for repo standards (high signal, CI-enforced)

---

## Sources Compared

**Upstream (source of truth)**:
- `/home/jeremy/000-projects/claude-code-plugins/scripts/validate-skills-schema.py`
- `/home/jeremy/000-projects/claude-code-plugins/scripts/validate-frontmatter.py`

**This repo**:
- `004-scripts/validate_skills_v2.py`
- `004-scripts/validate-all-plugins.sh` (structure + “has frontmatter” checks)

---

## Findings (Parity + Deltas)

### 1) Validation Scope / Discovery

- **Upstream** validates skill files under `plugins/**/skills/*/SKILL.md` and optionally `skills/*/SKILL.md`.
- **Nixtla repo** uses numbered directories and validates “shipped skills” under:
  - `003-skills/.claude/skills/*/SKILL.md`
  - `005-plugins/*/skills/*/SKILL.md`
  - `.claude/skills/*/SKILL.md`

✅ This is an intentional divergence; it prevents docs/workspace SKILL.md artifacts from failing CI.

### 2) Frontmatter Enforcement Level

- **Upstream** treats enterprise fields (`allowed-tools`, `version`, `author`, `license`) as warnings.
- **Nixtla v2** treats enterprise fields as required (errors).

✅ This matches the stated enterprise/marketplace requirement and current CI posture.

### 3) Hardcoded Path Detection (False Positive Risk)

- **Upstream** removes fenced code blocks and inline code before scanning for `/home/...`, `/Users/...`, `C:\\Users\\...`.
- **Nixtla v2** scans all body lines for absolute paths and previously flagged slash-command examples unless wrapped in inline code.

⚠️ Recommendation: adopt upstream’s “ignore code blocks + inline code” approach in Nixtla v2 for path checks, and keep strict checks for truly OS-specific paths.

### 4) Nixtla Strict Quality Additions (Not Upstream)

Nixtla v2 adds CI-enforced checks that upstream does not enforce:
- Required body sections (`## Overview`, `## Prerequisites`, `## Instructions`, `## Output`, `## Error Handling`, `## Examples`, `## Resources`)
- Description must include both “Use when …” and “Trigger with …”
- Reserved words forbidden in name/description (`anthropic`, `claude`)
- Unscoped `Bash` forbidden in `allowed-tools`

✅ These are Nixtla policy choices (higher strictness than upstream).

### 5) Commands/Agents Frontmatter Validation (Missing Here)

- **Upstream** validates command and agent markdown frontmatter field constraints (description length, category enums, etc.).
- **Nixtla repo** currently only checks “frontmatter exists” for plugin command/agent markdown via `validate-all-plugins.sh`.

⚠️ Recommendation: add a lightweight command/agent frontmatter validator step (either port upstream script or call it against `005-plugins/**/{commands,agents}/*.md`).

---

## Recommended Next Actions

Tracked in Beads epic `nixtla-7ut`:
- `nixtla-7ut.2`: Implement highest-value missing checks from `000-docs/6767-o-DR-STND-lee-han-chung-claude-skills-production-standard.md`
- `nixtla-7ut.3`: Resolve `CLAUDE.md` contradictions in skill frontmatter rules

Additional follow-ups to consider:
- Add a dedicated “frontmatter validator” command for `commands/*.md` and `agents/*.md` (parity with upstream).
- Refine path checks in `validate_skills_v2.py` to ignore fenced code blocks + inline code while retaining OS-specific path detection.

---

intent solutions io — confidential IP  
Contact: jeremy@intentsolutions.io

