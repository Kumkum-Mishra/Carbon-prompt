"""Unit tests for optimization service orchestration."""

import pytest

from analyzer.analyzer import PromptAnalyzer
from carbon.carbon_service import CarbonService
from optimizer.optimization_service import OptimizationService
from optimizer.optimizer import PromptOptimizer
from optimizer.providers.base import LLMProviderUnavailableError, LLMTimeoutError
from optimizer.providers.mock_provider import MockLLMProvider


@pytest.fixture
def service() -> OptimizationService:
    return OptimizationService(
        optimizer=PromptOptimizer(
            provider=MockLLMProvider(
                optimized_prompt=(
                    "Explain artificial intelligence with examples and its "
                    "applications across industries."
                )
            )
        )
    )


class TestOptimizationService:
    def test_complete_optimization_flow(self, service: OptimizationService) -> None:
        prompt = (
            "Can you please explain artificial intelligence in great detail with "
            "lots of examples and also discuss its applications in different industries?"
        )
        result = service.optimize_prompt(prompt)
        assert result.success is True
        assert result.optimization.original_prompt == prompt
        assert result.optimization.optimized_tokens > 0
        # Either shorter prompt OR constraints added (may raise input tokens).
        reduced = (
            result.optimization.original_tokens > result.optimization.optimized_tokens
        )
        constrained = any(
            marker in result.optimization.optimized_prompt.lower()
            for marker in ("word", "bullet", "simple", "fluff", "core idea")
        )
        assert reduced or constrained
        assert result.optimization.original_carbon_score > 0
        assert result.optimization.optimized_carbon_score > 0

    def test_coding_prompt(self) -> None:
        service = OptimizationService(
            optimizer=PromptOptimizer(
                provider=MockLLMProvider(
                    optimized_prompt="Write Python code to implement a CNN using PyTorch."
                )
            )
        )
        result = service.optimize_prompt(
            "Can you please write Python code to implement a CNN using PyTorch for me?"
        )
        assert result.success is True
        assert result.optimization.original_task_type == "Coding"

    def test_writing_prompt(self) -> None:
        service = OptimizationService(
            optimizer=PromptOptimizer(
                provider=MockLLMProvider(
                    optimized_prompt="Write a blog post about sustainable commuting."
                )
            )
        )
        result = service.optimize_prompt(
            "Please write a detailed blog post about sustainable commuting options."
        )
        assert result.success is True
        assert result.optimization.original_task_type == "Writing"

    def test_translation_prompt(self) -> None:
        service = OptimizationService(
            optimizer=PromptOptimizer(
                provider=MockLLMProvider(
                    optimized_prompt="Translate this paragraph into Hindi."
                )
            )
        )
        result = service.optimize_prompt(
            "Can you please translate this paragraph into Hindi for me?"
        )
        assert result.success is True
        assert result.optimization.original_task_type == "Translation"

    def test_llm_timeout(self) -> None:
        service = OptimizationService(
            optimizer=PromptOptimizer(
                provider=MockLLMProvider(
                    raise_error=LLMTimeoutError("Optimization timed out.")
                )
            )
        )
        result = service.optimize_prompt("Explain AI in detail.")
        assert result.success is False
        assert result.message == "Optimization timed out."

    def test_llm_unavailable(self) -> None:
        service = OptimizationService(
            optimizer=PromptOptimizer(
                provider=MockLLMProvider(
                    raise_error=LLMProviderUnavailableError("LLM provider unavailable.")
                )
            )
        )
        result = service.optimize_prompt("Explain AI in detail.")
        assert result.success is False
        assert result.message == "LLM provider unavailable."

    def test_llm_optimization_failed(self) -> None:
        service = OptimizationService(
            optimizer=PromptOptimizer(provider=MockLLMProvider(optimized_prompt=""))
        )
        result = service.optimize_prompt("Explain AI in detail.")
        assert result.success is False
        assert result.message == "Optimization failed."

    def test_pipeline_with_real_analyzer_and_carbon(self) -> None:
        analyzer = PromptAnalyzer()
        carbon = CarbonService(analyzer=analyzer)
        service = OptimizationService(
            analyzer=analyzer,
            carbon_service=carbon,
            optimizer=PromptOptimizer(
                provider=MockLLMProvider(optimized_prompt="Explain AI.")
            ),
        )
        result = service.optimize_prompt("Can you please explain AI in great detail?")
        assert result.success is True
        opt = result.optimization.optimized_prompt.lower()
        reduced = (
            result.optimization.original_tokens > result.optimization.optimized_tokens
        )
        constrained = any(m in opt for m in ("word", "bullet", "simple", "fluff"))
        assert reduced or constrained
