# Planned Skills Development

**Purpose**: Development workspace for creating 500 standalone Claude Code skills.

**Location**: `000-docs/000a-skills-schema/planned-skills-dev/`

---

## Overview

This directory contains the planning and development resources for creating 500 enterprise-grade standalone skills for the Claude Code Plugins marketplace.

### Goals
- **Target**: 500 total skills
- **Current**: 241 skills (in claude-code-plugins repo)
- **To Create**: 259 new skills

---

## Directory Structure

```
planned-skills-dev/
├── README.md                     # This file
├── skill-definitions/            # Skill definition YAML files
│   ├── 01-devops.yaml           # 40 DevOps skills
│   ├── 02-security.yaml         # 35 Security skills
│   ├── 03-database.yaml         # 30 Database skills
│   ├── 04-api.yaml              # 25 API skills
│   ├── 05-code-quality.yaml     # 25 Code quality skills
│   ├── 06-testing.yaml          # 25 Testing skills
│   ├── 07-documentation.yaml    # 20 Documentation skills
│   ├── 08-performance.yaml      # 20 Performance skills
│   ├── 09-ai-ml.yaml            # 20 AI/ML skills
│   └── 10-cloud.yaml            # 19 Cloud skills
├── templates/                    # Skill templates by type
│   ├── basic-skill.md           # Simple single-file skill
│   ├── advanced-skill.md        # Skill with scripts/references
│   └── read-only-skill.md       # Analysis-only skill
├── generated/                    # Staging for generated skills
│   ├── batch-001/               # First batch
│   ├── batch-002/               # Second batch
│   └── ...
└── validation/                   # Validation reports
    └── batch-001-report.md      # Validation results
```

---

## Skill Categories

| # | Category | Count | Priority | Status |
|---|----------|-------|----------|--------|
| 1 | DevOps Automation | 40 | High | Planned |
| 2 | Security & Compliance | 35 | High | Planned |
| 3 | Database Operations | 30 | High | Planned |
| 4 | API Development | 25 | Medium | Planned |
| 5 | Code Quality | 25 | Medium | Planned |
| 6 | Testing & QA | 25 | Medium | Planned |
| 7 | Documentation | 20 | Medium | Planned |
| 8 | Performance | 20 | Low | Planned |
| 9 | AI/ML Ops | 20 | Low | Planned |
| 10 | Cloud Architecture | 19 | Low | Planned |
| | **TOTAL** | **259** | | |

---

## Enterprise Standard Requirements

All skills MUST include these fields:

### Anthropic Required
```yaml
name: kebab-case-name          # Required, max 64 chars
description: |                 # Required, max 1024 chars
  What it does. When to use. Trigger phrases.
```

### Enterprise Required
```yaml
allowed-tools:                 # Required for security
  - Read
  - Write
  - Bash
version: 1.0.0                # Required, semver
author: Jeremy Longshore <jeremy@intentsolutions.io>  # Required
license: MIT                  # Required
```

### Recommended
```yaml
tags:                         # Recommended for discovery
  - devops
  - kubernetes
```

---

## Description Writing Guide (Critical for Discovery)

The `description` field is **the most important field** for skill activation. Claude uses it to decide when to invoke your skill from potentially 100+ available skills.

### The Description Formula

```
[Action Verbs] + [Specific Capabilities] + [Use When] + [Trigger Phrases]
```

**Max Length**: 1024 characters

### Action Verbs (Use These)

| Category | Action Verbs |
|----------|-------------|
| Data | Extract, analyze, parse, transform, convert, merge, split, validate |
| Creation | Generate, create, build, produce, synthesize, compose |
| Modification | Edit, update, refactor, optimize, fix, enhance, migrate |
| Analysis | Review, audit, scan, inspect, diagnose, profile, assess |
| Operations | Deploy, execute, run, configure, install, setup, provision |
| Documentation | Document, explain, summarize, annotate, describe |

### Description Patterns

**Pattern 1: Action-focused (Recommended)**
```yaml
description: |
  Extract text and tables from PDFs, fill forms, merge documents.
  Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**Pattern 2: Capability + Trigger**
```yaml
description: |
  Kubernetes pod debugging and troubleshooting toolkit.
  Use when pods crash, fail to start, or exhibit unexpected behavior.
  Trigger with "debug pod", "pod failing", "container crash".
```

### Good vs Bad Examples

| Quality | Example |
|---------|---------|
| **BAD** | `description: Helps with documents` |
| **BAD** | `description: Processes data` |
| **GOOD** | `description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.` |

### Key Rules

1. **Always write in third person** (not "I can help" or "You can use")
2. **Include specific file types** (.pdf, .xlsx, .yaml)
3. **Include domain keywords** (Kubernetes, SQL, Docker)
4. **Define boundaries** (what it can NOT do)
5. **Keep under 1024 characters**

---

## Workflow

### 1. Define Skills
Create YAML definitions in `skill-definitions/`:

```yaml
# skill-definitions/01-devops.yaml
skills:
  - name: kubernetes-pod-debugger
    description: |
      Debug failing Kubernetes pods by analyzing logs, events, and resource status.
      Use when pods crash, fail to start, or exhibit unexpected behavior.
      Trigger with "debug pod", "pod failing", "container crash".
    allowed-tools: [Read, Bash, Grep]
    tags: [devops, kubernetes, debugging]

  - name: helm-chart-generator
    description: |
      Generate Helm charts from existing Kubernetes manifests.
      Use when converting raw YAML to Helm or creating new charts.
      Trigger with "create helm chart", "convert to helm", "helm template".
    allowed-tools: [Read, Write, Bash]
    tags: [devops, kubernetes, helm]
```

### 2. Generate Skills
Run batch generation script:

```bash
# Generate batch from definitions
python3 scripts/batch-generate-skills.py \
  --input skill-definitions/01-devops.yaml \
  --output generated/batch-001/ \
  --batch-size 20
```

### 3. Validate
Run validation against enterprise spec:

```bash
python3 scripts/validate-skills-schema.py generated/batch-001/
```

### 4. Review & Merge
- Manual review of generated skills
- Fix any issues
- Copy to `claude-code-plugins/plugins/` or `claude-code-plugins/skills/`

---

## Skill Definition Template

```yaml
skills:
  - name: skill-name-kebab-case
    description: |
      [Primary capability as action verb]. [Secondary features].
      Use when [2-3 trigger scenarios].
      Trigger with "[phrase1]", "[phrase2]", "[phrase3]".
    allowed-tools:
      - Read
      - Write
      - Bash
    tags:
      - category
      - subcategory
    complexity: basic|advanced|expert
    estimated_tokens: 500-1500
```

---

## References

### Master Specification
- `../SKILLS-STANDARD-COMPLETE.md` - Complete skills standard (65KB)

### Validation Tools
- `claude-code-plugins/scripts/validate-skills-schema.py`
- `claude-code-plugins/scripts/fix-skills-enterprise.py`
- `claude-code-plugins/scripts/audit-skills-quality.py`

### Official Documentation
- [Anthropic Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Lee Han Chung Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

---

## Timeline (Estimated)

| Phase | Duration | Description |
|-------|----------|-------------|
| 1. Define | 2 days | Create all 259 skill definitions |
| 2. Setup | 1 day | Build generation infrastructure |
| 3. Generate | 13 days | 20 skills/day batch generation |
| 4. Validate | Ongoing | Continuous validation |
| 5. Release | 1 day | Final release as v2.0.0 |
| **Total** | **~17 days** | |

---

**Last Updated**: 2025-12-19
**Maintained By**: Intent Solutions (Jeremy Longshore)
**Target**: 500 enterprise-grade standalone skills
