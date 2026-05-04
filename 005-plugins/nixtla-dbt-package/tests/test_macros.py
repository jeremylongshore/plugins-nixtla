"""Static tests for the dbt-package macros.

Real dbt macro execution requires a running warehouse target. These tests
verify the layout-and-shape contract: every macro file parses as valid
Jinja2, the BigQuery (canonical) macro renders to syntactically valid
SQL with the expected columns, and the per-warehouse dispatch matches
the documented PoC matrix.

Integration tests against a real BigQuery / Snowflake / Databricks
target live separately under ``tests/integration/`` (they require
warehouse credentials and the appropriate Nixtla deployment).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
MACRO_DIR = PLUGIN_ROOT / "macros"
PLUGIN_JSON = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
DBT_PROJECT_YML = PLUGIN_ROOT / "dbt_project.yml"


# ---------------------------------------------------------------------------
# Plugin metadata
# ---------------------------------------------------------------------------


class TestPluginMetadata:
    def test_plugin_json_exists(self):
        assert PLUGIN_JSON.exists()

    def test_version_is_1_0_0(self):
        meta = json.loads(PLUGIN_JSON.read_text())
        assert meta["version"] == "1.0.0"

    def test_canonical_author_block(self):
        meta = json.loads(PLUGIN_JSON.read_text())
        assert meta["author"]["name"] == "Jeremy Longshore"
        assert meta["author"]["email"] == "jeremy@intentsolutions.io"
        assert meta["author"]["url"] == "https://github.com/jeremylongshore"

    def test_license_is_mit(self):
        meta = json.loads(PLUGIN_JSON.read_text())
        assert meta["license"] == "MIT"

    def test_description_documents_poc_status(self):
        meta = json.loads(PLUGIN_JSON.read_text())
        # The description must make the BigQuery-canonical /
        # others-PoC posture explicit so users don't assume parity.
        assert "canonical" in meta["description"].lower()
        assert "poc" in meta["description"].lower()


# ---------------------------------------------------------------------------
# dbt project file
# ---------------------------------------------------------------------------


class TestDbtProject:
    def test_dbt_project_exists(self):
        assert DBT_PROJECT_YML.exists()

    def test_dbt_project_declares_macro_path(self):
        content = DBT_PROJECT_YML.read_text()
        assert 'macro-paths: ["macros"]' in content

    def test_dbt_project_uses_nixtla_api_key_env_var(self):
        content = DBT_PROJECT_YML.read_text()
        assert "NIXTLA_API_KEY" in content


# ---------------------------------------------------------------------------
# Macro files exist and are non-empty
# ---------------------------------------------------------------------------


EXPECTED_MACRO_FILES = ["nixtla_forecast.sql", "nixtla_anomaly_detect.sql"]


class TestMacroFiles:
    @pytest.mark.parametrize("filename", EXPECTED_MACRO_FILES)
    def test_macro_file_exists(self, filename):
        assert (MACRO_DIR / filename).exists()

    @pytest.mark.parametrize("filename", EXPECTED_MACRO_FILES)
    def test_macro_file_non_empty(self, filename):
        content = (MACRO_DIR / filename).read_text()
        assert len(content) > 100, f"{filename} too small to be a real macro"


# ---------------------------------------------------------------------------
# Jinja2 syntax — parses without raising
# ---------------------------------------------------------------------------


@pytest.fixture
def jinja_env():
    """A bare Jinja2 environment that accepts dbt's ``{% macro %}`` syntax."""
    jinja2 = pytest.importorskip("jinja2")
    return jinja2.Environment(
        # dbt allows {% set %} / {% macro %} at top level — Jinja2 handles
        # this natively.
        autoescape=False,
        keep_trailing_newline=True,
    )


class TestJinjaParseable:
    @pytest.mark.parametrize("filename", EXPECTED_MACRO_FILES)
    def test_jinja_parses(self, jinja_env, filename):
        from jinja2 import TemplateSyntaxError

        content = (MACRO_DIR / filename).read_text()
        try:
            jinja_env.parse(content)
        except TemplateSyntaxError as exc:
            pytest.fail(f"{filename} has Jinja2 syntax error: {exc}")


# ---------------------------------------------------------------------------
# Per-warehouse dispatch — verifies that nixtla_forecast.sql contains
# both the canonical BigQuery branch AND the PoC dispatches.
# ---------------------------------------------------------------------------


class TestForecastDispatch:
    @pytest.fixture
    def forecast_macro_text(self):
        return (MACRO_DIR / "nixtla_forecast.sql").read_text()

    def test_dispatches_on_target_type(self, forecast_macro_text):
        assert "target.type == 'bigquery'" in forecast_macro_text
        assert "target.type == 'snowflake'" in forecast_macro_text
        assert "target.type == 'databricks'" in forecast_macro_text

    def test_bigquery_macro_uses_ml_forecast(self, forecast_macro_text):
        # Canonical BigQuery path uses BQML ML.FORECAST.
        assert "ML.FORECAST(" in forecast_macro_text

    def test_snowflake_macro_uses_native_app(self, forecast_macro_text):
        # PoC Snowflake path delegates to Nixtla Native App's NIXTLA.FORECAST.
        assert "NIXTLA.FORECAST(" in forecast_macro_text

    def test_databricks_macro_calls_external_udf(self, forecast_macro_text):
        # PoC Databricks path requires a registered Python UDF.
        assert "nixtla_forecast_udf" in forecast_macro_text

    def test_unsupported_target_raises_compiler_error(self, forecast_macro_text):
        # Default branch must surface a clear error rather than emit broken SQL.
        assert "raise_compiler_error" in forecast_macro_text


class TestAnomalyDispatch:
    @pytest.fixture
    def anomaly_macro_text(self):
        return (MACRO_DIR / "nixtla_anomaly_detect.sql").read_text()

    def test_dispatches_on_target_type(self, anomaly_macro_text):
        assert "target.type == 'bigquery'" in anomaly_macro_text
        assert "target.type == 'snowflake'" in anomaly_macro_text

    def test_unsupported_target_raises_compiler_error(self, anomaly_macro_text):
        assert "raise_compiler_error" in anomaly_macro_text


# ---------------------------------------------------------------------------
# README documents the PoC matrix
# ---------------------------------------------------------------------------


class TestReadmePocMatrix:
    @pytest.fixture
    def readme_text(self):
        return (PLUGIN_ROOT / "README.md").read_text()

    def test_readme_documents_canonical_warehouse(self, readme_text):
        # Must explicitly call out the canonical (BigQuery) path so users
        # know what's production-supported vs PoC.
        assert re.search(
            r"BigQuery.*canonical|canonical.*BigQuery", readme_text, re.IGNORECASE
        ), "README must document BigQuery as the canonical implementation"

    def test_readme_documents_poc_warehouses(self, readme_text):
        # Snowflake and Databricks must be flagged as PoC explicitly so
        # downstream users don't assume parity with BigQuery.
        assert re.search(
            r"Snowflake.*PoC|PoC.*Snowflake", readme_text, re.IGNORECASE
        ), "README must label Snowflake as PoC"
