# Claude Skills Deep Dive - Complete Requirements Analysis
**Source:** https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
**Author:** Lee Han Chung
**Analyzed:** 2025-12-21
**Analyst:** Intent Solutions Engineering Team

---

## Executive Summary

Lee Han Chung's deep dive reveals **91 distinct requirements** for building production-grade Claude Code Skills. Our current validators cover approximately **40% of these requirements**. This document provides:

1. Complete requirement extraction (forward + backward reading)
2. Gap analysis vs current validators
3. Implementation roadmap for missing validations
4. Non-negotiable standards for Intent Solutions

---

## Part 1: Complete Requirements Catalog (91 Items)

### A. YAML Frontmatter Requirements (23 items)

#### Required Fields (Anthropic Spec)
1. ✅ **name** - Skill identifier, used as command parameter
2. ✅ **description** - Brief summary determining when Claude invokes

#### Enterprise Required (Intent Solutions Standard)
3. ✅ **allowed-tools** - Tool permissions for security (CSV format)
4. ✅ **version** - Semantic versioning (e.g., 1.0.0)
5. ✅ **author** - Creator attribution
6. ✅ **license** - License (MIT recommended)

#### Optional Fields (Anthropic Spec)
7. ✅ **model** - Override model for skill execution (defaults to session model)
8. ✅ **disable-model-invocation** - Boolean preventing automatic invocation (manual `/skill-name` only)
9. ✅ **mode** - Boolean categorizing as mode command (appears in special section)
10. ⚠️ **tags** - Categorization keywords (validator checks but doesn't enforce)

#### Deprecated/Avoid
11. ✅ **when_to_use** - Undocumented, possibly deprecated (validator warns)

#### Field Constraints
12. ✅ name: Kebab-case format (lowercase + hyphens)
13. ✅ name: Max 64 characters
14. ⚠️ name: Should match folder name (INFO level, not enforced)
15. ✅ description: Min 20 characters recommended
16. ✅ description: Max 1,024 characters (hard limit)
17. ⚠️ description: Action-oriented language recommended
18. ✅ version: Semantic versioning format (x.y.z)
19. ✅ model: Valid values: inherit, sonnet, haiku, claude-*
20. ✅ allowed-tools: Comma-separated string format (NOT array)
21. ✅ allowed-tools: Support wildcards (e.g., Bash(git:*), Bash(npm:*))
22. ⚠️ allowed-tools: Minimize to necessity (6+ tools triggers INFO)
23. ❌ **Frontmatter size: Max 15,000 characters** (token budget limit) - NOT CHECKED

### B. Content Structure Requirements (18 items)

#### Markdown Content Organization
24. ❌ **Brief purpose statement** (1-2 sentences) - NOT CHECKED
25. ❌ **Overview section** - NOT CHECKED
26. ❌ **Prerequisites section** - NOT CHECKED
27. ❌ **Step-by-step instructions** - NOT CHECKED
28. ❌ **Output format specifications** - NOT CHECKED
29. ❌ **Error handling guidance** - NOT CHECKED
30. ❌ **Examples section** - NOT CHECKED

#### Content Quality Standards
31. ✅ Keep under 5,000 words (validator checks)
32. ⚠️ Use imperative language (partial check via keywords)
33. ❌ **Reference external files rather than embedding** - NOT CHECKED
34. ✅ Use {baseDir} variable for portable paths (validator checks hardcoded paths)
35. ✅ Never hardcode absolute paths (validator detects /home/, /Users/, C:\)

#### Writing Style
36. ⚠️ Imperative language ("Analyze code for...") - partial check
37. ⚠️ Avoid second-person phrasing ("you should/can/will") - INFO level check
38. ❌ **Action-oriented description** enabling accurate Claude matching - NOT FULLY CHECKED
39. ⚠️ Comprehensive without excessive verbosity - subjective, word count only
40. ❌ **Inline comments explaining complex workflows** - NOT CHECKED
41. ❌ **Organized resource directories with obvious purposes** - NOT CHECKED

### C. Resource Organization Requirements (15 items)

#### /scripts Directory
42. ❌ **Use /scripts for executable Python/Bash automation** - NOT CHECKED
43. ❌ **Scripts should be deterministic operations** - NOT CHECKED
44. ❌ **Claude invokes via Bash tool** - NOT CHECKED
45. ❌ **Example: python {baseDir}/scripts/init_skill.py <skill-name>** - NOT CHECKED

#### /references Directory
46. ❌ **Use /references for text documentation** - NOT CHECKED
47. ❌ **Loaded into context via Read tool** - NOT CHECKED
48. ❌ **Markdown files, JSON schemas, configuration templates** - NOT CHECKED
49. ❌ **Content injected when Claude needs detailed information** - NOT CHECKED

#### /assets Directory
50. ❌ **Use /assets for templates and binary files** - NOT CHECKED
51. ❌ **Referenced by path only, not loaded into context** - NOT CHECKED
52. ❌ **HTML/CSS templates, images, configuration boilerplate** - NOT CHECKED
53. ❌ **Files Claude manipulates or references** - NOT CHECKED

#### Directory Structure Validation
54. ❌ **Check /scripts exists if referenced** - NOT CHECKED
55. ❌ **Check /references exists if referenced** - NOT CHECKED
56. ❌ **Check /assets exists if referenced** - NOT CHECKED

### D. Tool Permissions & Security (12 items)

#### Tool Permission Design
57. ✅ Include only what skill genuinely needs
58. ✅ Use wildcards for scoped access: Bash(git:*), Bash(npm:*)
59. ⚠️ Narrow surface area prevents security risks (6+ tools = INFO)
60. ✅ Comma-separated format
61. ✅ Support tool-specific wildcards

#### Valid Tools
62. ✅ Read, Write, Edit, Bash, Glob, Grep - all checked
63. ✅ WebFetch, WebSearch, Task, TodoWrite - all checked
64. ✅ NotebookEdit, AskUserQuestion, Skill - all checked

#### Security Best Practices
65. ⚠️ Minimize allowed-tools to necessity
66. ⚠️ Avoid granting all-encompassing tool access
67. ✅ Use tool-specific wildcards where appropriate
68. ❌ **Test permission restrictions before deployment** - NOT AUTOMATED

### E. Performance Guidelines (6 items)

69. ✅ Keep main prompt under 5,000 words
70. ⚠️ Offload verbose content to /references (suggested, not enforced)
71. ⚠️ Use /assets for templates to avoid context consumption
72. ❌ **Structure scripts for deterministic execution** - NOT CHECKED
73. ⚠️ Content 3,500-5,000 words triggers INFO (consider references/)
74. ❌ **Progressive disclosure pattern** - NOT CHECKED

### F. Portability Requirements (5 items)

75. ✅ Use {baseDir} exclusively for relative paths
76. ✅ Never hardcode user paths (/home/, /Users/)
77. ✅ Never hardcode installation directories
78. ❌ **Ensure scripts work across different environments** - NOT CHECKED
79. ❌ **Document environment dependencies** - NOT CHECKED

### G. Discovery & Invocation (8 items)

#### CLI Invocation
80. ❌ **Manual invocation using /skill-name [arguments] syntax** - NOT DOCUMENTED
81. ❌ **Bypasses automatic invocation restrictions** - NOT CHECKED
82. ❌ **Works with disable-model-invocation: true** - NOT VERIFIED

#### Discovery Sources
83. ❌ **Skills scanned from ~/.config/claude/skills/** - NOT CHECKED
84. ❌ **Skills scanned from .claude/skills/** - NOT CHECKED
85. ❌ **Skills scanned from plugin-provided skills** - NOT CHECKED
86. ❌ **Skills scanned from built-in skills** - NOT CHECKED
87. ❌ **Token budget constraint: 15,000 character limit default** - NOT CHECKED
88. ❌ **All sources aggregated into single available list** - NOT CHECKED

### H. Execution Context (3 items)

89. ❌ **Skills modify conversation context via isMeta: true messages** - NOT CHECKED
90. ❌ **Skills modify execution context via pre-approved tool permissions** - NOT DOCUMENTED
91. ❌ **Two distinct user messages per invocation (isMeta: false + true)** - NOT VERIFIED

---

## Part 2: Common Skill Patterns (8 patterns)

Lee identifies 8 common patterns. Our validators don't detect or suggest these:

1. ❌ **Script Automation** - Execute Python/Bash scripts, Claude processes output
2. ❌ **Read-Process-Write** - Standard ETL pattern
3. ❌ **Search-Analyze-Report** - Grep → Read → Analyze → Report
4. ❌ **Command Chain Execution** - Multi-step operations with dependencies
5. ❌ **Wizard-Style Workflows** - Multi-step with user confirmation
6. ❌ **Template-Based Generation** - Load templates → fill → write
7. ❌ **Iterative Refinement** - Broad scan → deep analysis → recommendations
8. ❌ **Context Aggregation** - Synthesize from multiple files/tools

**Recommendation:** Add pattern detection to validator with suggestions.

---

## Part 3: Gap Analysis - What's Missing

### Critical Gaps (Breaking Production Standards)

#### 1. Resource Directory Validation
**Article Requirement:** Skills should organize resources in /scripts, /references, /assets
**Current State:** ❌ Not checked
**Impact:** HIGH - Skills may be disorganized, inefficient
**Fix Required:** Add directory structure validation

#### 2. Content Structure Validation
**Article Requirement:** Should include purpose, overview, prerequisites, steps, output format, error handling, examples
**Current State:** ❌ Not checked
**Impact:** HIGH - Skills may lack critical sections
**Fix Required:** Add content structure detection

#### 3. Frontmatter Size Limit
**Article Requirement:** Max 15,000 characters (token budget)
**Current State:** ❌ Not checked
**Impact:** MEDIUM - Could exceed context limits
**Fix Required:** Add frontmatter size validation

#### 4. Script Determinism
**Article Requirement:** Scripts should be deterministic operations
**Current State:** ❌ Not checked
**Impact:** MEDIUM - Scripts may have side effects
**Fix Required:** Add script validation (check for idempotency markers)

#### 5. Pattern Detection
**Article Requirement:** Skills follow 8 common patterns
**Current State:** ❌ No pattern detection
**Impact:** LOW - Organizational/quality issue
**Fix Required:** Add pattern detection and suggestions

### Moderate Gaps (Quality Issues)

#### 6. Enhanced Action-Oriented Language Check
**Article Requirement:** Description uses action-oriented language enabling Claude matching
**Current State:** ⚠️ Partial check via imperative keywords
**Impact:** MEDIUM - May affect skill invocation accuracy
**Fix Required:** Enhanced NLP-based action detection

#### 7. Reference vs Embed Detection
**Article Requirement:** Reference external files rather than embedding
**Current State:** ❌ Not checked
**Impact:** MEDIUM - Context bloat
**Fix Required:** Detect large code blocks that should be in /references

#### 8. Environment Dependency Documentation
**Article Requirement:** Document environment dependencies
**Current State:** ❌ Not checked
**Impact:** LOW - Portability issues
**Fix Required:** Check for dependency documentation

### Minor Gaps (Informational)

#### 9. CLI Invocation Documentation
**Article Requirement:** Document /skill-name [arguments] syntax
**Current State:** ❌ Not checked
**Impact:** LOW - User experience
**Fix Required:** Check for CLI usage examples

#### 10. Progressive Disclosure Pattern
**Article Requirement:** Implement tiered information loading
**Current State:** ❌ Not documented/checked
**Impact:** LOW - Optimization opportunity
**Fix Required:** Document pattern in skill templates

---

## Part 4: Validator Enhancement Roadmap

### Phase 1: Critical Fixes (Week 1)

**Priority 1A: Resource Directory Validation**
```python
def validate_resource_directories(skill_path: Path) -> List[str]:
    """Check for proper /scripts, /references, /assets structure"""
    issues = []

    # Check if directories exist when referenced in content
    scripts_dir = skill_path / "scripts"
    references_dir = skill_path / "references"
    assets_dir = skill_path / "assets"

    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()

    # Check for {baseDir}/scripts references
    if "{baseDir}/scripts" in content:
        if not scripts_dir.exists():
            issues.append("References {baseDir}/scripts but /scripts directory missing")
        else:
            # Check scripts are executable
            for script in scripts_dir.glob("*"):
                if script.suffix in ['.py', '.sh'] and not os.access(script, os.X_OK):
                    issues.append(f"Script not executable: {script.name}")

    # Check for {baseDir}/references references
    if "{baseDir}/references" in content:
        if not references_dir.exists():
            issues.append("References {baseDir}/references but /references directory missing")
        else:
            # Check references are text files
            for ref in references_dir.glob("*"):
                if ref.suffix not in ['.md', '.json', '.yaml', '.yml', '.txt']:
                    issues.append(f"Non-text file in references/: {ref.name}")

    # Check for {baseDir}/assets references
    if "{baseDir}/assets" in content:
        if not assets_dir.exists():
            issues.append("References {baseDir}/assets but /assets directory missing")

    return issues
```

**Priority 1B: Frontmatter Size Validation**
```python
def validate_frontmatter_size(content: str) -> List[str]:
    """Check frontmatter doesn't exceed 15,000 character token budget"""
    issues = []

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        char_count = len(frontmatter_text)

        if char_count > 15000:
            issues.append(f"Frontmatter exceeds 15,000 character limit ({char_count} chars)")
        elif char_count > 12000:
            issues.append(f"Frontmatter approaching limit ({char_count}/15000 chars)")

    return issues
```

**Priority 1C: Content Structure Validation**
```python
def validate_content_structure(content: str) -> Dict[str, bool]:
    """Check for recommended content sections"""
    # Remove frontmatter
    body = re.sub(r'^---\n.*?\n---\n?', '', content, flags=re.DOTALL)

    checks = {
        'has_purpose': bool(re.search(r'(?:^|\n)## Purpose|## Overview', body, re.IGNORECASE)),
        'has_prerequisites': bool(re.search(r'(?:^|\n)## Prerequisites?|## Requirements?', body, re.IGNORECASE)),
        'has_instructions': bool(re.search(r'(?:^|\n)## (?:Steps?|Instructions?|Usage)', body, re.IGNORECASE)),
        'has_examples': bool(re.search(r'(?:^|\n)## Examples?|```', body, re.IGNORECASE)),
        'has_error_handling': bool(re.search(r'(?:error|exception|troubleshoot|debug)', body, re.IGNORECASE)),
    }

    return checks
```

### Phase 2: Quality Enhancements (Week 2)

**Priority 2A: Pattern Detection**
```python
SKILL_PATTERNS = {
    'Script Automation': {
        'indicators': ['python {baseDir}/scripts', 'bash {baseDir}/scripts', 'Bash tool'],
        'description': 'Execute Python/Bash scripts for complex operations'
    },
    'Read-Process-Write': {
        'indicators': ['Read tool', 'Write tool', 'transform', 'process'],
        'description': 'Standard ETL pattern: read input, transform, write output'
    },
    'Search-Analyze-Report': {
        'indicators': ['Grep tool', 'search', 'analyze', 'report'],
        'description': 'Find patterns, read matches, analyze, generate report'
    },
    'Template-Based Generation': {
        'indicators': ['{baseDir}/assets', 'template', 'placeholder'],
        'description': 'Load templates, fill placeholders, write results'
    },
    # ... other patterns
}

def detect_skill_pattern(content: str) -> Optional[str]:
    """Detect which common pattern a skill follows"""
    content_lower = content.lower()

    for pattern_name, pattern_def in SKILL_PATTERNS.items():
        matches = sum(1 for indicator in pattern_def['indicators']
                     if indicator.lower() in content_lower)
        if matches >= 2:
            return pattern_name

    return None
```

**Priority 2B: Enhanced Action-Oriented Language**
```python
ACTION_VERBS = [
    # Analysis
    'analyze', 'audit', 'inspect', 'investigate', 'examine', 'review',
    # Creation
    'create', 'generate', 'build', 'construct', 'compose', 'design',
    # Modification
    'update', 'modify', 'refactor', 'optimize', 'improve', 'enhance',
    # Debugging
    'debug', 'fix', 'troubleshoot', 'diagnose', 'resolve',
    # Deployment
    'deploy', 'publish', 'release', 'install', 'configure',
    # Testing
    'test', 'validate', 'verify', 'check', 'ensure',
    # Monitoring
    'monitor', 'track', 'observe', 'measure', 'report',
]

def validate_action_oriented(description: str) -> Tuple[bool, str]:
    """Enhanced check for action-oriented language"""
    desc_lower = description.lower()

    # Check for action verbs
    has_action_verb = any(verb in desc_lower for verb in ACTION_VERBS)

    # Check for passive voice (discouraged)
    passive_indicators = [' is ', ' are ', ' was ', ' were ', ' been ']
    has_passive = any(ind in desc_lower for ind in passive_indicators)

    if not has_action_verb:
        return False, "Description lacks action-oriented language (use verbs like analyze, create, debug)"

    if has_passive:
        return True, "INFO: Consider active voice instead of passive"

    return True, "OK"
```

### Phase 3: Advanced Features (Week 3)

**Priority 3A: Script Determinism Check**
```python
def check_script_determinism(script_path: Path) -> List[str]:
    """Check if scripts appear deterministic"""
    issues = []
    content = script_path.read_text()

    # Warning signs of non-deterministic behavior
    warning_patterns = [
        (r'random\.', 'Uses random number generation'),
        (r'\bdate\b|\btime\b', 'Uses current time/date'),
        (r'uuid\.', 'Generates UUIDs'),
        (r'\$\(date\)', 'Shell command uses date'),
    ]

    for pattern, description in warning_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"Potential non-determinism: {description}")

    return issues
```

**Priority 3B: Embed vs Reference Detection**
```python
def check_embed_vs_reference(content: str) -> List[str]:
    """Detect large embedded content that should be in /references"""
    issues = []

    # Find all code blocks
    code_blocks = re.findall(r'```.*?```', content, re.DOTALL)

    for i, block in enumerate(code_blocks):
        lines = block.count('\n')
        if lines > 50:
            issues.append(f"Large code block ({lines} lines) at position {i+1} - consider moving to /references")

    # Check for large JSON/YAML blocks
    json_blocks = re.findall(r'\{[^}]{500,}\}', content, re.DOTALL)
    if json_blocks:
        issues.append(f"Large JSON structure detected - consider moving to /references")

    return issues
```

---

## Part 5: Intent Solutions Non-Negotiable Standards

Based on Lee's article, these are **MANDATORY** for all Intent Solutions skills (user said: "the optionals are not optional for us"):

### Mandatory Fields (All Skills)
1. ✅ name
2. ✅ description
3. ✅ allowed-tools (CSV format, minimal permissions)
4. ✅ version (semantic versioning)
5. ✅ author
6. ✅ license

### Mandatory Content Sections
7. ❌ Purpose statement (1-2 sentences)
8. ❌ Overview section
9. ❌ Prerequisites section
10. ❌ Step-by-step instructions
11. ❌ Output format specifications
12. ❌ Error handling guidance
13. ❌ Examples section

### Mandatory Organization
14. ❌ Use /scripts for executable automation
15. ❌ Use /references for documentation
16. ❌ Use /assets for templates
17. ✅ Use {baseDir} for all relative paths
18. ✅ No hardcoded absolute paths

### Mandatory Security
19. ✅ Minimal tool permissions
20. ✅ Tool-specific wildcards where appropriate
21. ❌ Test permission restrictions before deployment

### Mandatory Performance
22. ✅ Keep under 5,000 words
23. ❌ Offload verbose content to /references
24. ❌ Use /assets for templates

### Mandatory Quality
25. ⚠️ Action-oriented description
26. ⚠️ Imperative language
27. ✅ No second-person phrasing
28. ❌ Inline comments for complex workflows

### Mandatory Portability
29. ✅ {baseDir} exclusively
30. ❌ Cross-environment script testing
31. ❌ Document environment dependencies

---

## Part 6: Implementation Checklist

### Immediate Actions (This Week)

- [ ] Create enhanced validator: `scripts/validate-skills-lee-standard.py`
- [ ] Add resource directory validation
- [ ] Add frontmatter size check (15,000 char limit)
- [ ] Add content structure detection
- [ ] Add pattern detection
- [ ] Add enhanced action-oriented language check
- [ ] Add embed vs reference detection

### Documentation Updates

- [ ] Create 6767-d-lee-han-chung-skills-standard.md
- [ ] Update SKILLS-SCHEMA-2025.md with Lee's requirements
- [ ] Create skill-patterns-guide.md (8 common patterns)
- [ ] Update templates to include all mandatory sections

### Testing

- [ ] Run new validator against all 241 existing skills
- [ ] Fix compliance issues in existing skills
- [ ] Create test suite for validator
- [ ] Add CI/CD validation step

### Quality Gates

- [ ] Block deployment if missing mandatory sections
- [ ] Block deployment if frontmatter > 15,000 chars
- [ ] Block deployment if hardcoded paths detected
- [ ] Block deployment if resource directories referenced but missing
- [ ] Warn if no recognizable pattern detected
- [ ] Warn if description not action-oriented

---

## Part 7: Metrics & Compliance

### Current Compliance (Estimated)

Based on this analysis, our current skills are approximately:

- **40% compliant** with Anthropic spec (name, description)
- **60% compliant** with Intent Solutions enterprise standard (+ allowed-tools, version, author, license)
- **20% compliant** with Lee Han Chung's full standard (missing resource dirs, content structure, patterns)

### Target Compliance

Intent Solutions target (non-negotiable):

- **100% compliant** with all 91 requirements
- **100% of skills** include all 7 mandatory content sections
- **100% of skills** use proper resource organization (/scripts, /references, /assets)
- **100% of skills** follow at least one of 8 common patterns
- **100% of skills** have action-oriented descriptions
- **0 skills** with hardcoded paths
- **0 skills** exceeding 5,000 words or 15,000 char frontmatter

---

## Conclusion

Lee Han Chung's deep dive reveals that building production-grade Claude Code Skills requires attention to **91 distinct requirements** across 8 major categories. Our current validators cover approximately 40% of these requirements.

**Critical gaps:**
1. Resource directory validation (HIGH impact)
2. Content structure validation (HIGH impact)
3. Frontmatter size limits (MEDIUM impact)
4. Script determinism checks (MEDIUM impact)
5. Pattern detection (LOW impact, high value)

**Recommendation:** Implement Phase 1 (Critical Fixes) immediately, targeting 100% compliance within 2 weeks.

**ROI:** Higher quality skills, better Claude invocation accuracy, improved user experience, reduced context bloat, enhanced security.

---

**Document ID:** LEE-001
**Version:** 1.0.0
**Status:** Analysis Complete - Implementation Pending
**Next Action:** Create Beads epic and 6767 standard document
