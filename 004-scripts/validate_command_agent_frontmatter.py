#!/usr/bin/env python3
"""
Validates YAML frontmatter in command/agent markdown files for Nixtla Claude Code plugins.

Ported from: /home/jeremy/000-projects/claude-code-plugins/scripts/validate-frontmatter.py

Validates frontmatter in:
- 005-plugins/**/commands/*.md
- 005-plugins/**/agents/*.md

Author: Jeremy Longshore <jeremy@intentsolutions.io>
Version: 1.1.0
"""

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


def extract_frontmatter(file_path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Extract YAML frontmatter from markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return None, f"Cannot read file: {e}"

    # Match frontmatter between --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, "No frontmatter found"

    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return None, "Frontmatter is not a YAML mapping"
        return frontmatter, None
    except yaml.YAMLError as e:
        return None, f"Invalid YAML: {e}"


def validate_command_frontmatter(frontmatter: Dict[str, Any], file_path: Path) -> List[str]:
    """Validate frontmatter for command files."""
    errors = []

    # Required field: name
    if "name" not in frontmatter:
        errors.append("Missing required field: name")
    elif not isinstance(frontmatter["name"], str):
        errors.append("Field 'name' must be a string")
    else:
        name = frontmatter["name"]
        # Must be kebab-case
        if not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", name):
            errors.append("Field 'name' must be kebab-case (lowercase + hyphens)")
        # Should match filename (without .md extension)
        expected_name = file_path.stem
        if name != expected_name:
            errors.append(f"Field 'name' '{name}' should match filename '{expected_name}.md'")

    # Required field: description
    if "description" not in frontmatter:
        errors.append("Missing required field: description")
    elif not isinstance(frontmatter["description"], str):
        errors.append("Field 'description' must be a string")
    else:
        desc = frontmatter["description"]
        if len(desc) < 10:
            errors.append("Field 'description' must be at least 10 characters")
        if len(desc) > 80:
            errors.append("Field 'description' must be 80 characters or less")

    # Optional field: shortcut
    if "shortcut" in frontmatter:
        shortcut = frontmatter["shortcut"]
        if not isinstance(shortcut, str):
            errors.append("Field 'shortcut' must be a string")
        elif len(shortcut) < 1 or len(shortcut) > 4:
            errors.append("Field 'shortcut' must be 1-4 characters")
        elif not shortcut.islower():
            errors.append("Field 'shortcut' must be lowercase")
        elif not shortcut.isalpha():
            errors.append("Field 'shortcut' must contain only letters")

    # Optional field: category
    valid_categories = [
        "git",
        "deployment",
        "security",
        "testing",
        "documentation",
        "database",
        "api",
        "frontend",
        "backend",
        "devops",
        "forecasting",
        "analytics",
        "migration",
        "monitoring",
        "other",
    ]
    if "category" in frontmatter:
        if frontmatter["category"] not in valid_categories:
            errors.append(f"Invalid category. Must be one of: {', '.join(valid_categories)}")

    # Optional field: difficulty
    valid_difficulties = ["beginner", "intermediate", "advanced", "expert"]
    if "difficulty" in frontmatter:
        if frontmatter["difficulty"] not in valid_difficulties:
            errors.append(f"Invalid difficulty. Must be one of: {', '.join(valid_difficulties)}")

    return errors


def validate_agent_frontmatter(frontmatter: Dict[str, Any], file_path: Path) -> List[str]:
    """Validate current Claude Code agent fields plus the marketplace overlay."""
    errors = []

    allowed_fields = {
        "name",
        "description",
        "tools",
        "disallowedTools",
        "model",
        "permissionMode",
        "maxTurns",
        "skills",
        "mcpServers",
        "hooks",
        "memory",
        "background",
        "isolation",
        "effort",
        "color",
        "version",
        "author",
        "tags",
    }
    for field in sorted(set(frontmatter) - allowed_fields):
        errors.append(f"Unsupported agent field: {field}")

    # Required field: name
    if "name" not in frontmatter:
        errors.append("Missing required field: name")
    elif not isinstance(frontmatter["name"], str):
        errors.append("Field 'name' must be a string")
    else:
        name = frontmatter["name"]
        # Must be kebab-case
        if not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", name):
            errors.append("Field 'name' must be kebab-case (lowercase + hyphens)")

    # Required field: description
    if "description" not in frontmatter:
        errors.append("Missing required field: description")
    elif not isinstance(frontmatter["description"], str):
        errors.append("Field 'description' must be a string")
    else:
        desc = frontmatter["description"]
        if len(desc) < 20:
            errors.append("Field 'description' must be at least 20 characters")
        if len(desc) > 1536:
            errors.append("Field 'description' must be 1536 characters or less")

    # Marketplace-required execution and provenance fields.
    required_fields = {
        "tools": list,
        "disallowedTools": list,
        "model": str,
        "color": str,
        "version": str,
        "author": str,
        "tags": list,
    }
    for field, expected_type in required_fields.items():
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(frontmatter[field], expected_type):
            errors.append(f"Field '{field}' must be a {expected_type.__name__}")

    for field in ("tools", "disallowedTools", "skills", "tags"):
        value = frontmatter.get(field)
        if isinstance(value, list) and any(not isinstance(item, str) for item in value):
            errors.append(f"Field '{field}' must contain only strings")

    if isinstance(frontmatter.get("tools"), list) and not frontmatter["tools"]:
        errors.append("Field 'tools' must list at least one tool")
    if isinstance(frontmatter.get("tags"), list) and not frontmatter["tags"]:
        errors.append("Field 'tags' must list at least one tag")

    version = frontmatter.get("version")
    if isinstance(version, str) and not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("Field 'version' must use SemVer X.Y.Z")

    if "background" in frontmatter and not isinstance(frontmatter["background"], bool):
        errors.append("Field 'background' must be a boolean")

    return errors


def find_command_agent_files(root: Path) -> List[Tuple[Path, str]]:
    """Find all command and agent markdown files in 005-plugins/."""
    results = []

    plugins_dir = root / "005-plugins"
    if not plugins_dir.exists():
        return results

    # Find command files
    for cmd_file in plugins_dir.rglob("commands/*.md"):
        if cmd_file.is_file():
            results.append((cmd_file, "command"))

    # Find agent files
    for agent_file in plugins_dir.rglob("agents/*.md"):
        if agent_file.is_file():
            results.append((agent_file, "agent"))

    return results


def validate_file(file_path: Path, file_type: str) -> Dict[str, Any]:
    """Validate a single command or agent markdown file."""
    # Extract frontmatter
    frontmatter, error = extract_frontmatter(file_path)
    if error:
        return {"fatal": error}

    # Validate based on file type
    if file_type == "command":
        errors = validate_command_frontmatter(frontmatter, file_path)
    elif file_type == "agent":
        errors = validate_agent_frontmatter(frontmatter, file_path)
    else:
        return {"fatal": f"Unknown file type: {file_type}"}

    return {"errors": errors}


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    files = find_command_agent_files(repo_root)

    if not files:
        print("No command or agent files found - nothing to validate.")
        return 0

    print(f"🔍 COMMAND/AGENT FRONTMATTER VALIDATOR")
    print(f"   Nixtla Plugin Standard")
    print(f"{'=' * 70}\n")
    print(f"Found {len(files)} files to validate.\n")

    total_errors = 0
    files_with_errors = []
    files_compliant = []

    for file_path, file_type in files:
        rel = file_path.relative_to(repo_root)
        result = validate_file(file_path, file_type)

        if "fatal" in result:
            print(f"❌ {rel} ({file_type}): FATAL - {result['fatal']}")
            total_errors += 1
            files_with_errors.append(str(rel))
            continue

        if result["errors"]:
            print(f"❌ {rel} ({file_type}):")
            for error in result["errors"]:
                print(f"   ERROR: {error}")
            total_errors += len(result["errors"])
            files_with_errors.append(str(rel))
        else:
            files_compliant.append(str(rel))
            print(f"✅ {rel} ({file_type}) - OK")

    # Summary
    print(f"\n{'=' * 70}")
    print(f"📊 VALIDATION SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total files validated: {len(files)}")
    print(f"✅ Fully compliant: {len(files_compliant)}")
    print(f"❌ With errors: {len(files_with_errors)}")
    print(f"{'=' * 70}")

    # Compliance rate
    compliant_pct = (len(files_compliant) / len(files) * 100) if files else 0
    print(f"\n📈 Compliance rate: {compliant_pct:.1f}%")

    if total_errors > 0:
        print(f"\n❌ Validation FAILED with {total_errors} errors")
        return 1
    else:
        print(f"\n✅ All command/agent files fully compliant!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
