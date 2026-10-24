"""Rule-based task type classification."""

import re

from analyzer.config import TASK_CATEGORIES

_TASK_PATTERNS: list[tuple[str, list[str]]] = [
    (
        "Image Generation",
        [
            r"\bgenerate\s+(an?\s+)?image\b",
            r"\bcreate\s+(a\s+)?picture\b",
            r"\bdraw\s+(an?\s+)?(image|picture|illustration)\b",
            r"\billustration\b",
            r"\bimage\s+generation\b",
        ],
    ),
    (
        "Vision Analysis",
        [
            r"\banalyze\s+(this\s+)?image\b",
            r"\bdescribe\s+(this\s+)?image\b",
            r"\bscreenshot\b",
            r"\bvision\s+analysis\b",
            r"\bwhat\s+(is|are)\s+in\s+(this|the)\s+image\b",
        ],
    ),
    (
        "Translation",
        [
            r"\btranslate\b",
            r"\bin\s+hindi\b",
            r"\bin\s+french\b",
            r"\bin\s+spanish\b",
            r"\bin\s+german\b",
            r"\binto\s+(hindi|french|spanish|german|english|chinese|japanese)\b",
            r"\bconvert\s+(to|into)\s+\w+\s+language\b",
        ],
    ),
    (
        "Summarization",
        [
            r"\bsummarize\b",
            r"\bsummary\b",
            r"\bkey\s+points\b",
            r"\bshorten\b",
            r"\bcondense\b",
            r"\btl;?dr\b",
            r"\bin\s+fewer\s+words\b",
        ],
    ),
    (
        "Coding",
        [
            r"\bcode\b",
            r"\bpython\b",
            r"\bjavascript\b",
            r"\btypescript\b",
            r"\bjava\b",
            r"\bc\+\+\b",
            r"\brust\b",
            r"\bgolang\b",
            r"\bfunction\b",
            r"\bclass\b",
            r"\bapi\b",
            r"\bdebug\b",
            r"\bcnn\b",
            r"\bpytorch\b",
            r"\btensorflow\b",
            r"\bprogram(ming)?\b",
            r"\balgorithm\b",
            r"\bimplement\b.*\b(in|using)\b",
            r"\bwrite\s+.*\b(code|script|program)\b",
        ],
    ),
    (
        "Mathematics",
        [
            r"\bsolve\b",
            r"\bequation\b",
            r"\bcalculate\b",
            r"\bderivative\b",
            r"\bintegral\b",
            r"\bprobability\b",
            r"\bmath\b",
            r"\barithmetic\b",
            r"\balgebra\b",
            r"\bgeometry\b",
            r"\b\d+x\b",
            r"\b\d+\s*[\+\-\*/]\s*\d+\b",
        ],
    ),
    (
        "Search",
        [
            r"\bsearch\b",
            r"\bfind\b.*\b(latest|online|web)\b",
            r"\blook\s+up\b",
            r"\blatest\s+news\b",
            r"\bweb\s+search\b",
        ],
    ),
    (
        "Question Answering",
        [
            r"^\s*what\b",
            r"^\s*who\b",
            r"^\s*when\b",
            r"^\s*where\b",
            r"^\s*why\b",
            r"^\s*how\b",
            r"\?$",
        ],
    ),
    (
        "Reasoning",
        [
            r"\breason\b",
            r"\binfer\b",
            r"\banalyze\b",
            r"\bevaluate\b",
            r"\bcompare\b",
            r"\bdeduce\b",
            r"\blogic\b",
            r"\bexplain\s+why\b",
        ],
    ),
    (
        "Writing",
        [
            r"\bwrite\b",
            r"\bdraft\b",
            r"\bessay\b",
            r"\bemail\b",
            r"\bparagraph\b",
            r"\bblog\b",
            r"\bcompose\b",
            r"\bgenerate\s+a\s+(slogan|description|article|post)\b",
            r"\bcreate\s+a\s+(story|narrative)\b",
        ],
    ),
]


def classify_task(prompt: str) -> str:
    """Classify the prompt into exactly one supported task category."""
    text = prompt.lower()

    for category, patterns in _TASK_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return category

    return "General"
