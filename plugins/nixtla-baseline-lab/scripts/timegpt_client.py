#!/usr/bin/env python3
"""
TimeGPT API Client for Nixtla Baseline Lab

Provides optional TimeGPT integration for comparing baseline models
against Nixtla's hosted TimeGPT service.

Environment Variables:
- NIXTLA_TIMEGPT_API_KEY: Required API key for TimeGPT access

This module handles API authentication, request formatting, and error
handling to provide a clean interface for the MCP server.
"""

import os
import logging
from typing import Dict, Any, Optional, List
import pandas as pd

logger = logging.getLogger(__name__)


class TimeGPTClient:
    """Client for Nixtla TimeGPT API with graceful error handling."""

    def __init__(self):
        """Initialize TimeGPT client with API key from environment."""
        self.api_key = os.environ.get("NIXTLA_TIMEGPT_API_KEY")
        self.api_available = self.api_key is not None

        if not self.api_available:
            logger.info("TimeGPT API key not found (NIXTLA_TIMEGPT_API_KEY)")
        else:
            logger.info("TimeGPT API key detected")

    def is_available(self) -> bool:
        """Check if TimeGPT API is available (has valid key)."""
        return self.api_available

    def forecast(
        self,
        df: pd.DataFrame,
        horizon: int,
        freq: str = "D",
        level: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Generate forecast using TimeGPT API.

        Args:
            df: DataFrame with columns [unique_id, ds, y]
            horizon: Forecast horizon (number of periods)
            freq: Frequency string ('D' for daily, 'M' for monthly, etc.)
            level: Confidence levels for prediction intervals (e.g., [80, 90, 95])

        Returns:
            Dict with:
            - success: bool
            - forecast: DataFrame with columns [unique_id, ds, TimeGPT] if successful
            - error: str if failed
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "TimeGPT API key not available"
            }

        try:
            # Import nixtla SDK (only when needed)
            from nixtla import NixtlaClient

            # Initialize client
            client = NixtlaClient(api_key=self.api_key)

            # Validate input DataFrame
            required_cols = {'unique_id', 'ds', 'y'}
            if not required_cols.issubset(set(df.columns)):
                return {
                    "success": False,
                    "error": f"DataFrame missing required columns. Need: {required_cols}"
                }

            # Generate forecast
            logger.info(f"Calling TimeGPT API for {len(df['unique_id'].unique())} series, horizon={horizon}")

            forecast_df = client.forecast(
                df=df,
                h=horizon,
                freq=freq,
                level=level or [80, 90]  # Default confidence levels
            )

            # Rename TimeGPT column for consistency
            if 'TimeGPT' not in forecast_df.columns:
                logger.warning(f"TimeGPT column not found in forecast. Columns: {forecast_df.columns.tolist()}")
                return {
                    "success": False,
                    "error": "TimeGPT API returned unexpected format"
                }

            logger.info(f"TimeGPT forecast successful: {len(forecast_df)} predictions")

            return {
                "success": True,
                "forecast": forecast_df
            }

        except ImportError as e:
            error_msg = f"nixtla SDK not installed: {e}. Install with: pip install nixtla"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }

        except Exception as e:
            error_msg = f"TimeGPT API error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "error": error_msg
            }

    def get_status(self) -> Dict[str, Any]:
        """
        Get TimeGPT client status for diagnostics.

        Returns:
            Dict with status information
        """
        status = {
            "api_key_present": self.api_key is not None,
            "available": self.is_available()
        }

        # Check if nixtla SDK is importable
        try:
            import nixtla
            status["sdk_installed"] = True
            status["sdk_version"] = getattr(nixtla, "__version__", "unknown")
        except ImportError:
            status["sdk_installed"] = False
            status["sdk_version"] = None

        return status


def create_timegpt_client() -> TimeGPTClient:
    """
    Factory function to create TimeGPT client.

    Returns:
        TimeGPTClient instance
    """
    return TimeGPTClient()
