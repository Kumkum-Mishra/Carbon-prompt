"""Normalize metric priorities into weights that sum to 1."""

from __future__ import annotations

from dataclasses import dataclass

from recommendation.priority_engine import MetricPriorities


@dataclass(frozen=True)
class MetricWeights:
    speed: float
    latency: float
    context: float
    cost_efficiency: float


def normalize_weights(priorities: MetricPriorities) -> MetricWeights:
    """Convert priorities into normalized weights (sum = 1)."""
    total = (
        priorities.speed
        + priorities.latency
        + priorities.context
        + priorities.cost_efficiency
    )
    if total <= 0:
        return equal_weights()

    return MetricWeights(
        speed=priorities.speed / total,
        latency=priorities.latency / total,
        context=priorities.context / total,
        cost_efficiency=priorities.cost_efficiency / total,
    )


def equal_weights() -> MetricWeights:
    """Return equal 0.25 weights for each metric (GMES baseline)."""
    return MetricWeights(
        speed=0.25,
        latency=0.25,
        context=0.25,
        cost_efficiency=0.25,
    )


def weights_to_dict(weights: MetricWeights) -> dict[str, float]:
    return {
        "speed": round(weights.speed, 4),
        "latency": round(weights.latency, 4),
        "context": round(weights.context, 4),
        "cost_efficiency": round(weights.cost_efficiency, 4),
    }
