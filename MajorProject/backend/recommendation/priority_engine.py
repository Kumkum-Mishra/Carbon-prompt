"""Convert prompt features into metric priorities."""

from __future__ import annotations

from dataclasses import dataclass

from recommendation.config import (
    CONTEXT_PRIORITY_FLOOR,
    COST_PRIORITY_HIGH,
    COST_PRIORITY_LOW,
    COST_PRIORITY_MEDIUM,
    COST_SENSITIVITY_BOOST,
    LATENCY_PRIORITY_HIGH,
    LATENCY_PRIORITY_LOW,
    SPEED_PRIORITY_HIGH,
    SPEED_PRIORITY_LOW,
    SPEED_PRIORITY_MEDIUM,
    T_CONTEXT_REF,
    T_OUT_SPEED_HIGH,
    T_OUT_SPEED_LOW,
    T_TOTAL_COST_HIGH,
    T_TOTAL_COST_LOW,
)
from recommendation.feature_extractor import PromptFeatures


@dataclass(frozen=True)
class MetricPriorities:
    speed: float
    latency: float
    context: float
    cost_efficiency: float


def compute_priorities(features: PromptFeatures) -> MetricPriorities:
    """Compute non-negative priorities for each scoring dimension."""
    context = max(
        CONTEXT_PRIORITY_FLOOR,
        min(1.0, features.input_tokens / T_CONTEXT_REF),
    )

    if features.expected_output_tokens < T_OUT_SPEED_LOW:
        speed = SPEED_PRIORITY_LOW
    elif features.expected_output_tokens <= T_OUT_SPEED_HIGH:
        speed = SPEED_PRIORITY_MEDIUM
    else:
        speed = SPEED_PRIORITY_HIGH

    latency = LATENCY_PRIORITY_HIGH if features.urgency else LATENCY_PRIORITY_LOW

    if features.total_tokens < T_TOTAL_COST_LOW:
        cost = COST_PRIORITY_LOW
    elif features.total_tokens <= T_TOTAL_COST_HIGH:
        cost = COST_PRIORITY_MEDIUM
    else:
        cost = COST_PRIORITY_HIGH

    if features.cost_sensitive:
        cost = min(1.0, cost + COST_SENSITIVITY_BOOST)

    return MetricPriorities(
        speed=speed,
        latency=latency,
        context=context,
        cost_efficiency=cost,
    )


def priorities_to_dict(priorities: MetricPriorities) -> dict[str, float]:
    return {
        "speed": round(priorities.speed, 4),
        "latency": round(priorities.latency, 4),
        "context": round(priorities.context, 4),
        "cost_efficiency": round(priorities.cost_efficiency, 4),
    }
