"""Unit tests for model ranking."""

from recommendation.ranking import rank_models
from recommendation.scorer import score_model


class TestRanking:
    def test_rank_by_gmes_descending(self) -> None:
        models = [
            score_model(
                model="A",
                speed=70,
                latency=70,
                context=70,
                input_cost=50,
                output_cost=50,
            ),
            score_model(
                model="B",
                speed=95,
                latency=95,
                context=95,
                input_cost=50,
                output_cost=50,
            ),
            score_model(
                model="C",
                speed=80,
                latency=80,
                context=80,
                input_cost=50,
                output_cost=50,
            ),
        ]
        ranked = rank_models(models, top_n=3)
        assert [model.model for model in ranked] == ["B", "C", "A"]

    def test_top_n_limit(self) -> None:
        models = [
            score_model(
                model=f"M{i}",
                speed=float(i),
                latency=float(i),
                context=float(i),
                input_cost=50,
                output_cost=50,
            )
            for i in range(10)
        ]
        ranked = rank_models(models, top_n=3)
        assert len(ranked) == 3

    def test_tie_break_by_cost_efficiency(self) -> None:
        models = [
            score_model(
                model="Beta",
                speed=80,
                latency=80,
                context=80,
                input_cost=60,
                output_cost=60,
            ),
            score_model(
                model="Alpha",
                speed=80,
                latency=80,
                context=80,
                input_cost=40,
                output_cost=40,
            ),
        ]
        ranked = rank_models(models, top_n=2)
        assert ranked[0].model == "Alpha"

    def test_tie_break_alphabetical(self) -> None:
        models = [
            score_model(
                model="Zeta",
                speed=50,
                latency=50,
                context=50,
                input_cost=50,
                output_cost=50,
            ),
            score_model(
                model="Alpha",
                speed=50,
                latency=50,
                context=50,
                input_cost=50,
                output_cost=50,
            ),
        ]
        ranked = rank_models(models, top_n=2)
        assert ranked[0].model == "Alpha"
