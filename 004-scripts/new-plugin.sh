#!/bin/bash
# ============================================================
# new-plugin.sh - Scaffold new plugin with documentation
#
# Usage: ./004-scripts/new-plugin.sh <slug> "<Name>" <category>
# Example: ./004-scripts/new-plugin.sh nixtla-cost-optimizer "Cost Optimizer" efficiency
# ============================================================

set -e

PLUGIN_SLUG=$1
PLUGIN_NAME=$2
CATEGORY=$3  # efficiency or growth

if [ -z "$PLUGIN_SLUG" ] || [ -z "$PLUGIN_NAME" ]; then
  echo "❌ Usage: ./004-scripts/new-plugin.sh <slug> \"<Name>\" [category]"
  echo "   Example: ./004-scripts/new-plugin.sh nixtla-cost-optimizer \"Cost Optimizer\" efficiency"
  exit 1
fi

# Enforce kebab-case slug (matches skills/plugin validators)
if ! echo "$PLUGIN_SLUG" | grep -qE '^[a-z][a-z0-9-]*[a-z0-9]$'; then
  echo "❌ Invalid slug: '$PLUGIN_SLUG'"
  echo "   Use kebab-case starting with a letter (e.g., nixtla-cost-optimizer)"
  exit 1
fi

CATEGORY=${CATEGORY:-efficiency}
CATEGORY_DISPLAY=$(echo "$CATEGORY" | sed 's/^./\U&/')
TODAY=$(date +%Y-%m-%d)
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

echo "🔧 Creating plugin: $PLUGIN_NAME ($PLUGIN_SLUG)"
echo "   Category: $CATEGORY"
echo "   Date: $TODAY"
echo ""

# Create plugin directory structure
echo "📁 Creating plugin directory..."
mkdir -p "$REPO_ROOT/005-plugins/$PLUGIN_SLUG"/{.claude-plugin,commands,agents,tests}
mkdir -p "$REPO_ROOT/005-plugins/$PLUGIN_SLUG/skills/$PLUGIN_SLUG"/{scripts,references,assets/templates}

# Create plugin.json
cat > "$REPO_ROOT/005-plugins/$PLUGIN_SLUG/.claude-plugin/plugin.json" << EOF
{
  "name": "$PLUGIN_SLUG",
  "version": "0.1.0",
  "description": "$PLUGIN_NAME - [Add description]",
  "author": { "name": "Intent Solutions", "email": "jeremy@intentsolutions.io" },
  "license": "MIT",
  "mcpServers": {
    "$PLUGIN_SLUG": {
      "command": "python",
      "args": ["skills/$PLUGIN_SLUG/scripts/${PLUGIN_SLUG//-/_}_mcp_server.py"]
    }
  }
}
EOF

# Create skill SKILL.md (strict/Lee-compliant template)
TITLE_CASE=$(echo "$PLUGIN_SLUG" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++){ $i=toupper(substr($i,1,1)) substr($i,2)}; print}')
SKILL_DESC="Generates and operates $PLUGIN_NAME workflows. Use when scaffolding, operating, or extending $PLUGIN_SLUG. Trigger with '$PLUGIN_SLUG', 'run $PLUGIN_SLUG', or 'setup $PLUGIN_SLUG'."

cat > "$REPO_ROOT/005-plugins/$PLUGIN_SLUG/skills/$PLUGIN_SLUG/SKILL.md" << EOF
---
name: $PLUGIN_SLUG
description: "$SKILL_DESC"
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash(python:*)"
version: "0.1.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# $TITLE_CASE

Scaffold and operate the $TITLE_CASE plugin workflows with validated structure and predictable outputs.

## Overview

This skill helps you build and iterate on the \`$PLUGIN_SLUG\` plugin safely:

- Generate a compliant plugin manifest and skill package
- Create a starter MCP server entrypoint
- Provide a predictable structure for commands/agents/tests

## Prerequisites

- Python 3.11+
- Repo dev deps installed (\`pip install -r requirements-dev.txt\`)

## Instructions

1. Review the generated manifest: \`005-plugins/$PLUGIN_SLUG/.claude-plugin/plugin.json\`
2. Implement tool logic in: \`{baseDir}/scripts/${PLUGIN_SLUG//-/_}_mcp_server.py\`
3. Validate locally:
   - \`python 004-scripts/validate_skills_v2.py --fail-on-warn\`
   - \`bash 004-scripts/validate-all-plugins.sh 005-plugins/$PLUGIN_SLUG\`

## Output

- \`.claude-plugin/plugin.json\`: plugin manifest (schema-valid)
- \`skills/$PLUGIN_SLUG/SKILL.md\`: skill definition (strict-compliant)
- \`skills/$PLUGIN_SLUG/scripts/${PLUGIN_SLUG//-/_}_mcp_server.py\`: MCP server stub

## Error Handling

1. **Error**: Validator fails with missing fields
   **Solution**: Ensure required frontmatter and manifest fields are present and non-empty.

2. **Error**: Script path errors
   **Solution**: Ensure scripts are referenced as \`{baseDir}/scripts/<file>\` and exist under the skill folder.

## Examples

### Example 1: Run validators

\`\`\`bash
python 004-scripts/validate_skills_v2.py --fail-on-warn
bash 004-scripts/validate-all-plugins.sh 005-plugins/$PLUGIN_SLUG
\`\`\`

## Resources

- Plugin spec: https://code.claude.com/docs/en/plugins
- Skill authoring template: \`003-skills/.claude/skills/nixtla-plugin-scaffolder/assets/templates/skill_template.md\`
EOF

# Create MCP server stub under the skill package (matches plugin.json args)
cat > "$REPO_ROOT/005-plugins/$PLUGIN_SLUG/skills/$PLUGIN_SLUG/scripts/${PLUGIN_SLUG//-/_}_mcp_server.py" << EOF
#!/usr/bin/env python3
\"\"\"$TITLE_CASE MCP server stub.\"\"\"

from __future__ import annotations

import json
import sys
from typing import Any, Dict


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "ping":
        return {"ok": True, "message": "pong"}
    return {"ok": False, "error": f"Unknown tool: {name}", "known_tools": ["ping"]}


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    request = json.loads(raw)
    response = handle_tool_call(request.get("name", ""), request.get("arguments", {}) or {})
    sys.stdout.write(json.dumps(response))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF
chmod +x "$REPO_ROOT/005-plugins/$PLUGIN_SLUG/skills/$PLUGIN_SLUG/scripts/${PLUGIN_SLUG//-/_}_mcp_server.py"

# Create plugin README
cat > "$REPO_ROOT/005-plugins/$PLUGIN_SLUG/README.md" << EOF
# $PLUGIN_NAME

> [One-line description]

## Quick Start

\`\`\`bash
# Setup
./scripts/setup.sh

# In Claude Code
/[command-name] [params]
\`\`\`

## Documentation

- [Business Case](../../000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG/01-BUSINESS-CASE.md)
- [PRD](../../000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG/02-PRD.md)
- [Architecture](../../000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG/03-ARCHITECTURE.md)
- [User Journey](../../000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG/04-USER-JOURNEY.md)
- [Technical Spec](../../000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG/05-TECHNICAL-SPEC.md)
- [Status](../../000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG/06-STATUS.md)
EOF

# Create docs directory
echo "📄 Creating documentation..."
mkdir -p "$REPO_ROOT/000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG"

# Copy and customize templates
for template in 01-BUSINESS-CASE 02-PRD 03-ARCHITECTURE 04-USER-JOURNEY 05-TECHNICAL-SPEC 06-STATUS; do
  if [ -f "$REPO_ROOT/000-docs/000a-dev-planning-templates/$template-TEMPLATE.md" ]; then
    sed -e "s/\[Plugin Name\]/$PLUGIN_NAME/g" \
        -e "s/\[plugin-slug\]/$PLUGIN_SLUG/g" \
        -e "s/\[TODAY\]/$TODAY/g" \
        -e "s/\[Efficiency | Growth\]/$CATEGORY_DISPLAY/g" \
        "$REPO_ROOT/000-docs/000a-dev-planning-templates/$template-TEMPLATE.md" > "$REPO_ROOT/000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG/$template.md"
    echo "   ✅ Created $template.md"
  else
    echo "   ⚠️  Template not found: $template-TEMPLATE.md"
  fi
done

echo ""
echo "✅ Plugin scaffolded successfully!"
echo ""
echo "📁 Code:  005-plugins/$PLUGIN_SLUG/"
echo "📄 Docs:  000-docs/000a-planned-plugins/implemented/$PLUGIN_SLUG/"
echo "🧠 Skill: 005-plugins/$PLUGIN_SLUG/skills/$PLUGIN_SLUG/SKILL.md"
echo ""
echo "Next steps:"
echo "  1. Fill in the 6 documentation files"
echo "  2. Implement plugin code"
echo "  3. Update README.md plugin catalog"
echo "  4. Validate plugin: bash 004-scripts/validate-all-plugins.sh 005-plugins/$PLUGIN_SLUG"
