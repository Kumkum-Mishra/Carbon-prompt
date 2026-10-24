"""OpenAI LLM provider for prompt optimization."""

import httpx

from optimizer.config import DEFAULT_MODELS, LLM_MODEL, LLM_TIMEOUT_SECONDS, OPENAI_API_KEY
from optimizer.providers.base import (
    BaseLLMProvider,
    LLMOptimizationError,
    LLMProviderUnavailableError,
    LLMTimeoutError,
)


class OpenAIProvider(BaseLLMProvider):
    """Optimize prompts using the OpenAI Chat Completions API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = LLM_TIMEOUT_SECONDS,
    ) -> None:
        self._api_key = api_key if api_key is not None else OPENAI_API_KEY
        self._model = model or LLM_MODEL or DEFAULT_MODELS["openai"]
        self._timeout = timeout

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return self._model

    def optimize(self, prompt: str, system_prompt: str) -> str:
        if not self._api_key:
            raise LLMProviderUnavailableError("LLM provider unavailable.")

        try:
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self._model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
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
            content = response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMOptimizationError("Optimization failed.") from exc

        optimized = str(content).strip()
        if not optimized:
            raise LLMOptimizationError("Optimization failed.")
        return optimized
