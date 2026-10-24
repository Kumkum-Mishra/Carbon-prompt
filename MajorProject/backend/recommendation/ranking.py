"""Model ranking by GMES or DGMES with tie-breaking rules."""

from recommendation.config import TOP_N_MODELS
from recommendation.scorer import ScoredModel
from recommendation.weight_normalizer import MetricWeights


def _effective_score(model: ScoredModel) -> float:
    return model.dgmes if model.dgmes is not None else model.gmes


def rank_models(
    models: list[ScoredModel],
    top_n: int = TOP_N_MODELS,
    *,
    weights: MetricWeights | None = None,
) -> list[ScoredModel]:
    """Sort models by GMES or DGMES descending and return the top N."""
    if weights is not None:
        from recommendation.scorer import apply_dynamic_scoring

        models = apply_dynamic_scoring(models, weights)

    sorted_models = sorted(
        models,
        key=lambda model: (
            -_effective_score(model),
            -model.cost_efficiency,
            -model.speed,
            -model.context,
            model.model.lower(),
        ),
    )
    return sorted_models[:top_n]
