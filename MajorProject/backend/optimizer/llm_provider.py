"""LLM provider selection and initialization."""

from optimizer.config import LLM_PROVIDER
from optimizer.providers.anthropic_provider import AnthropicProvider
from optimizer.providers.base import BaseLLMProvider
from optimizer.providers.gemini_provider import GeminiProvider
from optimizer.providers.mock_provider import MockLLMProvider
from optimizer.providers.openai_provider import OpenAIProvider
from optimizer.providers.rule_based_provider import RuleBasedProvider
from optimizer.providers.trained_model_provider import TrainedModelProvider

_PROVIDER_REGISTRY: dict[str, type[BaseLLMProvider]] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "trained_model": TrainedModelProvider,
    "rule_based": RuleBasedProvider,
    "mock": MockLLMProvider,
}


def get_llm_provider(provider_name: str | None = None) -> BaseLLMProvider:
    """Instantiate the configured LLM provider."""
    name = (provider_name or LLM_PROVIDER).lower()
    provider_class = _PROVIDER_REGISTRY.get(name)
    if provider_class is None:
        raise ValueError(f"Unsupported LLM provider: {name}")
    return provider_class()


def get_supported_providers() -> list[str]:
    """Return the list of supported provider identifiers."""
    return list(_PROVIDER_REGISTRY.keys())
