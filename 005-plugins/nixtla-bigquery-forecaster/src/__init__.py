"""
Nixtla BigQuery Forecaster

Run Nixtla statsforecast models on BigQuery time series data.
"""

__version__ = "1.0.0"

# Note: heavy imports (statsforecast, google-cloud-bigquery) are loaded
# lazily on attribute access so that lightweight modules like
# `from src.sql_validation import validate_identifier` work in
# environments where the heavy deps aren't installed (e.g., the
# sql_validation/retry test jobs in CI).

__all__ = [
    "BigQueryConnector",
    "NixtlaForecaster",
    "InvalidIdentifierError",
    "safe_where_value",
    "validate_identifier",
    "validate_project_id",
]


def __getattr__(name: str):
    if name in {"BigQueryConnector"}:
        from .bigquery_connector import BigQueryConnector

        return BigQueryConnector
    if name in {"NixtlaForecaster"}:
        from .forecaster import NixtlaForecaster

        return NixtlaForecaster
    if name in {
        "InvalidIdentifierError",
        "safe_where_value",
        "validate_identifier",
        "validate_project_id",
    }:
        from . import sql_validation

        return getattr(sql_validation, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
