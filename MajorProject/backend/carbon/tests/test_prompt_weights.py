"""Unit tests for prompt weight lookup."""

import pytest

from carbon.prompt_weights import UnknownPromptTypeError, get_all_prompt_weights, get_prompt_weight


class TestPromptWeights:
    def test_zero_shot_weight(self) -> None:
        assert get_prompt_weight("Zero-shot") == 1.0

    def test_few_shot_weight(self) -> None:
        assert get_prompt_weight("Few-shot") == 1.2

    def test_chain_of_thought_weight(self) -> None:
        assert get_prompt_weight("Chain of Thought") == 1.5

    def test_unknown_prompt_type(self) -> None:
        with pytest.raises(UnknownPromptTypeError, match="Prompt type not recognized."):
            get_prompt_weight("Unknown Type")

    def test_all_supported_types_present(self) -> None:
        weights = get_all_prompt_weights()
        assert "Zero-shot" in weights
        assert "Few-shot" in weights
        assert "Chain of Thought" in weights
        assert len(weights) == 10
