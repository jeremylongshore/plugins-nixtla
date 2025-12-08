"""
Nixtla BigQuery Forecaster

Run Nixtla statsforecast models on BigQuery time series data.
"""

__version__ = "0.1.0"

from .bigquery_connector import BigQueryConnector
from .forecaster import NixtlaForecaster

__all__ = ["BigQueryConnector", "NixtlaForecaster"]
