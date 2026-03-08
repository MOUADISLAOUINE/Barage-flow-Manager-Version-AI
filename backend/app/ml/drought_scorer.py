"""
ml/drought_scorer.py — Drought Severity Index (DSI)

AI Job 3: Compute weekly composite drought risk score (0.0 to 1.0)

Component weights:
  - Current fill level:               35%
  - Rainfall vs historical average:   30%
  - Inflow vs outflow rate:           20%
  - 6-month forecast trend:           15%

Score interpretation:
  < 0.30  → GREEN  — Normal
  0.30–0.50 → YELLOW — Monitor, start conservation
  0.50–0.75 → ORANGE — Reduce allocations, alert coops
  > 0.75  → RED    — Activate emergency protocol
"""


class DroughtScorer:

    FILL_WEIGHT = 0.35
    RAINFALL_WEIGHT = 0.30
    FLOW_RATIO_WEIGHT = 0.20
    FORECAST_TREND_WEIGHT = 0.15

    def compute(
        self,
        current_fill_pct: float,
        rainfall_vs_avg_ratio: float,   # e.g. 0.7 = 30% below average
        inflow_outflow_ratio: float,     # e.g. 0.8 = outflow > inflow
        forecast_trend: float,           # e.g. -0.05 = declining forecast
    ) -> float:
        """
        Compute the Drought Severity Index (DSI).
        All inputs are normalised 0–1 where 1 = most severe.
        Returns composite score 0.0 (no risk) to 1.0 (maximum risk).
        """
        fill_score = max(0.0, 1.0 - (current_fill_pct / 100.0))
        rainfall_score = max(0.0, 1.0 - rainfall_vs_avg_ratio)
        flow_score = max(0.0, 1.0 - inflow_outflow_ratio)
        trend_score = max(0.0, min(1.0, -forecast_trend + 0.5))

        dsi = (
            fill_score * self.FILL_WEIGHT
            + rainfall_score * self.RAINFALL_WEIGHT
            + flow_score * self.FLOW_RATIO_WEIGHT
            + trend_score * self.FORECAST_TREND_WEIGHT
        )
        return round(min(1.0, max(0.0, dsi)), 3)

    @staticmethod
    def interpret(score: float) -> dict:
        if score < 0.30:
            return {"level": "GREEN", "label": "Normal", "action": "Proceed normally."}
        elif score < 0.50:
            return {"level": "YELLOW", "label": "Monitor", "action": "Start conservation measures."}
        elif score < 0.75:
            return {"level": "ORANGE", "label": "Alert", "action": "Reduce allocations. Alert cooperatives."}
        else:
            return {"level": "RED", "label": "Emergency", "action": "Activate emergency protocol immediately."}
