# Repository Guidelines

## Project Structure & Module Organization

- `005-plugins/`: primary plugin implementations (each plugin typically has `.claude-plugin/`, `commands/`, `scripts/`, and sometimes `src/`, `tests/`, `templates/`).
- `003-skills/.claude/skills/`: reusable Claude skills shipped with this repo.
- `006-packages/`: installable Python tooling (notably `nixtla-claude-skills-installer/`).
- `000-docs/`: canonical documentation (symlinked from `CONTRIBUTING.md`, `SECURITY.md`, etc.).
- `tests/`: repo-level pytest suite (default `pytest` target); `007-tests/` contains extra/e2e tests run explicitly.

## Build, Test, and Development Commands

- Create a venv + install dev deps: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt`
- Optional bootstrap script: `./004-scripts/setup-dev-environment.sh` (creates `venv/`, installs deps, writes a starter `.env`).
- Run tests (repo-level): `pytest -v`
- Run plugin tests: `pytest 005-plugins/<plugin>/tests -v`
- Validate skills (strict): `python 004-scripts/validate_skills_v2.py --fail-on-warn`
- Validate plugins (canonical): `bash 004-scripts/validate-all-plugins.sh .`
- Generate a deterministic evidence bundle: `python 003-skills/.claude/skills/nixtla-universal-validator/scripts/run_validator_suite.py --target . --project pr-1234 --out reports/pr-1234 --profile default`
- Coverage artifacts: `.coverage` plus HTML output in `001-htmlcov/` (see `pytest.ini`).

## Coding Style & Naming Conventions

- Indentation: 4 spaces for Python (see `.editorconfig`); keep lines ≤ 100 chars (Black/Flake8).
- Format/imports: `black .` and `isort .`
- Lint/type checks (when applicable): `flake8 .`, `mypy <path>` (start with the package or plugin you changed).
- Naming: plugin folders use kebab-case like `nixtla-forecast-explainer`; Python modules/functions use `snake_case`.

## Testing Guidelines

- Framework: `pytest` with markers like `unit`, `integration`, `slow`, `cloud`, `api` (see `pytest.ini`).
- Prefer small unit tests near the code you change; add integration tests only when behavior depends on external services.
- Useful filters: `pytest -m "not integration"` or `pytest -m "unit"`.

## Security & Configuration Tips

- Use `.env` for local secrets (created by `./004-scripts/setup-dev-environment.sh`) and keep it uncommitted.
- Common vars: `NIXTLA_TIMEGPT_API_KEY` (TimeGPT features) plus standard cloud credentials for any plugin that integrates with AWS/GCP/Azure.

## Commit & Pull Request Guidelines

- Commit messages follow Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `style:` (optional scope: `feat(skills): ...`).
- PRs should include: what/why, how to test, linked issue(s), and any required env vars (never include secrets).
- Update `000-docs/` when behavior or usage changes; keep directory naming with numeric prefixes (don’t reshuffle for aesthetics).

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
