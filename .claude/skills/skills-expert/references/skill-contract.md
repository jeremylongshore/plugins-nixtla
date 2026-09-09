# Skill Contract and Authority Map

Use this reference to choose the right validation layer before making claims.

## Portable package

An Agent Skill is a directory whose entry point is `SKILL.md`. Keep support
files inside that directory and link them with relative paths so the package
survives installation in a different location.

## Claude Code behavior

The current official reference is:

- <https://code.claude.com/docs/en/skills>

The page is titled "Extend Claude with skills" and documents discovery,
frontmatter, invocation control, tool pre-approval, arguments, dynamic context,
subagent execution, and support files. Recheck it before asserting a current
field list or exact character limit.

Important distinctions:

- `description` is recommended for reliable discovery, while the portable or
  Claude Code base does not make every marketplace metadata field mandatory.
- `disable-model-invocation: true` prevents automatic model invocation.
- `user-invocable: false` hides the skill from the slash-command menu; it does
  not by itself block programmatic invocation.
- `allowed-tools` is a pre-approval list, not a complete tool-availability
  sandbox. Deny rules belong in permission settings.
- Use `${CLAUDE_SKILL_DIR}` in shell examples that must locate a bundled script
  at runtime. Do not rely on the obsolete `{baseDir}` placeholder.
- Empty `scripts/`, `references/`, or `assets/` directories are unnecessary.
  Add support directories only when the package uses them.

For SDK-hosted skills, verify the separate official SDK documentation because
CLI-specific `allowed-tools` behavior does not automatically carry over:

- <https://code.claude.com/docs/en/agent-sdk/skills>

## Intent Solutions marketplace overlay

The marketplace validator intentionally imposes a stricter publication
contract. At schema 4.1.0, the required metadata is `name`, `description`,
`allowed-tools`, `version`, `author`, `license`, `compatibility`, and `tags`.
Conditional fields and quality scoring may add warnings or affect the grade.

Use the validator from the current marketplace checkout rather than copying its
rubric into a skill permanently:

```bash
python3 scripts/validate-skills-schema.py --marketplace path/to/SKILL.md
```

Publication quality also requires semantic verification. A high structural
score does not prove that tools exist, commands work, permissions are safe, or
examples describe real output.

## Review checklist

1. Establish which layer owns each rule.
2. Verify paths, commands, and tool names against the target repository.
3. Treat permission expansion and external side effects as security decisions.
4. Run the canonical validator and focused behavior tests.
5. Record the validator version, grade/tier, warnings, and unresolved risks.
