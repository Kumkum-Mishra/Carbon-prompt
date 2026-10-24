"""Unit tests for prompt feature extraction."""

from recommendation.feature_extractor import extract_prompt_features


class TestFeatureExtractor:
    def test_short_qa_prompt(self) -> None:
        features = extract_prompt_features(
            prompt="What is AI?",
            task_type="Question Answering",
            input_tokens=20,
        )
        assert features.input_tokens == 20
        assert features.expected_output_tokens == 80
        assert features.urgency is False
        assert features.cost_sensitive is False

    def test_urgency_and_cost_keywords(self) -> None:
        features = extract_prompt_features(
            prompt="Quickly summarize this report in a cheap way.",
            task_type="Summarization",
            input_tokens=40000,
        )
        assert features.urgency is True
        assert features.cost_sensitive is True
        assert features.expected_output_tokens == 250

    def test_explicit_word_count(self) -> None:
        features = extract_prompt_features(
            prompt="Write a 5000-word article about renewable energy.",
            task_type="Writing",
            input_tokens=15,
        )
        assert features.expected_output_tokens == 6500

    def test_high_detail_multiplier(self) -> None:
        features = extract_prompt_features(
            prompt="Give a detailed step-by-step explanation of CNNs.",
            task_type="Coding",
            input_tokens=30,
        )
        assert features.detail_level == "high"
        assert features.expected_output_tokens == 700
