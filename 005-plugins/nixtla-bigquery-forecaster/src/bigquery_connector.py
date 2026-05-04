"""
BigQuery Connector for Nixtla Forecasting

Handles reading time series data from BigQuery and writing forecasts back.

Production-grade hardening (v1.0):
  - All identifiers (project / dataset / table / column) are validated
    against BigQuery's identifier regex BEFORE interpolation. Untrusted
    input cannot inject into the query string.
  - read_timeseries() supports a structured ``filters`` mapping for
    safe column-equality WHERE clauses with parameterized values. The
    legacy ``where_clause`` string is still accepted but emits a
    DeprecationWarning — callers should migrate.
  - All BigQuery API calls are wrapped with retry_on_transient for
    exponential-backoff retry on 429 / 503 / 504 / DeadlineExceeded.
"""

import logging
import warnings
from typing import Any, Dict, Optional

import pandas as pd
from google.cloud import bigquery

from .retry import retry_on_transient
from .sql_validation import (
    safe_where_value,
    validate_identifier,
    validate_project_id,
)

logger = logging.getLogger(__name__)


class BigQueryConnector:
    """Connect to BigQuery and handle time series data operations."""

    def __init__(self, project_id: str):
        """
        Initialize BigQuery client.

        Args:
            project_id: GCP project ID. Validated against the GCP project-ID
                rules (6–30 chars, lowercase letters/digits/hyphens, must
                start with a letter, must not end with a hyphen).

        Raises:
            InvalidIdentifierError: if project_id fails validation.
        """
        self.project_id = validate_project_id(project_id)
        self.client = bigquery.Client(project=self.project_id)
        logger.info(f"BigQuery client initialized for project: {self.project_id}")

    @retry_on_transient()
    def _execute_query(self, query: str) -> pd.DataFrame:
        """Execute a query and return its DataFrame. Wrapped for retry."""
        return self.client.query(query).to_dataframe()

    def read_timeseries(
        self,
        dataset: str,
        table: str,
        timestamp_col: str,
        value_col: str,
        group_by: Optional[str] = None,
        where_clause: Optional[str] = None,
        limit: Optional[int] = None,
        source_project: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> pd.DataFrame:
        """
        Read time series data from BigQuery.

        Args:
            dataset: BigQuery dataset name. Validated.
            table: Table name. Validated.
            timestamp_col: Column with timestamps. Validated.
            value_col: Column with values. Validated.
            group_by: Optional column to group time series by. Validated if set.
            where_clause: Optional pre-built WHERE clause string. DEPRECATED —
                use ``filters`` instead. If supplied, the caller is fully
                responsible for SQL-safe construction (this argument is
                interpolated as-is). Emits a DeprecationWarning.
            limit: Optional row limit (must be a non-negative int).
            source_project: Optional source project ID (for public datasets).
                Validated against project-ID rules if provided.
            filters: Optional ``{column_name: value}`` dict. Each column name
                is validated as an identifier and each value is rendered via
                ``safe_where_value`` (only YYYY-MM-DD dates and numeric
                literals are accepted). Combined with AND.

        Returns:
            DataFrame in Nixtla format (unique_id, ds, y).

        Raises:
            InvalidIdentifierError: if any identifier or filter value fails
                validation.
            ValueError: if ``limit`` is negative.
        """
        # --- Validate identifiers up front ---
        validate_identifier(dataset, kind="dataset")
        validate_identifier(table, kind="table")
        validate_identifier(timestamp_col, kind="timestamp_col")
        validate_identifier(value_col, kind="value_col")
        if group_by is not None:
            validate_identifier(group_by, kind="group_by")
        if source_project is not None:
            validate_project_id(source_project)
        if limit is not None and (not isinstance(limit, int) or limit < 0):
            raise ValueError(f"limit must be a non-negative int, got {limit!r}")

        data_project = source_project if source_project else self.project_id

        # --- Build SELECT clause from validated identifiers ---
        if group_by:
            query = (
                f"SELECT\n"
                f"    {group_by} as unique_id,\n"
                f"    CAST({timestamp_col} AS DATE) as ds,\n"
                f"    SUM({value_col}) as y\n"
                f"FROM `{data_project}.{dataset}.{table}`"
            )
        else:
            query = (
                f"SELECT\n"
                f"    'series_1' as unique_id,\n"
                f"    CAST({timestamp_col} AS DATE) as ds,\n"
                f"    SUM({value_col}) as y\n"
                f"FROM `{data_project}.{dataset}.{table}`"
            )

        # --- Build WHERE from structured filters (preferred) ---
        where_parts = []
        if filters:
            for col, value in filters.items():
                validate_identifier(col, kind="filter column")
                rendered = safe_where_value(value)
                where_parts.append(f"{col} = {rendered}")

        if where_clause:
            warnings.warn(
                "where_clause is deprecated; use filters={col: value} for "
                "SQL-safe filtering. The where_clause string is interpolated "
                "as-is and is the caller's responsibility to keep safe.",
                DeprecationWarning,
                stacklevel=2,
            )
            where_parts.append(f"({where_clause})")

        if where_parts:
            query += "\nWHERE " + " AND ".join(where_parts)

        query += "\nGROUP BY unique_id, ds\nORDER BY unique_id, ds"

        if limit:
            query += f"\nLIMIT {limit}"

        logger.info(f"Executing BigQuery query:\n{query}")

        # Execute query (retry-wrapped on transient GCP errors)
        df = self._execute_query(query)

        # Convert ds to datetime for statsforecast compatibility
        df["ds"] = pd.to_datetime(df["ds"])

        logger.info(f"Read {len(df)} rows, {df['unique_id'].nunique()} unique time series")

        return df

    @retry_on_transient()
    def write_forecasts(
        self, df: pd.DataFrame, dataset: str, table: str, if_exists: str = "replace"
    ) -> str:
        """
        Write forecast results to BigQuery.

        Args:
            df: Forecast DataFrame
            dataset: BigQuery dataset name. Validated.
            table: Table name. Validated.
            if_exists: 'fail', 'replace', or 'append'.

        Returns:
            Full table ID.

        Raises:
            InvalidIdentifierError: if dataset or table fails validation.
            KeyError: if if_exists is not one of the allowed values.
        """
        validate_identifier(dataset, kind="dataset")
        validate_identifier(table, kind="table")
        if if_exists not in {"replace", "append", "fail"}:
            raise ValueError(f"if_exists must be 'replace', 'append', or 'fail'; got {if_exists!r}")

        table_id = f"{self.project_id}.{dataset}.{table}"

        write_disposition = {
            "replace": bigquery.WriteDisposition.WRITE_TRUNCATE,
            "append": bigquery.WriteDisposition.WRITE_APPEND,
            "fail": bigquery.WriteDisposition.WRITE_EMPTY,
        }[if_exists]

        job_config = bigquery.LoadJobConfig(write_disposition=write_disposition, autodetect=True)

        logger.info(f"Writing {len(df)} forecast rows to {table_id}")

        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Wait for completion

        logger.info(f"Successfully wrote forecasts to {table_id}")

        return table_id

    @retry_on_transient()
    def get_table_info(self, dataset: str, table: str) -> dict:
        """
        Get metadata about a BigQuery table.

        Args:
            dataset: Dataset name. Validated.
            table: Table name. Validated.

        Returns:
            Dict with table metadata.

        Raises:
            InvalidIdentifierError: if dataset or table fails validation.
        """
        validate_identifier(dataset, kind="dataset")
        validate_identifier(table, kind="table")
        table_ref = f"{self.project_id}.{dataset}.{table}"
        table_obj = self.client.get_table(table_ref)

        return {
            "table_id": table_ref,
            "num_rows": table_obj.num_rows,
            "num_bytes": table_obj.num_bytes,
            "created": table_obj.created,
            "modified": table_obj.modified,
            "schema": [
                {"name": field.name, "type": field.field_type} for field in table_obj.schema
            ],
        }


if __name__ == "__main__":
    # Test with BigQuery public data
    logging.basicConfig(level=logging.INFO)

    connector = BigQueryConnector(project_id="bigquery-public-data")

    # Test reading (limit to small sample)
    df = connector.read_timeseries(
        dataset="chicago_taxi_trips",
        table="taxi_trips",
        timestamp_col="trip_start_timestamp",
        value_col="trip_total",
        group_by="payment_type",
        where_clause="trip_start_timestamp >= '2024-01-01'",
        limit=10000,
    )

    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"Unique series: {df['unique_id'].nunique()}")
