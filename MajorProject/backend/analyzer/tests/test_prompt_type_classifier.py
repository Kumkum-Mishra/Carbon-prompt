"""Unit tests for prompt type classification."""

from analyzer.config import PROMPT_TYPES
from analyzer.prompt_type_classifier import classify_prompt_type


class TestPromptTypeClassifier:
    def test_zero_shot(self) -> None:
        assert classify_prompt_type("Write CNN code") == "Zero-shot"

    def test_one_shot(self) -> None:
        prompt = "Example: input -> output. Now translate: hello -> ?"
        assert classify_prompt_type(prompt) == "One-shot"

    def test_few_shot(self) -> None:
        prompt = "Example 1: a -> 1. Example 2: b -> 2. Now answer: c -> ?"
        assert classify_prompt_type(prompt) == "Few-shot"

    def test_chain_of_thought(self) -> None:
        assert classify_prompt_type("Think step by step.") == "Chain of Thought"

    def test_role_prompting(self) -> None:
        assert classify_prompt_type("Act as a software engineer.") == "Role Prompting"

    def test_persona_prompting(self) -> None:
        assert classify_prompt_type("You are a friendly travel guide.") == "Persona Prompting"

    def test_tree_of_thought(self) -> None:
        assert classify_prompt_type("Use tree of thought reasoning.") == "Tree of Thought"

    def test_react(self) -> None:
        prompt = "Thought: I need to search. Action: search web. Observation: found results."
        assert classify_prompt_type(prompt) == "ReAct"

    def test_structured_prompt(self) -> None:
        prompt = "Question: What is AI? Answer: Artificial Intelligence."
        assert classify_prompt_type(prompt) == "Structured Prompt"

    def test_other_fallback(self) -> None:
        result = classify_prompt_type("...")
        assert result in PROMPT_TYPES

    def test_returns_supported_type(self) -> None:
        prompts = [
            "Write code",
            "Act as expert",
            "Think step by step",
            "Example 1: a. Example 2: b.",
        ]
        for prompt in prompts:
            assert classify_prompt_type(prompt) in PROMPT_TYPES
