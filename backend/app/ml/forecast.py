"""
ml/forecast.py — Water Level Forecasting

AI Job 1: LSTM + SARIMA ensemble forecast for next 180 days.

Inputs:
  - Historical water levels (20+ years)
  - Rainfall data
  - Temperature (evaporation proxy)
  - Historical release records
  - Season

Output:
  - List of {date, predicted_pct, lower_bound, upper_bound} for 180 days
  - MAE score vs holdout test set

Algorithms:
  - LSTM neural network (primary) — learns temporal patterns
  - SARIMA ensemble (secondary) — classical seasonal decomposition
  - Final prediction = weighted average of both models

Target accuracy: MAE < 3% of dam capacity.
"""
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict


class WaterLevelForecaster:
    """
    Wrapper for the LSTM + SARIMA ensemble model.
    Call .train() once on historical data, then .predict() for 180-day forecast.
    """

    MODEL_VERSION = "1.0.0-lstm-sarima"

    def __init__(self):
        self.lstm_model = None
        self.sarima_model = None
        self.scaler = None
        self.is_trained = False

    def train(self, historical_levels: List[float], rainfall: List[float], temps: List[float]):
        """
        Train the LSTM and SARIMA models on historical data.
        TODO: Implement using TensorFlow/Keras LSTM and statsmodels SARIMA.
        """
        # Placeholder — replace with real training logic
        self.is_trained = True

    def predict(self, horizon_days: int = 180) -> List[Dict]:
        """
        Generate a forecast for the next `horizon_days` days.
        Returns a list of dicts with keys:
          date, predicted_pct, lower_bound_pct, upper_bound_pct
        TODO: Replace stub with real model inference.
        """
        if not self.is_trained:
            raise RuntimeError("Model has not been trained. Call .train() first.")

        # Stub: returns a flat forecast — replace with real predictions
        today = datetime.utcnow().date()
        results = []
        for i in range(horizon_days):
            day = today + timedelta(days=i)
            predicted = 50.0  # TODO: replace with model output
            results.append({
                "date": day.isoformat(),
                "predicted_pct": predicted,
                "lower_bound_pct": predicted - 5.0,
                "upper_bound_pct": predicted + 5.0,
            })
        return results

    def evaluate(self, actual_levels: List[float], predicted_levels: List[float]) -> float:
        """Compute Mean Absolute Error as percentage of capacity."""
        errors = [abs(a - p) for a, p in zip(actual_levels, predicted_levels)]
        return float(np.mean(errors))
