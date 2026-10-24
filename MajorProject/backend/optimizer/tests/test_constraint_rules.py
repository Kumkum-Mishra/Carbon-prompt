"""Unit tests for constraint-focused rule-based optimization."""

from optimizer.constraint_rules import (
    ConstraintKind,
    apply_constraints,
    build_constraint_candidates,
    clean_fillers,
    constraint_density,
    detect_existing_constraints,
    detect_intent,
    optimize_with_constraints,
    plan_constraints,
)
from optimizer.providers.rule_based_provider import RuleBasedProvider
from optimizer.ranking_engine import semantic_similarity


class TestConstraintDetection:
    def test_detects_word_limit(self) -> None:
        found = detect_existing_constraints("Explain AI in 50 words.")
        assert ConstraintKind.WORD_LIMIT in found

    def test_detects_at_most_word_limit(self) -> None:
        found = detect_existing_constraints("Explain AI. Answer in at most 40 words.")
        assert ConstraintKind.WORD_LIMIT in found

    def test_detects_simplicity(self) -> None:
        found = detect_existing_constraints("Explain gravity in simple language.")
        assert ConstraintKind.SIMPLICITY in found

    def test_detects_bullet_limit(self) -> None:
        found = detect_existing_constraints("List the top 5 benefits of solar power.")
        assert ConstraintKind.BULLET_LIMIT in found

    def test_open_prompt_has_no_constraints(self) -> None:
        found = detect_existing_constraints("Explain artificial intelligence")
        assert found == set()


class TestIntentAndCleaning:
    def test_explain_intent(self) -> None:
        assert detect_intent("Explain machine learning") == "explain"

    def test_code_intent(self) -> None:
        assert detect_intent("Write a Python function to sort a list") == "code"

    def test_strips_politeness_fillers(self) -> None:
        cleaned = clean_fillers(
            "Can you please explain artificial intelligence in great detail?"
        )
        assert "please" not in cleaned.lower()
        assert "great detail" not in cleaned.lower()
        assert "artificial intelligence" in cleaned.lower()


class TestConstraintPlanning:
    def test_open_explain_gets_word_and_simplicity(self) -> None:
        plan = plan_constraints("Explain AI")
        kinds = {c.kind for c in plan.constraints}
        assert ConstraintKind.WORD_LIMIT in kinds
        assert ConstraintKind.SIMPLICITY in kinds
        assert plan.already_constrained is False

    def test_already_constrained_skips_word_limit(self) -> None:
        plan = plan_constraints("Explain AI in 50 words using simple language.")
        kinds = {c.kind for c in plan.constraints}
        assert ConstraintKind.WORD_LIMIT not in kinds

    def test_code_prompt_gets_code_only(self) -> None:
        plan = plan_constraints("Write a Python function to reverse a string")
        kinds = {c.kind for c in plan.constraints}
        assert ConstraintKind.CODE_STYLE in kinds

    def test_list_prompt_gets_bullet_limit(self) -> None:
        plan = plan_constraints("List benefits of renewable energy")
        kinds = {c.kind for c in plan.constraints}
        assert ConstraintKind.BULLET_LIMIT in kinds


class TestApplyAndOptimize:
    def test_optimize_explain_adds_word_cap(self) -> None:
        result = optimize_with_constraints("Explain AI or machine learning")
        lower = result.lower()
        assert "explain" in lower
        assert "word" in lower or "sentence" in lower
        assert constraint_density(result) > constraint_density(
            "Explain AI or machine learning"
        )

    def test_apply_constraints_appends_text(self) -> None:
        from optimizer.constraint_rules import ConstraintSpec

        out = apply_constraints(
            "Explain AI",
            [
                ConstraintSpec(
                    ConstraintKind.WORD_LIMIT, "Answer in at most 50 words.", 10
                )
            ],
        )
        assert out.startswith("Explain AI")
        assert "50 words" in out

    def test_candidates_are_unique_and_nonempty(self) -> None:
        candidates = build_constraint_candidates(
            "Can you please explain quantum computing?",
            num_candidates=5,
        )
        assert 1 <= len(candidates) <= 5
        assert len(candidates) == len(set(candidates))
        assert any("word" in c.lower() or "simple" in c.lower() for c in candidates)


class TestRuleBasedProvider:
    def test_provider_adds_constraints(self) -> None:
        provider = RuleBasedProvider()
        result = provider.optimize("Explain machine learning", "unused")
        assert "machine learning" in result.lower()
        assert constraint_density(result) > 0

    def test_provider_returns_multiple_candidates(self) -> None:
        provider = RuleBasedProvider()
        candidates = provider.optimize_candidates(
            "What is climate change?", "unused", num_candidates=4
        )
        assert len(candidates) >= 2

    def test_preserves_user_number_constraints(self) -> None:
        provider = RuleBasedProvider()
        result = provider.optimize("List 3 causes of inflation", "unused")
        assert "3" in result


class TestRankingConstraintBonus:
    def test_constrained_candidate_stays_similar(self) -> None:
        original = "Explain artificial intelligence"
        candidate = (
            "Explain artificial intelligence. Answer in at most 40 words. "
            "Use simple language a beginner can understand."
        )
        assert semantic_similarity(original, candidate) >= 0.5
