"""Unit tests for metric priority calculation."""

from recommendation.feature_extractor import PromptFeatures
from recommendation.priority_engine import compute_priorities


class TestPriorityEngine:
    def test_long_context_prompt(self) -> None:
        features = PromptFeatures(
            task_type="Summarization",
            input_tokens=40000,
            expected_output_tokens=250,
            total_tokens=40250,
            urgency=True,
            cost_sensitive=True,
            detail_level="medium",
        )
        priorities = compute_priorities(features)
        assert priorities.context == 0.5
        assert priorities.latency == 1.0
        assert priorities.cost_efficiency == 1.0
        assert priorities.speed == 0.55

    def test_tiny_prompt(self) -> None:
        features = PromptFeatures(
            task_type="Question Answering",
            input_tokens=20,
            expected_output_tokens=80,
            total_tokens=100,
            urgency=False,
            cost_sensitive=False,
            detail_level="medium",
        )
        priorities = compute_priorities(features)
        assert priorities.context == 0.05
        assert priorities.latency == 0.30
        assert priorities.cost_efficiency == 0.20
