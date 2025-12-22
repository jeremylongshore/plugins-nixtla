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
