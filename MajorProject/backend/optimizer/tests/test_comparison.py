"""Unit tests for optimization comparison logic."""

from analyzer.schemas import AnalysisResult
from optimizer.comparison import build_comparison


def _analysis(
    prompt: str,
    *,
    token_count: int,
    task_type: str = "Question Answering",
    prompt_type: str = "Zero-shot",
) -> AnalysisResult:
    return AnalysisResult(
        prompt=prompt,
        prompt_type=prompt_type,
        task_type=task_type,
        category=task_type,
        token_count=token_count,
        character_count=len(prompt),
        word_count=len(prompt.split()),
    )


class TestComparison:
    def test_build_comparison(self) -> None:
        original = _analysis(
            "Can you please explain AI?",
            token_count=26,
        )
        optimized = _analysis(
            "Explain artificial intelligence with examples.",
            token_count=13,
        )
        comparison = build_comparison(
            original_analysis=original,
            optimized_analysis=optimized,
            original_carbon_score=0.00039,
            optimized_carbon_score=0.00021,
        )
        assert comparison.original_tokens == 26
        assert comparison.optimized_tokens == 13
        assert comparison.token_reduction_percent == 50.0
        assert comparison.carbon_reduction_percent == 46.15
        assert comparison.original_task_type == "Question Answering"
        assert comparison.optimized_task_type == "Question Answering"

    def test_task_type_mismatch_still_returns_metrics(self, caplog) -> None:
        original = _analysis("Write code", token_count=10, task_type="Coding")
        optimized = _analysis("Write", token_count=5, task_type="Writing")
        comparison = build_comparison(
            original_analysis=original,
            optimized_analysis=optimized,
            original_carbon_score=0.0001,
            optimized_carbon_score=0.00005,
        )
        assert comparison.original_task_type == "Coding"
        assert comparison.optimized_task_type == "Writing"
