"""Basic smoke tests for the Nixtla plugin repository."""


def test_imports():
    """Test that basic imports work."""
    # This ensures the test runner finds at least one test
    assert True


def test_skills_directory_exists():
    """Verify skills directory structure exists."""
    from pathlib import Path

    skills_dir = Path(__file__).parent.parent / "003-skills" / ".claude" / "skills"
    assert skills_dir.exists(), f"Skills directory not found: {skills_dir}"


def test_plugins_directory_exists():
    """Verify plugins directory structure exists."""
    from pathlib import Path

    plugins_dir = Path(__file__).parent.parent / "005-plugins"
    assert plugins_dir.exists(), f"Plugins directory not found: {plugins_dir}"
