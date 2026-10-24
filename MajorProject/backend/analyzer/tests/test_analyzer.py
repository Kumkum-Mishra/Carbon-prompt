"""Unit tests for the PromptAnalyzer orchestration layer."""

import pytest

from analyzer.analyzer import PromptAnalyzer


@pytest.fixture
def analyzer() -> PromptAnalyzer:
    return PromptAnalyzer()


class TestPromptAnalyzer:
    def test_valid_coding_prompt(self, analyzer: PromptAnalyzer) -> None:
        result = analyzer.analyze("Write Python code to implement CNN.")
        assert result.success is True
        assert result.analysis.task_type == "Coding"
        assert result.analysis.category == "Coding"
        assert result.analysis.token_count > 0
        assert result.analysis.character_count > 0
        assert result.analysis.word_count > 0

    def test_valid_mathematics_prompt(self, analyzer: PromptAnalyzer) -> None:
        result = analyzer.analyze("Solve 2x + 5 = 11.")
        assert result.success is True
        assert result.analysis.task_type == "Mathematics"

    def test_valid_translation_prompt(self, analyzer: PromptAnalyzer) -> None:
        result = analyzer.analyze("Translate this paragraph into Hindi.")
        assert result.success is True
        assert result.analysis.task_type == "Translation"

    def test_valid_summarization_prompt(self, analyzer: PromptAnalyzer) -> None:
        result = analyzer.analyze("Summarize this article.")
        assert result.success is True
        assert result.analysis.task_type == "Summarization"

    def test_role_prompting(self, analyzer: PromptAnalyzer) -> None:
        result = analyzer.analyze("Act as a software engineer.")
        assert result.success is True
        assert result.analysis.prompt_type == "Role Prompting"

    def test_persona_prompting(self, analyzer: PromptAnalyzer) -> None:
        result = analyzer.analyze("You are a friendly travel guide.")
        assert result.success is True
        assert result.analysis.prompt_type == "Persona Prompting"

    def test_chain_of_thought(self, analyzer: PromptAnalyzer) -> None:
        result = analyzer.analyze("Think step by step.")
        assert result.success is True
        assert result.analysis.prompt_type == "Chain of Thought"

    def test_few_shot(self, analyzer: PromptAnalyzer) -> None:
        prompt = "Example 1: cat -> feline. Example 2: dog -> canine. Now answer: bird -> ?"
        result = analyzer.analyze(prompt)
        assert result.success is True
        assert result.analysis.prompt_type == "Few-shot"

    def test_trims_whitespace(self, analyzer: PromptAnalyzer) -> None:
        result = analyzer.analyze("  Write CNN code  ")
        assert result.success is True
        assert result.analysis.prompt == "Write CNN code"

    def test_end_to_end_example(self, analyzer: PromptAnalyzer) -> None:
        prompt = (
            "Act as a software engineer. "
            "Write Python code to implement a CNN using PyTorch."
        )
        result = analyzer.analyze(prompt)
        assert result.success is True
        assert result.analysis.prompt_type == "Role Prompting"
        assert result.analysis.task_type == "Coding"
        assert result.analysis.category == "Coding"
