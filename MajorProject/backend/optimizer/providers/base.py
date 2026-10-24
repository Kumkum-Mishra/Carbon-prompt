"""Abstract base class for LLM optimization providers."""

from abc import ABC, abstractmethod


class LLMProviderError(Exception):
    """Base exception for LLM provider failures."""


class LLMProviderUnavailableError(LLMProviderError):
    """Raised when the LLM provider cannot be reached or is not configured."""


class LLMTimeoutError(LLMProviderError):
    """Raised when an LLM optimization request times out."""


class LLMOptimizationError(LLMProviderError):
    """Raised when optimization fails or returns an invalid response."""


class BaseLLMProvider(ABC):
    """Abstract interface for prompt optimization LLM backends."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider identifier."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier used for optimization."""

    @abstractmethod
    def optimize(self, prompt: str, system_prompt: str) -> str:
        """Return an optimized version of the given prompt."""

    def optimize_candidates(
        self,
        prompt: str,
        system_prompt: str,
        num_candidates: int = 5,
    ) -> list[str]:
        """Return one or more optimized candidates.

        Providers that only support a single output can rely on this default.
        Trained/local providers can override it to return beam candidates.
        """
        return [self.optimize(prompt, system_prompt)]
