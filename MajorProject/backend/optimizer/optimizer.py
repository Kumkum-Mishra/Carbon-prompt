"""Prompt optimization via configurable LLM providers."""

import logging
import re

from optimizer.config import (
    ENABLE_CONSTRAINT_RULES,
    LLM_MAX_RETRIES,
    SYSTEM_PROMPT_PATH,
)
from optimizer.llm_provider import get_llm_provider
from optimizer.providers.base import (
    BaseLLMProvider,
    LLMOptimizationError,
    LLMProviderError,
    LLMProviderUnavailableError,
    LLMTimeoutError,
)

logger = logging.getLogger(__name__)


class OptimizationFailedError(Exception):
    """Raised when prompt optimization cannot be completed."""


class PromptOptimizer:
    """Coordinates LLM-based prompt optimization."""

    def __init__(self, provider: BaseLLMProvider | None = None) -> None:
        self._provider = provider or get_llm_provider()

    @property
    def provider_name(self) -> str:
        return self._provider.provider_name

    @property
    def model_name(self) -> str:
        return self._provider.model_name

    def optimize(self, prompt: str) -> str:
        """Return an optimized version of the prompt."""
        candidates = self.optimize_candidates(prompt, num_candidates=1)
        if not candidates:
            raise OptimizationFailedError("Optimization failed.")
        return candidates[0]

    def optimize_candidates(self, prompt: str, num_candidates: int = 5) -> list[str]:
        """Return optimized candidate prompts from the configured provider.

        When constraint rules are enabled and the primary provider is not already
        rule-based, also merges rule-based constraint candidates (and constrained
        versions of model outputs) into the pool for ranking.
        """
        system_prompt = self._load_system_prompt()
        last_error: Exception | None = None

        for attempt in range(LLM_MAX_RETRIES + 1):
            try:
                candidates = self._provider.optimize_candidates(
                    prompt,
                    system_prompt,
                    num_candidates=num_candidates,
                )
                cleaned = [
                    " ".join(candidate.strip().split())
                    for candidate in candidates
                    if candidate and candidate.strip()
                ]
                deduped = list(dict.fromkeys(cleaned))
                if not deduped:
                    raise OptimizationFailedError("Optimization failed.")
                return self._merge_constraint_candidates(
                    prompt,
                    deduped,
                    num_candidates=num_candidates,
                )
            except LLMTimeoutError:
                raise
            except LLMProviderUnavailableError as exc:
                # Fall back to rule-based when trained_model/torch is unavailable.
                if self._provider.provider_name != "rule_based":
                    logger.warning(
                        "Primary provider unavailable (%s); falling back to rule_based",
                        exc,
                    )
                    self._provider = get_llm_provider("rule_based")
                    continue
                raise
            except LLMOptimizationError as exc:
                last_error = exc
                logger.warning("Optimization attempt %d failed: %s", attempt + 1, exc)
            except LLMProviderError as exc:
                last_error = exc
                logger.warning("Provider error on attempt %d: %s", attempt + 1, exc)

        raise OptimizationFailedError(
            str(last_error) if last_error else "Optimization failed."
        )

    def _merge_constraint_candidates(
        self,
        prompt: str,
        provider_candidates: list[str],
        *,
        num_candidates: int,
    ) -> list[str]:
        """Add rule-based constraint variants without replacing the primary provider."""
        if not ENABLE_CONSTRAINT_RULES:
            return provider_candidates
        if self._provider.provider_name == "rule_based":
            return provider_candidates

        from optimizer.constraint_rules import (
            build_constraint_candidates,
            optimize_with_constraints,
        )

        original_norm = " ".join(prompt.split()).strip()
        original_compact = re.sub(r"[?\s]+$", "", original_norm).lower()

        # Prefer model rewrites that actually change content; drop near-identical
        # FLAN no-ops (punctuation-only) so they do not crowd out constraints.
        merged: list[str] = []
        for candidate in provider_candidates:
            compact = re.sub(r"[?\s]+$", "", candidate).lower()
            if compact == original_compact:
                continue
            merged.append(candidate)
        if not merged:
            merged = list(provider_candidates)

        # Constrain each model/provider candidate (FLAN cleanup + output bounds).
        for candidate in provider_candidates:
            constrained = optimize_with_constraints(candidate)
            if (
                constrained
                and constrained not in merged
                and constrained != original_norm
            ):
                merged.append(constrained)

        # Also add rule-based candidates from the original prompt.
        # Never re-inject the untouched original — ranking would prefer it
        # (similarity=1) over shorter model rewrites.
        for rule_candidate in build_constraint_candidates(
            prompt,
            num_candidates=max(num_candidates, 3),
        ):
            if (
                rule_candidate
                and rule_candidate not in merged
                and rule_candidate != original_norm
            ):
                merged.append(rule_candidate)

        return merged

    def _load_system_prompt(self) -> str:
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
