"""Extract prompt features for dynamic recommendation weighting."""

from __future__ import annotations

import re
from dataclasses import dataclass

from recommendation.config import (
    DETAIL_HIGH_KEYWORDS,
    DETAIL_LOW_KEYWORDS,
    TASK_OUTPUT_BASE_TOKENS,
    TOKENS_PER_WORD,
    T_OUT_MAX,
    T_OUT_MIN,
)

_URGENCY_PATTERN = re.compile(
    r"\b("
    r"quick(?:ly)?|fast|immediately|urgent|asap|"
    r"real[\s-]?time|low[\s-]?latency|right[\s-]?now"
    r")\b",
    re.IGNORECASE,
)

_COST_SENSITIVE_PATTERN = re.compile(
    r"\b("
    r"cheap|low[\s-]?cost|inexpensive|budget|efficient|"
    r"cost[\s-]?effective|affordable"
    r")\b",
    re.IGNORECASE,
)

_WORD_COUNT_PATTERN = re.compile(
    r"\b(\d{1,6})\s*[-\s]?(?:word|words)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class PromptFeatures:
    task_type: str
    input_tokens: int
    expected_output_tokens: int
    total_tokens: int
    urgency: bool
    cost_sensitive: bool
    detail_level: str  # low | medium | high


def extract_prompt_features(
    *,
    prompt: str,
    task_type: str,
    input_tokens: int,
) -> PromptFeatures:
    """Derive recommendation features from prompt text and analyzer metadata."""
    detail_level = _detect_detail_level(prompt)
    expected_output_tokens = _estimate_output_tokens(
        prompt=prompt,
        task_type=task_type,
        detail_level=detail_level,
    )
    return PromptFeatures(
        task_type=task_type,
        input_tokens=max(0, input_tokens),
        expected_output_tokens=expected_output_tokens,
        total_tokens=max(0, input_tokens) + expected_output_tokens,
        urgency=bool(_URGENCY_PATTERN.search(prompt)),
        cost_sensitive=bool(_COST_SENSITIVE_PATTERN.search(prompt)),
        detail_level=detail_level,
    )


def _detect_detail_level(prompt: str) -> str:
    lowered = prompt.lower()
    if any(keyword in lowered for keyword in DETAIL_HIGH_KEYWORDS):
        return "high"
    if any(keyword in lowered for keyword in DETAIL_LOW_KEYWORDS):
        return "low"
    return "medium"


def _estimate_output_tokens(
    *,
    prompt: str,
    task_type: str,
    detail_level: str,
) -> int:
    explicit_words = _WORD_COUNT_PATTERN.search(prompt)
    if explicit_words:
        words = int(explicit_words.group(1))
        return int(max(T_OUT_MIN, min(T_OUT_MAX, round(words * TOKENS_PER_WORD))))

    base = TASK_OUTPUT_BASE_TOKENS.get(task_type, TASK_OUTPUT_BASE_TOKENS["General"])
    multiplier = {"low": 0.6, "medium": 1.0, "high": 2.0}[detail_level]
    return int(max(T_OUT_MIN, min(T_OUT_MAX, round(base * multiplier))))


def features_to_dict(features: PromptFeatures) -> dict[str, int | bool | str]:
    return {
        "input_tokens": features.input_tokens,
        "expected_output_tokens": features.expected_output_tokens,
        "total_tokens": features.total_tokens,
        "urgency": features.urgency,
        "cost_sensitive": features.cost_sensitive,
        "detail_level": features.detail_level,
    }
