"""Unit tests for nixtla-airflow-operator MCP server."""

from __future__ import annotations

import asyncio
import json

import airflow_mcp as mcp
import pytest

VALID_DAG_SOURCE = """
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "data-team",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def extract_data():
    pass

def run_forecast():
    pass

with DAG(
    "test_dag",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
) as dag:
    extract = PythonOperator(task_id="extract_data", python_callable=extract_data)
    forecast = PythonOperator(task_id="run_forecast", python_callable=run_forecast)
    extract >> forecast
"""


SYNTAX_ERROR_DAG = """
from airflow import DAG

with DAG("broken" as dag:
    pass
"""


DAG_WITH_DUPES = """
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG("dupes", schedule_interval="@daily", start_date=datetime(2024,1,1)) as dag:
    a = PythonOperator(task_id="same", python_callable=lambda: None)
    b = PythonOperator(task_id="same", python_callable=lambda: None)
"""


DAG_WITH_HARDCODED_KEY = """
from airflow import DAG

api_key = "supersecret_abc123_value"  # this should be flagged

with DAG("k", schedule_interval="@daily", start_date=datetime(2024,1,1)) as dag:
    pass
"""


# ---------------------------------------------------------------------------
# generate_dag
# ---------------------------------------------------------------------------


class TestGenerateDag:
    def test_dag_template_substitution(self):
        # Direct call_tool to exercise the dispatch.
        async def go():
            return await mcp.call_tool(
                "generate_dag",
                {
                    "dag_name": "my_test_dag",
                    "schedule": "@hourly",
                    "source": "bigquery",
                    "horizon": 21,
                    "freq": "H",
                    "alert_email": "team@example.com",
                },
            )

        result = asyncio.run(go())
        text = result[0].text
        assert "my_test_dag" in text
        assert "@hourly" in text
        assert "h=21" in text
        assert "freq='H'" in text
        assert "team@example.com" in text


# ---------------------------------------------------------------------------
# validate_dag
# ---------------------------------------------------------------------------


class TestValidateDag:
    def test_valid_dag(self):
        result = mcp.validate_dag(source=VALID_DAG_SOURCE)
        assert result["valid"] is True
        assert result["task_count"] == 2
        assert "extract_data" in result["task_ids"]
        assert "run_forecast" in result["task_ids"]
        assert result["dag_id"] == "test_dag"

    def test_syntax_error(self):
        result = mcp.validate_dag(source=SYNTAX_ERROR_DAG)
        assert result["valid"] is False
        assert any("syntax" in e["message"].lower() for e in result["errors"])

    def test_duplicate_task_ids_flagged(self):
        result = mcp.validate_dag(source=DAG_WITH_DUPES)
        assert any("duplicate" in e["message"].lower() for e in result["errors"])

    def test_hardcoded_credential_flagged_as_warning(self):
        result = mcp.validate_dag(source=DAG_WITH_HARDCODED_KEY)
        assert any("credential" in w["message"].lower() for w in result["warnings"])

    def test_missing_default_args_warned(self):
        source = """
from airflow import DAG
from datetime import datetime

with DAG("no_defaults", schedule_interval="@daily", start_date=datetime(2024,1,1)) as dag:
    pass
"""
        result = mcp.validate_dag(source=source)
        assert any("default_args" in w["message"] for w in result["warnings"])

    def test_missing_dag_path_and_source_returns_error(self):
        result = mcp.validate_dag()
        assert result["valid"] is False

    def test_missing_file_returns_error(self):
        result = mcp.validate_dag(dag_path="/nonexistent/dag.py")
        assert result["valid"] is False
        assert any("file not found" in e["message"].lower() for e in result["errors"])


# ---------------------------------------------------------------------------
# configure_connection
# ---------------------------------------------------------------------------


class TestConfigureConnection:
    def test_nixtla(self):
        result = mcp.configure_connection(
            source="nixtla", connection_id="nixtla_default", config={"api_key": "test123"}
        )
        assert result["status"] == "success"
        assert result["connection"]["conn_type"] == "http"
        assert result["connection"]["password"] == "test123"
        assert "airflow connections add nixtla_default" in result["cli_command"]

    def test_bigquery_requires_project_id(self):
        result = mcp.configure_connection(source="bigquery", connection_id="bq", config={})
        assert result["status"] == "error"
        assert "project_id" in result["message"]

    def test_bigquery_with_project_id(self):
        result = mcp.configure_connection(
            source="bigquery", connection_id="bq", config={"project_id": "my-proj"}
        )
        assert result["status"] == "success"
        extra = json.loads(result["connection"]["extra"])
        assert extra["project"] == "my-proj"

    def test_snowflake_complete(self):
        result = mcp.configure_connection(
            source="snowflake",
            connection_id="snow",
            config={
                "account": "abc",
                "user": "u",
                "password": "p",
                "warehouse": "w",
                "database": "d",
                "schema": "s",
            },
        )
        assert result["status"] == "success"
        assert result["connection"]["host"] == "abc.snowflakecomputing.com"

    def test_snowflake_missing_field(self):
        result = mcp.configure_connection(
            source="snowflake", connection_id="snow", config={"account": "abc"}
        )
        assert result["status"] == "error"

    def test_postgres(self):
        result = mcp.configure_connection(
            source="postgres",
            connection_id="pg",
            config={
                "host": "localhost",
                "port": 5432,
                "user": "u",
                "password": "p",
                "database": "d",
            },
        )
        assert result["status"] == "success"
        assert result["connection"]["port"] == 5432

    def test_s3_with_region(self):
        result = mcp.configure_connection(
            source="s3",
            connection_id="s3default",
            config={
                "aws_access_key_id": "AKIA",
                "aws_secret_access_key": "secret",
                "region_name": "eu-west-1",
            },
        )
        assert result["status"] == "success"
        extra = json.loads(result["connection"]["extra"])
        assert extra["region_name"] == "eu-west-1"

    def test_unknown_source(self):
        result = mcp.configure_connection(source="oracle", connection_id="x")
        assert result["status"] == "error"
        assert "unsupported" in result["message"].lower()


# ---------------------------------------------------------------------------
# generate_tests
# ---------------------------------------------------------------------------


class TestGenerateTests:
    def test_with_source_extracts_task_ids(self):
        result = mcp.generate_tests(dag_name="test_dag", source=VALID_DAG_SOURCE)
        assert result["status"] == "success"
        assert "extract_data" in result["expected_task_ids"]
        assert "run_forecast" in result["expected_task_ids"]
        assert "test_test_dag.py" == result["test_filename"]

    def test_no_source_uses_default_task_ids(self):
        result = mcp.generate_tests(dag_name="default_dag")
        assert result["expected_task_ids"] == ["extract_data", "run_forecast", "load_results"]

    def test_test_module_uses_dagbag(self):
        result = mcp.generate_tests(dag_name="d", source=VALID_DAG_SOURCE)
        assert "from airflow.models.dagbag import DagBag" in result["test_module"]
        assert "test_dag_loads_without_errors" in result["test_module"]
        assert "test_dag_present" in result["test_module"]

    def test_includes_run_instructions(self):
        result = mcp.generate_tests(dag_name="x")
        assert "pytest dags/tests/test_x.py" in result["instructions"]


# ---------------------------------------------------------------------------
# call_tool dispatch
# ---------------------------------------------------------------------------


class TestCallTool:
    @pytest.fixture
    def run(self):
        def _run(coro):
            return asyncio.run(coro)

        return _run

    def test_validate_dag_dispatch(self, run):
        result = run(mcp.call_tool("validate_dag", {"source": VALID_DAG_SOURCE}))
        parsed = json.loads(result[0].text)
        assert parsed["valid"] is True

    def test_configure_connection_dispatch(self, run):
        result = run(
            mcp.call_tool(
                "configure_connection",
                {"source": "nixtla", "connection_id": "n", "config": {"api_key": "k"}},
            )
        )
        parsed = json.loads(result[0].text)
        assert parsed["status"] == "success"

    def test_generate_tests_dispatch(self, run):
        result = run(mcp.call_tool("generate_tests", {"dag_name": "x"}))
        parsed = json.loads(result[0].text)
        assert parsed["status"] == "success"

    def test_unknown_tool(self, run):
        result = run(mcp.call_tool("zzz", {}))
        assert "Unknown" in result[0].text

    def test_list_tools_includes_all_four(self, run):
        tools = run(mcp.list_tools())
        names = {t.name for t in tools}
        assert names == {"generate_dag", "validate_dag", "configure_connection", "generate_tests"}
