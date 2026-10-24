"""Google Gemini LLM provider for prompt optimization."""

import httpx

from optimizer.config import DEFAULT_MODELS, GEMINI_API_KEY, LLM_MODEL, LLM_TIMEOUT_SECONDS
from optimizer.providers.base import (
    BaseLLMProvider,
    LLMOptimizationError,
    LLMProviderUnavailableError,
    LLMTimeoutError,
)


class GeminiProvider(BaseLLMProvider):
    """Optimize prompts using the Google Gemini API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = LLM_TIMEOUT_SECONDS,
    ) -> None:
        self._api_key = api_key if api_key is not None else GEMINI_API_KEY
        self._model = model or LLM_MODEL or DEFAULT_MODELS["gemini"]
        self._timeout = timeout

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return self._model

    def optimize(self, prompt: str, system_prompt: str) -> str:
        if not self._api_key:
            raise LLMProviderUnavailableError("LLM provider unavailable.")

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._model}:generateContent"
        )

        try:
            response = httpx.post(
                url,
                params={"key": self._api_key},
                json={
                    "systemInstruction": {"parts": [{"text": system_prompt}]},
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.2},
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
            content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMOptimizationError("Optimization failed.") from exc

        optimized = str(content).strip()
        if not optimized:
            raise LLMOptimizationError("Optimization failed.")
        return optimized
