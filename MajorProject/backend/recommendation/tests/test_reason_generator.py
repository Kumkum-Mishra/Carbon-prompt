"""Unit tests for recommendation reason generation."""

from recommendation.reason_generator import generate_reasons
from recommendation.scorer import score_model


class TestReasonGenerator:
    def test_highest_gmes_always_included(self) -> None:
        top = score_model(
            model="Top",
            speed=90,
            latency=90,
            context=90,
            input_cost=50,
            output_cost=50,
        )
        others = [
            score_model(
                model="Other",
                speed=80,
                latency=80,
                context=80,
                input_cost=60,
                output_cost=60,
            )
        ]
        reasons = generate_reasons(top, [top, *others])
        assert "Highest overall GMES" in reasons

    def test_fastest_response_reason(self) -> None:
        top = score_model(
            model="Fast",
            speed=100,
            latency=50,
            context=50,
            input_cost=50,
            output_cost=50,
        )
        other = score_model(
            model="Slow",
            speed=50,
            latency=50,
            context=50,
            input_cost=50,
            output_cost=50,
        )
        reasons = generate_reasons(top, [top, other])
        assert "Fastest response" in reasons

    def test_cost_efficient_reason(self) -> None:
        top = score_model(
            model="Cheap",
            speed=40,
            latency=40,
            context=40,
            input_cost=10,
            output_cost=10,
        )
        other = score_model(
            model="Expensive",
            speed=90,
            latency=90,
            context=90,
            input_cost=90,
            output_cost=90,
        )
        reasons = generate_reasons(top, [top, other])
        assert "Most cost-efficient option" in reasons

    def test_max_four_reasons(self) -> None:
        top = score_model(
            model="Best",
            speed=100,
            latency=100,
            context=100,
            input_cost=0,
            output_cost=0,
        )
        reasons = generate_reasons(top, [top])
        assert len(reasons) <= 4
