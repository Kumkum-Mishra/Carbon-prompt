"""Anthropic LLM provider for prompt optimization."""

import httpx

from optimizer.config import (
    ANTHROPIC_API_KEY,
    DEFAULT_MODELS,
    LLM_MODEL,
    LLM_TIMEOUT_SECONDS,
)
from optimizer.providers.base import (
    BaseLLMProvider,
    LLMOptimizationError,
    LLMProviderUnavailableError,
    LLMTimeoutError,
)


class AnthropicProvider(BaseLLMProvider):
    """Optimize prompts using the Anthropic Messages API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = LLM_TIMEOUT_SECONDS,
    ) -> None:
        self._api_key = api_key if api_key is not None else ANTHROPIC_API_KEY
        self._model = model or LLM_MODEL or DEFAULT_MODELS["anthropic"]
        self._timeout = timeout

    @property
    def provider_name(self) -> str:
        return "anthropic"

    @property
    def model_name(self) -> str:
        return self._model

    def optimize(self, prompt: str, system_prompt: str) -> str:
        if not self._api_key:
            raise LLMProviderUnavailableError("LLM provider unavailable.")

        try:
            response = httpx.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self._api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self._model,
                    "max_tokens": 1024,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=self._timeout,
            )
        except httpx.TimeoutException as exc:
            raise LLMTimeoutError("Optimization timed out.") from exc
        except httpx.HTTPError as exc:
            raise LLMProviderUnavailableError("LLM provider unavailable.") from exc

        if response.status_code >= 400:
            raise LLMProviderUnavailableError("LLM provider unavailable.")

        try:
            content = response.json()["content"][0]["text"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMOptimizationError("Optimization failed.") from exc

        optimized = str(content).strip()
        if not optimized:
            raise LLMOptimizationError("Optimization failed.")
        return optimized
