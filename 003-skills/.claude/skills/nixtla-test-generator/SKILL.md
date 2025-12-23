---
name: nixtla-test-generator
description: Generate comprehensive pytest test suites from PRD functional requirements with fixtures, parameterization, and coverage tracking. Use when creating tests for new plugins, validating PRD requirements, or scaffolding test infrastructure. Trigger with 'generate tests from PRD', 'create test suite', or 'scaffold pytest tests'.
allowed-tools: "Write,Read,Glob,Bash(python:*),Bash(pytest:*)"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Test Generator

## Purpose

Generate production-ready pytest test suites from PRD (Product Requirements Document) functional requirements, ensuring comprehensive test coverage for Nixtla plugins.

## Overview

This skill automates the tedious process of creating test infrastructure for new plugins. It:
- Parses PRD documents to extract functional requirements (FR-X items)
- Generates pytest test files with proper structure (test_unit.py, test_integration.py)
- Creates pytest fixtures for common test scenarios
- Includes parameterized tests for multiple input scenarios
- Generates conftest.py with shared fixtures
- Creates test documentation with coverage matrix

**Key Benefits**:
- Reduces test scaffolding time from 2-3 hours to 2 minutes
- Ensures consistent test structure across all plugins
- Auto-generates test stubs for every functional requirement
- Includes best practices (fixtures, markers, parameterization)

## Prerequisites

- PRD document with structured functional requirements (FR-X format)
- Python 3.8+ with pytest installed
- Target plugin directory structure exists

## Instructions

### Step 1: Parse PRD for Requirements

The script automatically:
1. Reads PRD markdown file
2. Extracts all functional requirements (FR-1, FR-2, etc.)
3. Identifies MCP tools from FR-X sections
4. Captures acceptance criteria from user stories

**PRD Structure Expected**:
```markdown
## Functional Requirements

### FR-1: Feature Name
- Requirement detail 1
- Requirement detail 2

### FR-2: Another Feature
- More requirements
```

### Step 2: Generate Test Structure

Creates the following test files:

**test_unit.py** - Unit tests for individual functions
```python
import pytest
from plugin_name.core import function_name

class TestFR1FeatureName:
    """Test FR-1: Feature Name"""

    def test_basic_functionality(self):
        """Test basic happy path for FR-1"""
        result = function_name(input_data)
        assert result.success

    def test_error_handling(self):
        """Test error handling for FR-1"""
        with pytest.raises(ValueError):
            function_name(invalid_input)
```

**test_integration.py** - Integration tests for MCP tools
```python
import pytest
from mcp_server import ToolName

class TestMCPToolName:
    """Test MCP tool: tool_name"""

    @pytest.mark.integration
    def test_tool_execution(self, mock_api_client):
        """Test tool_name MCP tool end-to-end"""
        result = ToolName.execute(params)
        assert result["status"] == "success"
```

**conftest.py** - Shared fixtures
```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample test data"""
    return {"series": [...], "horizon": 14}

@pytest.fixture
def mock_api_client(monkeypatch):
    """Mock external API calls"""
    class MockClient:
        def forecast(self, **kwargs):
            return {"predictions": [...]}
    return MockClient()
```

### Step 3: Add Pytest Markers

Generated tests include appropriate markers:
- `@pytest.mark.unit` - Fast, isolated tests
- `@pytest.mark.integration` - Tests with external dependencies
- `@pytest.mark.slow` - Long-running tests (>1 second)
- `@pytest.mark.parametrize` - Multiple input scenarios

### Step 4: Create Coverage Matrix

Generates `tests/COVERAGE_MATRIX.md`:
```markdown
# Test Coverage Matrix

| Requirement | Test File | Test Function | Status |
|-------------|-----------|---------------|--------|
| FR-1: Feature Name | test_unit.py | test_basic_functionality | ✅ |
| FR-2: Another Feature | test_unit.py | test_feature_2 | ✅ |
| MCP: tool_name | test_integration.py | test_tool_execution | ✅ |
```

### Step 5: Run Generated Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=plugin_name --cov-report=html

# Run only unit tests
pytest tests/ -m unit
```

## Output

The script generates:
1. **tests/test_unit.py** - Unit tests for all FR-X requirements
2. **tests/test_integration.py** - Integration tests for MCP tools
3. **tests/conftest.py** - Shared pytest fixtures
4. **tests/COVERAGE_MATRIX.md** - Test-to-requirement mapping
5. **tests/README.md** - Test suite documentation

## Error Handling

**Missing PRD File**:
```
Error: PRD not found at /path/to/PRD.md
Solution: Verify PRD path and ensure file exists
```

**No Functional Requirements Found**:
```
Warning: No FR-X sections found in PRD
Solution: Ensure PRD has "### FR-X: Title" format sections
```

**Invalid Python Syntax in Generated Tests**:
```
Error: Generated test file has syntax errors
Solution: Run black formatter on generated files
```

**Import Errors in Generated Tests**:
```
Error: Cannot import plugin_name module
Solution: Update import paths in generated tests to match actual module structure
```

## Examples

### Example 1: Generate Full Test Suite

```bash
python {baseDir}/scripts/generate_test_suite.py \
    --prd 000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md \
    --output 005-plugins/nixtla-roi-calculator/tests \
    --plugin-name nixtla-roi-calculator
```

**Output**:
```
✓ Parsed PRD: Found 5 functional requirements, 4 MCP tools
✓ Generated tests/test_unit.py (15 test functions)
✓ Generated tests/test_integration.py (4 MCP tool tests)
✓ Generated tests/conftest.py (6 fixtures)
✓ Generated tests/COVERAGE_MATRIX.md
✓ Generated tests/README.md

Test Coverage: 19/19 requirements (100%)
```

### Example 2: Generate Unit Tests Only

```bash
python {baseDir}/scripts/generate_test_suite.py \
    --prd /path/to/PRD.md \
    --output /path/to/tests \
    --unit-only
```

### Example 3: Dry Run (Preview Without Writing)

```bash
python {baseDir}/scripts/generate_test_suite.py \
    --prd /path/to/PRD.md \
    --output /path/to/tests \
    --dry-run
```

## Best Practices

1. **Review Generated Tests**: Always review and customize generated test stubs
2. **Add Real Assertions**: Replace placeholder assertions with actual validation logic
3. **Mock External APIs**: Use fixtures to mock TimeGPT API, BigQuery, etc.
4. **Parameterize Edge Cases**: Add @pytest.mark.parametrize for boundary conditions
5. **Document Test Intent**: Keep docstrings explaining what each test validates
6. **Run Tests Locally**: Verify tests pass before committing
7. **Track Coverage**: Aim for 80%+ code coverage on core logic

## Resources

- **Script**: `{baseDir}/scripts/generate_test_suite.py`
- **Template**: `{baseDir}/assets/templates/pytest_template.py`
- **Example PRD**: `000-docs/000a-planned-plugins/implemented/nixtla-roi-calculator/02-PRD.md`
- **Pytest Docs**: https://docs.pytest.org/
- **Coverage Guide**: https://coverage.readthedocs.io/
