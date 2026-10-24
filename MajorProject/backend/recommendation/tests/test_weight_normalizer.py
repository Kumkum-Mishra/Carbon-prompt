"""Unit tests for weight normalization."""

from recommendation.priority_engine import MetricPriorities
from recommendation.weight_normalizer import equal_weights, normalize_weights


class TestWeightNormalizer:
    def test_weights_sum_to_one(self) -> None:
        priorities = MetricPriorities(
            speed=0.55,
            latency=1.0,
            context=0.5,
            cost_efficiency=1.0,
        )
        weights = normalize_weights(priorities)
        total = (
            weights.speed
            + weights.latency
            + weights.context
            + weights.cost_efficiency
        )
        assert abs(total - 1.0) < 1e-9

    def test_prd_example_weights(self) -> None:
        priorities = MetricPriorities(
            speed=0.55,
            latency=1.0,
            context=0.5,
            cost_efficiency=1.0,
        )
        weights = normalize_weights(priorities)
        assert round(weights.speed, 4) == 0.1803
        assert round(weights.latency, 4) == 0.3279
        assert round(weights.context, 4) == 0.1639
        assert round(weights.cost_efficiency, 4) == 0.3279

    def test_equal_weights(self) -> None:
        weights = equal_weights()
        assert weights.speed == 0.25
        assert weights.latency == 0.25
