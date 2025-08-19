"""Machine learning forecast utilities v0.1.0 (2025-08-19)"""
from pathlib import Path
from typing import Sequence

import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

__version__ = "0.1.0"

MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_DIR.mkdir(exist_ok=True)


def forecast_prices(symbol: str, history: Sequence[float]) -> float:
    """Forecast the next price for *symbol* based on *history* of prices.

    A simple RandomForestRegressor is trained per symbol and cached under
    ``strategy-engine/models``. If insufficient history is provided, the latest
    price is returned.
    """
    prices = list(history)
    if len(prices) < 2:
        return float(prices[-1]) if prices else 0.0

    model_path = MODEL_DIR / f"{symbol}_rf.joblib"
    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)

    if model_path.exists():
        model = joblib.load(model_path)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        joblib.dump(model, model_path)

    next_index = np.array([[len(prices)]])
    return float(model.predict(next_index)[0])
