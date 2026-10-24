"""Tests for prompt optimization candidate ranking."""

from analyzer.schemas import AnalysisResult
from carbon.schemas import CarbonResult
from optimizer.ranking_engine import (
    grammar_score,
    preserves_constraints,
    rank_candidate,
    semantic_similarity,
)


def analysis(prompt: str, tokens: int) -> AnalysisResult:
    return AnalysisResult(
        prompt=prompt,
        prompt_type="Zero-shot",
        task_type="Question Answering",
        category="Question Answering",
        token_count=tokens,
        character_count=len(prompt),
        word_count=len(prompt.split()),
    )


def carbon(tokens: int) -> CarbonResult:
    return CarbonResult(
        token_count=tokens,
        prompt_type="Zero-shot",
        task_type="Question Answering",
        prompt_weight=1.0,
        task_weight=1.0,
        scaling_constant=0.00001,
        green_carbon_score=round(tokens * 0.00001, 6),
    )


class TestRankingEngine:
    def test_semantic_similarity_accepts_compact_rewrite(self) -> None:
        original = "Can you please explain Artificial Intelligence in detail?"
        candidate = "Explain Artificial Intelligence in detail."
        assert semantic_similarity(original, candidate) >= 0.55

    def test_constraints_preserve_numbers_and_quotes(self) -> None:
        original = 'Summarize "Attention Is All You Need" in 3 points.'
        assert preserves_constraints(
            original,
            'Summarize "Attention Is All You Need" in 3 bullet points.',
        )
        assert not preserves_constraints(original, "Summarize the paper.")

    def test_grammar_score_penalizes_rough_output(self) -> None:
        assert grammar_score("Explain AI.") > grammar_score("explain  AI")

    def test_rank_candidate_prefers_short_same_meaning_candidate(self) -> None:
        original = analysis(
            "Can you please explain Artificial Intelligence in detail?",
            tokens=16,
        )
        candidate = analysis("Explain Artificial Intelligence in detail.", tokens=7)

        ranked = rank_candidate(
            original_analysis=original,
            original_carbon=carbon(16),
            candidate_analysis=candidate,
            candidate_carbon=carbon(7),
        )

        assert ranked is not None
        assert ranked.prompt == candidate.prompt
        assert ranked.token_reduction_percent > 0
        assert ranked.carbon_reduction_percent > 0

    def test_rank_candidate_rejects_meaning_drift(self) -> None:
        original = analysis("Explain Artificial Intelligence in detail.", tokens=8)
        candidate = analysis("Write a poem about flowers.", tokens=6)

        ranked = rank_candidate(
            original_analysis=original,
            original_carbon=carbon(8),
            candidate_analysis=candidate,
            candidate_carbon=carbon(6),
        )

        assert ranked is None
