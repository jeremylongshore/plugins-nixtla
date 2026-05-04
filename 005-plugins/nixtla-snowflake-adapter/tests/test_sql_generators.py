"""Pytest tests for the snowflake-adapter SQL generators + MCP dispatch.

These tests cover the deterministic, offline surface of the plugin:

  - generate_forecast_sql() with and without group_by_col
  - generate_setup_validation_sql() invariants
  - call_tool() dispatch for all four tool names
  - list_tools() shape

Integration tests against an actual Snowflake account live under
tests/integration/ (created later when an account is wired up); they
are NOT part of this default pytest run.
"""

from __future__ import annotations

import asyncio

import pytest
from snowflake_mcp import (
    call_tool,
    generate_forecast_sql,
    generate_setup_validation_sql,
    list_tools,
)


# ---------------------------------------------------------------------------
# generate_forecast_sql
# ---------------------------------------------------------------------------


class TestGenerateForecastSQL:
    def test_minimal_args(self):
        sql = generate_forecast_sql(table="sales")
        # Required: NIXTLA.FORECAST CALL with the table interpolated.
        assert "CALL NIXTLA.FORECAST(" in sql
        assert "INPUT_TABLE => 'sales'" in sql

    def test_default_columns_and_horizon(self):
        sql = generate_forecast_sql(table="sales")
        assert "TIMESTAMP_COL => 'ds'" in sql
        assert "VALUE_COL => 'y'" in sql
        assert "HORIZON => 30" in sql
        assert "FREQUENCY => 'D'" in sql

    def test_group_by_emits_clause_and_results_order(self):
        sql = generate_forecast_sql(table="sales", group_by_col="store")
        assert "GROUP_BY_COL => 'store'" in sql
        # Results-ordering should include the group key.
        assert "ORDER BY 'store', FORECAST_DATE" in sql

    def test_no_group_by_omits_clause(self):
        sql = generate_forecast_sql(table="sales")
        assert "GROUP_BY_COL" not in sql
        assert "ORDER BY FORECAST_DATE" in sql

    def test_custom_levels_serialized_to_array(self):
        sql = generate_forecast_sql(table="sales", levels=[50, 80])
        assert "LEVEL => ARRAY_CONSTRUCT(50, 80)" in sql

    def test_default_levels_80_90_95(self):
        sql = generate_forecast_sql(table="sales")
        assert "LEVEL => ARRAY_CONSTRUCT(80, 90, 95)" in sql

    def test_custom_columns_and_freq(self):
        sql = generate_forecast_sql(
            table="hourly_traffic",
            timestamp_col="event_ts",
            value_col="visits",
            horizon=72,
            freq="H",
        )
        assert "INPUT_TABLE => 'hourly_traffic'" in sql
        assert "TIMESTAMP_COL => 'event_ts'" in sql
        assert "VALUE_COL => 'visits'" in sql
        assert "HORIZON => 72" in sql
        assert "FREQUENCY => 'H'" in sql

    def test_includes_results_select(self):
        sql = generate_forecast_sql(table="sales")
        assert "SELECT *" in sql
        assert "NIXTLA.FORECAST_RESULTS" in sql


# ---------------------------------------------------------------------------
# generate_setup_validation_sql
# ---------------------------------------------------------------------------


class TestGenerateSetupValidationSQL:
    def test_returns_non_empty_string(self):
        sql = generate_setup_validation_sql()
        assert isinstance(sql, str)
        assert len(sql) > 100

    def test_includes_all_validation_checks(self):
        sql = generate_setup_validation_sql()
        # The validation script must check (a) app installed, (b) grants,
        # (c) function definitions, and (d) run a smoke forecast.
        assert "SHOW APPLICATIONS LIKE 'NIXTLA%'" in sql
        assert "SHOW GRANTS ON APPLICATION NIXTLA" in sql
        assert "DESCRIBE FUNCTION NIXTLA.FORECAST" in sql
        assert "DESCRIBE FUNCTION NIXTLA.DETECT_ANOMALIES" in sql
        assert "DESCRIBE FUNCTION NIXTLA.CROSS_VALIDATE" in sql
        assert "CALL NIXTLA.FORECAST(" in sql

    def test_cleans_up_test_data(self):
        sql = generate_setup_validation_sql()
        assert "DROP TABLE IF EXISTS test_data" in sql


# ---------------------------------------------------------------------------
# list_tools (MCP surface)
# ---------------------------------------------------------------------------


class TestListTools:
    def test_returns_four_tools(self):
        tools = asyncio.run(list_tools())
        assert len(tools) == 4

    def test_tool_names(self):
        tools = asyncio.run(list_tools())
        names = {t.name for t in tools}
        assert names == {
            "generate_forecast_sql",
            "validate_setup",
            "generate_anomaly_sql",
            "export_looker_view",
        }

    def test_forecast_sql_tool_requires_table(self):
        tools = asyncio.run(list_tools())
        forecast = next(t for t in tools if t.name == "generate_forecast_sql")
        assert "table" in forecast.inputSchema["required"]


# ---------------------------------------------------------------------------
# call_tool (MCP dispatch)
# ---------------------------------------------------------------------------


class TestCallToolDispatch:
    def test_generate_forecast_sql_through_dispatch(self):
        result = asyncio.run(
            call_tool("generate_forecast_sql", {"table": "demo_table", "horizon": 14})
        )
        assert len(result) == 1
        assert result[0].type == "text"
        assert "INPUT_TABLE => 'demo_table'" in result[0].text
        assert "HORIZON => 14" in result[0].text

    def test_validate_setup_through_dispatch(self):
        result = asyncio.run(call_tool("validate_setup", {}))
        assert "SHOW APPLICATIONS LIKE 'NIXTLA%'" in result[0].text

    def test_anomaly_sql_includes_level(self):
        result = asyncio.run(
            call_tool("generate_anomaly_sql", {"table": "metrics", "level": 99})
        )
        assert "DETECT_ANOMALIES" in result[0].text
        assert "INPUT_TABLE => 'metrics'" in result[0].text
        assert "LEVEL => 99" in result[0].text
        # Default columns when not provided
        assert "TIMESTAMP_COL => 'ds'" in result[0].text
        assert "VALUE_COL => 'y'" in result[0].text

    def test_anomaly_sql_default_level(self):
        result = asyncio.run(call_tool("generate_anomaly_sql", {"table": "metrics"}))
        assert "LEVEL => 95" in result[0].text

    def test_export_looker_view_default_name(self):
        result = asyncio.run(call_tool("export_looker_view", {}))
        text = result[0].text
        assert "view: nixtla_forecasts {" in text
        assert "NIXTLA.FORECAST_RESULTS" in text

    def test_export_looker_view_custom_name(self):
        result = asyncio.run(call_tool("export_looker_view", {"view_name": "weekly_sales_fc"}))
        assert "view: weekly_sales_fc {" in result[0].text

    def test_unknown_tool_returns_text_message(self):
        result = asyncio.run(call_tool("totally_fake", {}))
        assert "Unknown tool" in result[0].text
        assert "totally_fake" in result[0].text


# ---------------------------------------------------------------------------
# Defensive checks against accidental SQL injection in args
# ---------------------------------------------------------------------------


class TestArgumentEscaping:
    """The generators trust caller input — these tests document that contract.

    If escaping is added later, these tests should still pass: the generated
    SQL must continue to embed the table name verbatim. The point is to
    surface drift rather than block insecure behavior; production use should
    parameterize via Snowflake bind variables.
    """

    def test_table_name_passes_through_verbatim(self):
        sql = generate_forecast_sql(table="weird-but-quoted_table")
        assert "INPUT_TABLE => 'weird-but-quoted_table'" in sql
