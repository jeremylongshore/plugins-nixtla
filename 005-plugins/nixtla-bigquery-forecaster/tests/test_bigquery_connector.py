"""Tests for BigQueryConnector.

These tests mock the google.cloud.bigquery client at import time so the
connector's query construction + retry contract can be verified without
hitting a real BigQuery account. Integration tests against a live GCP
project live separately under tests/integration/.
"""

from __future__ import annotations

import warnings
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from src.sql_validation import InvalidIdentifierError

# ---------------------------------------------------------------------------
# Init validation
# ---------------------------------------------------------------------------


class TestInit:
    def test_init_validates_project_id(self):
        from src.bigquery_connector import BigQueryConnector

        with pytest.raises(InvalidIdentifierError):
            BigQueryConnector(project_id="UPPERCASE-NOT-ALLOWED")

    def test_init_rejects_short_project_id(self):
        from src.bigquery_connector import BigQueryConnector

        with pytest.raises(InvalidIdentifierError):
            BigQueryConnector(project_id="abc")

    @patch("src.bigquery_connector.bigquery.Client")
    def test_init_succeeds_with_valid_project_id(self, mock_client):
        from src.bigquery_connector import BigQueryConnector

        c = BigQueryConnector(project_id="my-project")
        assert c.project_id == "my-project"
        mock_client.assert_called_once_with(project="my-project")


# ---------------------------------------------------------------------------
# read_timeseries — identifier validation
# ---------------------------------------------------------------------------


@patch("src.bigquery_connector.bigquery.Client")
class TestReadTimeseriesValidation:
    def _make_connector(self):
        from src.bigquery_connector import BigQueryConnector

        return BigQueryConnector(project_id="test-project")

    @pytest.mark.parametrize(
        "kwarg,bad_value",
        [
            ("dataset", "bad-dataset"),
            ("table", "table; DROP"),
            ("timestamp_col", "1starts_with_digit"),
            ("value_col", "has space"),
            ("group_by", "DROP TABLE x; --"),
        ],
    )
    def test_invalid_identifier_raises_before_query(self, _client, kwarg, bad_value):
        conn = self._make_connector()
        good_kwargs = dict(
            dataset="ds",
            table="tbl",
            timestamp_col="ts",
            value_col="val",
        )
        good_kwargs[kwarg] = bad_value
        with pytest.raises(InvalidIdentifierError):
            conn.read_timeseries(**good_kwargs)

    def test_invalid_source_project_raises(self, _client):
        conn = self._make_connector()
        with pytest.raises(InvalidIdentifierError):
            conn.read_timeseries(
                dataset="ds",
                table="tbl",
                timestamp_col="ts",
                value_col="val",
                source_project="UPPER-CASE",
            )

    def test_negative_limit_rejected(self, _client):
        conn = self._make_connector()
        with pytest.raises(ValueError):
            conn.read_timeseries(
                dataset="ds",
                table="tbl",
                timestamp_col="ts",
                value_col="val",
                limit=-1,
            )

    def test_filters_with_invalid_column_raises(self, _client):
        conn = self._make_connector()
        with pytest.raises(InvalidIdentifierError):
            conn.read_timeseries(
                dataset="ds",
                table="tbl",
                timestamp_col="ts",
                value_col="val",
                filters={"bad-col": "2024-01-01"},
            )

    def test_filters_with_unsafe_value_raises(self, _client):
        conn = self._make_connector()
        with pytest.raises(InvalidIdentifierError):
            conn.read_timeseries(
                dataset="ds",
                table="tbl",
                timestamp_col="ts",
                value_col="val",
                filters={"region": "'; DROP TABLE users; --"},
            )


# ---------------------------------------------------------------------------
# read_timeseries — query shape
# ---------------------------------------------------------------------------


@patch("src.bigquery_connector.bigquery.Client")
class TestReadTimeseriesQueryShape:
    def _make_connector_with_query_stub(self, mock_client_cls, captured_queries):
        """Wire a connector whose .client.query() captures the SQL string."""
        from src.bigquery_connector import BigQueryConnector

        # Mock the BQ client so .client.query(sql) returns a Mock whose
        # to_dataframe() yields a small valid DataFrame.
        mock_client = MagicMock()
        df = pd.DataFrame({"unique_id": ["x"], "ds": ["2024-01-01"], "y": [1.0]})

        def query_capture(sql):
            captured_queries.append(sql)
            mock_query = MagicMock()
            mock_query.to_dataframe.return_value = df
            return mock_query

        mock_client.query.side_effect = query_capture
        mock_client_cls.return_value = mock_client

        return BigQueryConnector(project_id="test-project")

    def test_basic_query_uses_validated_identifiers(self, mock_client_cls):
        captured = []
        conn = self._make_connector_with_query_stub(mock_client_cls, captured)
        conn.read_timeseries(
            dataset="my_dataset",
            table="my_table",
            timestamp_col="event_ts",
            value_col="amount",
        )
        sql = captured[0]
        assert "my_dataset" in sql
        assert "my_table" in sql
        assert "CAST(event_ts AS DATE)" in sql
        assert "SUM(amount)" in sql

    def test_filters_are_emitted_with_safe_values(self, mock_client_cls):
        captured = []
        conn = self._make_connector_with_query_stub(mock_client_cls, captured)
        conn.read_timeseries(
            dataset="my_dataset",
            table="my_table",
            timestamp_col="event_ts",
            value_col="amount",
            filters={"region": "2024-01-15", "store_id": 42},
        )
        sql = captured[0]
        assert "WHERE" in sql
        assert "region = '2024-01-15'" in sql
        assert "store_id = 42" in sql
        # Joined with AND
        assert "AND" in sql

    def test_legacy_where_clause_emits_deprecation_warning(self, mock_client_cls):
        captured = []
        conn = self._make_connector_with_query_stub(mock_client_cls, captured)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            conn.read_timeseries(
                dataset="ds",
                table="tbl",
                timestamp_col="ts",
                value_col="val",
                where_clause="ts >= '2024-01-01'",
            )
        deprecation_warnings = [w for w in caught if issubclass(w.category, DeprecationWarning)]
        assert len(deprecation_warnings) >= 1
        # And the where_clause string still ends up in the SQL
        assert "ts >= '2024-01-01'" in captured[0]

    def test_limit_appended_to_query(self, mock_client_cls):
        captured = []
        conn = self._make_connector_with_query_stub(mock_client_cls, captured)
        conn.read_timeseries(
            dataset="ds",
            table="tbl",
            timestamp_col="ts",
            value_col="val",
            limit=100,
        )
        assert "LIMIT 100" in captured[0]


# ---------------------------------------------------------------------------
# write_forecasts validation
# ---------------------------------------------------------------------------


@patch("src.bigquery_connector.bigquery.Client")
class TestWriteForecasts:
    def _make_connector(self, mock_client_cls):
        from src.bigquery_connector import BigQueryConnector

        mock_client = MagicMock()
        # load_table_from_dataframe returns a job with a .result() method
        mock_job = MagicMock()
        mock_client.load_table_from_dataframe.return_value = mock_job
        mock_client_cls.return_value = mock_client
        return BigQueryConnector(project_id="test-project"), mock_client, mock_job

    def test_invalid_dataset_rejected(self, mock_client_cls):
        conn, _, _ = self._make_connector(mock_client_cls)
        df = pd.DataFrame({"unique_id": ["x"], "ds": ["2024-01-01"], "y": [1.0]})
        with pytest.raises(InvalidIdentifierError):
            conn.write_forecasts(df, dataset="bad-ds", table="t")

    def test_invalid_if_exists_rejected(self, mock_client_cls):
        conn, _, _ = self._make_connector(mock_client_cls)
        df = pd.DataFrame({"unique_id": ["x"], "ds": ["2024-01-01"], "y": [1.0]})
        with pytest.raises(ValueError):
            conn.write_forecasts(df, dataset="ds", table="t", if_exists="weird")

    def test_valid_call_returns_table_id(self, mock_client_cls):
        conn, mock_client, mock_job = self._make_connector(mock_client_cls)
        df = pd.DataFrame({"unique_id": ["x"], "ds": ["2024-01-01"], "y": [1.0]})
        result = conn.write_forecasts(df, dataset="ds", table="t", if_exists="replace")
        assert result == "test-project.ds.t"
        mock_client.load_table_from_dataframe.assert_called_once()
        mock_job.result.assert_called_once()
