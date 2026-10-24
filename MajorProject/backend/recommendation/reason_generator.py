"""Generate supported recommendation reasons."""

from recommendation.feature_extractor import PromptFeatures
from recommendation.scorer import ScoredModel
from recommendation.weight_normalizer import MetricWeights, weights_to_dict


def generate_reasons(
    top_model: ScoredModel,
    all_models: list[ScoredModel],
    *,
    weights: MetricWeights | None = None,
    features: PromptFeatures | None = None,
) -> list[str]:
    """Return 1-4 reason strings supported by the dataset metrics."""
    if not all_models:
        return []

    using_dgmes = top_model.dgmes is not None and weights is not None
    score_label = "DGMES" if using_dgmes else "GMES"
    reasons: list[str] = [f"Highest overall {score_label}"]

    max_speed = max(model.speed for model in all_models)
    max_latency = max(model.latency for model in all_models)
    max_context = max(model.context for model in all_models)
    max_cost_efficiency = max(model.cost_efficiency for model in all_models)

    if top_model.speed >= max_speed:
        reasons.append("Fastest response")

    if top_model.latency >= max_latency:
        reasons.append("Lowest latency")

    if top_model.context >= max_context:
        reasons.append("Large context window")

    if top_model.cost_efficiency >= max_cost_efficiency:
        reasons.append("Most cost-efficient option")

    if using_dgmes and weights is not None:
        weight_map = weights_to_dict(weights)
        dominant = max(weight_map.items(), key=lambda item: item[1])
        metric_label = {
            "speed": "speed",
            "latency": "latency",
            "context": "context",
            "cost_efficiency": "cost",
        }[dominant[0]]
        reasons.append(
            f"Prompt-weighted for {metric_label} "
            f"(w={dominant[1]:.2f})"
        )

        if features is not None and features.urgency:
            reasons.append("Low-latency fit for urgency keywords detected")

        if features is not None and features.cost_sensitive:
            reasons.append("Cost weight elevated for budget-sensitive prompt")

    return reasons[:4]
