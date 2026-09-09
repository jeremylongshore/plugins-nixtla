"""Regression tests for skills published from the repository root."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_SKILLS = ROOT / ".claude" / "skills"
BASELINE_ROOT = PUBLIC_SKILLS / "nixtla-baseline-review"
BASELINE_PLUGIN = ROOT / "005-plugins" / "nixtla-baseline-lab" / "skills" / "nixtla-baseline-review"


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", 2)
    return yaml.safe_load(frontmatter)


def package_files(path: Path) -> dict[Path, bytes]:
    return {
        candidate.relative_to(path): candidate.read_bytes()
        for candidate in path.rglob("*")
        if candidate.is_file() and "__pycache__" not in candidate.parts
    }


def load_analyzer():
    path = BASELINE_ROOT / "scripts" / "analyze_results.py"
    spec = importlib.util.spec_from_file_location("baseline_results_analyzer", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_agent_validator():
    path = ROOT / "004-scripts" / "validate_command_agent_frontmatter.py"
    spec = importlib.util.spec_from_file_location("command_agent_validator", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_root_exposes_only_intended_skills():
    names = sorted(path.parent.name for path in PUBLIC_SKILLS.glob("*/SKILL.md"))
    assert names == ["nixtla-baseline-review", "skills-expert"]


@pytest.mark.parametrize("skill_name", ["nixtla-baseline-review", "skills-expert"])
def test_public_skills_have_marketplace_metadata_and_support(skill_name: str):
    skill_dir = PUBLIC_SKILLS / skill_name
    metadata = parse_frontmatter(skill_dir / "SKILL.md")
    required = {
        "name",
        "description",
        "allowed-tools",
        "version",
        "author",
        "license",
        "compatibility",
        "tags",
    }
    assert required <= metadata.keys()
    assert metadata["name"] == skill_name
    assert list((skill_dir / "references").glob("*.md"))


def test_baseline_plugin_mirror_is_byte_identical():
    assert package_files(BASELINE_ROOT) == package_files(BASELINE_PLUGIN)


def test_analyzer_summarizes_repository_fixture():
    analyzer = load_analyzer()
    fixture = (
        ROOT
        / "005-plugins"
        / "nixtla-baseline-lab"
        / "tests"
        / "m4_test"
        / "results_M4_Daily_h7.csv"
    )
    receipt = analyzer.summarize(fixture)
    assert receipt["status"] == "valid"
    assert receipt["row_count"] == 15
    assert receipt["series_count"] == 5
    assert receipt["coverage_gaps"] == {}
    assert receipt["models"]["AutoETS"]["mean_sMAPE"] == pytest.approx(0.768)


def test_analyzer_rejects_duplicate_pairs(tmp_path: Path):
    analyzer = load_analyzer()
    bad_csv = tmp_path / "results_duplicate.csv"
    bad_csv.write_text(
        "series_id,model,sMAPE,MASE\n" "D1,AutoETS,1.0,0.9\n" "D1,AutoETS,1.1,1.0\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate series/model pair"):
        analyzer.summarize(bad_csv)


def test_skills_expert_omits_retired_guidance():
    skill_text = (PUBLIC_SKILLS / "skills-expert" / "SKILL.md").read_text(encoding="utf-8")
    contract_text = (
        PUBLIC_SKILLS / "skills-expert" / "references" / "skill-contract.md"
    ).read_text(encoding="utf-8")
    assert "{baseDir}" not in skill_text
    assert "Skills are NOT concurrency-safe" not in skill_text
    assert "Include all four directories" not in skill_text
    assert "`allowed-tools` pre-approves matching tools" in skill_text
    assert "https://code.claude.com/docs/en/skills" in contract_text


def test_current_agent_contract_passes_repository_validator():
    validator = load_agent_validator()
    agent_path = (
        ROOT / "005-plugins" / "nixtla-baseline-lab" / "agents" / "nixtla-baseline-analyst.md"
    )
    frontmatter = parse_frontmatter(agent_path)
    assert validator.validate_agent_frontmatter(frontmatter, agent_path) == []


def test_retired_capabilities_field_is_rejected():
    validator = load_agent_validator()
    agent_path = Path("agents/example.md")
    frontmatter = {
        "name": "example",
        "description": "Analyze a selected result set with explicit evidence boundaries.",
        "tools": ["Read"],
        "disallowedTools": ["Write"],
        "model": "inherit",
        "color": "blue",
        "version": "1.0.0",
        "author": "Example Author",
        "tags": ["example"],
        "capabilities": ["legacy field"],
    }
    assert validator.validate_agent_frontmatter(frontmatter, agent_path) == [
        "Unsupported agent field: capabilities"
    ]
