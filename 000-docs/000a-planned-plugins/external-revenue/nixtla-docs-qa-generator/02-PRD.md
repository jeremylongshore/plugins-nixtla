# Docs QA Generator - Product Requirements Document

**Plugin:** nixtla-docs-qa-generator
**Version:** 0.1.0
**Status:** Planned
**Last Updated:** 2025-12-15

---

## Overview

A plugin that monitors SDK changes (via git diff or changelog), automatically generates documentation updates, creates executable test cases from code examples, and alerts on docs/code drift before users encounter it.

---

## Problem Statement

Documentation drift is a constant challenge: SDK changes ship, but docs lag behind. Users encounter "it doesn't work like the docs say" issues, generating support tickets and eroding trust. Manual doc updates are tedious and often deprioritized.

---

## Goals

1. Monitor statsforecast, nixtla SDK, and mlforecast repos for API changes
2. Produce markdown patches showing required documentation updates
3. Parse docs for code blocks, generate pytest-compatible test files
4. CI job that fails when doc examples don't execute against current SDK
5. Automatically create PRs for doc updates when drift detected

## Non-Goals

- Replace technical writers entirely
- Generate marketing copy
- Handle non-code documentation

---

## Target Users

| User | Need |
|------|------|
| Documentation maintainers | Automated update suggestions |
| SDK developers | Know when docs need updates |
| DevRel team | Accurate, tested documentation |
| QA engineers | Executable doc examples |

---

## Functional Requirements

### FR-1: Change Detection
- Monitor statsforecast, nixtla SDK, and mlforecast repos
- Detect changes to public API surfaces
- Track function signature changes, new parameters, deprecations
- Identify breaking changes vs additions

### FR-2: Doc Diff Generation
- Analyze existing documentation for affected sections
- Generate markdown patches for required updates
- Preserve existing narrative while updating code/API details
- Highlight breaking changes prominently

### FR-3: Example Extraction
- Parse documentation for code blocks
- Extract Python examples with proper context
- Generate pytest-compatible test files
- Support async examples and fixtures

### FR-4: Drift Detection CI
- GitHub Actions workflow for drift detection
- Run all doc examples against current SDK
- Fail CI if any example doesn't execute
- Report specific failures with line numbers

### FR-5: Auto-PR Generation
- Create PRs automatically when drift detected
- Include diff summary and affected sections
- Tag appropriate reviewers
- Link to failing CI run

### FR-6: MCP Server Tools
Expose 5 tools to Claude Code:
1. `detect_changes` - Scan repos for API changes
2. `generate_doc_diff` - Create documentation patches
3. `extract_examples` - Parse docs for code blocks
4. `run_doc_tests` - Execute examples and report results
5. `create_update_pr` - Generate PR for doc updates

---

## Non-Functional Requirements

### NFR-1: Performance
- Change detection: <30 seconds per repo
- Example extraction: <5 seconds per doc file
- Test execution: Parallel, 10 examples/minute

### NFR-2: Dependencies
- Python 3.10+
- Git access to SDK repos
- GitHub API for PR creation
- pytest for example execution

### NFR-3: Security
- Read-only access to SDK repos
- Write access only to docs repo
- No execution of untrusted code

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Doc/code drift at release | 0% (all examples pass) |
| "Docs wrong" ticket reduction | 80% |
| Doc update cycle | 2 weeks → 2 days |
| Auto-PR acceptance rate | 70%+ |

---

## Scope

### In Scope
- statsforecast, nixtla, mlforecast SDKs
- Python code examples
- API reference documentation
- GitHub integration

### Out of Scope
- Non-Python documentation
- Marketing content
- Video tutorials
- Community contributions

---

## Technical Approach

- **Git Integration**: Watch for commits affecting public API surfaces
- **AST Parsing**: Extract function signatures, parameters, return types from Python code
- **Claude Skill**: Generate natural language doc updates from structured diffs
- **GitHub Actions**: CI workflow for drift detection and auto-PR creation

---

## Estimated Effort

3-4 weeks for core drift detection and alerting. Additional 2 weeks for auto-PR generation.

---

## Revenue Impact

Indirect. Reduces churn from frustrated users, decreases support burden, accelerates release cycles.
