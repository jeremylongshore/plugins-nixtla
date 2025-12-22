# 6767-o: Lee Han Chung Claude Skills Production Standard

**Standard ID:** 6767-o-DR-STND
**Document Type:** Definitive Reference Standard
**Author Source:** Lee Han Chung
**Article:** https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
**Adopted By:** Intent Solutions Engineering
**Effective Date:** 2025-12-21
**Supersedes:** Partial requirements in 6767-c
**Status:** ACTIVE - MANDATORY COMPLIANCE

---

## 🎯 Executive Summary

This standard codifies Lee Han Chung's comprehensive Claude Skills production requirements as **mandatory compliance rules** for all Intent Solutions skills. Where Lee's article describes features as "optional," Intent Solutions treats them as **required** for production deployment.

**Scope:** All SKILL.md files in the claude-code-plugins repository
**Enforcement:** Automated validator + manual code review
**Compliance Target:** 100% of all 91 requirements

---

## 📋 Standard Categories

### Category A: YAML Frontmatter (23 requirements)
### Category B: Content Structure (18 requirements)
### Category C: Resource Organization (15 requirements)
### Category D: Tool Permissions & Security (12 requirements)
### Category E: Performance Guidelines (6 requirements)
### Category F: Portability Requirements (5 requirements)
### Category G: Discovery & Invocation (8 requirements)
### Category H: Execution Context (4 requirements)

**Total:** 91 distinct requirements

---

## Category A: YAML Frontmatter

### A1: Required Fields (Anthropic Specification)

#### A1.1: name (REQUIRED)
```yaml
name: docker-container-debugger
```

**Rules:**
- ✅ MUST be present
- ✅ MUST be lowercase + hyphens (kebab-case)
- ✅ MUST be max 64 characters
- ✅ MUST match folder name (best practice)
- ✅ MUST match pattern: `^[a-z][a-z0-9-]*[a-z0-9]$`

**Validator Check:** ✅ AUTOMATED
**Failure Level:** ERROR (blocks deployment)

#### A1.2: description (REQUIRED)
```yaml
description: "Debugs Docker containers. Use when containers crash or fail to start. Trigger: 'debug container', 'docker not working'"
```

**Rules:**
- ✅ MUST be present
- ✅ MUST be string (not multi-line)
- ✅ MUST be min 20 characters
- ✅ MUST be max 1,024 characters
- ✅ MUST use action-oriented language (see A6)
- ✅ MUST include trigger phrases
- ✅ SHOULD start with action verb

**Validator Check:** ✅ PARTIAL (enhanced check needed)
**Failure Level:** ERROR (blocks deployment)

---

### A2: Enterprise Required Fields (Intent Solutions)

#### A2.1: allowed-tools (ENTERPRISE REQUIRED)
```yaml
allowed-tools: "Read,Bash(docker:*),Grep"
```

**Rules:**
- ✅ MUST be present (Intent Solutions requirement)
- ✅ MUST be CSV string format (NOT array)
- ✅ MUST use comma-separated values
- ✅ MUST include only necessary tools (minimize attack surface)
- ✅ SHOULD use wildcards for scoped access: `Bash(git:*)`, `Bash(npm:*)`
- ✅ SHOULD limit to 6 or fewer tools
- ❌ MUST NOT grant all-encompassing access

**Valid Tools:**
- Read, Write, Edit, Bash, Glob, Grep
- WebFetch, WebSearch, Task, TodoWrite
- NotebookEdit, AskUserQuestion, Skill

**Wildcard Syntax:**
```yaml
# ✅ CORRECT: Scoped access
allowed-tools: "Read,Bash(git status:*),Bash(git diff:*)"

# ❌ WRONG: Too broad
allowed-tools: "Read,Bash(*)"
```

**Validator Check:** ✅ AUTOMATED
**Failure Level:** ERROR if missing, WARN if > 6 tools

#### A2.2: version (ENTERPRISE REQUIRED)
```yaml
version: "1.0.0"
```

**Rules:**
- ✅ MUST be present
- ✅ MUST use semantic versioning (x.y.z)
- ✅ MUST match pattern: `^\d+\.\d+\.\d+`

**Validator Check:** ✅ AUTOMATED
**Failure Level:** WARN (enterprise standard)

#### A2.3: author (ENTERPRISE REQUIRED)
```yaml
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
```

**Rules:**
- ✅ MUST be present
- ✅ SHOULD include email

**Validator Check:** ✅ AUTOMATED
**Failure Level:** WARN (enterprise standard)

#### A2.4: license (ENTERPRISE REQUIRED)
```yaml
license: "MIT"
```

**Rules:**
- ✅ MUST be present
- ✅ SHOULD be MIT or reference to LICENSE file

**Validator Check:** ✅ AUTOMATED
**Failure Level:** WARN (enterprise standard)

---

### A3: Optional Fields (Anthropic Specification)

#### A3.1: model
```yaml
model: "sonnet"
```

**Rules:**
- ⚠️ OPTIONAL (defaults to session model)
- ✅ MUST be one of: `inherit`, `sonnet`, `haiku`, `claude-*`
- ❌ MUST NOT use `opus` (deprecated)

**Validator Check:** ✅ AUTOMATED
**Failure Level:** WARN if invalid value

#### A3.2: disable-model-invocation
```yaml
disable-model-invocation: true
```

**Rules:**
- ⚠️ OPTIONAL
- ✅ MUST be boolean if present
- ℹ️ Prevents automatic invocation, requires manual `/skill-name`

**Validator Check:** ✅ AUTOMATED
**Failure Level:** N/A (informational)

#### A3.3: mode
```yaml
mode: true
```

**Rules:**
- ⚠️ OPTIONAL
- ✅ MUST be boolean if present
- ℹ️ Categorizes as mode command (special UI section)

**Validator Check:** ✅ AUTOMATED
**Failure Level:** N/A (informational)

#### A3.4: tags
```yaml
tags: "devops,docker,debugging"
```

**Rules:**
- ⚠️ OPTIONAL
- ✅ SHOULD be comma-separated if present

**Validator Check:** ⚠️ PARTIAL
**Failure Level:** N/A (informational)

---

### A4: Deprecated Fields

#### A4.1: when_to_use (DEPRECATED)
```yaml
# ❌ DO NOT USE
when_to_use: "Use when debugging Docker"
```

**Rules:**
- ❌ MUST NOT be present (undocumented, possibly deprecated)
- ℹ️ Use detailed `description` instead

**Validator Check:** ✅ AUTOMATED
**Failure Level:** WARN (deprecated field)

---

### A5: Frontmatter Size Constraint

#### A5.1: Token Budget Limit
**Rules:**
- ✅ MUST NOT exceed 15,000 characters (token budget limit)
- ⚠️ SHOULD warn if approaching 12,000 characters
- ℹ️ Skills from all sources aggregated, subject to context limits

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** ERROR if > 15,000 chars
**Action Required:** ADD TO VALIDATOR (Priority 1B)

---

### A6: Action-Oriented Language (Description Field)

#### A6.1: Required Action Verbs

**Compliant Examples:**
```yaml
✅ description: "Analyzes code for security vulnerabilities"
✅ description: "Creates deployment pipelines for cloud infrastructure"
✅ description: "Debugs failing tests and identifies root causes"
✅ description: "Optimizes database queries for performance"
```

**Non-Compliant Examples:**
```yaml
❌ description: "This skill helps you debug Docker containers"
❌ description: "You can use this to analyze code"
❌ description: "Provides assistance with deployment"
```

**Action Verb Categories:**
- **Analysis:** analyze, audit, inspect, investigate, examine, review
- **Creation:** create, generate, build, construct, compose, design
- **Modification:** update, modify, refactor, optimize, improve, enhance
- **Debugging:** debug, fix, troubleshoot, diagnose, resolve
- **Deployment:** deploy, publish, release, install, configure
- **Testing:** test, validate, verify, check, ensure
- **Monitoring:** monitor, track, observe, measure, report

**Validator Check:** ⚠️ PARTIAL (basic keyword check)
**Failure Level:** WARN if no action verb detected
**Action Required:** ENHANCE VALIDATOR (Priority 2B)

---

## Category B: Content Structure

### B1: Required Content Sections (MANDATORY)

All skills MUST include these sections in the markdown content:

#### B1.1: Purpose Statement
```markdown
## Purpose

This skill debugs Docker container failures by analyzing logs, inspecting configurations, and identifying common issues.
```

**Rules:**
- ✅ MUST be 1-2 sentences
- ✅ MUST clearly state what the skill does
- ✅ MUST be near the top of the document

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** ERROR
**Action Required:** ADD TO VALIDATOR (Priority 1C)

#### B1.2: Overview Section
```markdown
## Overview

Docker containers can fail for various reasons: misconfigured environment variables, port conflicts, resource limits, or image issues. This skill systematically checks each potential cause and provides actionable recommendations.
```

**Rules:**
- ✅ MUST provide context about the problem domain
- ✅ SHOULD be 2-4 sentences
- ✅ MUST explain when the skill applies

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD TO VALIDATOR (Priority 1C)

#### B1.3: Prerequisites Section
```markdown
## Prerequisites

- Docker installed and running
- Container ID or name
- Access to container logs (`docker logs` permission)
```

**Rules:**
- ✅ MUST list required tools, permissions, or setup
- ✅ SHOULD use bullet points
- ✅ MUST be actionable (user can verify they meet them)

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD TO VALIDATOR (Priority 1C)

#### B1.4: Step-by-Step Instructions
```markdown
## Instructions

1. Identify the failing container
2. Inspect container logs for error messages
3. Check container configuration (ports, volumes, env vars)
4. Verify image integrity
5. Provide diagnosis and recommendations
```

**Rules:**
- ✅ MUST provide clear, numbered steps
- ✅ MUST be actionable
- ✅ SHOULD reference tools Claude will use
- ✅ SHOULD use imperative language

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** ERROR
**Action Required:** ADD TO VALIDATOR (Priority 1C)

#### B1.5: Output Format Specifications
```markdown
## Output Format

**Diagnosis Report:**
- Container Status: [running/stopped/failed]
- Error Summary: [brief description]
- Root Cause: [identified issue]
- Recommendations: [actionable fixes]
```

**Rules:**
- ✅ MUST specify what format Claude will produce
- ✅ SHOULD use structured format (markdown, JSON, etc.)
- ✅ MUST be clear to users what to expect

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD TO VALIDATOR (Priority 1C)

#### B1.6: Error Handling Guidance
```markdown
## Error Handling

- If container not found: Verify container ID/name is correct
- If logs inaccessible: Check Docker daemon is running and you have permissions
- If image missing: Suggest re-pulling the image
```

**Rules:**
- ✅ MUST address common failure scenarios
- ✅ MUST provide recovery steps
- ✅ SHOULD use conditional format (If X, then Y)

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD TO VALIDATOR (Priority 1C)

#### B1.7: Examples Section
```markdown
## Examples

### Example 1: Port Conflict
```
User: "My nginx container won't start"
Diagnosis: Port 80 already in use by another process
Recommendation: Stop conflicting process or use different port mapping
```
```

**Rules:**
- ✅ MUST include at least one example
- ✅ SHOULD show input → output flow
- ✅ SHOULD cover common use cases

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** ERROR
**Action Required:** ADD TO VALIDATOR (Priority 1C)

---

### B2: Content Quality Standards

#### B2.1: Word Count Limit
**Rules:**
- ✅ MUST be under 5,000 words total
- ⚠️ SHOULD warn if 3,500-5,000 words (consider offloading to /references)
- ℹ️ Prevents context bloat

**Validator Check:** ✅ AUTOMATED
**Failure Level:** WARN if > 5,000 words

#### B2.2: Imperative Language
**Rules:**
- ✅ MUST use imperative voice ("Analyze code for...")
- ❌ MUST NOT use second-person ("You should analyze...")
- ❌ AVOID passive voice ("Code is analyzed...")

**Validator Check:** ⚠️ PARTIAL (basic check)
**Failure Level:** INFO
**Action Required:** ENHANCE (Priority 2B)

#### B2.3: External References
**Rules:**
- ✅ SHOULD reference external files rather than embedding large content
- ✅ SHOULD use `/references` for detailed documentation
- ✅ SHOULD use `/assets` for templates
- ❌ MUST NOT embed > 50 lines of code directly

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD TO VALIDATOR (Priority 3B)

---

## Category C: Resource Organization

### C1: Directory Structure (MANDATORY)

All skills using external resources MUST organize them properly:

```
skill-name/
├── SKILL.md              # Main skill definition
├── scripts/              # Executable automation (optional)
│   ├── init.py          # Python scripts
│   └── setup.sh         # Bash scripts
├── references/           # Documentation (optional)
│   ├── api-spec.md      # Markdown docs
│   └── schema.json      # JSON schemas
└── assets/               # Templates (optional)
    ├── config.yaml      # Configuration templates
    └── template.html    # HTML templates
```

### C2: /scripts Directory

#### C2.1: Purpose
**Rules:**
- ✅ MUST contain executable Python/Bash automation
- ✅ MUST be deterministic operations
- ✅ MUST be invoked via Bash tool
- ✅ MUST use {baseDir} for path references

**Example:**
```bash
python {baseDir}/scripts/init_skill.py docker-debugger
```

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** ERROR if referenced but missing
**Action Required:** ADD TO VALIDATOR (Priority 1A)

#### C2.2: Script Requirements
**Rules:**
- ✅ MUST be executable (`chmod +x`)
- ✅ MUST have shebang line (`#!/usr/bin/env python3` or `#!/bin/bash`)
- ✅ SHOULD be idempotent (can run multiple times safely)
- ✅ SHOULD handle errors gracefully
- ⚠️ AVOID random generation, timestamps, UUIDs (non-deterministic)

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD TO VALIDATOR (Priority 3A)

---

### C3: /references Directory

#### C3.1: Purpose
**Rules:**
- ✅ MUST contain text documentation loaded into context via Read tool
- ✅ MUST be markdown, JSON schemas, or configuration templates
- ✅ MUST provide detailed information Claude needs
- ❌ MUST NOT contain binary files

**Allowed File Types:**
- `.md` - Markdown documentation
- `.json` - JSON schemas, data structures
- `.yaml` / `.yml` - YAML configuration
- `.txt` - Plain text documentation

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN if non-text files present
**Action Required:** ADD TO VALIDATOR (Priority 1A)

#### C3.2: Content Injection
**Rules:**
- ✅ Content gets injected when Claude needs detailed information
- ✅ Supports progressive disclosure pattern
- ✅ Prevents context bloat in main SKILL.md

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** DOCUMENT ONLY

---

### C4: /assets Directory

#### C4.1: Purpose
**Rules:**
- ✅ MUST contain templates and binary files
- ✅ MUST be referenced by path only (not loaded into context)
- ✅ MUST be files Claude manipulates or references
- ✅ MAY contain images, HTML/CSS templates, configuration boilerplate

**Allowed Content:**
- Templates (HTML, CSS, config files)
- Images (PNG, JPG, SVG)
- Binary files (not loaded into context)

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** ADD TO VALIDATOR (Priority 1A)

#### C4.2: Template Usage
**Rules:**
- ✅ Templates loaded to avoid context consumption
- ✅ Claude fills placeholders and writes results
- ✅ Supports Template-Based Generation pattern

**Example:**
```markdown
Load template from {baseDir}/assets/config.yaml, fill placeholders, write to user's project.
```

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** DOCUMENT ONLY

---

## Category D: Tool Permissions & Security

### D1: Principle of Least Privilege

#### D1.1: Minimal Tool Access
**Rules:**
- ✅ MUST include only tools the skill genuinely needs
- ✅ MUST use tool-specific wildcards for scoped access
- ✅ MUST narrow attack surface
- ❌ MUST NOT grant all-encompassing access

**Examples:**

```yaml
# ✅ GOOD: Minimal, scoped access
allowed-tools: "Read,Bash(docker ps:*),Bash(docker logs:*),Grep"

# ⚠️ ACCEPTABLE: Broader but justified
allowed-tools: "Read,Write,Edit,Bash(git:*),Grep"

# ❌ BAD: Too broad, security risk
allowed-tools: "Read,Write,Edit,Bash,Grep,WebFetch,Task,TodoWrite"
```

**Validator Check:** ⚠️ PARTIAL (warns if > 6 tools)
**Failure Level:** INFO if > 6 tools, ERROR if obviously excessive
**Action Required:** ENHANCE VALIDATOR

### D2: Wildcard Syntax

#### D2.1: Scoped Bash Commands
**Rules:**
- ✅ MUST use wildcards to limit Bash command scope
- ✅ MUST follow pattern: `Bash(command:*)`
- ✅ MUST include colon separator

**Valid Patterns:**
```yaml
Bash(git:*)              # All git commands
Bash(git status:*)       # Only git status
Bash(npm install:*)      # Only npm install
Bash(docker ps:*)        # Only docker ps
```

**Invalid Patterns:**
```yaml
Bash(*)                  # Too broad
Bash(git)                # Missing colon
Bash                     # No restriction
```

**Validator Check:** ✅ AUTOMATED (checks for colon)
**Failure Level:** ERROR if invalid syntax
**Action Required:** ENHANCE for pattern validation

### D3: Security Testing

#### D3.1: Pre-Deployment Testing
**Rules:**
- ✅ MUST test permission restrictions before deployment
- ✅ MUST verify skill cannot execute unintended commands
- ✅ MUST verify scoped wildcards work as expected

**Validator Check:** ❌ NOT AUTOMATED
**Failure Level:** N/A (manual testing)
**Action Required:** CREATE TEST SUITE

---

## Category E: Performance Guidelines

### E1: Context Management

#### E1.1: Word Count Limit
**Rules:**
- ✅ MUST keep main SKILL.md under 5,000 words
- ⚠️ SHOULD warn if 3,500-5,000 words
- ℹ️ Prevents context bloat and improves performance

**Validator Check:** ✅ AUTOMATED
**Failure Level:** WARN if > 5,000 words

#### E1.2: Offload Verbose Content
**Rules:**
- ✅ SHOULD move detailed documentation to `/references`
- ✅ SHOULD move templates to `/assets`
- ✅ SHOULD use progressive disclosure pattern

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** ADD SUGGESTIONS (Priority 2)

### E2: Script Performance

#### E2.1: Deterministic Execution
**Rules:**
- ✅ SHOULD structure scripts for deterministic execution
- ⚠️ AVOID non-deterministic operations (random, timestamps, UUIDs)
- ✅ SHOULD be idempotent (safe to run multiple times)

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD TO VALIDATOR (Priority 3A)

### E3: Progressive Disclosure Pattern

#### E3.1: Tiered Information Loading
**Rules:**
- ✅ Frontmatter disclosure: Minimal metadata (name, description)
- ✅ Full SKILL.md loading: Comprehensive instructions when invoked
- ✅ Resource loading on-demand: Helper files loaded as Claude executes
- ℹ️ Prevents context bloat while maintaining discoverability

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** DOCUMENT PATTERN

---

## Category F: Portability Requirements

### F1: Path Portability

#### F1.1: {baseDir} Variable
**Rules:**
- ✅ MUST use `{baseDir}` exclusively for relative paths
- ✅ MUST reference skill resources via `{baseDir}/scripts/*`, `{baseDir}/references/*`, etc.
- ❌ MUST NOT hardcode user paths (`/home/user/`, `/Users/user/`)
- ❌ MUST NOT hardcode installation directories

**Examples:**

```markdown
✅ CORRECT:
python {baseDir}/scripts/init.py
cat {baseDir}/references/api-spec.md

❌ WRONG:
python /home/jeremy/.config/claude/skills/my-skill/scripts/init.py
cat /Users/jeremy/skills/my-skill/references/api-spec.md
```

**Validator Check:** ✅ AUTOMATED (detects hardcoded paths)
**Failure Level:** ERROR

### F2: Cross-Environment Compatibility

#### F2.1: Environment Independence
**Rules:**
- ✅ MUST ensure scripts work across different environments (Linux, macOS, Windows)
- ✅ MUST document environment dependencies (if any)
- ✅ SHOULD use platform-agnostic commands where possible

**Validator Check:** ❌ NOT AUTOMATED
**Failure Level:** N/A (manual testing)
**Action Required:** ADD TESTING CHECKLIST

#### F2.2: Dependency Documentation
**Rules:**
- ✅ MUST document required dependencies in Prerequisites section
- ✅ MUST specify versions if critical
- ✅ SHOULD provide installation instructions

**Example:**
```markdown
## Prerequisites

- Python 3.8+ (`python --version`)
- Docker 20.10+ (`docker --version`)
- jq 1.6+ for JSON parsing (`jq --version`)
```

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD TO VALIDATOR (Priority 3)

---

## Category G: Discovery & Invocation

### G1: CLI Invocation

#### G1.1: Manual Invocation Syntax
**Rules:**
- ℹ️ Users can manually invoke skills using: `/skill-name [arguments]`
- ℹ️ Bypasses automatic invocation restrictions
- ℹ️ Works even with `disable-model-invocation: true`

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** DOCUMENT IN SKILL TEMPLATES

### G2: Discovery Sources

#### G2.1: Scan Locations
**Rules:**
- ℹ️ Claude Code scans skills from:
  - User configuration: `~/.config/claude/skills/`
  - Project configuration: `.claude/skills/`
  - Plugin-provided skills
  - Built-in skills
- ℹ️ All sources aggregated into single available list
- ℹ️ Subject to token budget constraints (default 15,000 characters)

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** DOCUMENT ONLY

### G3: Token Budget

#### G3.1: Aggregated Limit
**Rules:**
- ✅ MUST NOT exceed 15,000 character limit (all skills combined)
- ⚠️ Individual skill frontmatter contributes to total budget
- ℹ️ Excessive skills may not be loaded

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** WARN
**Action Required:** ADD BUDGET CALCULATOR

---

## Category H: Execution Context

### H1: Meta-Tool System

#### H1.1: Context Modification
**Rules:**
- ℹ️ Skills modify conversation context via `isMeta: true` messages
- ℹ️ Skills modify execution context via pre-approved tool permissions
- ℹ️ Tool named "Skill" manages individual skills

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** DOCUMENT ONLY

### H2: Message Structure

#### H2.1: Dual-Message Invocation
**Rules:**
- ℹ️ Two distinct user messages per skill invocation:
  - Message 1: `isMeta: false` - Visible status indicator in UI
  - Message 2: `isMeta: true` - Detailed prompt hidden from users but sent to Claude

**Validator Check:** ❌ NOT IMPLEMENTED
**Failure Level:** INFO
**Action Required:** DOCUMENT ONLY

---

## 🎨 Common Skill Patterns (8 Patterns)

Lee identifies 8 common patterns for organizing skills. Intent Solutions skills SHOULD follow at least one of these patterns:

### Pattern 1: Script Automation
**Description:** Execute Python/Bash scripts for complex operations, with Claude processing output.

**Structure:**
```
skill-name/
├── SKILL.md
└── scripts/
    ├── analyze.py
    └── process.sh
```

**Example:**
```markdown
Run `python {baseDir}/scripts/analyze.py <input>` to perform analysis.
Claude processes the output and generates recommendations.
```

### Pattern 2: Read-Process-Write
**Description:** Standard ETL pattern: read input, transform per instructions, write output.

**Structure:**
```markdown
1. Read input files using Read tool
2. Process data according to specifications
3. Write transformed output using Write tool
```

### Pattern 3: Search-Analyze-Report
**Description:** Find patterns via Grep, read matching files, analyze, generate structured report.

**Structure:**
```markdown
1. Search codebase for patterns using Grep tool
2. Read matching files for detailed analysis
3. Analyze findings for issues/patterns
4. Generate structured report
```

### Pattern 4: Command Chain Execution
**Description:** Multi-step operations with dependencies (CI/CD-like workflows).

**Structure:**
```markdown
1. Build project → Test → Deploy (sequential steps)
2. Each step depends on previous success
3. Fail fast on errors
```

### Pattern 5: Wizard-Style Workflows
**Description:** Multi-step processes requiring user confirmation between phases.

**Structure:**
```markdown
1. Analyze current state
2. Ask user for confirmation via AskUserQuestion tool
3. Apply changes
4. Verify results
```

### Pattern 6: Template-Based Generation
**Description:** Load templates from `/assets`, fill placeholders, write results.

**Structure:**
```
skill-name/
├── SKILL.md
└── assets/
    ├── config.template.yaml
    └── dockerfile.template
```

**Example:**
```markdown
1. Load template from {baseDir}/assets/config.template.yaml
2. Fill placeholders with user-specific values
3. Write completed config to project
```

### Pattern 7: Iterative Refinement
**Description:** Broad scan → deep analysis → recommendations across multiple passes.

**Structure:**
```markdown
1. First pass: Broad scan for all issues
2. Second pass: Deep analysis of critical issues
3. Third pass: Generate prioritized recommendations
```

### Pattern 8: Context Aggregation
**Description:** Synthesize information from multiple files/tools into coherent summary.

**Structure:**
```markdown
1. Gather information from multiple sources (Read, Grep, Bash)
2. Synthesize into coherent summary
3. Present unified view to user
```

---

## 📊 Compliance Metrics

### Required Compliance Levels

Intent Solutions mandates **100% compliance** across all categories:

| Category | Requirements | Current | Target | Priority |
|----------|--------------|---------|--------|----------|
| A: YAML Frontmatter | 23 | ~80% | 100% | P1 |
| B: Content Structure | 18 | ~20% | 100% | P1 |
| C: Resource Organization | 15 | ~10% | 100% | P1 |
| D: Tool Permissions | 12 | ~70% | 100% | P2 |
| E: Performance | 6 | ~60% | 100% | P2 |
| F: Portability | 5 | ~80% | 100% | P2 |
| G: Discovery | 8 | ~10% | 100% | P3 |
| H: Execution Context | 4 | ~0% | 100% | P3 |
| **TOTAL** | **91** | **~40%** | **100%** | - |

### Enforcement Strategy

**Phase 1: Critical (Week 1)**
- Implement resource directory validation (C1-C4)
- Implement content structure validation (B1)
- Implement frontmatter size check (A5)
- Target: 70% compliance

**Phase 2: Quality (Week 2)**
- Implement pattern detection (8 patterns)
- Implement enhanced action-oriented language (A6, B2.2)
- Implement embed vs reference detection (B2.3)
- Target: 85% compliance

**Phase 3: Advanced (Week 3)**
- Implement script determinism checks (C2.2, E2.1)
- Implement dependency documentation check (F2.2)
- Implement token budget calculator (G3.1)
- Target: 100% compliance

---

## 🔧 Validator Implementation

### Required Validators

#### 1. scripts/validate-skills-lee-standard.py (NEW)
**Purpose:** Comprehensive Lee Han Chung standard compliance checker

**Checks:**
- ✅ All 23 YAML frontmatter requirements
- ✅ All 18 content structure requirements
- ✅ All 15 resource organization requirements
- ✅ All 12 tool permission requirements
- ✅ All 6 performance requirements
- ✅ All 5 portability requirements
- ✅ Pattern detection (8 patterns)

**Output:**
```
🔍 LEE HAN CHUNG STANDARD VALIDATOR
Based on: leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/

📊 COMPLIANCE REPORT:
Category A (YAML): 23/23 ✅ 100%
Category B (Content): 16/18 ⚠️ 89%
Category C (Resources): 12/15 ⚠️ 80%
Category D (Security): 12/12 ✅ 100%
Category E (Performance): 6/6 ✅ 100%
Category F (Portability): 5/5 ✅ 100%
Category G (Discovery): 5/8 ⚠️ 63%
Category H (Execution): 2/4 ⚠️ 50%

OVERALL: 81/91 ⚠️ 89% COMPLIANT

Pattern Detected: Template-Based Generation
```

#### 2. Enhancement to validate-skills-schema.py (EXISTING)
**Add:**
- Frontmatter size check (15,000 char limit)
- Content structure detection
- Enhanced action-oriented language check
- Embed vs reference detection

---

## 🚀 Implementation Roadmap

### Week 1: Critical Foundations
- [ ] Create `scripts/validate-skills-lee-standard.py`
- [ ] Implement Category C validation (resource directories)
- [ ] Implement Category B.1 validation (content structure)
- [ ] Implement Category A.5 validation (frontmatter size)
- [ ] Test against all 241 existing skills
- [ ] Fix blocking compliance issues

### Week 2: Quality Enhancements
- [ ] Implement pattern detection (8 patterns)
- [ ] Implement enhanced action-oriented language check
- [ ] Implement embed vs reference detection
- [ ] Update skill templates with all mandatory sections
- [ ] Document progressive disclosure pattern

### Week 3: Advanced Features
- [ ] Implement script determinism checks
- [ ] Implement dependency documentation check
- [ ] Implement token budget calculator
- [ ] Create comprehensive test suite
- [ ] Achieve 100% compliance across all 241 skills

### Week 4: Documentation & Training
- [ ] Update SKILLS-SCHEMA-2025.md
- [ ] Create skill-patterns-guide.md (8 patterns)
- [ ] Create skill-creation-checklist.md
- [ ] Train team on new standards
- [ ] Deploy to CI/CD pipeline

---

## 📚 References

### Primary Sources
- **Lee Han Chung Article:** https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
- **Anthropic Official Docs:** https://code.claude.com/docs/en/skills
- **Claude Code GitHub:** https://github.com/anthropics/claude-code

### Related Standards
- **6767-c:** Enterprise Standard for Claude Code Extensions (partial overlap)
- **SKILLS-SCHEMA-2025.md:** Technical schema documentation (superseded by this standard)

### Intent Solutions Documentation
- **skill-creation-guide.md:** Step-by-step skill creation (to be updated)
- **skill-patterns-guide.md:** 8 common patterns explained (to be created)
- **skill-validation-checklist.md:** Pre-deployment checklist (to be created)

---

## 📋 Appendix A: Complete Requirements Checklist

Use this checklist when creating or auditing skills:

### YAML Frontmatter
- [ ] A1.1: name field present, kebab-case, max 64 chars, matches folder
- [ ] A1.2: description field present, 20-1024 chars, action-oriented
- [ ] A2.1: allowed-tools present, CSV format, minimal permissions, wildcards
- [ ] A2.2: version present, semantic versioning (x.y.z)
- [ ] A2.3: author present with email
- [ ] A2.4: license present (MIT or LICENSE file)
- [ ] A3.1: model field valid (if present): inherit/sonnet/haiku/claude-*
- [ ] A3.2: disable-model-invocation boolean (if present)
- [ ] A3.3: mode boolean (if present)
- [ ] A4.1: when_to_use field NOT present (deprecated)
- [ ] A5.1: Frontmatter under 15,000 characters
- [ ] A6.1: Description uses action verbs

### Content Structure
- [ ] B1.1: Purpose statement (1-2 sentences)
- [ ] B1.2: Overview section (context)
- [ ] B1.3: Prerequisites section (requirements)
- [ ] B1.4: Step-by-step instructions
- [ ] B1.5: Output format specifications
- [ ] B1.6: Error handling guidance
- [ ] B1.7: Examples section (at least one)
- [ ] B2.1: Under 5,000 words total
- [ ] B2.2: Uses imperative language
- [ ] B2.3: References external files (not embedding large content)

### Resource Organization
- [ ] C1: Proper directory structure (scripts/, references/, assets/)
- [ ] C2.1: /scripts contains executable automation (if used)
- [ ] C2.2: Scripts are executable, have shebang, deterministic
- [ ] C3.1: /references contains text documentation (if used)
- [ ] C4.1: /assets contains templates/binary files (if used)

### Tool Permissions & Security
- [ ] D1.1: Minimal tool access (only what's needed)
- [ ] D2.1: Scoped Bash wildcards (e.g., Bash(git:*))
- [ ] D3.1: Permission restrictions tested

### Performance
- [ ] E1.1: Main SKILL.md under 5,000 words
- [ ] E1.2: Verbose content offloaded to /references
- [ ] E2.1: Scripts structured for deterministic execution

### Portability
- [ ] F1.1: Uses {baseDir} exclusively, no hardcoded paths
- [ ] F2.1: Scripts work across environments
- [ ] F2.2: Environment dependencies documented

### Discovery & Invocation
- [ ] G1.1: CLI invocation syntax documented (if applicable)
- [ ] G3.1: Frontmatter contributes reasonably to 15K token budget

### Execution Context
- [ ] H1.1: Understands meta-tool system (informational)
- [ ] H2.1: Understands dual-message structure (informational)

### Pattern Compliance
- [ ] Follows at least one of 8 common patterns

---

## 📋 Appendix B: Non-Compliant Examples

### Example 1: Missing Content Structure

**❌ BAD:**
```markdown
---
name: docker-debug
description: "Debug Docker containers"
allowed-tools: "Read,Bash"
---

# Docker Debugger

This skill helps debug Docker issues.

Run docker commands to find problems.
```

**Issues:**
- Missing purpose statement
- Missing overview
- Missing prerequisites
- Missing step-by-step instructions
- Missing output format
- Missing error handling
- Missing examples

**✅ GOOD:**
```markdown
---
name: docker-debug
description: "Debugs Docker containers by analyzing logs and configurations. Use when containers crash or fail to start."
allowed-tools: "Read,Bash(docker:*),Grep"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: "MIT"
---

## Purpose

This skill debugs Docker container failures by systematically analyzing logs, inspecting configurations, and identifying common issues.

## Overview

Docker containers fail for various reasons: misconfigured environment variables, port conflicts, resource limits, or image issues. This skill checks each potential cause and provides actionable recommendations.

## Prerequisites

- Docker installed and running
- Container ID or name
- Permission to access Docker daemon

## Instructions

1. Identify the failing container using `docker ps -a`
2. Inspect container logs for error messages
3. Check container configuration (ports, volumes, env vars)
4. Verify image integrity
5. Provide diagnosis and recommendations

## Output Format

**Diagnosis Report:**
- Container Status: [running/stopped/failed]
- Error Summary: [brief description]
- Root Cause: [identified issue]
- Recommendations: [actionable fixes]

## Error Handling

- If container not found: Verify container ID/name
- If logs inaccessible: Check Docker daemon status
- If image missing: Suggest re-pulling image

## Examples

### Example 1: Port Conflict
User: "My nginx container won't start"
Diagnosis: Port 80 already in use
Recommendation: Stop conflicting process or use different port
```

---

## 📝 Document Control

**Version History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-12-21 | Initial standard creation based on Lee Han Chung article | Intent Solutions Engineering |

**Review Schedule:** Quarterly review against Anthropic official documentation

**Approval:**
- [x] Engineering Lead
- [ ] Security Review
- [ ] Compliance Review

**Status:** DRAFT - PENDING APPROVAL

---

**END OF STANDARD 6767-d**

---

**Next Steps:**
1. Create Beads epic for implementation
2. Develop comprehensive validator
3. Audit all 241 existing skills
4. Achieve 100% compliance
5. Deploy to CI/CD pipeline
