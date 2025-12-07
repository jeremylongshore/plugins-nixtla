# Claude Skills Technical Reference

Source: https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/

## Complete Frontmatter Schema

```yaml
---
# REQUIRED
name: skill-name                    # 64 chars max, lowercase + hyphens
description: >                      # 1024 chars max
  Action-oriented description.

# OPTIONAL
allowed-tools: "Read,Write,Glob"    # CSV of tools
model: inherit                      # or specific model ID
version: "1.0.0"                   # semver
license: "MIT"                     # license ref
mode: false                        # true = mode skill
disable-model-invocation: false    # true = manual only

# UNDOCUMENTED (functional)
when_to_use: >                     # appends to description
  Additional context.
---
```

## Skill Tool Architecture

The Skill tool is a meta-tool with dynamic prompt generation:

```javascript
{
  name: "Skill",
  inputSchema: {
    command: string  // skill name
  },
  outputSchema: {
    success: boolean,
    commandName: string
  },
  prompt: dynamic   // aggregates all skill descriptions
}
```

## Message Injection Pattern

Skills inject two messages:

### Message 1 - Visible Metadata
```xml
<command-message>The "pdf" skill is loading</command-message>
<command-name>pdf</command-name>
<command-args>report.pdf</command-args>
```
- `isMeta: false`
- Shown to user

### Message 2 - Hidden Prompt
- Full SKILL.md content
- `isMeta: true`
- Hidden from UI, sent to API

## Execution Context Modification

Skills yield a `contextModifier` function that:
1. Pre-approves tools in `allowed-tools`
2. Optionally overrides model
3. Scoped to skill execution only

## Validation Error Codes

1. Empty command input
2. Unknown skill
3. File loading failure
4. Model invocation disabled
5. Non-prompt-based skill

## Tool Permission Syntax

```yaml
# All tools of type
allowed-tools: "Read,Write,Bash"

# Scoped commands
allowed-tools: "Bash(git:*),Read"
allowed-tools: "Bash(npm:*),Bash(npx:*),Read"

# Read-only
allowed-tools: "Read,Glob,Grep"
```

## Discovery Sources (Priority)

1. User: `~/.config/claude/skills/`
2. Project: `.claude/skills/`
3. Plugin-provided
4. Built-in

Later sources override earlier.

## Filtering Rules

Skill is filtered out if:
- Missing both `description` AND `when_to_use`
- `disable-model-invocation: true` (excluded from Skill tool list)

## Token Constraints

- Skill description budget: 15,000 chars
- Typical skill size: 500-5,000 words
