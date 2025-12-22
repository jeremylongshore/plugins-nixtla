# PRD — Universal Validator Skill (Template)

## Problem

Validation systems drift when schema rules, tests, and CI checks are defined in multiple places without a single evidence-producing runner.

## Goal

Provide a reusable skill template that:

- runs validations in phases
- produces deterministic evidence bundles (logs + JSON)
- supports profiles (skills-only, plugins-only, full repo)
- enables strict CI gating (fail on error, optionally fail on warn)

## Non-Goals

- Implement organization-specific validators (the template provides hooks and structure).

## Acceptance Criteria

- Deterministic runner writes `summary.json`, `report.md`, and `checks/*.log`.
- Profiles can enable/disable checks via flags.
- Scaffold validates that phase docs and procedures exist for the skill.

