"""
tests/unit/test_allocation_service.py

Tests for Rule 2 — The Fair Share Formula
and Rule 3 — Drought Alert Escalation.
"""
import pytest
from app.services.allocation_service import (
    calculate_fair_share,
    CoopInput,
    AllocationResult,
)
from app.models.cooperative import PriorityClass
from app.models.dam import WaterZone


def make_coops():
    return [
        CoopInput(coop_id=1, name="Ajdal",       priority_class=PriorityClass.A, contracted_volume_m3=620_000),
        CoopInput(coop_id=2, name="Tafraout",    priority_class=PriorityClass.B, contracted_volume_m3=450_000),
        CoopInput(coop_id=3, name="Souss Vert",  priority_class=PriorityClass.C, contracted_volume_m3=280_000),
    ]


class TestFairShareFormula:

    def test_normal_zone_allocations_sum_to_available(self):
        coops = make_coops()
        available = 1_000_000.0
        results = calculate_fair_share(coops, available, WaterZone.NORMAL)
        total = sum(r.allocated_volume_m3 for r in results)
        assert abs(total - available) < 1.0, f"Expected sum={available}, got {total}"

    def test_class_a_gets_more_than_class_b(self):
        coops = make_coops()
        results = calculate_fair_share(coops, 1_000_000.0, WaterZone.NORMAL)
        by_id = {r.coop_id: r for r in results}
        assert by_id[1].allocated_volume_m3 > by_id[2].allocated_volume_m3

    def test_class_c_suspended_in_warning_zone(self):
        coops = make_coops()
        results = calculate_fair_share(coops, 1_000_000.0, WaterZone.WARNING)
        by_id = {r.coop_id: r for r in results}
        assert by_id[3].allocated_volume_m3 == 0.0, "Class C should get zero in WARNING zone"

    def test_alert_zone_applies_10_percent_reduction(self):
        coops = make_coops()
        available = 1_000_000.0
        results = calculate_fair_share(coops, available, WaterZone.ALERT)
        total = sum(r.allocated_volume_m3 for r in results)
        expected_total = available * 0.90  # 10% reduction
        assert abs(total - expected_total) < 1.0

    def test_warning_zone_applies_30_percent_reduction(self):
        coops = make_coops()
        available = 1_000_000.0
        results = calculate_fair_share(coops, available, WaterZone.WARNING)
        # Class C gets 0, A+B get 70% of available
        total = sum(r.allocated_volume_m3 for r in results)
        expected_total = available * 0.70
        assert abs(total - expected_total) < 1.0

    def test_zero_available_gives_zero_allocations(self):
        coops = make_coops()
        results = calculate_fair_share(coops, 0.0, WaterZone.NORMAL)
        for r in results:
            assert r.allocated_volume_m3 == 0.0


class TestDamZoneCalculation:

    def test_zone_normal(self):
        from app.services.dam_service import calculate_zone
        from unittest.mock import MagicMock
        dam = MagicMock()
        dam.safety_reserve_pct = 25.0
        assert calculate_zone(70.0, dam) == WaterZone.NORMAL

    def test_zone_alert(self):
        from app.services.dam_service import calculate_zone
        from unittest.mock import MagicMock
        dam = MagicMock()
        dam.safety_reserve_pct = 25.0
        assert calculate_zone(50.0, dam) == WaterZone.ALERT

    def test_zone_warning(self):
        from app.services.dam_service import calculate_zone
        from unittest.mock import MagicMock
        dam = MagicMock()
        dam.safety_reserve_pct = 25.0
        assert calculate_zone(30.0, dam) == WaterZone.WARNING

    def test_zone_critical(self):
        from app.services.dam_service import calculate_zone
        from unittest.mock import MagicMock
        dam = MagicMock()
        dam.safety_reserve_pct = 25.0
        assert calculate_zone(24.0, dam) == WaterZone.CRITICAL

    def test_safety_lock_blocked_at_critical(self):
        from app.services.dam_service import can_submit_release_order
        from unittest.mock import MagicMock
        dam = MagicMock()
        dam.safety_lock_active = True
        dam.current_zone = WaterZone.CRITICAL
        allowed, _ = can_submit_release_order(dam)
        assert allowed is False


class TestDroughtScorer:

    def test_green_score(self):
        from app.ml.drought_scorer import DroughtScorer
        scorer = DroughtScorer()
        score = scorer.compute(
            current_fill_pct=75.0,
            rainfall_vs_avg_ratio=1.1,
            inflow_outflow_ratio=1.2,
            forecast_trend=0.02,
        )
        assert score < 0.30

    def test_red_score(self):
        from app.ml.drought_scorer import DroughtScorer
        scorer = DroughtScorer()
        score = scorer.compute(
            current_fill_pct=15.0,
            rainfall_vs_avg_ratio=0.3,
            inflow_outflow_ratio=0.4,
            forecast_trend=-0.15,
        )
        assert score > 0.75
