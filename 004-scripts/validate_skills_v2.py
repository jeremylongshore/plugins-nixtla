#!/usr/bin/env python3
"""
Claude Skills Validator v2.0 (Enterprise + Strict Quality Mode)

Combines:
- Anthropic 2025 Skills Specification (code.claude.com/docs/en/skills)
- Intent Solutions Enterprise Standard (6767-c v3.0.0)
- Nixtla Quality Standards (strict mode)

Based on source of truth:
- /home/jeremy/000-projects/claude-code-plugins/scripts/validate-skills-schema.py
- /home/jeremy/000-projects/claude-code-plugins/000-docs/6767-b-SPEC-MASTER-claude-skills-standard.md
- /home/jeremy/000-projects/claude-code-plugins/000-docs/6767-c-DR-STND-claude-code-extensions-standard.md

Usage:
    python 004-scripts/validate_skills_v2.py [--verbose|-v]

Author: Jeremy Longshore <jeremy@intentsolutions.io>
Version: 2.0.0
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# === CONSTANTS ===

# Valid tools per Claude Code spec (2025)
VALID_TOOLS = {
    'Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep',
    'WebFetch', 'WebSearch', 'Task', 'TodoWrite',
    'NotebookEdit', 'AskUserQuestion', 'Skill'
}

# Anthropic required fields (minimum spec)
ANTHROPIC_REQUIRED = {'name', 'description'}

# Enterprise required fields (Intent Solutions marketplace)
ENTERPRISE_REQUIRED = {'allowed-tools', 'version', 'author', 'license'}

# All required fields (Anthropic + Enterprise)
REQUIRED_FIELDS = ANTHROPIC_REQUIRED | ENTERPRISE_REQUIRED

# Optional fields per Anthropic spec
OPTIONAL_FIELDS = {'model', 'disable-model-invocation', 'mode', 'tags', 'metadata'}

# Deprecated fields (warn but don't error)
DEPRECATED_FIELDS = {'when_to_use'}

# Nixtla required sections (strict quality mode)
REQUIRED_SECTIONS = [
    "# ",  # title line
    "## Overview",
    "## Prerequisites",
    "## Instructions",
    "## Output",
    "## Error Handling",
    "## Examples",
    "## Resources",
]

# Regex patterns
RE_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
RE_DESCRIPTION_USE_WHEN = re.compile(r"\bUse when\b", re.IGNORECASE)
RE_DESCRIPTION_TRIGGER_WITH = re.compile(r"\bTrigger with\b", re.IGNORECASE)
RE_ABSOLUTE_PATH = re.compile(r"(^/|[A-Za-z]:\\)")
RE_BASEDIR_SCRIPTS = re.compile(r"{baseDir}/scripts/([\w\-./]+)")
RE_FIRST_PERSON = re.compile(r"\b(I can|I will|I'm going to|I help)\b", re.IGNORECASE)
RE_SECOND_PERSON = re.compile(r"\b(You can|You should|You will)\b", re.IGNORECASE)
FORBIDDEN_WORDS = ("anthropic", "claude")

# Defaults
DEFAULT_AUTHOR = "Jeremy Longshore <jeremy@intentsolutions.io>"
DEFAULT_LICENSE = "MIT"


# === UTILITY FUNCTIONS ===

def find_skill_files(root: Path) -> List[Path]:
    """Find all SKILL.md files, excluding archive and backup directories."""
    excluded_dirs = {"archive", "backups", "backup", ".git", "node_modules", "__pycache__", ".venv", "010-archive"}
    results = []
    for p in root.rglob("SKILL.md"):
        if p.is_file():
            parts = p.relative_to(root).parts
            if not any(part in excluded_dirs for part in parts):
                results.append(p)
    return results


def parse_frontmatter(content: str) -> Tuple[dict, str]:
    """Parse YAML frontmatter from SKILL.md content."""
    m = RE_FRONTMATTER.match(content)
    if not m:
        raise ValueError("Invalid or absent YAML frontmatter block at top of SKILL.md")
    front_str, body = m.groups()
    try:
        data = yaml.safe_load(front_str) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parse error: {e}")
    if not isinstance(data, dict):
        raise ValueError("Frontmatter is not a YAML mapping")
    return data, body


def parse_allowed_tools(tools_value: Any) -> List[str]:
    """Parse allowed-tools which can be CSV string or YAML array."""
    if isinstance(tools_value, list):
        return tools_value
    elif isinstance(tools_value, str):
        return [t.strip() for t in tools_value.split(',')]
    return []


def validate_tool_permission(tool: str) -> Tuple[bool, str]:
    """Validate a single tool permission including wildcards like Bash(git:*)."""
    base_tool = tool.split('(')[0].strip()

    if base_tool not in VALID_TOOLS:
        return False, f"Unknown tool: {base_tool}"

    # Validate wildcard syntax if present
    if '(' in tool:
        if not tool.endswith(')'):
            return False, f"Invalid wildcard syntax (missing closing paren): {tool}"
        inner = tool[tool.index('(')+1:-1]
        if ':' not in inner:
            return False, f"Wildcard missing colon (use cmd:*): {tool}"

    return True, ""


def estimate_word_count(content: str) -> int:
    """Estimate word count for content length check."""
    # Remove frontmatter
    content_body = re.sub(r'^---\n.*?\n---\n?', '', content, flags=re.DOTALL)
    return len(content_body.split())


# === VALIDATION FUNCTIONS ===

def validate_frontmatter(path: Path, fm: dict) -> Tuple[List[str], List[str]]:
    """
    Validate SKILL.md frontmatter.
    Returns: (errors, warnings)
    """
    errors: List[str] = []
    warnings: List[str] = []

    # === REQUIRED FIELDS (Anthropic + Enterprise) ===

    for key in REQUIRED_FIELDS:
        if key not in fm:
            errors.append(f"[frontmatter] Missing required field: '{key}'")

    # === FIELD-SPECIFIC VALIDATION ===

    # name field
    if 'name' in fm:
        name = str(fm['name']).strip()
        if not name:
            errors.append("[frontmatter] 'name' must be non-empty")
        else:
            # Kebab-case check
            if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', name) and len(name) > 1:
                errors.append(f"[frontmatter] 'name' must be kebab-case (lowercase + hyphens): {name}")

            # Length check
            if len(name) > 64:
                errors.append("[frontmatter] 'name' exceeds 64 characters")

            # Reserved words
            name_lower = name.lower()
            if 'anthropic' in name_lower or 'claude' in name_lower:
                errors.append(f"[frontmatter] 'name' contains reserved word: {name}")

            # Folder match check (best practice, not error)
            folder_name = path.parent.name
            if name != folder_name:
                warnings.append(f"[frontmatter] 'name' '{name}' differs from folder '{folder_name}' (best practice: match them)")

    # description field
    if 'description' in fm:
        desc = str(fm['description']).strip()

        if not desc:
            errors.append("[frontmatter] 'description' must be non-empty")
        else:
            # Length checks
            if len(desc) < 20:
                warnings.append("[frontmatter] 'description' too short (< 20 chars) - may not trigger well")
            if len(desc) > 1024:
                errors.append("[frontmatter] 'description' exceeds 1024 characters")

            # Nixtla strict quality checks (ERRORS in strict mode)
            if not RE_DESCRIPTION_USE_WHEN.search(desc):
                errors.append("[frontmatter] 'description' must include 'Use when ...' phrase (nixtla quality standard)")

            if not RE_DESCRIPTION_TRIGGER_WITH.search(desc):
                errors.append("[frontmatter] 'description' must include 'Trigger with ...' phrase (nixtla quality standard)")

            # Voice checks (nixtla strict mode)
            if RE_FIRST_PERSON.search(desc):
                errors.append("[frontmatter] 'description' must NOT use first person (I can / I will / etc.) - use third person")

            if RE_SECOND_PERSON.search(desc):
                errors.append("[frontmatter] 'description' must NOT use second person (You can / You should) - use third person")

            # Reserved words
            desc_lower = desc.lower()
            for bad in FORBIDDEN_WORDS:
                if bad in desc_lower:
                    errors.append(f"[frontmatter] 'description' contains reserved word: '{bad}'")

            # Imperative language check (best practice)
            imperative_starts = ['analyze', 'create', 'generate', 'build', 'debug',
                               'optimize', 'validate', 'test', 'deploy', 'monitor',
                               'fix', 'review', 'extract', 'convert', 'implement',
                               'detect', 'forecast', 'transform', 'compare']
            has_imperative = any(v in desc_lower for v in imperative_starts)
            if not has_imperative:
                warnings.append("[frontmatter] Consider using action verbs (analyze, detect, forecast, etc.)")

    # allowed-tools field
    if 'allowed-tools' in fm:
        tools = parse_allowed_tools(fm['allowed-tools'])

        if not tools:
            errors.append("[frontmatter] 'allowed-tools' is empty - must list at least one tool")

        for tool in tools:
            valid, msg = validate_tool_permission(tool)
            if not valid:
                errors.append(f"[frontmatter] allowed-tools: {msg}")

        # Nixtla strict mode: forbid unscoped Bash
        if 'Bash' in tools:
            errors.append("[frontmatter] allowed-tools: unscoped 'Bash' forbidden - use scoped Bash(git:*) or Bash(npm:*)")

        # Info about over-permissioning
        if len(tools) > 6:
            warnings.append(f"[frontmatter] Many tools permitted ({len(tools)}) - consider limiting for security")

    # version field
    if 'version' in fm:
        version = str(fm['version'])
        if not re.match(r'^\d+\.\d+\.\d+', version):
            errors.append(f"[frontmatter] 'version' should be semver format (X.Y.Z): {version}")

    # author field
    if 'author' in fm:
        author = str(fm['author']).strip()
        if not author:
            errors.append("[frontmatter] 'author' must be non-empty")
        # Recommend email format
        if '@' not in author:
            warnings.append("[frontmatter] 'author' best practice: include email (Name <email>)")

    # license field
    if 'license' in fm:
        license_val = str(fm['license']).strip()
        if not license_val:
            errors.append("[frontmatter] 'license' must be non-empty")

    # === OPTIONAL FIELDS ===

    # model field
    if 'model' in fm:
        model = fm['model']
        valid_models = ['inherit', 'sonnet', 'haiku', 'opus']
        if model not in valid_models and not str(model).startswith('claude-'):
            warnings.append(f"[frontmatter] 'model' value '{model}' not standard (use: inherit, sonnet, haiku, opus, or claude-*)")

    # disable-model-invocation field
    if 'disable-model-invocation' in fm:
        dmi = fm['disable-model-invocation']
        if not isinstance(dmi, bool):
            errors.append(f"[frontmatter] 'disable-model-invocation' must be boolean, got: {type(dmi).__name__}")

    # mode field
    if 'mode' in fm:
        mode = fm['mode']
        if not isinstance(mode, bool):
            errors.append(f"[frontmatter] 'mode' must be boolean, got: {type(mode).__name__}")

    # tags field
    if 'tags' in fm:
        tags = fm['tags']
        if not isinstance(tags, list):
            errors.append(f"[frontmatter] 'tags' must be array of strings, got: {type(tags).__name__}")
        elif not all(isinstance(t, str) for t in tags):
            errors.append("[frontmatter] 'tags' must contain only strings")

    # === DEPRECATED FIELDS ===

    for field in DEPRECATED_FIELDS:
        if field in fm:
            warnings.append(f"[frontmatter] Deprecated field '{field}' - use detailed 'description' instead")

    # === UNKNOWN FIELDS ===

    known_fields = REQUIRED_FIELDS | OPTIONAL_FIELDS | DEPRECATED_FIELDS
    unknown_fields = set(fm.keys()) - known_fields
    for field in unknown_fields:
        warnings.append(f"[frontmatter] Non-standard field: '{field}'")

    return errors, warnings


def validate_body(path: Path, body: str) -> Tuple[List[str], List[str]]:
    """
    Validate SKILL.md body content.
    Returns: (errors, warnings)
    """
    errors: List[str] = []
    warnings: List[str] = []
    lines = body.splitlines()

    # === LENGTH CHECKS ===

    # Nixtla strict mode: 500 line limit
    if len(lines) > 500:
        errors.append(f"[body] SKILL.md body has {len(lines)} lines (max 500). Use progressive disclosure (extract to references/)")

    # Source of truth: word count check
    word_count = len(body.split())
    if word_count > 5000:
        warnings.append(f"[body] Content exceeds 5000 words ({word_count}) - may overwhelm context")
    elif word_count > 3500:
        warnings.append(f"[body] Content is lengthy ({word_count} words) - consider references/ directory")

    # === REQUIRED SECTIONS (Nixtla strict mode) ===

    for sec in REQUIRED_SECTIONS:
        if sec not in body:
            errors.append(f"[body] Required section missing: '{sec}' (nixtla quality standard)")

    # === PATH CHECKS ===

    for i, line in enumerate(lines, start=1):
        # Absolute paths forbidden
        if RE_ABSOLUTE_PATH.search(line):
            errors.append(f"[body] Line {i}: contains absolute/OS-specific path - use '{{baseDir}}/...'")

        # Backslashes forbidden
        if "\\scripts\\" in line:
            errors.append(f"[body] Line {i}: uses backslashes in path - use forward slashes")

    # === VOICE CHECKS ===

    if re.search(r'\byou should\b|\byou can\b|\byou will\b', body, re.IGNORECASE):
        warnings.append("[body] Consider imperative language instead of 'you should/can/will'")

    return errors, warnings


def validate_scripts_exist(path: Path, body: str) -> List[str]:
    """
    Validate that all {baseDir}/scripts/... references point to real files.
    Nixtla strict mode: HARD FAIL if script doesn't exist.
    """
    errors: List[str] = []
    skill_dir = path.parent

    referenced = set(m.group(1) for m in RE_BASEDIR_SCRIPTS.finditer(body))

    for rel in sorted(referenced):
        script_path = (skill_dir / "scripts" / rel).resolve()

        # Ensure path doesn't escape skill directory
        try:
            script_path.relative_to(skill_dir)
        except ValueError:
            errors.append(f"[scripts] Reference escapes skill directory: {rel}")
            continue

        if not script_path.exists():
            errors.append(
                f"[scripts] Referenced script not found: '{{baseDir}}/scripts/{rel}' "
                f"(expected at {skill_dir.name}/scripts/{rel})"
            )

    return errors


def validate_skill(path: Path) -> Dict[str, Any]:
    """
    Validate a single SKILL.md file.
    Returns dict with errors, warnings, and metadata.
    """
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return {'fatal': f'Cannot read file: {e}'}

    try:
        fm, body = parse_frontmatter(content)
    except Exception as e:
        return {'fatal': str(e)}

    errors: List[str] = []
    warnings: List[str] = []

    # Validate frontmatter
    fm_errors, fm_warnings = validate_frontmatter(path, fm)
    errors.extend(fm_errors)
    warnings.extend(fm_warnings)

    # Validate body
    body_errors, body_warnings = validate_body(path, body)
    errors.extend(body_errors)
    warnings.extend(body_warnings)

    # Validate scripts
    script_errors = validate_scripts_exist(path, body)
    errors.extend(script_errors)

    return {
        'errors': errors,
        'warnings': warnings,
        'word_count': estimate_word_count(content),
        'line_count': len(body.splitlines())
    }


# === MAIN ===

def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    skills = find_skill_files(repo_root)

    if not skills:
        print("No SKILL.md files found - nothing to validate.")
        return 0

    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    print(f"🔍 CLAUDE CODE SKILLS VALIDATOR v2.0")
    print(f"   Enterprise + Nixtla Strict Quality Mode")
    print(f"   Source of Truth: claude-code-plugins repo")
    print(f"{'=' * 70}\n")
    print(f"Found {len(skills)} SKILL.md files to validate.\n")

    total_errors = 0
    total_warnings = 0
    files_with_errors = []
    files_with_warnings = []
    files_compliant = []

    for skill in skills:
        rel = skill.relative_to(repo_root)
        result = validate_skill(skill)

        if 'fatal' in result:
            print(f"❌ {rel}: FATAL - {result['fatal']}")
            total_errors += 1
            files_with_errors.append(str(rel))
            continue

        has_issues = False

        if result['errors']:
            print(f"❌ {rel}:")
            for error in result['errors']:
                print(f"   ERROR: {error}")
            total_errors += len(result['errors'])
            files_with_errors.append(str(rel))
            has_issues = True

        if result['warnings']:
            if not has_issues:
                print(f"⚠️  {rel}:")
            for warning in result['warnings']:
                print(f"   WARN: {warning}")
            total_warnings += len(result['warnings'])
            if str(rel) not in files_with_errors:
                files_with_warnings.append(str(rel))
            has_issues = True

        if verbose and not has_issues:
            print(f"✅ {rel} - OK ({result['word_count']} words, {result['line_count']} lines)")

        if not result['errors'] and not result['warnings']:
            files_compliant.append(str(rel))

    # Summary
    print(f"\n{'=' * 70}")
    print(f"📊 VALIDATION SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total skills validated: {len(skills)}")
    print(f"✅ Fully compliant: {len(files_compliant)}")
    print(f"⚠️  Warnings only: {len(files_with_warnings)}")
    print(f"❌ With errors: {len(files_with_errors)}")
    print(f"{'=' * 70}")

    # Compliance rate
    compliant_pct = (len(files_compliant) / len(skills) * 100) if skills else 0
    print(f"\n📈 Compliance rate: {compliant_pct:.1f}%")

    if total_errors > 0:
        print(f"\n❌ Validation FAILED with {total_errors} errors")
        print("\nTo fix: Add missing enterprise fields to all skills:")
        print("  author: \"Jeremy Longshore <jeremy@intentsolutions.io>\"")
        print("  license: \"MIT\"")
        return 1
    elif total_warnings > 0:
        print(f"\n⚠️  Validation PASSED with {total_warnings} warnings")
        print("(Warnings are best practices - not blocking)")
        return 0
    else:
        print(f"\n✅ All skills fully compliant!")
        print("   - Anthropic 2025 spec ✓")
        print("   - Enterprise standard ✓")
        print("   - Nixtla quality standards ✓")
        return 0


if __name__ == '__main__':
    sys.exit(main())
