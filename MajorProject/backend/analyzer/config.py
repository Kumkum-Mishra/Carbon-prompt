"""Configuration constants for the Prompt Analyzer module."""

MAX_PROMPT_LENGTH: int = 10_000
MIN_PROMPT_LENGTH: int = 2
TOKENIZER_ENCODING: str = "cl100k_base"
LOG_FULL_PROMPT: bool = False

TASK_CATEGORIES: list[str] = [
    "Coding",
    "Mathematics",
    "Writing",
    "Summarization",
    "Translation",
    "Question Answering",
    "Reasoning",
    "Image Generation",
    "Vision Analysis",
    "Search",
    "General",
]

PROMPT_TYPES: list[str] = [
    "Zero-shot",
    "One-shot",
    "Few-shot",
    "Chain of Thought",
    "Role Prompting",
    "Persona Prompting",
    "Tree of Thought",
    "ReAct",
    "Structured Prompt",
    "Other",
]
