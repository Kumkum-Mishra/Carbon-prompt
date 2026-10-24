"""Unit tests for task type classification."""

from analyzer.config import TASK_CATEGORIES
from analyzer.task_classifier import classify_task


class TestTaskClassifier:
    def test_coding(self) -> None:
        assert classify_task("Write Python code to implement CNN.") == "Coding"

    def test_mathematics(self) -> None:
        assert classify_task("Solve 2x + 5 = 11.") == "Mathematics"

    def test_writing(self) -> None:
        assert classify_task("Write a blog post about climate change.") == "Writing"

    def test_summarization(self) -> None:
        assert classify_task("Summarize this article.") == "Summarization"

    def test_translation(self) -> None:
        assert classify_task("Translate this paragraph into Hindi.") == "Translation"

    def test_question_answering(self) -> None:
        assert classify_task("What is the capital of France?") == "Question Answering"

    def test_reasoning(self) -> None:
        assert classify_task("Compare and evaluate both approaches.") == "Reasoning"

    def test_image_generation(self) -> None:
        assert classify_task("Generate an image of a sunset.") == "Image Generation"

    def test_vision_analysis(self) -> None:
        assert classify_task("Describe this image in detail.") == "Vision Analysis"

    def test_search(self) -> None:
        assert classify_task("Search for the latest news on AI.") == "Search"

    def test_general_fallback(self) -> None:
        assert classify_task("Hello there.") == "General"

    def test_returns_supported_category(self) -> None:
        for prompt in [
            "Write Python code.",
            "Solve equation.",
            "Summarize text.",
            "Random greeting.",
        ]:
            assert classify_task(prompt) in TASK_CATEGORIES
