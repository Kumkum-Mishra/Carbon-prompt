"""Rule-based prompt engineering strategy detection."""

import re

from analyzer.config import PROMPT_TYPES


def _count_examples(text: str) -> int:
    """Count explicit example markers in the prompt."""
    patterns = [
        r"\bexample\s+\d+\b",
        r"\bexample\s*:\s*",
        r"\bfor\s+example\b",
        r"\be\.g\.\b",
        r"\bsample\s+\d+\b",
        r"\bdemo\s+\d+\b",
    ]
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def classify_prompt_type(prompt: str) -> str:
    """Detect the prompt engineering strategy used in the prompt."""
    text = prompt.lower()

    if re.search(r"\bthink\s+step\s+by\s+step\b", text):
        return "Chain of Thought"
    if re.search(r"\bexplain\s+your\s+reasoning\b", text):
        return "Chain of Thought"
    if re.search(r"\bchain\s+of\s+thought\b", text):
        return "Chain of Thought"

    if re.search(r"\btree\s+of\s+thought\b", text):
        return "Tree of Thought"
    if re.search(r"\bexplore\s+multiple\s+reasoning\s+paths\b", text):
        return "Tree of Thought"

    if re.search(r"\bthought\s*:\s*", text) and re.search(
        r"\baction\s*:\s*", text
    ):
        return "ReAct"
    if re.search(r"\bobservation\s*:\s*", text) and re.search(
        r"\baction\s*:\s*", text
    ):
        return "ReAct"

    example_count = _count_examples(text)
    if example_count >= 2:
        return "Few-shot"
    if example_count == 1:
        return "One-shot"

    if re.search(r"\bact\s+as\b", text):
        return "Role Prompting"
    if re.search(r"\bbehave\s+as\b", text):
        return "Role Prompting"
    if re.search(r"\btake\s+the\s+role\s+of\b", text):
        return "Role Prompting"

    if re.search(r"\byou\s+are\s+(a|an)\s+", text):
        return "Persona Prompting"
    if re.search(r"\byou\s+are\s+(helpful|friendly|expert)\b", text):
        return "Persona Prompting"

    if re.search(r"\bquestion\s*:\s*", text) and re.search(
        r"\banswer\s*:\s*", text
    ):
        return "Structured Prompt"
    if re.search(r"<\s*\w+\s*>", text) and re.search(r"<\s*/\s*\w+\s*>", text):
        return "Structured Prompt"
    if re.search(r"\bjson\s+format\b", text) or re.search(
        r"\boutput\s+format\s*:\s*json\b", text
    ):
        return "Structured Prompt"

    # Direct task with no examples or role instructions
    has_role_or_persona = bool(
        re.search(r"\b(act\s+as|behave\s+as|you\s+are)\b", text)
    )
    if not has_role_or_persona and example_count == 0:
        return "Zero-shot"

    return "Other"
