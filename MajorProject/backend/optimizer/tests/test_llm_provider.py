"""Unit tests for LLM provider selection and behavior."""

import pytest

from optimizer.llm_provider import get_llm_provider, get_supported_providers
from optimizer.optimizer import OptimizationFailedError, PromptOptimizer
from optimizer.providers.base import (
    LLMOptimizationError,
    LLMProviderUnavailableError,
    LLMTimeoutError,
)
from optimizer.providers.mock_provider import MockLLMProvider
from optimizer.providers.openai_provider import OpenAIProvider
from optimizer.providers.rule_based_provider import RuleBasedProvider


class TestLLMProvider:
    def test_supported_providers(self) -> None:
        providers = get_supported_providers()
        assert "openai" in providers
        assert "anthropic" in providers
        assert "gemini" in providers
        assert "rule_based" in providers
        assert "mock" in providers

    def test_get_rule_based_provider(self) -> None:
        provider = get_llm_provider("rule_based")
        assert isinstance(provider, RuleBasedProvider)

    def test_openai_without_api_key(self) -> None:
        provider = OpenAIProvider(api_key="")
        with pytest.raises(LLMProviderUnavailableError):
            provider.optimize("test prompt", "system prompt")

    def test_mock_provider_returns_configured_text(self) -> None:
        provider = MockLLMProvider(
            optimized_prompt="Explain artificial intelligence with examples."
        )
        result = provider.optimize("long prompt", "system")
        assert result == "Explain artificial intelligence with examples."

    def test_rule_based_removes_filler(self) -> None:
        provider = RuleBasedProvider()
        result = provider.optimize(
            "Can you please explain artificial intelligence in great detail?",
            "system",
        )
        assert "please" not in result.lower()
        assert "artificial intelligence" in result.lower()

    def test_rule_based_adds_output_constraints(self) -> None:
        provider = RuleBasedProvider()
        result = provider.optimize("Explain AI", "system")
        assert "explain" in result.lower()
        assert "ai" in result.lower()
        # Open-ended explain prompts must gain a length or simplicity bound.
        assert any(
            marker in result.lower()
            for marker in ("word", "simple", "fluff", "core idea")
        )

    def test_optimizer_uses_mock_provider(self) -> None:
        optimizer = PromptOptimizer(
            provider=MockLLMProvider(optimized_prompt="Explain AI.")
        )
        assert optimizer.optimize("Can you please explain AI in detail?") == "Explain AI."

    def test_optimizer_rejects_empty_response(self) -> None:
        optimizer = PromptOptimizer(provider=MockLLMProvider(optimized_prompt="   "))
        with pytest.raises(OptimizationFailedError, match="Optimization failed."):
            optimizer.optimize("test prompt")

    def test_optimizer_propagates_timeout(self) -> None:
        optimizer = PromptOptimizer(
            provider=MockLLMProvider(raise_error=LLMTimeoutError("Optimization timed out."))
        )
        with pytest.raises(LLMTimeoutError):
            optimizer.optimize("test prompt")

    def test_optimizer_propagates_unavailable(self) -> None:
        optimizer = PromptOptimizer(
            provider=MockLLMProvider(
                raise_error=LLMProviderUnavailableError("LLM provider unavailable.")
            )
        )
        with pytest.raises(LLMProviderUnavailableError):
            optimizer.optimize("test prompt")

    def test_optimizer_retries_on_optimization_error(self) -> None:
        call_count = 0

        class FlakyProvider(MockLLMProvider):
            def optimize(self, prompt: str, system_prompt: str) -> str:
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise LLMOptimizationError("temporary failure")
                return "Optimized prompt text."

        optimizer = PromptOptimizer(provider=FlakyProvider())
        result = optimizer.optimize("test prompt")
        assert result == "Optimized prompt text."
        assert call_count == 2
