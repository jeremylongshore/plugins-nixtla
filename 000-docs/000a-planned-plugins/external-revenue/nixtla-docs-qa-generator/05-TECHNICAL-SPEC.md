# Docs QA Generator - Technical Specification

**Plugin:** nixtla-docs-qa-generator
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Runtime | Python 3.10+ | AST parsing, SDK compatibility |
| MCP Server | FastAPI + MCP SDK | Standard plugin architecture |
| AST Parsing | ast, inspect | Native Python introspection |
| Git | GitPython | Repository operations |
| Testing | pytest | Example execution |
| Diff | difflib | Patch generation |

---

## API Specification

### MCP Tools

#### 1. `detect_changes`
```json
{
  "name": "detect_changes",
  "description": "Scan repos for API changes",
  "inputSchema": {
    "type": "object",
    "properties": {
      "repo": {
        "type": "string",
        "enum": ["statsforecast", "nixtla", "mlforecast", "all"]
      },
      "since": {
        "type": "string",
        "description": "Git ref (tag, commit, branch) to compare from"
      },
      "to": {
        "type": "string",
        "default": "HEAD"
      }
    }
  }
}
```

#### 2. `generate_doc_diff`
```json
{
  "name": "generate_doc_diff",
  "description": "Create documentation patches",
  "inputSchema": {
    "type": "object",
    "properties": {
      "changes": {
        "type": "array",
        "description": "API changes to generate docs for"
      },
      "output_format": {
        "type": "string",
        "enum": ["unified", "markdown", "json"],
        "default": "unified"
      }
    }
  }
}
```

#### 3. `extract_examples`
```json
{
  "name": "extract_examples",
  "description": "Parse docs for code blocks",
  "inputSchema": {
    "type": "object",
    "properties": {
      "doc_path": {
        "type": "string",
        "description": "Path to documentation file or directory"
      },
      "language": {
        "type": "string",
        "default": "python"
      }
    }
  }
}
```

#### 4. `run_doc_tests`
```json
{
  "name": "run_doc_tests",
  "description": "Execute examples and report results",
  "inputSchema": {
    "type": "object",
    "properties": {
      "doc_path": {
        "type": "string"
      },
      "fail_fast": {
        "type": "boolean",
        "default": false
      },
      "timeout": {
        "type": "integer",
        "default": 60
      }
    }
  }
}
```

#### 5. `create_update_pr`
```json
{
  "name": "create_update_pr",
  "description": "Generate PR for doc updates",
  "inputSchema": {
    "type": "object",
    "properties": {
      "patches": {
        "type": "array",
        "description": "Patches to apply"
      },
      "title": {
        "type": "string"
      },
      "reviewers": {
        "type": "array",
        "items": {"type": "string"}
      }
    }
  }
}
```

---

## Data Models

### API Change Schema
```python
@dataclass
class APIChange:
    type: str                  # new, changed, deprecated, removed
    module: str                # e.g., statsforecast.core
    name: str                  # e.g., StatsForecast.forecast
    old_signature: Optional[str]
    new_signature: Optional[str]
    breaking: bool
    affected_docs: List[str]
```

### Example Schema
```python
@dataclass
class DocExample:
    file_path: str
    line_number: int
    language: str
    code: str
    context: str              # Surrounding text
    imports: List[str]        # Required imports
    fixtures: List[str]       # Required test fixtures
```

### Test Result Schema
```python
@dataclass
class TestResult:
    example: DocExample
    passed: bool
    error: Optional[str]
    stdout: Optional[str]
    execution_time: float
```

---

## Configuration

```yaml
# config.yaml
repositories:
  statsforecast:
    url: "https://github.com/Nixtla/statsforecast"
    paths: ["src/statsforecast/"]
  nixtla:
    url: "https://github.com/Nixtla/nixtla"
    paths: ["nixtla/"]
  mlforecast:
    url: "https://github.com/Nixtla/mlforecast"
    paths: ["mlforecast/"]

documentation:
  repo: "https://github.com/Nixtla/docs"
  paths: ["docs/"]
  exclude: ["docs/blog/", "docs/community/"]

testing:
  timeout_per_example: 60
  parallel_workers: 4
  install_deps: true

pr_creation:
  auto_create: false
  default_reviewers: ["@devrel"]
  labels: ["documentation", "automated"]
```

---

## AST Analysis

```python
def extract_public_api(module_path: str) -> List[APIItem]:
    """Extract public API from Python module."""
    with open(module_path) as f:
        tree = ast.parse(f.read())

    items = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):
                items.append(APIItem(
                    type='function',
                    name=node.name,
                    signature=get_signature(node),
                    docstring=ast.get_docstring(node),
                    lineno=node.lineno
                ))
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith('_'):
                items.append(APIItem(
                    type='class',
                    name=node.name,
                    methods=extract_methods(node),
                    docstring=ast.get_docstring(node),
                    lineno=node.lineno
                ))
    return items
```

---

## Performance Requirements

| Metric | Target |
|--------|--------|
| Change detection | <30 seconds per repo |
| Example extraction | <5 seconds per file |
| Test execution | 10 examples/minute (parallel) |
| PR creation | <10 seconds |

---

## Dependencies

```txt
# requirements.txt
fastapi>=0.100.0
uvicorn>=0.23.0
gitpython>=3.1.0
pytest>=7.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pygithub>=2.0.0
```

---

## Directory Structure

```
nixtla-docs-qa-generator/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── docs-qa.md
├── scripts/
│   ├── mcp_server.py
│   ├── change_detector.py
│   ├── ast_parser.py
│   ├── example_extractor.py
│   ├── test_runner.py
│   └── pr_creator.py
├── config.yaml
├── requirements.txt
└── README.md
```
