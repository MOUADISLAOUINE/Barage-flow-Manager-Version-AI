"""
ml/optimizer.py — Allocation Optimization (NSGA-II)

AI Job 4: When there is not enough water for everyone, find the
          fairest and most economically efficient split.

Algorithm: NSGA-II (Non-dominated Sorting Genetic Algorithm II)
           — multi-objective evolutionary algorithm (via DEAP library)

Objectives being balanced simultaneously:
  1. Fairness: minimise deviation from proportional contract shares
  2. Economic value: maximise total harvest value preserved
  3. Safety: maximise probability of reservoir staying above threshold

Output:
  Pareto-optimal allocation table with suggested volumes per cooperative
  and reasons for any reductions vs their contract.

TODO: Implement full DEAP NSGA-II integration.
      See: https://deap.readthedocs.io/en/master/examples/nsga2.html
"""
from dataclasses import dataclass
from typing import List


@dataclass
class CoopOptInput:
    coop_id: int
    name: str
    contracted_volume_m3: float
    priority_class: str          # "A", "B", or "C"
    crop_drought_sensitivity: float  # 0–1, higher = crops die faster
    economic_value_per_m3: float     # MAD (Moroccan Dirham) per m³


@dataclass
class OptimizedAllocation:
    coop_id: int
    name: str
    recommended_volume_m3: float
    reason: str
    fairness_score: float
    economic_preservation_score: float


class AllocationOptimizer:
    """
    NSGA-II based multi-objective optimizer for water allocation.
    Used when available water is insufficient for all contracted volumes.
    """

    def __init__(self, population_size: int = 100, generations: int = 200):
        self.population_size = population_size
        self.generations = generations

    def optimize(
        self,
        cooperatives: List[CoopOptInput],
        available_volume_m3: float,
        safety_threshold_m3: float,
    ) -> List[OptimizedAllocation]:
        """
        Run NSGA-II optimization and return the recommended allocation.
        TODO: Replace stub with full DEAP NSGA-II implementation.
        """
        # Stub: proportional fallback until NSGA-II is implemented
        total_contracted = sum(c.contracted_volume_m3 for c in cooperatives)
        results = []

        for coop in cooperatives:
            if total_contracted > 0:
                share = (coop.contracted_volume_m3 / total_contracted) * available_volume_m3
            else:
                share = 0.0

            results.append(OptimizedAllocation(
                coop_id=coop.coop_id,
                name=coop.name,
                recommended_volume_m3=round(share, 2),
                reason="Proportional allocation (NSGA-II optimization pending implementation).",
                fairness_score=1.0,
                economic_preservation_score=1.0,
            ))

        return results
