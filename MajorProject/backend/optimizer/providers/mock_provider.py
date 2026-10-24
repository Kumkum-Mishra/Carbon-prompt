"""Mock LLM provider for testing."""

from optimizer.providers.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """Returns a predefined optimized prompt for deterministic tests."""

    def __init__(
        self,
        optimized_prompt: str | None = None,
        *,
        raise_error: Exception | None = None,
    ) -> None:
        self._optimized_prompt = optimized_prompt
        self._raise_error = raise_error

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return "mock"

    def optimize(self, prompt: str, system_prompt: str) -> str:
        if self._raise_error is not None:
            raise self._raise_error
        if self._optimized_prompt is not None:
            return self._optimized_prompt
        return prompt.strip()
