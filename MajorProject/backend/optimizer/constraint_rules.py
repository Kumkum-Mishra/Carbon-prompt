"""Rule-based output-constraint engine for sustainable prompt optimization.

Adds explicit length, simplicity, format, and scope constraints to open-ended
prompts so downstream LLMs produce fewer tokens without changing intent.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum


class ConstraintKind(str, Enum):
    """Categories of output constraints the engine can inject."""

    WORD_LIMIT = "word_limit"
    SENTENCE_LIMIT = "sentence_limit"
    BULLET_LIMIT = "bullet_limit"
    SIMPLICITY = "simplicity"
    FORMAT = "format"
    SCOPE = "scope"
    DIRECTNESS = "directness"
    CODE_STYLE = "code_style"
    NO_FLUFF = "no_fluff"
    STEP_LIMIT = "step_limit"


@dataclass(frozen=True)
class ConstraintSpec:
    """A single constraint to append or merge into a prompt."""

    kind: ConstraintKind
    text: str
    priority: int = 50  # lower = applied earlier / preferred


@dataclass
class ConstraintPlan:
    """Detected gaps and constraints chosen for a prompt."""

    cleaned_prompt: str
    intent: str
    missing_kinds: list[ConstraintKind] = field(default_factory=list)
    constraints: list[ConstraintSpec] = field(default_factory=list)
    already_constrained: bool = False


# ---------------------------------------------------------------------------
# Detection: what constraints already exist in the user prompt?
# ---------------------------------------------------------------------------

_EXISTING_CONSTRAINT_PATTERNS: dict[ConstraintKind, re.Pattern[str]] = {
    ConstraintKind.WORD_LIMIT: re.compile(
        r"\b("
        r"in\s+(?:at\s+most\s+)?\d+\s*[-–]?\s*\d*\s*words?"
        r"|at\s+most\s+\d+\s*words?"
        r"|max(?:imum)?\s+(?:of\s+)?\d+\s*words?"
        r"|no\s+more\s+than\s+\d+\s*words?"
        r"|under\s+\d+\s*words?"
        r"|fewer\s+than\s+\d+\s*words?"
        r"|\d+\s*words?\s+or\s+(?:less|fewer)"
        r"|word\s+limit\s*(?:of|:)?\s*\d+"
        r"|keep\s+(?:the\s+)?(?:answer|response|it)\s+(?:short|brief|concise)"
        r"|in\s+brief"
        r"|tl;?dr"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.SENTENCE_LIMIT: re.compile(
        r"\b("
        r"in\s+\d+\s*[-–]?\s*\d*\s*sentences?"
        r"|one\s+sentence"
        r"|two\s+sentences?"
        r"|a\s+few\s+sentences?"
        r"|in\s+(?:one|a)\s+paragraph"
        r"|short\s+paragraph"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.BULLET_LIMIT: re.compile(
        r"\b("
        r"top\s+\d+"
        r"|list\s+\d+"
        r"|\d+\s*(?:key\s+)?(?:points?|bullets?|items?|tips?|reasons?|"
        r"causes?|benefits?|ways?|types?|examples?|ideas?|steps?)"
        r"|bullet\s*points?"
        r"|as\s+a\s+(?:bulleted\s+)?list"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.SIMPLICITY: re.compile(
        r"\b("
        r"simple(?:\s+language|\s+terms)?"
        r"|eli5"
        r"|explain\s+like\s+(?:i'?m|i\s+am)\s+\d+"
        r"|like\s+(?:i'?m|i\s+am)\s+(?:\d+|five|5)"
        r"|for\s+(?:a\s+)?(?:five|5)[- ]year[- ]old"
        r"|beginner(?:-|\s+)friendly"
        r"|no\s+jargon"
        r"|layman'?s?\s+terms"
        r"|easy\s+to\s+understand"
        r"|for\s+(?:a\s+)?(?:beginner|kid|child|non[- ]?expert)"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.FORMAT: re.compile(
        r"\b("
        r"json|yaml|xml|csv|markdown|table"
        r"|bullet(?:ed)?\s*(?:points?|list)?"
        r"|numbered\s+(?:list|steps?)"
        r"|as\s+a\s+(?:list|table|json|markdown|bulleted\s+list)"
        r"|return\s+only"
        r"|output\s+(?:format|as)"
        r"|respond\s+(?:with|in)\s+(?:json|yaml|a\s+list)"
        r"|bulleted\s+list\s+only"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.SCOPE: re.compile(
        r"\b("
        r"only\s+(?:cover|focus|include|discuss)"
        r"|focus\s+(?:only\s+)?on"
        r"|do\s+not\s+(?:include|mention|discuss|cover)"
        r"|without\s+(?:examples?|history|background|fluff)"
        r"|skip\s+(?:the\s+)?(?:history|background|intro)"
        r"|key\s+(?:ideas?|points?)\s+only"
        r"|main\s+(?:idea|points?)\s+only"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.DIRECTNESS: re.compile(
        r"\b("
        r"direct(?:\s+answer)?"
        r"|answer\s+first"
        r"|no\s+(?:preamble|introduction|outro)"
        r"|get\s+straight\s+to\s+the\s+point"
        r"|just\s+(?:the\s+)?answer"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.CODE_STYLE: re.compile(
        r"\b("
        r"code\s+only"
        r"|no\s+(?:explanation|comments?|prose)"
        r"|without\s+(?:explanation|comments?)"
        r"|minimal\s+comments?"
        r"|return\s+only\s+(?:the\s+)?code"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.NO_FLUFF: re.compile(
        r"\b("
        r"no\s+fluff"
        r"|no\s+(?:filler|padding|rambling)"
        r"|avoid\s+(?:verbosity|waffle|filler)"
        r"|be\s+(?:terse|succinct)"
        r")\b",
        re.IGNORECASE,
    ),
    ConstraintKind.STEP_LIMIT: re.compile(
        r"\b("
        r"in\s+\d+\s*[-–]?\s*\d*\s*steps?"
        r"|max(?:imum)?\s+\d+\s*steps?"
        r"|\d+\s*steps?\s+(?:only|max|maximum)?"
        r"|step[- ]by[- ]step\s+in\s+\d+"
        r")\b",
        re.IGNORECASE,
    ),
}

# Soft length cues that already limit output somewhat (not task verbs like summarize)
_SOFT_LENGTH_CUES = re.compile(
    r"\b(short|brief|concise|overview|quick|tldr|tl;dr)\b",
    re.IGNORECASE,
)

# Structured / few-shot prompts: do not aggressively rewrite
_STRUCTURE_MARKERS = re.compile(
    r"(Example\s*\d*:|Task:|Input:|Output:|Constraints?:|Instructions?:|"
    r"Thought:|Action:|Observation:|System:|User:|Assistant:|"
    r"Use ReAct|Think step by step|You are |```|"
    r"Example:|Q:|A:)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Intent detection (lightweight; complements analyzer task types)
# ---------------------------------------------------------------------------

_INTENT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "compare",
        re.compile(
            r"\b(compare|versus|vs\.?|difference\s+between|pros\s+and\s+cons|"
            r"contrast)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "image",
        re.compile(
            r"\b("
            r"generate\s+(an?\s+)?image"
            r"|create\s+(an?\s+)?image"
            r"|draw"
            r"|illustration"
            r"|picture\s+of"
            r")\b",
            re.IGNORECASE,
        ),
    ),
    (
        "qa",
        re.compile(
            r"\b("
            r"who\s+(?:is|was|are|were)\b"
            r"|when\s+(?:did|was|is|were)\b"
            r"|where\s+(?:is|was|are)\b"
            r"|which\s+\w+\b"
            r"|capital\s+of\b"
            r"|true\s+or\s+false\b"
            r")",
            re.IGNORECASE,
        ),
    ),
    (
        "explain",
        re.compile(
            r"\b(explain|what\s+is|what\s+are|describe|"
            r"tell\s+me\s+(?:everything\s+)?about|"
            r"define|definition\s+of|how\s+does|how\s+do)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "summarize",
        re.compile(
            r"\b(summarize|summary|tl;?dr|condense|key\s+points)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "code",
        re.compile(
            r"\b(code|function|class|script|implement|program|debug|algorithm|"
            r"python|javascript|typescript|java|sql|api|refactor)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "write",
        re.compile(
            r"\b(write|draft|compose|essay|blog|article|email|letter|story|"
            r"paragraph|post)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "translate",
        re.compile(r"\b(translate|translation)\b", re.IGNORECASE),
    ),
    (
        "math",
        re.compile(
            r"\b(solve|calculate|compute|equation|integral|derivative|math)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "howto",
        re.compile(
            r"\b(how\s+to|steps?\s+to|guide|tutorial|walk\s*me\s+through|"
            r"instructions?\s+for)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "list",
        re.compile(
            r"\b("
            r"list\s+\w+"
            r"|enumerate"
            r"|name\s+(?:some|the|all)"
            r"|give\s+me\s+(?:some|a\s+few|a\s+list)"
            r"|what\s+are\s+(?:the\s+)?(?:types|kinds|ways|benefits|pros|cons)"
            r")\b",
            re.IGNORECASE,
        ),
    ),
    (
        "reason",
        re.compile(
            r"\b(reason|analyze|analyse|evaluate|why|how\s+would|think\s+through|"
            r"step\s+by\s+step)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "brainstorm",
        re.compile(
            r"\b(brainstorm|ideas?|suggestions?|recommend|recommendations?)\b",
            re.IGNORECASE,
        ),
    ),
]


# ---------------------------------------------------------------------------
# Filler / verbosity cleanup (input-side optimization)
# ---------------------------------------------------------------------------

_FILLER_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^can you please\s+", re.IGNORECASE), ""),
    (re.compile(r"^could you please\s+", re.IGNORECASE), ""),
    (re.compile(r"^could you kindly\s+", re.IGNORECASE), ""),
    (re.compile(r"^would you (?:mind|please)\s+", re.IGNORECASE), ""),
    (re.compile(r"^please\s+", re.IGNORECASE), ""),
    (re.compile(r"^can you\s+", re.IGNORECASE), ""),
    (re.compile(r"^could you\s+", re.IGNORECASE), ""),
    (re.compile(r"^would you\s+", re.IGNORECASE), ""),
    (re.compile(r"^i want you to\s+", re.IGNORECASE), ""),
    (re.compile(r"^i would like you to\s+", re.IGNORECASE), ""),
    (re.compile(r"^i need you to\s+", re.IGNORECASE), ""),
    (re.compile(r"^i was wondering if you could(?:\s+please)?\s+", re.IGNORECASE), ""),
    (re.compile(r"^it would be great if you could\s+", re.IGNORECASE), ""),
    (re.compile(r"^hey,?\s+", re.IGNORECASE), ""),
    (re.compile(r"\s+please\b", re.IGNORECASE), ""),
    (re.compile(r"\bin great detail with lots of\b", re.IGNORECASE), ""),
    (re.compile(r"\bin great detail with\b", re.IGNORECASE), ""),
    (re.compile(r"\bin (?:great |full )?detail\b", re.IGNORECASE), ""),
    (re.compile(r"\band also discuss\b", re.IGNORECASE), " and "),
    (re.compile(r"\band also explain\b", re.IGNORECASE), " and "),
    (re.compile(r"\bwith lots of examples\b", re.IGNORECASE), ""),
    (re.compile(r"\bwith lots of\b", re.IGNORECASE), " with "),
    (re.compile(r"\bas comprehensively as possible\b", re.IGNORECASE), ""),
    (re.compile(r"\bas thoroughly as possible\b", re.IGNORECASE), ""),
    (re.compile(r"\bin as much detail as possible\b", re.IGNORECASE), ""),
    (re.compile(r"\beverything you know about\b", re.IGNORECASE), ""),
    (re.compile(r"\beverything about\b", re.IGNORECASE), "about"),
    (re.compile(r"\ba comprehensive (?:overview|explanation|guide)\s+(?:to|of|on)\b", re.IGNORECASE), "a short guide to"),
    (re.compile(r"\bcomprehensive\b", re.IGNORECASE), ""),
    (re.compile(r"\b(?:a\s+)?deep dive into\b", re.IGNORECASE), "an overview of"),
    (re.compile(r"\bacross different industries\b", re.IGNORECASE), "across industries"),
    # Open-ended "Describe X" usually yields long essays — tighten the verb.
    (re.compile(r"^Describe\b", re.IGNORECASE), "Explain"),
    (re.compile(r"^Tell me about\b", re.IGNORECASE), "Explain"),
    (
        re.compile(
            r"\s*(?:thanks in advance|thank you|i would really appreciate (?:it|your help))"
            r"(?:\.|!)?\s*$",
            re.IGNORECASE,
        ),
        "",
    ),
    (
        re.compile(
            r"\s*(?:if (?:that is okay|possible)|when you get a chance|as soon as you can)"
            r"(?:\.|!)?\s*$",
            re.IGNORECASE,
        ),
        "",
    ),
]

# Phrases that signal unbounded / high-token output risk
_UNBOUNDED_MARKERS = re.compile(
    r"\b("
    r"in\s+(?:great|full|complete)\s+detail"
    r"|as\s+(?:much|many)\s+.*\s+as\s+possible"
    r"|everything\s+(?:you\s+know|about)"
    r"|comprehensive"
    r"|exhaustive"
    r"|thorough(?:ly)?"
    r"|all\s+(?:aspects|details|information)"
    r"|deep\s+dive"
    r"|complete\s+guide"
    r"|from\s+scratch\s+with\s+examples"
    r")\b",
    re.IGNORECASE,
)


def detect_existing_constraints(prompt: str) -> set[ConstraintKind]:
    """Return constraint kinds already present in the prompt."""
    found: set[ConstraintKind] = set()
    for kind, pattern in _EXISTING_CONSTRAINT_PATTERNS.items():
        if pattern.search(prompt):
            found.add(kind)
    return found


def has_soft_length_cue(prompt: str) -> bool:
    """True for weak cues like 'short'/'brief' that are not hard caps."""
    return bool(_SOFT_LENGTH_CUES.search(prompt))


def has_hard_length_constraint(prompt: str) -> bool:
    """True only for numeric / explicit length bounds (not just 'briefly')."""
    return bool(
        re.search(
            r"\b("
            r"in\s+(?:at\s+most\s+)?\d+\s*words?"
            r"|at\s+most\s+\d+\s*words?"
            r"|max(?:imum)?\s+(?:of\s+)?\d+\s*words?"
            r"|no\s+more\s+than\s+\d+\s*words?"
            r"|under\s+\d+\s*words?"
            r"|in\s+\d+\s*sentences?"
            r"|at\s+most\s+\d+\s*(?:bullet|points?|steps?)"
            r"|top\s+\d+"
            r")\b",
            prompt,
            re.IGNORECASE,
        )
    )

def detect_intent(prompt: str) -> str:
    """Return the primary intent label for constraint selection."""
    for intent, pattern in _INTENT_PATTERNS:
        if pattern.search(prompt):
            return intent
    return "general"


def is_structured_prompt(prompt: str) -> bool:
    """True when the prompt is few-shot / role / multi-section structured."""
    if _STRUCTURE_MARKERS.search(prompt):
        return True
    # Long multi-line instructional prompts
    if prompt.count("\n") >= 3 and len(prompt) > 200:
        return True
    return False


def clean_fillers(prompt: str) -> str:
    """Strip politeness fillers and verbosity wrappers."""
    text = " ".join(prompt.split()).strip()
    if not text:
        return text

    original_ends_question = text.endswith("?")

    for _ in range(2):
        for pattern, repl in _FILLER_PATTERNS:
            text = pattern.sub(repl, text)
        text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    text = re.sub(r"^[,\s]+", "", text)
    text = re.sub(r"^please\s+", "", text, flags=re.IGNORECASE).strip()

    if text and text[0].islower():
        text = text[0].upper() + text[1:]

    # Avoid stray "?" after filler removal turned a statement into "Explain X?"
    if text.endswith("?"):
        is_imperative = bool(
            re.match(
                r"^(Explain|Describe|Write|List|Summarize|Compare|Solve|"
                r"Translate|Give|Create|Draft|Define|Implement|Debug)\b",
                text,
                re.IGNORECASE,
            )
        )
        has_wh = bool(
            re.search(
                r"\b(what|why|how|when|where|who|which|can|could|would|is|are|do|does)\b",
                text,
                re.IGNORECASE,
            )
        )
        if is_imperative and not has_wh:
            text = text[:-1].rstrip()
        elif (
            not original_ends_question
            and not has_wh
        ):
            text = text[:-1].rstrip()
    elif (
        original_ends_question
        and text
        and text[-1] not in ".?!"
        and re.search(
            r"\b(what|why|how|when|where|who|which|can|could|would|is|are|do|does)\b",
            text,
            re.IGNORECASE,
        )
    ):
        text += "?"

    return text or prompt.strip()


def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+", text))


def _default_constraints_for_intent(
    intent: str,
    *,
    unbounded: bool,
    prompt_words: int,
) -> list[ConstraintSpec]:
    """Pick best-practice constraints by intent.

    Open-ended educational prompts get tight word caps; coding gets code-only
    style; listing gets bullet caps, etc.
    """
    # Scale word caps slightly with topic breadth signals
    tight = 40 if unbounded or prompt_words <= 8 else 60
    medium = 80 if unbounded else 100
    loose = 120 if unbounded else 150

    by_intent: dict[str, list[ConstraintSpec]] = {
        "explain": [
            ConstraintSpec(
                ConstraintKind.WORD_LIMIT,
                "Answer in at most 100 words.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.FORMAT,
                "Use at most 5 short bullet points.",
                priority=15,
            ),
            ConstraintSpec(
                ConstraintKind.SIMPLICITY,
                "Use simple language a beginner can understand.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.SCOPE,
                "Cover only the core idea; skip history and side topics.",
                priority=30,
            ),
            ConstraintSpec(
                ConstraintKind.NO_FLUFF,
                "No fluff or filler.",
                priority=40,
            ),
        ],
        "summarize": [
            ConstraintSpec(
                ConstraintKind.SENTENCE_LIMIT,
                "Summarize in 3 sentences or fewer.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.SCOPE,
                "Include only the main points.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.NO_FLUFF,
                "No fluff.",
                priority=30,
            ),
        ],
        "list": [
            ConstraintSpec(
                ConstraintKind.BULLET_LIMIT,
                "Return at most 5 concise bullet points.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.FORMAT,
                "Use a bulleted list only.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.NO_FLUFF,
                "No intro or outro.",
                priority=30,
            ),
        ],
        "compare": [
            ConstraintSpec(
                ConstraintKind.FORMAT,
                "Compare in a short table or at most 5 bullets.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.WORD_LIMIT,
                f"Keep the whole answer under {medium} words.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.SCOPE,
                "Focus only on the key differences.",
                priority=30,
            ),
        ],
        "code": [
            ConstraintSpec(
                ConstraintKind.CODE_STYLE,
                "Return code only; no prose explanation.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.SCOPE,
                "Keep the solution minimal and focused.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.NO_FLUFF,
                "No preamble.",
                priority=30,
            ),
        ],
        "write": [
            ConstraintSpec(
                ConstraintKind.WORD_LIMIT,
                f"Write at most {loose} words.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.DIRECTNESS,
                "Get straight to the point; no long introduction.",
                priority=20,
            ),
        ],
        "translate": [
            ConstraintSpec(
                ConstraintKind.SCOPE,
                "Translate only; do not add commentary or alternatives.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.DIRECTNESS,
                "Return only the translation.",
                priority=20,
            ),
        ],
        "math": [
            ConstraintSpec(
                ConstraintKind.DIRECTNESS,
                "Give the final answer first, then a short solution.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.STEP_LIMIT,
                "Use at most 5 short steps.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.NO_FLUFF,
                "No extra commentary.",
                priority=30,
            ),
        ],
        "reason": [
            ConstraintSpec(
                ConstraintKind.STEP_LIMIT,
                "Reason in at most 5 short steps.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.WORD_LIMIT,
                f"Keep the full answer under {medium} words.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.DIRECTNESS,
                "End with a one-sentence conclusion.",
                priority=30,
            ),
        ],
        "howto": [
            ConstraintSpec(
                ConstraintKind.STEP_LIMIT,
                "Give at most 6 numbered steps.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.FORMAT,
                "Use a numbered list.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.WORD_LIMIT,
                f"Keep each step under 20 words; total under {medium} words.",
                priority=30,
            ),
        ],
        "qa": [
            ConstraintSpec(
                ConstraintKind.DIRECTNESS,
                "Answer directly in one or two sentences.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.NO_FLUFF,
                "No preamble.",
                priority=20,
            ),
        ],
        "brainstorm": [
            ConstraintSpec(
                ConstraintKind.BULLET_LIMIT,
                "Propose at most 5 ideas as short bullets.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.WORD_LIMIT,
                "Each idea in one short line.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.NO_FLUFF,
                "No intro or outro.",
                priority=30,
            ),
        ],
        "image": [
            ConstraintSpec(
                ConstraintKind.SCOPE,
                "Keep the image prompt concise and concrete.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.WORD_LIMIT,
                "Describe the scene in at most 40 words.",
                priority=20,
            ),
        ],
        "general": [
            ConstraintSpec(
                ConstraintKind.WORD_LIMIT,
                f"Respond in at most {tight} words.",
                priority=10,
            ),
            ConstraintSpec(
                ConstraintKind.DIRECTNESS,
                "Be direct; no preamble.",
                priority=20,
            ),
            ConstraintSpec(
                ConstraintKind.NO_FLUFF,
                "No fluff.",
                priority=30,
            ),
        ],
    }
    return list(by_intent.get(intent, by_intent["general"]))


def plan_constraints(prompt: str) -> ConstraintPlan:
    """Analyze a prompt and decide which constraints to add."""
    cleaned = clean_fillers(prompt)
    intent = detect_intent(cleaned)
    existing = detect_existing_constraints(prompt) | detect_existing_constraints(cleaned)
    structured = is_structured_prompt(prompt)
    unbounded = bool(_UNBOUNDED_MARKERS.search(prompt))
    words = _word_count(cleaned)

    # Structured prompts: only light cleanup unless clearly unbounded and short
    if structured and not unbounded:
        return ConstraintPlan(
            cleaned_prompt=cleaned,
            intent=intent,
            missing_kinds=[],
            constraints=[],
            already_constrained=True,
        )

    candidates = _default_constraints_for_intent(
        intent, unbounded=unbounded, prompt_words=words
    )
    missing = [c.kind for c in candidates if c.kind not in existing]
    selected = [c for c in candidates if c.kind not in existing]

    # If already has a hard numeric length constraint, skip stacking more length kinds
    if has_hard_length_constraint(prompt) or has_hard_length_constraint(cleaned):
        selected = [
            c
            for c in selected
            if c.kind
            not in {
                ConstraintKind.WORD_LIMIT,
                ConstraintKind.SENTENCE_LIMIT,
            }
        ]

    already = len(selected) == 0 and len(existing) > 0
    return ConstraintPlan(
        cleaned_prompt=cleaned,
        intent=intent,
        missing_kinds=missing,
        constraints=selected,
        already_constrained=already,
    )


def apply_constraints(
    cleaned_prompt: str,
    constraints: list[ConstraintSpec],
    *,
    max_constraints: int | None = None,
) -> str:
    """Append selected constraints to the cleaned prompt."""
    if not cleaned_prompt:
        return cleaned_prompt

    ordered = sorted(constraints, key=lambda c: c.priority)
    if max_constraints is not None:
        ordered = ordered[: max(0, max_constraints)]

    if not ordered:
        return cleaned_prompt

    body = cleaned_prompt.rstrip()
    # Prefer ending the core ask with punctuation before constraints
    if body[-1] not in ".?!":
        body += "."

    constraint_text = " ".join(spec.text.rstrip(".") + "." for spec in ordered)
    return f"{body} {constraint_text}".strip()


def build_constraint_candidates(
    prompt: str,
    *,
    num_candidates: int = 5,
) -> list[str]:
    """Build ranked optimization candidates with progressive constraint sets.

    Candidate strategy (best → lighter):
    1. Clean + top constraints (tightest sustainable rewrite)
    2. Clean + length-only constraint
    3. Clean + simplicity/directness (no numeric word cap if possible)
    4. Clean only (filler strip)
    5. Original cleaned lightly
    """
    plan = plan_constraints(prompt)
    cleaned = plan.cleaned_prompt or prompt.strip()
    candidates: list[str] = []

    def _add(text: str) -> None:
        normalized = " ".join(text.split()).strip()
        if normalized and normalized not in candidates:
            candidates.append(normalized)

    if plan.constraints:
        # Full constraint pack (up to 3 for clarity)
        _add(apply_constraints(cleaned, plan.constraints, max_constraints=3))
        # Length-focused only
        length_kinds = {
            ConstraintKind.WORD_LIMIT,
            ConstraintKind.SENTENCE_LIMIT,
            ConstraintKind.BULLET_LIMIT,
            ConstraintKind.STEP_LIMIT,
        }
        length_only = [c for c in plan.constraints if c.kind in length_kinds]
        if length_only:
            _add(apply_constraints(cleaned, length_only, max_constraints=1))
        # Style/clarity without numeric caps
        style_kinds = {
            ConstraintKind.SIMPLICITY,
            ConstraintKind.DIRECTNESS,
            ConstraintKind.NO_FLUFF,
            ConstraintKind.SCOPE,
            ConstraintKind.CODE_STYLE,
            ConstraintKind.FORMAT,
        }
        style_only = [c for c in plan.constraints if c.kind in style_kinds]
        if style_only:
            _add(apply_constraints(cleaned, style_only, max_constraints=2))
        # Single highest-priority constraint
        _add(apply_constraints(cleaned, plan.constraints, max_constraints=1))

    _add(cleaned)

    original_normalized = " ".join(prompt.split()).strip()
    if original_normalized != cleaned:
        _add(original_normalized)

    return candidates[: max(1, num_candidates)]


def optimize_with_constraints(prompt: str) -> str:
    """Return the primary constraint-optimized prompt."""
    candidates = build_constraint_candidates(prompt, num_candidates=1)
    return candidates[0] if candidates else prompt.strip()


def constraint_density(prompt: str) -> float:
    """Fraction of known constraint kinds present (0–1). Used for ranking bonus."""
    existing = detect_existing_constraints(prompt)
    # Soft cues alone should not look like a fully constrained prompt.
    score = len(existing) / max(len(ConstraintKind), 1)
    if has_hard_length_constraint(prompt):
        score = max(score, 0.2)
    elif has_soft_length_cue(prompt) and not existing:
        score = max(score, 0.05)
    return round(min(score, 1.0), 4)
