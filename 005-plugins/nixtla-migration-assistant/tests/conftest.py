"""Pytest fixtures for nixtla-migration-assistant tests."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


PROPHET_SOURCE = """
import pandas as pd
from prophet import Prophet

df = pd.read_csv("sales.csv")
m = Prophet(yearly_seasonality=True)
m.fit(df)
future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)
"""


STATSMODELS_ARIMA_SOURCE = """
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv("sales.csv")
model = ARIMA(df["y"], order=(1, 1, 1))
fit = model.fit()
forecast = fit.forecast(steps=30)
"""


STATSMODELS_ETS_SOURCE = """
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd

df = pd.read_csv("sales.csv")
model = ExponentialSmoothing(df["y"], trend="add", seasonal="add", seasonal_periods=12).fit()
forecast = model.forecast(30)
"""


SKLEARN_SOURCE = """
from sklearn.linear_model import LinearRegression
import pandas as pd

df = pd.read_csv("sales.csv")
X = df[["lag_1", "lag_2"]]
y = df["y"]
model = LinearRegression().fit(X, y)
"""


@pytest.fixture
def prophet_source():
    return PROPHET_SOURCE


@pytest.fixture
def statsmodels_arima_source():
    return STATSMODELS_ARIMA_SOURCE


@pytest.fixture
def statsmodels_ets_source():
    return STATSMODELS_ETS_SOURCE


@pytest.fixture
def sklearn_source():
    return SKLEARN_SOURCE


@pytest.fixture
def synthetic_csv(tmp_path):
    """A small CSV with date + value + group columns suitable for transform_data."""
    rng = np.random.default_rng(42)
    n = 60
    rows = []
    for group in ["A", "B"]:
        for i in range(n):
            rows.append(
                {
                    "date": (pd.Timestamp("2026-01-01") + pd.Timedelta(days=i)).strftime(
                        "%Y-%m-%d"
                    ),
                    "sales": float(100 + i + rng.normal(0, 1)),
                    "store": group,
                }
            )
    df = pd.DataFrame(rows)
    p = tmp_path / "sales.csv"
    df.to_csv(p, index=False)
    return str(p)


@pytest.fixture
def csv_with_nans(tmp_path):
    """A small CSV with some NaN values in the target column."""
    df = pd.DataFrame(
        {
            "ds": pd.date_range("2026-01-01", periods=20, freq="D"),
            "y": [1.0, 2.0, np.nan, 4.0, 5.0] * 4,
        }
    )
    p = tmp_path / "with_nans.csv"
    df.to_csv(p, index=False)
    return str(p)
