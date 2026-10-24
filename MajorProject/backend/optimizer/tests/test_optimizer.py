"""Unit tests for PromptOptimizer."""

import pytest

from optimizer.optimizer import OptimizationFailedError, PromptOptimizer
from optimizer.providers.mock_provider import MockLLMProvider
from optimizer.providers.rule_based_provider import RuleBasedProvider


class TestOptimizer:
    def test_short_prompt_optimization(self) -> None:
        optimizer = PromptOptimizer(
            provider=MockLLMProvider(optimized_prompt="Explain AI.")
        )
        result = optimizer.optimize("Can you please explain AI in detail?")
        assert result == "Explain AI."

    def test_long_prompt_optimization(self) -> None:
        long_prompt = (
            "Can you please explain artificial intelligence in great detail with "
            "lots of examples and also discuss its applications in different industries?"
        )
        optimized = (
            "Explain artificial intelligence with examples and its applications "
            "across industries."
        )
        optimizer = PromptOptimizer(provider=MockLLMProvider(optimized_prompt=optimized))
        result = optimizer.optimize(long_prompt)
        assert result == optimized

    def test_trims_whitespace_from_llm_response(self) -> None:
        optimizer = PromptOptimizer(
            provider=MockLLMProvider(optimized_prompt="  Explain AI.  ")
        )
        assert optimizer.optimize("Explain AI in detail.") == "Explain AI."

    def test_empty_response_raises(self) -> None:
        optimizer = PromptOptimizer(provider=MockLLMProvider(optimized_prompt=""))
        with pytest.raises(OptimizationFailedError):
            optimizer.optimize("test")

    def test_merges_rule_constraints_with_provider_candidates(self) -> None:
        optimizer = PromptOptimizer(
            provider=MockLLMProvider(optimized_prompt="Explain artificial intelligence.")
        )
        candidates = optimizer.optimize_candidates(
            "Explain artificial intelligence",
            num_candidates=3,
        )
        assert candidates[0] == "Explain artificial intelligence."
        assert len(candidates) > 1
        assert any("word" in c.lower() or "simple" in c.lower() for c in candidates)

    def test_skips_constraint_merge_for_rule_based_provider(self) -> None:
        optimizer = PromptOptimizer(provider=RuleBasedProvider())
        prompt = "Explain AI"
        candidates = optimizer.optimize_candidates(prompt, num_candidates=3)
        # Same as provider-only output — no double-merge explosion.
        provider_only = RuleBasedProvider().optimize_candidates(prompt, "", 3)
        assert candidates == provider_only
