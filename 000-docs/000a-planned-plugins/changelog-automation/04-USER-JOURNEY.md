# Changelog Automation - User Journey

**Plugin:** changelog-automation
**Last Updated:** 2025-12-28

---

## Persona

**Name:** Engineering Lead Emma
**Role:** Engineering Manager at a fast-moving SaaS startup
**Company Type:** Startup (30 developers, weekly releases)
**Technical Level:** Advanced (Python, Git, CI/CD expert)
**Goal:** Automate weekly changelog generation to save 2-3 hours/week and improve release note quality

---

## Prerequisites

Before using this plugin, ensure:

- [ ] Claude Code is installed
- [ ] Git repository with GitHub remote configured
- [ ] GitHub Personal Access Token with `repo:read` + `repo:write` scopes
- [ ] Environment variable `GITHUB_TOKEN` set
- [ ] (Optional) Slack Bot Token if using Slack integration
- [ ] Python 3.10+ installed

---

## Journey Overview

```
[Install Plugin] ──▶ [Configure] ──▶ [Validate Setup] ──▶ [Generate First Changelog] ──▶ [Review & Merge PR] ──▶ [Success!]
```

---

## Step-by-Step Journey

### Step 1: Install Plugin

**User wants to:** Install the changelog-automation plugin

**User does:**
```bash
cd /my-project
/plugin install changelog-automation
```

**System responds:**
```
✅ Installed changelog-automation v1.0.0
📁 Created .changelog-config.json (example config)
📄 Run /changelog-validate to test your setup
```

**User sees:**
- Plugin files copied to `.claude/plugins/changelog-automation/`
- Example config created at `.changelog-config.json`
- Slash commands available: `/changelog-weekly`, `/changelog-custom`, `/changelog-validate`

**Next:** Proceed to Step 2 (Configure)

---

### Step 2: Configure Data Sources

**User wants to:** Set up GitHub as data source

**User does:**
```bash
# Edit .changelog-config.json
cat > .changelog-config.json <<EOF
{
  "sources": [
    {
      "type": "github",
      "config": {
        "repo": "myorg/myrepo",
        "token_env": "GITHUB_TOKEN"
      }
    }
  ],
  "template": "changelogs/weekly-template.md",
  "output_path": "CHANGELOG.md",
  "quality_threshold": 80,
  "pr_config": {
    "base_branch": "main",
    "labels": ["documentation", "changelog"]
  }
}
EOF

# Set token
export GITHUB_TOKEN="ghp_..."
```

**System responds:**
```
(No output yet - file saved)
```

**User sees:**
- Config file created with GitHub source
- Token stored in environment variable (not committed to git)

**Next:** Proceed to Step 3 (Validate)

---

### Step 3: Validate Setup

**User wants to:** Verify configuration before running

**User does:**
```bash
/changelog-validate
```

**System responds:**
```
🔍 Validating changelog automation setup...

✅ Config file found: .changelog-config.json
✅ GitHub token: GITHUB_TOKEN (found, valid)
✅ Repository: myorg/myrepo (accessible)
✅ Template: changelogs/weekly-template.md (exists)
✅ Output path: CHANGELOG.md (writable)
✅ Quality threshold: 80 (valid range)

🎉 All checks passed! Ready to generate changelog.

Run: /changelog-weekly to generate changelog for last 7 days
```

**User sees:**
- All validation checks passed
- Confirmation that GitHub API is accessible
- Template exists and is valid
- Suggested next command

**Next:** Proceed to Step 4 (Generate First Changelog)

---

### Step 4: Generate First Changelog

**User wants to:** Create changelog for the last 7 days

**User does:**
```bash
/changelog-weekly
```

**System responds:**
```
📊 Changelog Automation - Weekly Run
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: Data Fetch ⏳
  ✓ Fetched 12 merged PRs from GitHub
  ✓ Fetched 8 closed issues
  ✓ Total items: 20 changes

Phase 2: AI Synthesis ⏳
  ✓ Grouped by type: 7 features, 10 fixes, 3 breaking
  ✓ Generated narrative summary
  ✓ Identified top 3 highlights

Phase 3: Template Formatting ⏳
  ✓ Loaded template: changelogs/weekly-template.md
  ✓ Generated frontmatter
  ✓ Applied variable substitution

Phase 4: Quality Review ⏳
  ✓ Deterministic checks: 95/100 (frontmatter valid, links work)
  ✓ Editorial review: 88/100 (tone good, completeness excellent)
  ✓ Combined score: 92/100 ✅ (threshold: 80)

Phase 5: PR Creation ⏳
  ✓ Wrote changelog: CHANGELOG.md (42 lines)
  ✓ Created branch: changelog-2025-12-28
  ✓ Committed changes (SHA: a1b2c3d)
  ✓ Opened PR: https://github.com/myorg/myrepo/pull/1234

Phase 6: User Handoff ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Changelog PR created successfully!

📋 Summary:
  - Date range: 2025-12-21 to 2025-12-28
  - Changes: 20 items (12 PRs, 8 issues)
  - Quality score: 92/100
  - PR: https://github.com/myorg/myrepo/pull/1234

Next steps:
  1. Review PR: Click link above
  2. Merge when ready: Changelog will be added to repo
  3. Iterate: Run /changelog-custom for different date ranges
```

**User sees:**
- Progress through all 6 phases
- Quality score exceeds threshold (92 > 80)
- PR created with changelog file
- Link to review PR

**Next:** Proceed to Step 5 (Review & Merge PR)

---

### Step 5: Review & Merge PR

**User wants to:** Review AI-generated changelog and merge

**User does:**
```bash
# Open PR in browser
open https://github.com/myorg/myrepo/pull/1234

# Or use GitHub CLI
gh pr view 1234

# Review changes
gh pr diff 1234

# Merge if satisfied
gh pr merge 1234 --squash
```

**System responds:**
```
✓ Pull request #1234 merged
✓ Branch changelog-2025-12-28 deleted
```

**User sees:**
- PR contains well-formatted changelog
- Frontmatter includes date, version, authors
- Content grouped by type (features, fixes, breaking)
- Links to PRs/issues work
- Tone is user-friendly and professional

**Success!** Changelog merged to main branch, available to users

---

## Complete Example

### Scenario
Emma ships a weekly release every Friday. She wants to automate changelog creation to save time and ensure consistency.

### Full Walkthrough

```bash
# Start here (Monday morning)
cd ~/projects/myapp

# Install plugin
/plugin install changelog-automation

# Output:
# ✅ Installed changelog-automation v1.0.0
# 📁 Created .changelog-config.json

# Configure GitHub source
export GITHUB_TOKEN="ghp_abc123..."
cat > .changelog-config.json <<EOF
{
  "sources": [{"type": "github", "config": {"repo": "myorg/myapp", "token_env": "GITHUB_TOKEN"}}],
  "template": "changelogs/weekly-template.md",
  "output_path": "CHANGELOG.md",
  "quality_threshold": 80
}
EOF

# Validate setup
/changelog-validate

# Output:
# ✅ All checks passed! Ready to generate changelog.

# Generate changelog (Friday afternoon)
/changelog-weekly

# Output:
# 🎉 Changelog PR created successfully!
# PR: https://github.com/myorg/myapp/pull/1234

# Review and merge
gh pr view 1234
gh pr merge 1234 --squash

# Final result:
# ✓ Changelog merged to main
# ✓ Time saved: 2.5 hours → 15 minutes (90% reduction)
```

---

## Error Scenarios

| Scenario | What User Sees | What Went Wrong | How to Fix |
|----------|---------------|-----------------|------------|
| Missing GitHub token | `❌ Error: GITHUB_TOKEN not found in environment` | Token not set or expired | Run `export GITHUB_TOKEN="ghp_..."` with valid token |
| Invalid repository | `❌ Error: Repository 'org/repo' not accessible (404)` | Typo in repo name or insufficient permissions | Check repo name in config, verify token has `repo:read` scope |
| Template not found | `❌ Error: Template 'changelogs/weekly-template.md' not found` | Template path incorrect | Create template file or update `template` field in config |
| Quality gate failure | `⚠️ Quality score: 68/100 (threshold: 80)` | Generated content doesn't meet quality standards | Lower threshold in config or review AI feedback for issues |
| PR creation conflict | `❌ Error: Branch 'changelog-2025-12-28' already exists` | Previous run wasn't cleaned up | Delete branch manually: `git push origin --delete changelog-2025-12-28` |
| No changes found | `⚠️ No changes found in date range` | No PRs/issues in selected timeframe | Adjust date range with `/changelog-custom start_date=... end_date=...` |

---

## Tips & Best Practices

1. **Run weekly on Fridays:** Automate with cron or CI/CD to generate changelog every Friday afternoon before release
2. **Customize templates:** Create templates for different changelog formats (weekly, monthly, release notes)
3. **Add multiple sources:** Combine GitHub PRs + Slack announcements + Git commits for comprehensive coverage
4. **Review before merging:** Always review AI-generated content for accuracy and completeness
5. **Adjust quality threshold:** Start at 80, increase to 85-90 as you refine templates and data sources
6. **Use conventional commits:** If using Git source, follow conventional commit format (feat:, fix:, etc.) for better categorization
7. **Archive old changelogs:** Store historical changelogs in `changelogs/archive/` to keep main file clean

---

## FAQ

**Q: Can I generate changelogs for custom date ranges?**
A: Yes! Use `/changelog-custom start_date=2025-12-01 end_date=2025-12-15` to specify a custom range.

**Q: What if I don't use GitHub?**
A: The plugin supports extensible data sources. You can add custom sources (GitLab, Jira, Linear) by subclassing `ChangelogDataSource` in the MCP server.

**Q: How do I customize the changelog format?**
A: Create a custom template in `changelogs/my-template.md` with your preferred structure and variables, then update the `template` field in `.changelog-config.json`.

**Q: Can I run this in CI/CD?**
A: Yes! Set `GITHUB_TOKEN` in CI environment variables and run `/changelog-weekly` in a scheduled job. The plugin will create PRs automatically for human review.

**Q: What if the quality score is too low?**
A: The Reviewer Agent provides feedback on what's missing (e.g., "Add more context for breaking changes"). You can iterate by adjusting templates or lowering the threshold temporarily.

**Q: How do I add Slack integration?**
A: Add a Slack source to your config:
```json
{
  "sources": [
    {"type": "github", "config": {...}},
    {"type": "slack", "config": {"channel": "changelog", "token_env": "SLACK_TOKEN"}}
  ]
}
```
