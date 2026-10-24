"""Unit tests for DGMES scoring and dynamic ranking."""

from recommendation.ranking import rank_models
from recommendation.scorer import (
    apply_dynamic_scoring,
    calculate_dgmes,
    score_model,
)
from recommendation.weight_normalizer import MetricWeights


class TestDynamicScoring:
    def test_dgmes_formula(self) -> None:
      weights = MetricWeights(
          speed=0.1803,
          latency=0.3279,
          context=0.1639,
          cost_efficiency=0.3279,
      )
      dgmes = calculate_dgmes(95, 92, 40, 90, weights)
      assert abs(dgmes - 83.37) < 0.02

    def test_ranking_changes_with_weights(self) -> None:
      fast_cheap = score_model(
          model="FastCheap",
          speed=95,
          latency=92,
          context=40,
          input_cost=10,
          output_cost=10,
      )
      big_context = score_model(
          model="BigContext",
          speed=60,
          latency=70,
          context=98,
          input_cost=55,
          output_cost=55,
      )
      balanced = score_model(
          model="Balanced",
          speed=75,
          latency=75,
          context=98,
          input_cost=20,
          output_cost=20,
      )

      gmes_ranked = rank_models([fast_cheap, big_context, balanced], top_n=3)
      assert gmes_ranked[0].model == "Balanced"

      weights = MetricWeights(
          speed=0.1803,
          latency=0.3279,
          context=0.1639,
          cost_efficiency=0.3279,
      )
      dgmes_ranked = rank_models(
          [fast_cheap, big_context, balanced],
          top_n=3,
          weights=weights,
      )
      assert dgmes_ranked[0].model == "FastCheap"
      assert dgmes_ranked[0].dgmes is not None
      assert dgmes_ranked[0].dgmes > dgmes_ranked[1].dgmes

    def test_apply_dynamic_scoring_preserves_base_metrics(self) -> None:
      model = score_model(
          model="A",
          speed=90,
          latency=88,
          context=100,
          input_cost=80,
          output_cost=82,
      )
      weights = MetricWeights(0.25, 0.25, 0.25, 0.25)
      scored = apply_dynamic_scoring([model], weights)[0]
      assert scored.speed == model.speed
      assert scored.gmes == model.gmes
      assert scored.dgmes == model.gmes
