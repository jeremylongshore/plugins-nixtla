---
name: skills-expert
description: |
  Audit, debug, and improve Agent Skills without conflating the portable base
  format with repository-specific marketplace rules. Use when creating or
  repairing SKILL.md packages; trigger with "skill not loading", "frontmatter",
  "allowed-tools", or "validate this skill".
allowed-tools: 'Read, Glob, Grep, Edit, Bash(python3:*)'
version: 1.1.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
compatibility: "Claude Code with Agent Skills support. Repository-specific validation requires that repository's Python dependencies; edits require a writable target."
tags: [agent-skills, skill-authoring, validation, frontmatter, permissions]
argument-hint: '[path/to/skill] [audit | fix | explain]'
model: inherit
---

# Skills Expert

## Overview

Diagnose or improve one Agent Skill against an explicit contract. Keep the
portable Agent Skills format, Claude Code extensions, and local marketplace
requirements separate; do not present one layer's rules as universal.

## Prerequisites

- Identify the target skill directory or `SKILL.md` file.
- Confirm whether the user wants a read-only audit or an implementation.
- Locate repository instructions and validators before changing files.

## Authority and safety

- Treat current official Claude Code documentation as authoritative for Claude
  Code behavior. Use local validators for stricter repository overlays.
- `allowed-tools` pre-approves matching tools; it does not remove every other
  tool. Permission settings still govern tools not listed.
- Never add broad write or shell permissions merely to raise a score.
- Do not edit during an audit-only request. Before replacing behavior, explain
  the mismatch and preserve intentional project conventions.
- See [the source and contract map](references/skill-contract.md).

## Instructions

1. Use `Glob` to resolve the canonical package. Confirm that the directory name
   and frontmatter `name` agree, and distinguish live files from examples,
   backups, generated copies, or archived packages.
2. Read the complete `SKILL.md`, directly linked support files, applicable
   `AGENTS.md`/`CLAUDE.md`, and the validator configuration.
3. Select the contract explicitly:
   - portable Agent Skills base;
   - Claude Code invocation and permission extensions;
   - repository or marketplace overlay.
4. Check discovery metadata, activation boundaries, prerequisites, executable
   steps, permissions, validation, outputs, failures, examples, and support-file
   links. Use `Grep` to trace every claimed command, tool, path, and side effect
   back to source.
5. Run the repository's canonical validator. In this repository, use
   `python3 004-scripts/validate_skills_v2.py --fail-on-warn`. When checking an
   Intent Solutions marketplace submission, use its marketplace validator on
   the specific file rather than silently applying that overlay everywhere.
6. In fix mode, use `Edit` to make the smallest coherent change. Move durable
   detail into one level of `references/`, remove stale claims and unused
   permissions, and add focused regression tests for important contracts.
7. Rerun the target validator and package tests. Inspect the diff for unrelated
   rewrites and report residual warnings separately from failures.

## Validation

- Every support-file link resolves relative to the skill directory.
- Every pre-approved tool is used by the workflow and no required tool is
  omitted.
- Examples demonstrate the real workflow rather than fabricated output.
- Destructive or external side effects have explicit confirmation boundaries.
- The final report names the standard and validator version actually used.

## Output

Return the canonical path, selected contract, findings by severity, exact
changes (when authorized), validator/test receipts, remaining risks, and a clear
pass/fail result. Do not call a skill "valid" without naming the validation tier.

## Error Handling

- **Multiple live copies:** identify the source of truth before editing and
  test any required mirrors for drift.
- **Missing validator:** perform a manual structural audit and label it as such.
- **Conflicting rules:** follow the higher-precedence repository instruction and
  describe the conflict.
- **Unverified platform behavior:** consult current official documentation or
  state the uncertainty; do not preserve folklore as fact.
- **Unsafe requested permissions:** narrow the workflow or require explicit
  approval instead of granting blanket access.

## Examples

These requests demonstrate both read-only and authorized-fix modes:

```text
Audit .claude/skills/release/SKILL.md against the portable format and this
repository's marketplace overlay. Do not edit; list failures and warnings.
```

```text
Fix skills/report-builder so its declared tools match its workflow, move the
long API table into references/, and rerun the repository validator.
```

## Resources

- [Skill contract and authority map](references/skill-contract.md)
- Repository validator: `004-scripts/validate_skills_v2.py`
