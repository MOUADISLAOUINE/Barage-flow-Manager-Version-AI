"""
ml/anomaly.py — Sensor Anomaly Detection

AI Job 2: Detect unusual sensor readings and raise alerts.

Algorithms:
  - Isolation Forest: detects statistical outliers in sensor data
  - LSTM Autoencoder: learns normal patterns; flags deviations

Alert severity: LOW | MEDIUM | HIGH | CRITICAL
Probable causes: SENSOR_FAULT | PHYSICAL_EVENT | DATA_QUALITY_ISSUE

Examples that should trigger alerts:
  - Water level drops 1.5m in 2 hours with no approved release order
  - Flow sensor reads exactly 0.00 for 6+ consecutive hours
  - Rain gauge reports outlier value far outside historical range
"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class AlertSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AnomalyCause(str, Enum):
    SENSOR_FAULT = "SENSOR_FAULT"
    PHYSICAL_EVENT = "PHYSICAL_EVENT"
    DATA_QUALITY_ISSUE = "DATA_QUALITY_ISSUE"
    UNKNOWN = "UNKNOWN"


@dataclass
class AnomalyAlert:
    sensor_id: int
    severity: AlertSeverity
    probable_cause: AnomalyCause
    description: str
    recommended_action: str
    detected_value: float
    expected_range: tuple


class SensorAnomalyDetector:
    """
    Isolation Forest + LSTM Autoencoder anomaly detector.
    Call .fit() on historical readings, then .detect() on new readings.
    """

    def __init__(self, contamination: float = 0.01):
        self.contamination = contamination  # Expected fraction of outliers
        self.isolation_forest = None
        self.lstm_autoencoder = None
        self.is_fitted = False

    def fit(self, historical_readings: List[float]):
        """
        Train the anomaly detection models on normal historical data.
        TODO: Implement using sklearn IsolationForest and TF/Keras LSTM Autoencoder.
        """
        self.is_fitted = True

    def detect(
        self,
        sensor_id: int,
        recent_values: List[float],
        sensor_type: str,
    ) -> Optional[AnomalyAlert]:
        """
        Evaluate recent readings and return an AnomalyAlert if detected.
        Returns None if readings look normal.
        TODO: Replace stub logic with real model inference.
        """
        if not self.is_fitted:
            raise RuntimeError("Detector not fitted. Call .fit() first.")

        # Stub: check for exact-zero flow (simple rule-based example)
        if sensor_type == "FLOW" and len(recent_values) >= 6:
            if all(v == 0.0 for v in recent_values[-6:]):
                return AnomalyAlert(
                    sensor_id=sensor_id,
                    severity=AlertSeverity.HIGH,
                    probable_cause=AnomalyCause.SENSOR_FAULT,
                    description="Flow sensor has read exactly 0.00 for 6+ consecutive readings.",
                    recommended_action="Physically inspect sensor and verify gate status.",
                    detected_value=0.0,
                    expected_range=(0.5, 100.0),
                )

        # TODO: Add Isolation Forest and LSTM Autoencoder inference
        return None
