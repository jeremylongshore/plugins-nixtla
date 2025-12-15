# Docs QA Generator - Architecture

**Plugin:** nixtla-docs-qa-generator
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  SDK REPOSITORIES                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ statsforecast│  │ nixtla       │  │ mlforecast      │   │
│  │ (GitHub)     │  │ (GitHub)     │  │ (GitHub)        │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  CHANGE DETECTION LAYER                                     │
│  - Git diff analysis                                        │
│  - AST parsing for function signatures                      │
│  - Changelog parsing                                        │
│  - Breaking change detection                                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  ANALYSIS ENGINE                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Change Catalog                                  │   │
│  │  - New functions/classes                             │   │
│  │  - Changed signatures                                │   │
│  │  - Deprecated items                                  │   │
│  │  - Removed items                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Documentation Mapper                                │   │
│  │  - Map API items to doc sections                     │   │
│  │  - Identify affected pages                           │   │
│  │  - Locate code examples                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  DOC GENERATION LAYER                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Diff         │  │ Example      │  │ Test            │   │
│  │ Generator    │  │ Extractor    │  │ Generator       │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  MCP SERVER (5 tools)                                       │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────────┐  │
│  │ detect_    │ │ generate_  │ │ extract_examples       │  │
│  │ changes    │ │ doc_diff   │ │                        │  │
│  └────────────┘ └────────────┘ └────────────────────────┘  │
│  ┌────────────┐ ┌────────────────────────────────────────┐ │
│  │ run_doc_   │ │ create_update_pr                       │ │
│  │ tests      │ │                                        │ │
│  └────────────┘ └────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT LAYER                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Markdown     │  │ Test         │  │ GitHub          │   │
│  │ Patches      │  │ Reports      │  │ PRs             │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Change Detection Service
- **Git Watcher**: Monitor repos for new commits/releases
- **AST Parser**: Extract Python function signatures
- **Diff Analyzer**: Compare old vs new API surfaces
- **Breaking Change Detector**: Flag incompatible changes

### 2. Documentation Mapper
- **Doc Scanner**: Index all documentation pages
- **Code Block Finder**: Locate examples in markdown
- **API Linker**: Map functions to doc sections
- **Impact Analyzer**: Determine which docs need updates

### 3. Generation Engine
- **Diff Generator**: Create markdown patches
- **Example Extractor**: Pull code from docs
- **Test Generator**: Convert examples to pytest
- **PR Creator**: Format and submit GitHub PRs

---

## Data Flow

1. **Detect**: Watch SDK repos for changes
2. **Parse**: Extract API signatures with AST
3. **Compare**: Diff against previous version
4. **Map**: Find affected documentation
5. **Generate**: Create doc update patches
6. **Test**: Run all examples against new SDK
7. **PR**: Create update PR if tests fail

---

## Integration Points

| System | Integration Type | Purpose |
|--------|------------------|---------|
| statsforecast | Git clone | API extraction |
| nixtla SDK | Git clone | API extraction |
| mlforecast | Git clone | API extraction |
| Nixtla docs | Git clone/push | Doc updates |
| GitHub API | REST | PR creation |
| pytest | CLI | Example execution |

---

## CI/CD Integration

```yaml
# .github/workflows/docs-qa.yml
name: Documentation QA
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run doc tests
        run: /docs-qa run-tests --fail-on-drift
      - name: Create PR if drift detected
        if: failure()
        run: /docs-qa create-update-pr
```

---

## Deployment Model

- **Local Development**: Clone repos locally
- **CI**: GitHub Actions runner
- **Production**: Scheduled GitHub Actions workflow
