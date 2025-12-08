"""
BigQuery Connector for Nixtla Forecasting

Handles reading time series data from BigQuery and writing forecasts back.
"""

import logging
from typing import List, Optional

import pandas as pd
from google.cloud import bigquery

logger = logging.getLogger(__name__)


class BigQueryConnector:
    """Connect to BigQuery and handle time series data operations."""

    def __init__(self, project_id: str):
        """
        Initialize BigQuery client.

        Args:
            project_id: GCP project ID
        """
        self.project_id = project_id
        self.client = bigquery.Client(project=project_id)
        logger.info(f"BigQuery client initialized for project: {project_id}")

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
    ) -> pd.DataFrame:
        """
        Read time series data from BigQuery.

        Args:
            dataset: BigQuery dataset name
            table: Table name
            timestamp_col: Column with timestamps
            value_col: Column with values
            group_by: Optional column to group time series by
            where_clause: Optional WHERE clause for filtering
            limit: Optional row limit
            source_project: Optional source project ID (for public datasets, defaults to self.project_id)

        Returns:
            DataFrame in Nixtla format (unique_id, ds, y)
        """
        # Determine which project the data lives in
        data_project = source_project if source_project else self.project_id

        # Build query
        if group_by:
            query = f"""
            SELECT
                {group_by} as unique_id,
                CAST({timestamp_col} AS DATE) as ds,
                SUM({value_col}) as y
            FROM `{data_project}.{dataset}.{table}`
            """
        else:
            query = f"""
            SELECT
                'series_1' as unique_id,
                CAST({timestamp_col} AS DATE) as ds,
                SUM({value_col}) as y
            FROM `{data_project}.{dataset}.{table}`
            """

        if where_clause:
            query += f"\nWHERE {where_clause}"

        query += f"\nGROUP BY unique_id, ds\nORDER BY unique_id, ds"

        if limit:
            query += f"\nLIMIT {limit}"

        logger.info(f"Executing BigQuery query:\n{query}")

        # Execute query
        df = self.client.query(query).to_dataframe()

        # Convert ds to datetime for statsforecast compatibility
        df["ds"] = pd.to_datetime(df["ds"])

        logger.info(f"Read {len(df)} rows, {df['unique_id'].nunique()} unique time series")

        return df

    def write_forecasts(
        self, df: pd.DataFrame, dataset: str, table: str, if_exists: str = "replace"
    ) -> str:
        """
        Write forecast results to BigQuery.

        Args:
            df: Forecast DataFrame
            dataset: BigQuery dataset name
            table: Table name
            if_exists: 'fail', 'replace', or 'append'

        Returns:
            Full table ID
        """
        table_id = f"{self.project_id}.{dataset}.{table}"

        # Configure write disposition
        write_disposition = {
            "replace": bigquery.WriteDisposition.WRITE_TRUNCATE,
            "append": bigquery.WriteDisposition.WRITE_APPEND,
            "fail": bigquery.WriteDisposition.WRITE_EMPTY,
        }[if_exists]

        job_config = bigquery.LoadJobConfig(write_disposition=write_disposition, autodetect=True)

        logger.info(f"Writing {len(df)} forecast rows to {table_id}")

        # Write to BigQuery
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Wait for completion

        logger.info(f"Successfully wrote forecasts to {table_id}")

        return table_id

    def get_table_info(self, dataset: str, table: str) -> dict:
        """
        Get metadata about a BigQuery table.

        Args:
            dataset: Dataset name
            table: Table name

        Returns:
            Dict with table metadata
        """
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
