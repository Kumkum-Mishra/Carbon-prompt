"""Cost Efficiency, GMES, and DGMES calculations."""

from dataclasses import dataclass

from recommendation.config import (
    COST_EFFICIENCY_DECIMAL_PLACES,
    DGMES_DECIMAL_PLACES,
    GMES_DECIMAL_PLACES,
)
from recommendation.weight_normalizer import MetricWeights


@dataclass(frozen=True)
class ScoredModel:
    model: str
    speed: float
    latency: float
    context: float
    input_cost: float
    output_cost: float
    cost_efficiency: float
    gmes: float
    dgmes: float | None = None


def calculate_cost_efficiency(input_cost: float, output_cost: float) -> float:
    """Calculate cost efficiency from normalized cost scores."""
    average_cost = (input_cost + output_cost) / 2
    return round(100 - average_cost, COST_EFFICIENCY_DECIMAL_PLACES)


def calculate_gmes(
    speed: float,
    latency: float,
    context: float,
    cost_efficiency: float,
) -> float:
    """Calculate the Green Model Efficiency Score."""
    return round(
        (speed + latency + context + cost_efficiency) / 4,
        GMES_DECIMAL_PLACES,
    )


def calculate_dgmes(
    speed: float,
    latency: float,
    context: float,
    cost_efficiency: float,
    weights: MetricWeights,
) -> float:
    """Calculate the Dynamic Green Model Efficiency Score."""
    return round(
        (weights.speed * speed)
        + (weights.latency * latency)
        + (weights.context * context)
        + (weights.cost_efficiency * cost_efficiency),
        DGMES_DECIMAL_PLACES,
    )


def score_model(
    *,
    model: str,
    speed: float,
    latency: float,
    context: float,
    input_cost: float,
    output_cost: float,
) -> ScoredModel:
    """Score a single model with Cost Efficiency and GMES."""
    cost_efficiency = calculate_cost_efficiency(input_cost, output_cost)
    gmes = calculate_gmes(speed, latency, context, cost_efficiency)
    return ScoredModel(
        model=model,
        speed=speed,
        latency=latency,
        context=context,
        input_cost=input_cost,
        output_cost=output_cost,
        cost_efficiency=cost_efficiency,
        gmes=gmes,
    )


def apply_dynamic_scoring(
    models: list[ScoredModel],
    weights: MetricWeights,
) -> list[ScoredModel]:
    """Attach DGMES to each model without changing base metrics."""
    return [
        ScoredModel(
            model=model.model,
            speed=model.speed,
            latency=model.latency,
            context=model.context,
            input_cost=model.input_cost,
            output_cost=model.output_cost,
            cost_efficiency=model.cost_efficiency,
            gmes=model.gmes,
            dgmes=calculate_dgmes(
                model.speed,
                model.latency,
                model.context,
                model.cost_efficiency,
                weights,
            ),
        )
        for model in models
    ]
