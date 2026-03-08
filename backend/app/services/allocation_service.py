"""
services/allocation_service.py

Implements Rule 2 — The Fair Share Formula:
    cooperative_allocation = Priority Weight × Contract Share × Available Volume

Weights: Class A = 1.5 | Class B = 1.0 | Class C = 0.6
All shares sum to exactly the available volume.
"""
from dataclasses import dataclass
from typing import List

from app.config import settings
from app.models.cooperative import PriorityClass
from app.models.dam import WaterZone


PRIORITY_WEIGHTS = {
    PriorityClass.A: settings.PRIORITY_WEIGHT_CLASS_A,  # 1.5
    PriorityClass.B: settings.PRIORITY_WEIGHT_CLASS_B,  # 1.0
    PriorityClass.C: settings.PRIORITY_WEIGHT_CLASS_C,  # 0.6
}

# Zone-based allocation reduction rules (Rule 3)
ZONE_REDUCTION = {
    WaterZone.NORMAL: 0.0,
    WaterZone.ALERT: settings.ALERT_ZONE_REDUCTION,      # 10%
    WaterZone.WARNING: settings.WARNING_ZONE_REDUCTION,  # 30%
    WaterZone.CRITICAL: 1.0,                             # 100% blocked
}


@dataclass
class CoopInput:
    coop_id: int
    name: str
    priority_class: PriorityClass
    contracted_volume_m3: float
    suspended: bool = False


@dataclass
class AllocationResult:
    coop_id: int
    name: str
    contracted_volume_m3: float
    allocated_volume_m3: float
    reduction_reason: str


def calculate_fair_share(
    cooperatives: List[CoopInput],
    available_volume_m3: float,
    current_zone: WaterZone,
) -> List[AllocationResult]:
    """
    Distribute available_volume_m3 fairly across all cooperatives.

    Steps:
    1. Apply zone-based reduction to determine total distributable volume.
    2. Suspend Class C cooperatives in WARNING zone per Rule 3.
    3. Apply the Fair Share Formula.
    4. Verify all shares sum to exactly the distributable volume.
    """
    reduction_factor = ZONE_REDUCTION[current_zone]
    distributable_volume = available_volume_m3 * (1.0 - reduction_factor)

    results: List[AllocationResult] = []
    eligible = []

    for coop in cooperatives:
        # Rule 3: Class C suspended in WARNING or CRITICAL
        if coop.priority_class == PriorityClass.C and current_zone in (
            WaterZone.WARNING, WaterZone.CRITICAL
        ):
            results.append(AllocationResult(
                coop_id=coop.coop_id,
                name=coop.name,
                contracted_volume_m3=coop.contracted_volume_m3,
                allocated_volume_m3=0.0,
                reduction_reason=f"Suspended — {current_zone} zone: Class C allocations halted.",
            ))
        elif coop.suspended:
            results.append(AllocationResult(
                coop_id=coop.coop_id,
                name=coop.name,
                contracted_volume_m3=coop.contracted_volume_m3,
                allocated_volume_m3=0.0,
                reduction_reason="Contract suspended.",
            ))
        else:
            eligible.append(coop)

    if not eligible or distributable_volume <= 0:
        return results

    # Weighted contract shares
    weight_map = {c.coop_id: PRIORITY_WEIGHTS[c.priority_class] for c in eligible}
    total_weighted_contracts = sum(
        weight_map[c.coop_id] * c.contracted_volume_m3 for c in eligible
    )

    for coop in eligible:
        if total_weighted_contracts == 0:
            share = 0.0
        else:
            weighted_share = weight_map[coop.coop_id] * coop.contracted_volume_m3
            share = (weighted_share / total_weighted_contracts) * distributable_volume

        reduction_reason = "Full allocation." if reduction_factor == 0 else (
            f"Reduced {int(reduction_factor * 100)}% — {current_zone} zone."
        )
        results.append(AllocationResult(
            coop_id=coop.coop_id,
            name=coop.name,
            contracted_volume_m3=coop.contracted_volume_m3,
            allocated_volume_m3=round(share, 2),
            reduction_reason=reduction_reason,
        ))

    # Verify total (floating point safety check)
    total_allocated = sum(r.allocated_volume_m3 for r in results)
    assert abs(total_allocated - distributable_volume) < 1.0, (
        f"Allocation sum mismatch: {total_allocated} != {distributable_volume}"
    )

    return results
