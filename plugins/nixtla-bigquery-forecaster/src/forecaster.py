"""
Nixtla Forecaster

Handles statsforecast and TimeGPT forecasting for time series data.
"""

import logging
from typing import List, Optional

import pandas as pd

# Nixtla open-source models
from statsforecast import StatsForecast
from statsforecast.models import AutoETS, AutoTheta, SeasonalNaive

logger = logging.getLogger(__name__)


class NixtlaForecaster:
    """Run Nixtla forecasting models on time series data."""

    def __init__(self, timegpt_api_key: Optional[str] = None):
        """
        Initialize forecaster.

        Args:
            timegpt_api_key: Optional TimeGPT API key for proprietary model
        """
        self.timegpt_api_key = timegpt_api_key
        self.timegpt_client = None

        if timegpt_api_key:
            try:
                from nixtla import NixtlaClient

                self.timegpt_client = NixtlaClient(api_key=timegpt_api_key)
                logger.info("TimeGPT client initialized")
            except ImportError:
                logger.warning("nixtla package not installed, TimeGPT disabled")
            except Exception as e:
                logger.warning(f"Could not initialize TimeGPT: {e}")

    def forecast(
        self,
        df: pd.DataFrame,
        horizon: int,
        models: List[str] = None,
        include_timegpt: bool = False,
        freq: str = "D",
    ) -> pd.DataFrame:
        """
        Generate forecasts for time series data.

        Args:
            df: DataFrame with columns (unique_id, ds, y)
            horizon: Forecast horizon (number of periods)
            models: List of model names (default: ["AutoETS", "AutoTheta"])
            include_timegpt: Whether to include TimeGPT forecasts
            freq: Frequency of time series (D=daily, W=weekly, M=monthly)

        Returns:
            DataFrame with forecasts
        """
        if models is None:
            models = ["AutoETS", "AutoTheta"]

        logger.info(f"Running statsforecast with models: {models}")

        # Map model names to statsforecast model classes
        model_map = {
            "AutoETS": AutoETS(season_length=7),
            "AutoTheta": AutoTheta(season_length=7),
            "SeasonalNaive": SeasonalNaive(season_length=7),
        }

        # Select requested models
        selected_models = []
        for model_name in models:
            if model_name in model_map:
                selected_models.append(model_map[model_name])
            else:
                logger.warning(f"Unknown model: {model_name}, skipping")

        if not selected_models:
            raise ValueError(f"No valid models specified. Available: {list(model_map.keys())}")

        # Run statsforecast
        sf = StatsForecast(models=selected_models, freq=freq, n_jobs=-1)  # Use all available cores

        try:
            forecasts = sf.forecast(df=df, h=horizon)
            logger.info(f"Generated {len(forecasts)} forecast points with statsforecast")
        except Exception as e:
            logger.error(f"Error running statsforecast: {e}")
            raise

        # Optionally add TimeGPT forecasts
        if include_timegpt and self.timegpt_client:
            try:
                logger.info("Running TimeGPT forecasts...")
                timegpt_forecast = self.timegpt_client.forecast(
                    df=df, h=horizon, freq=freq, time_col="ds", target_col="y"
                )
                # Merge TimeGPT results
                forecasts = forecasts.merge(
                    timegpt_forecast[["unique_id", "ds", "TimeGPT"]],
                    on=["unique_id", "ds"],
                    how="left",
                )
                logger.info("TimeGPT forecasts added")
            except Exception as e:
                logger.warning(f"TimeGPT forecasting failed: {e}")

        return forecasts.reset_index()

    def backtest(
        self,
        df: pd.DataFrame,
        horizon: int,
        n_windows: int = 3,
        models: List[str] = None,
        freq: str = "D",
    ) -> pd.DataFrame:
        """
        Run backtesting for model evaluation.

        Args:
            df: DataFrame with columns (unique_id, ds, y)
            horizon: Forecast horizon
            n_windows: Number of cross-validation windows
            models: List of model names
            freq: Frequency of time series

        Returns:
            DataFrame with backtest results
        """
        if models is None:
            models = ["AutoETS", "AutoTheta"]

        logger.info(f"Running backtest with {n_windows} windows, horizon={horizon}")

        model_map = {
            "AutoETS": AutoETS(season_length=7),
            "AutoTheta": AutoTheta(season_length=7),
            "SeasonalNaive": SeasonalNaive(season_length=7),
        }

        selected_models = [model_map[m] for m in models if m in model_map]

        sf = StatsForecast(models=selected_models, freq=freq, n_jobs=-1)

        try:
            cv_results = sf.cross_validation(
                df=df, h=horizon, step_size=horizon, n_windows=n_windows
            )
            logger.info(f"Backtest complete: {len(cv_results)} results")
            return cv_results
        except Exception as e:
            logger.error(f"Error during backtesting: {e}")
            raise
