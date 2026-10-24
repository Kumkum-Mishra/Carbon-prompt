"""Unit tests for Cost Efficiency and GMES calculations."""

from recommendation.scorer import (
    calculate_cost_efficiency,
    calculate_gmes,
    score_model,
)


class TestScorer:
    def test_cost_efficiency_prd_example(self) -> None:
        assert calculate_cost_efficiency(80, 70) == 25.0

    def test_gmes_gpt5_example(self) -> None:
        gmes = calculate_gmes(90, 88, 100, 19)
        assert gmes == 74.25

    def test_gmes_gemini_example(self) -> None:
        gmes = calculate_gmes(95, 94, 96, 29)
        assert gmes == 78.5

    def test_score_model(self) -> None:
        scored = score_model(
            model="GPT-5",
            speed=90,
            latency=88,
            context=100,
            input_cost=80,
            output_cost=82,
        )
        assert scored.cost_efficiency == 19.0
        assert scored.gmes == 74.25

    def test_gemini_scores_higher_than_gpt5(self) -> None:
        gpt5 = score_model(
            model="GPT-5",
            speed=90,
            latency=88,
            context=100,
            input_cost=80,
            output_cost=82,
        )
        gemini = score_model(
            model="Gemini Pro",
            speed=95,
            latency=94,
            context=96,
            input_cost=70,
            output_cost=72,
        )
        assert gemini.gmes > gpt5.gmes
