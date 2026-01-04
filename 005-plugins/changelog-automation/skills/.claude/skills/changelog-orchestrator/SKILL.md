---
name: changelog-orchestrator
description: Orchestrate 6-phase changelog generation workflow with AI synthesis, multi-source data fetching (GitHub/Slack/Git), quality validation, and automated PR creation. Use when automating release notes, weekly changelogs, or documentation updates. Trigger with "generate changelog", "weekly changelog", or "automate release notes".
allowed-tools: Read,Write,Bash(python:*)
version: 0.1.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
---

# Changelog Orchestrator

## Purpose

Orchestrate a 6-phase workflow to automate changelog generation: fetch data from multiple sources, synthesize narrative with AI, validate quality, and create pull requests.

## Overview

This skill coordinates changelog automation through progressive disclosure:
- **Phase 1**: Initialize & fetch data from GitHub/Slack/Git
- **Phase 2**: AI synthesis (Writer Agent groups changes, generates narrative)
- **Phase 3**: Template formatting with frontmatter validation
- **Phase 4**: Quality review with two-layer gate (deterministic + editorial)
- **Phase 5**: PR creation with changelog file
- **Phase 6**: User handoff with summary and next steps

Integrates with MCP server (`changelog_mcp.py`) for deterministic operations while handling editorial work (synthesis, tone, quality judgment) directly.

## Prerequisites

**Environment:**
- Python 3.10+ installed
- MCP server dependencies installed: `pip install -r scripts/requirements.txt`
- `.changelog-config.json` configured in project root

**Required Tokens:**
- GitHub: `GITHUB_TOKEN` environment variable with `repo:read` + `repo:write` scopes
- Slack (optional): `SLACK_TOKEN` environment variable with `channels:history` scope

**Files:**
- Config file: `.changelog-config.json` (see `config/.changelog-config.example.json`)
- Template: Markdown file with frontmatter (see `assets/templates/default-changelog.md`)

## Instructions

### Phase 1: Initialize & Fetch Data

1. **Load Configuration**
   - Call MCP tool `get_changelog_config` (no arguments for default `.changelog-config.json`)
   - If error: Display error message with suggestion (e.g., "Run /changelog-validate")
   - If success: Store config for later phases

2. **Determine Date Range**
   - For `/changelog-weekly`: Calculate start_date = today - 7 days, end_date = today
   - For `/changelog-custom`: Use provided `start_date` and `end_date` parameters
   - Validate dates are in ISO 8601 format (YYYY-MM-DD)
   - Ensure start_date < end_date

3. **Fetch Data from All Sources**
   - For each source in `config["sources"]`:
     - Call MCP tool `fetch_changelog_data` with:
       - `source_type`: From config (github/slack/git)
       - `start_date`: Calculated or provided date
       - `end_date`: Calculated or provided date
       - `config`: Source-specific config from file
     - Collect items from response `data["items"]`
   - Aggregate all items into unified dataset
   - Sort by timestamp (oldest to newest)

4. **Display Fetch Summary**
   - Total items fetched
   - Breakdown by source (e.g., "GitHub: 12 PRs, Slack: 5 messages")
   - Date range covered

### Phase 2: Writer Agent - AI Synthesis

**Role**: You are now the Writer Agent. Your job is to transform raw data into user-friendly changelog content.

1. **Group Items by Type**
   - **Features**: Items with labels/types: enhancement, feature, new
   - **Fixes**: Items with labels/types: bug, fix, bugfix
   - **Breaking Changes**: Items with labels: breaking, breaking-change
   - **Other**: Everything else

2. **Generate Narrative Summary**
   - Write 2-3 sentences summarizing the overall theme of changes
   - Focus on what matters to users (not internal details)
   - Example: "This week focused on improving performance and user experience. Key highlights include a new dark mode toggle and faster page load times. Several critical bugs were fixed in the checkout flow."

3. **Identify Top Highlights**
   - Select 3-5 most impactful changes
   - Criteria: User-facing, significant value, breaking changes
   - Write 1-sentence description for each

4. **Write Detailed Sections**
   - For each type (features/fixes/breaking/other):
     - List items with title + link
     - Add brief context if needed
     - Use bullet points
   - Example:
     ```
     - Add dark mode toggle (#123) - Users can now switch between light and dark themes
     - Improve page load speed (#124) - 40% faster initial render
     ```

5. **Apply Tone Guidelines**
   - User-focused (not developer jargon)
   - Concise (no unnecessary details)
   - Professional (no slang or humor)
   - Active voice ("Added X" not "X was added")

6. **Output**: Draft markdown content (no frontmatter yet)

### Phase 3: Formatter Agent - Template Compliance

**Role**: You are now the Formatter Agent. Your job is to apply the template structure and validate formatting.

1. **Load Template**
   - Read template file from `config["template"]`
   - Parse frontmatter placeholders (variables in `{{...}}`)
   - Parse body structure (required sections)

2. **Generate Frontmatter**
   - Extract required fields:
     - `date`: End date from Phase 1 (YYYY-MM-DD)
     - `version`: Extract from latest git tag or increment (e.g., "1.2.0")
     - `authors`: Unique authors from all items (deduplicate)
     - `categories`: Derive from types (e.g., ["features", "fixes"])
   - Create frontmatter dictionary

3. **Validate Frontmatter**
   - Call MCP tool `validate_frontmatter` with:
     - `frontmatter`: Generated dictionary
     - `schema_path`: Optional (uses default schema)
   - If errors: Display and fix
   - If warnings: Note but continue

4. **Apply Template Substitution**
   - Replace all `{{variable}}` placeholders:
     - `{{date}}` → frontmatter.date
     - `{{version}}` → frontmatter.version
     - `{{summary}}` → From Phase 2
     - `{{highlights}}` → From Phase 2 (bullet list)
     - `{{features}}` → From Phase 2 (bullet list)
     - `{{fixes}}` → From Phase 2 (bullet list)
     - `{{breaking_changes}}` → From Phase 2 or "None" if empty
     - `{{other_changes}}` → From Phase 2 or "None" if empty
   - Combine frontmatter (YAML) + body (markdown)

5. **Run Deterministic Quality Check**
   - Call MCP tool `validate_changelog_quality` with:
     - `content`: Full markdown with frontmatter
   - Store quality score for Phase 4

6. **Output**: Complete formatted changelog markdown

### Phase 4: Reviewer Agent - Quality Gate

**Role**: You are now the Reviewer Agent. Your job is to ensure the changelog meets quality standards before publishing.

1. **Review Deterministic Score**
   - Check MCP quality score from Phase 3
   - Required checks:
     - Frontmatter valid (YAML syntax)
     - All links accessible (no 404s)
     - Required sections present
     - Markdown syntax valid
   - Minimum score: 70/100 (deterministic only)

2. **Editorial Review**
   - **Completeness**: All fetched items represented (no missing changes)
   - **Accuracy**: No hallucinations (facts match source data)
   - **Tone**: User-friendly (no jargon, clear language)
   - **Clarity**: Easy to understand (no ambiguity)
   - Assign editorial score: 0-100

3. **Calculate Combined Score**
   - Combined = (Deterministic × 0.4) + (Editorial × 0.6)
   - Threshold: `config["quality_threshold"]` (default 80)

4. **Decision**
   - If combined score ≥ threshold: **APPROVE** → Proceed to Phase 5
   - If combined score < threshold: **REJECT** → Provide feedback

5. **Feedback Loop (If Rejected)**
   - Identify specific issues:
     - Missing changes: "Items X, Y not mentioned"
     - Tone issues: "Too technical in Features section"
     - Clarity issues: "Breaking changes unclear"
   - Return to Phase 2 with feedback
   - **Maximum 2 iterations** (if still fails after 2, warn user and allow override)

6. **Output**: Approval status + quality score + feedback (if any)

### Phase 5: PR Writer Agent - Repository Operations

**Role**: You are now the PR Writer Agent. Your job is to commit the changelog and create a pull request.

1. **Write Changelog File**
   - Call MCP tool `write_changelog` with:
     - `content`: Approved markdown from Phase 4
     - `output_path`: From `config["output_path"]`
     - `overwrite`: true
   - Store file metadata (path, SHA256, line count)

2. **Generate PR Description**
   - Create markdown body:
     ```markdown
     ## Summary
     Changelog for {start_date} to {end_date}

     ## Changes
     - Total: {count} items
     - Features: {feature_count}
     - Fixes: {fix_count}
     - Breaking: {breaking_count}

     ## Quality Score
     {combined_score}/100 (Deterministic: {det_score}, Editorial: {ed_score})

     ## Reviewer Checklist
     - [ ] All changes accurately represented
     - [ ] Tone is user-friendly
     - [ ] No sensitive information leaked
     - [ ] Links work correctly
     ```

3. **Create Pull Request**
   - Call MCP tool `create_changelog_pr` with:
     - `branch_name`: `changelog-{end_date}` (e.g., "changelog-2025-12-28")
     - `commit_message`: `docs: add changelog for {end_date}`
     - `pr_title`: `Changelog for Week of {start_date} to {end_date}`
     - `pr_body`: Generated description from step 2
     - `base_branch`: From `config["pr_config"]["base_branch"]` (default "main")
   - Store PR URL and number

4. **Handle Errors**
   - Branch exists: Suggest unique name or force delete
   - Permission denied: Check GitHub token has `repo:write`
   - Merge conflict: Suggest manual resolution

5. **Output**: PR metadata (URL, number, branch, diff summary)

### Phase 6: User Handoff

**Role**: You are the Orchestrator Agent again. Present results to the user.

1. **Display Success Summary**
   ```
   🎉 Changelog PR created successfully!

   📋 Summary:
     - Date range: {start_date} to {end_date}
     - Changes: {count} items ({source breakdown})
     - Quality score: {score}/100
     - PR: {pr_url}

   Next steps:
     1. Review PR: Click link above
     2. Merge when ready: Changelog will be added to repo
     3. Iterate: Run /changelog-custom for different date ranges
   ```

2. **Provide Next Actions**
   - Review PR (link)
   - Merge when satisfied
   - Run `/changelog-custom` for different date range
   - Adjust quality threshold in config if needed

3. **Save Reproducibility Bundle** (Optional)
   - Create `run_manifest.json` with:
     - Execution timestamp
     - MCP server version
     - Data source versions
     - Item count per source
     - Quality scores
     - PR metadata
   - Store in project root or `.claude/` directory

4. **End Session**
   - Thank user
   - Remind them of validation command: `/changelog-validate`

## Output

**Primary Artifact**: GitHub Pull Request with changelog file

**Secondary Artifacts**:
- Changelog markdown file (e.g., `CHANGELOG.md`)
- Run manifest JSON (optional, for reproducibility)

**Console Output**: Phase-by-phase progress with status emojis

## Error Handling

| Error Type | Phase | Response | Recovery |
|------------|-------|----------|----------|
| Config file missing | Phase 1 | Display error + suggest `/changelog-validate` | User creates config |
| GitHub token invalid | Phase 1 | Display error + token setup instructions | User sets `GITHUB_TOKEN` |
| Template not found | Phase 3 | Display error + template path | User fixes path in config |
| Quality gate fails | Phase 4 | Provide feedback, iterate (max 2 rounds) | Lower threshold or fix content |
| PR creation fails (branch exists) | Phase 5 | Suggest unique branch or delete existing | User resolves conflict |

**General Error Pattern**:
1. Catch exception
2. Identify root cause
3. Display clear error message
4. Suggest specific fix
5. Provide fallback or recovery path

## Examples

### Example 1: Weekly Changelog (Happy Path)

**User**: `/changelog-weekly`

**Phase 1**: Fetched 20 items (GitHub: 12 PRs, Slack: 8 messages)

**Phase 2**: Generated summary + highlights + 4 sections

**Phase 3**: Applied template, validated frontmatter (✓)

**Phase 4**: Quality score: 92/100 (approved)

**Phase 5**: Created PR #1234

**Phase 6**: Displayed summary with PR link

### Example 2: Custom Date Range

**User**: `/changelog-custom start_date=2025-12-01 end_date=2025-12-15`

**Workflow**: Same as Example 1, but uses provided date range

### Example 3: Quality Gate Failure

**Phase 4**: Quality score: 68/100 (rejected, threshold 80)

**Feedback**: "Missing 3 PRs in Features section, tone too technical in Breaking Changes"

**Phase 2 (iteration 2)**: Fixed issues

**Phase 4 (retry)**: Quality score: 85/100 (approved)

**Continue**: Proceeds to Phase 5

## Resources

**Documentation**:
- Architecture: `000-docs/000a-planned-plugins/changelog-automation/03-ARCHITECTURE.md`
- User Journey: `000-docs/000a-planned-plugins/changelog-automation/04-USER-JOURNEY.md`
- Technical Spec: `000-docs/000a-planned-plugins/changelog-automation/05-TECHNICAL-SPEC.md`

**MCP Server**: Plugin-level script at `scripts/changelog_mcp.py`

**Templates**: Available in `assets/templates/` directory
- `default-changelog.md` - Default format
- `weekly-template.md` - Weekly format (future)
- `release-template.md` - Release notes format (future)

**Config Schema**: `config/.changelog-config.schema.json`
