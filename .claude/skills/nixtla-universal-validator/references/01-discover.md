# Phase 1 Procedure: Discover Scope & Risks

## Goal

Determine the validation scope for the provided `target` and select an appropriate check profile. Prefer deterministic signals (filesystem + git state) over assumptions.

## Steps

1. Classify the target:
   - If it contains `005-plugins/` and has a plugin structure → `plugin`
   - If it contains `SKILL.md` under `003-skills/.claude/skills/` → `skill`
   - If it is the repo root (`.git` present) → `repo`

2. Capture change signals (if git is available):
   - staged/unstaged/untracked counts
   - whether changes touch `003-skills/`, `005-plugins/`, `.github/workflows/`, or `004-scripts/`

3. Recommend a profile:
   - `default` for mixed changes or unknown scope
   - `skills-only` for skill-only edits
   - `plugins-only` for plugin-only edits

4. Recommend whether to run tests:
   - Run tests when changes touch executable code (`.py`, `.ts`, `.js`) or workflows
   - Skip tests for doc-only changes unless CI gates require it

5. Write the report:
   - Include: target type, changed paths summary, recommended profile/flags
   - Do not include full diffs; include file counts and key paths only

## Output Checklist

- [ ] Report written to `{session_dir}/01-discover.md`
- [ ] JSON return matches the contract (absolute `report_path`)

