"""Shared helper functions for prompt analysis."""


def clean_prompt(prompt: str) -> str:
    """Trim leading and trailing whitespace from the prompt."""
    return prompt.strip()


def count_words(prompt: str) -> int:
    """Count whitespace-separated words in the prompt."""
    if not prompt:
        return 0
    return len(prompt.split())
