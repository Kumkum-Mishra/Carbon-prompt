"""Rule-based prompt optimizer with constraint injection."""

from optimizer.constraint_rules import (
    build_constraint_candidates,
    optimize_with_constraints,
)
from optimizer.providers.base import BaseLLMProvider


class RuleBasedProvider(BaseLLMProvider):
    """Deterministic optimizer: strip fillers and add output constraints.

    Open-ended prompts like "explain AI" become constrained prompts such as
    "Explain AI. Answer in at most 40 words. Use simple language..." so
    downstream models emit far fewer tokens.
    """

    @property
    def provider_name(self) -> str:
        return "rule_based"

    @property
    def model_name(self) -> str:
        return "rule-based-constraints"

    def optimize(self, prompt: str, system_prompt: str) -> str:
        del system_prompt  # unused — fully deterministic rules
        return optimize_with_constraints(prompt)

    def optimize_candidates(
        self,
        prompt: str,
        system_prompt: str,
        num_candidates: int = 5,
    ) -> list[str]:
        del system_prompt
        return build_constraint_candidates(prompt, num_candidates=num_candidates)
