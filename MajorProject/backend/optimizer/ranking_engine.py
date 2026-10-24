"""Candidate filtering and ranking for prompt optimization."""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher

from analyzer.schemas import AnalysisResult
from carbon.schemas import CarbonResult
from optimizer.config import SEMANTIC_SIMILARITY_THRESHOLD
from optimizer.constraint_rules import constraint_density
from optimizer.reduction import (
    calculate_carbon_reduction_percent,
    calculate_token_reduction_percent,
)


@dataclass(frozen=True)
class RankedCandidate:
    prompt: str
    analysis: AnalysisResult
    carbon: CarbonResult
    semantic_similarity: float
    readability_score: float
    token_reduction_percent: float
    carbon_reduction_percent: float
    score: float


def normalize_words(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


STOPWORDS = {
    "a",
    "an",
    "and",
    "also",
    "as",
    "can",
    "could",
    "for",
    "in",
    "is",
    "me",
    "of",
    "please",
    "the",
    "to",
    "you",
    "your",
}


def semantic_similarity(original: str, candidate: str) -> float:
    """Lightweight local semantic proxy based on word-order overlap."""
    original_words = normalize_words(original)
    candidate_words = normalize_words(candidate)
    if not original_words and not candidate_words:
        return 1.0
    if not original_words or not candidate_words:
        return 0.0

    sequence_score = SequenceMatcher(
        None,
        original_words,
        candidate_words,
        autojunk=False,
    ).ratio()
    original_set = set(original_words)
    candidate_set = set(candidate_words)
    jaccard = len(original_set & candidate_set) / max(
        len(original_set | candidate_set),
        1,
    )

    original_content = {word for word in original_words if word not in STOPWORDS}
    candidate_content = {word for word in candidate_words if word not in STOPWORDS}
    overlap = original_content & candidate_content
    # How much of the original meaning is retained in the candidate.
    original_coverage = len(overlap) / max(len(original_content), 1)
    # How much of the candidate is grounded in the original (favors shortening).
    candidate_coverage = len(overlap) / max(len(candidate_content), 1)

    # SequenceMatcher preserves phrasing/order; Jaccard and coverage protect
    # key concepts. original_coverage allows constraint *injection* (slightly
    # longer prompts) while candidate_coverage still favors concise rewrites.
    score = max(
        (sequence_score * 0.65) + (jaccard * 0.35),
        original_coverage * 0.92,
        candidate_coverage * 0.6,
    )
    return round(score, 4)


def preserves_constraints(original: str, candidate: str) -> bool:
    """Ensure explicit numbers and quoted terms are preserved."""
    original_numbers = set(re.findall(r"\b\d+(?:\.\d+)?\b", original))
    candidate_numbers = set(re.findall(r"\b\d+(?:\.\d+)?\b", candidate))
    if not original_numbers.issubset(candidate_numbers):
        return False

    quoted = re.findall(r"['\"]([^'\"]+)['\"]", original)
    candidate_lower = candidate.lower()
    return all(term.lower() in candidate_lower for term in quoted)


def grammar_score(text: str) -> float:
    """Small grammar/readability heuristic for generated candidates."""
    cleaned = text.strip()
    if not cleaned:
        return 0.0

    score = 1.0
    if cleaned[0].islower():
        score -= 0.15
    if cleaned[-1] not in ".?!":
        score -= 0.1
    if re.search(r"\s{2,}", cleaned):
        score -= 0.15
    if len(normalize_words(cleaned)) < 2:
        score -= 0.25
    return round(max(score, 0.0), 4)


def rank_candidate(
    *,
    original_analysis: AnalysisResult,
    original_carbon: CarbonResult,
    candidate_analysis: AnalysisResult,
    candidate_carbon: CarbonResult,
) -> RankedCandidate | None:
    """Filter invalid candidates and compute a weighted ranking score."""
    candidate = candidate_analysis.prompt
    similarity = semantic_similarity(original_analysis.prompt, candidate)
    if similarity < SEMANTIC_SIMILARITY_THRESHOLD:
        return None
    if not preserves_constraints(original_analysis.prompt, candidate):
        return None

    token_reduction = calculate_token_reduction_percent(
        original_analysis.token_count,
        candidate_analysis.token_count,
    )
    carbon_reduction = calculate_carbon_reduction_percent(
        original_carbon.green_carbon_score,
        candidate_carbon.green_carbon_score,
    )
    readability = grammar_score(candidate)

    token_component = max(min(token_reduction / 100, 1.0), -0.5)
    carbon_component = max(min(carbon_reduction / 100, 1.0), -0.5)
    task_penalty = (
        0.12
        if original_analysis.task_type != candidate_analysis.task_type
        else 0.0
    )
    prompt_type_penalty = (
        0.04
        if original_analysis.prompt_type != candidate_analysis.prompt_type
        else 0.0
    )

    # Prefer prompts that add output constraints (word caps, bullets, etc.).
    # A slightly longer prompt that bounds downstream tokens is a net win.
    original_constraint_density = constraint_density(original_analysis.prompt)
    candidate_constraint_density = constraint_density(candidate)
    constraint_gain = max(
        candidate_constraint_density - original_constraint_density,
        0.0,
    )
    # Soften / nearly ignore prompt-token growth when we added output bounds.
    # Downstream reply length dominates carbon; input tokens rising slightly is fine.
    if constraint_gain > 0 and token_component < 0:
        token_component *= 0.1

    # Strong preference: unconstrained open-ended prompts must pick a constrained rewrite.
    if original_constraint_density < 0.05 and constraint_gain > 0:
        constraint_bonus = 0.30 + (constraint_gain * 0.25)
    else:
        constraint_bonus = constraint_gain * 0.18

    # Penalize no-op rewrites (same meaning, no constraints) so FLAN identity
    # copies do not beat real constraint injection.
    noop_penalty = 0.0
    if (
        constraint_gain == 0
        and similarity >= 0.95
        and abs(token_reduction) < 8
    ):
        noop_penalty = 0.18

    score = (
        (similarity * 0.35)
        + (token_component * 0.12)
        + (readability * 0.10)
        + (carbon_component * 0.08)
        + constraint_bonus
        - task_penalty
        - prompt_type_penalty
        - noop_penalty
    )

    return RankedCandidate(
        prompt=candidate,
        analysis=candidate_analysis,
        carbon=candidate_carbon,
        semantic_similarity=similarity,
        readability_score=readability,
        token_reduction_percent=token_reduction,
        carbon_reduction_percent=carbon_reduction,
        score=round(score, 4),
    )
