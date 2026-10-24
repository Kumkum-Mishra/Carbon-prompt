#!/usr/bin/env python3
"""Build prompt_optimization_dataset.csv with 10,000 original/optimized pairs."""

import csv
import random
import re
from pathlib import Path

random.seed(42)

VERBOSITY_PREFIXES = [
    "Can you please ",
    "Could you kindly ",
    "Would you mind ",
    "I would really appreciate it if you could ",
    "If it's not too much trouble, please ",
    "Hey, can you ",
    "I was wondering if you could please ",
    "Do you think you could ",
    "It would be great if you could ",
    "Can I ask you to please ",
]

VERBOSITY_SUFFIXES = [
    " if that is okay.",
    " when you get a chance.",
    " thanks in advance.",
    " I would really appreciate your help.",
    " please and thank you.",
    " if possible.",
    " as soon as you can.",
    " that would be really helpful.",
    " I hope that makes sense.",
    " let me know if you need more context.",
]

FILLER_PATTERNS = [
    (r"\b(?:please|kindly|just|really|actually|basically|simply)\b", " "),
    (r"\b(?:I would like you to|I want you to|I need you to)\b", ""),
    (r"\b(?:Can you|Could you|Would you|Will you)\b", ""),
    (r"\b(?:help me|assist me with)\b", ""),
    (r"\b(?:in order to)\b", "to"),
    (r"\b(?:a little bit|a bit)\b", ""),
    (r"\s{2,}", " "),
]

STRUCTURE_MARKERS = re.compile(
    r"(Example\s*\d*:|Task:|Input:|Output:|Constraints:|Instructions?:|"
    r"Thought:|Action:|Observation:|Sections?:|Labels?:|Fields?:|"
    r"Use ReAct|Think step by step|Explore \d+|Generate \d+|"
    r"You are |Example:|Q:|A:)",
    re.IGNORECASE,
)


def count_tokens(text: str) -> int:
    parts = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
    total = 0
    for p in parts:
        if p.isalnum():
            total += max(1, (len(p) + 3) // 4) if len(p) > 8 else 1
        else:
            total += 1
    return total


def is_structured(prompt: str) -> bool:
    return bool(STRUCTURE_MARKERS.search(prompt))


def make_verbose(original: str, variant: int) -> str:
    """Create a deliberately verbose version of a concise prompt."""
    p = original.strip()
    if not p:
        return p

    # Don't break structured / few-shot / ReAct prompts with heavy wrappers
    if is_structured(p) and len(p) > 80:
        fillers = [
            f"I need your help with this. {p} Please make sure you keep all the required details.",
            f"Could you please handle the following carefully? {p} Thanks.",
            f"When you have a moment, please work on this: {p}",
            f"I would really appreciate your help here: {p} Please be thorough.",
            f"Can you please take care of the following task? {p}",
            f"If possible, please complete this exactly as described: {p}",
            f"I was hoping you could help me with this: {p} Thank you.",
            f"Would you mind helping with the following? {p}",
            f"Please help me with this when you can: {p}",
            f"Could you kindly assist with this? {p} I appreciate it.",
        ]
        return fillers[variant % len(fillers)]

    lower = p[0].lower() + p[1:] if len(p) > 1 else p.lower()
    if p.endswith("?"):
        question_wrappers = [
            "Can you please answer this question: {q}",
            "Could you kindly help me with this: {q}",
            "I was wondering if you could please tell me {q_lower}",
            "Would you mind answering the following: {q}",
            "If possible, can you please respond to this: {q}",
            "Hey, can you please help me figure out {q_lower}",
            "Do you think you could answer {q_lower}",
            "It would be great if you could explain {q_lower}",
            "Can I ask you to please address this: {q}",
            "I would really appreciate it if you could answer {q_lower}",
        ]
        w = question_wrappers[variant % len(question_wrappers)]
        suffix = VERBOSITY_SUFFIXES[variant % len(VERBOSITY_SUFFIXES)]
        q_lower = lower.rstrip("?") + "?"
        return w.format(q=p, q_lower=q_lower) + suffix

    lower = lower.rstrip(".")
    prefix = VERBOSITY_PREFIXES[variant % len(VERBOSITY_PREFIXES)]
    suffix = VERBOSITY_SUFFIXES[variant % len(VERBOSITY_SUFFIXES)]
    return f"{prefix}{lower}.{suffix}"


def optimize_prompt(prompt: str, concise_target: str | None = None) -> str:
    """Optimize while preserving meaning, constraints, roles, and examples."""
    text = " ".join(prompt.split()).strip()
    if not text:
        return text

    structured = is_structured(text)

    # Remove common verbose wrappers at edges
    wrapper_patterns = [
        r"^(?:I need your help with this\.|Could you please handle the following carefully\?|"
        r"When you have a moment, please work on this:|I would really appreciate your help here:|"
        r"Can you please take care of the following task\?|If possible, please complete this exactly as described:|"
        r"I was hoping you could help me with this:|Would you mind helping with the following\?|"
        r"Please help me with this when you can:|Could you kindly assist with this\?|"
        r"Can you please answer this question:|Could you kindly help me with this:|"
        r"I was wondering if you could please tell me |Would you mind answering the following:|"
        r"If possible, can you please respond to this:|Hey, can you please help me figure out |"
        r"Do you think you could answer |It would be great if you could explain |"
        r"Can I ask you to please address this:|I would really appreciate it if you could answer )\s*",
        r"\s*(?:Please make sure you keep all the required details\.|Thanks\.|Thank you\.|"
        r"I appreciate it\.|I would really appreciate your help\.|thanks in advance\.|"
        r"please and thank you\.|I hope that makes sense\.|let me know if you need more context\.|"
        r"that would be really helpful\.|as soon as you can\.|if possible\.|when you get a chance\.|"
        r"if that is okay\.)\s*$",
    ]
    for pat in wrapper_patterns:
        text = re.sub(pat, "", text, flags=re.IGNORECASE).strip()

    if not structured:
        for pat, repl in FILLER_PATTERNS:
            text = re.sub(pat, repl, text, flags=re.IGNORECASE)
        text = re.sub(r"^\s*(?:and\s+)?", "", text, flags=re.IGNORECASE)
        text = text.strip(" .")
        if text and not text.endswith(("?", ".", ":", '"', "'")):
            first_word = text.split()[0].lower() if text.split() else ""
            if first_word in {"what", "who", "how", "why", "when", "where", "which", "is", "are", "can", "do"}:
                text = text.rstrip(".") + "?"
            else:
                text += "."

    # Normalize spacing around punctuation
    text = re.sub(r"\s+([,.;:?])", r"\1", text)
    text = re.sub(r"\?{2,}", "?", text)
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r"\s{2,}", " ", text).strip()

    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]

    # Prefer concise target when rule-based output is not shorter
    if concise_target:
        concise_target = " ".join(concise_target.split()).strip()
        if count_tokens(text) >= count_tokens(prompt) or count_tokens(text) > count_tokens(concise_target):
            text = concise_target

    return text


def load_source_prompts(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [r["Prompt"].strip() for r in rows if r.get("Prompt", "").strip()]


def generate_extra_prompts(target: int) -> list[str]:
    """Generate additional diverse base prompts to reach target originals."""
    tasks = [
        "summarize this article",
        "translate this text to Spanish",
        "classify the sentiment",
        "extract the date from the sentence",
        "write a product description",
        "solve the math problem step by step",
        "explain the concept in simple terms",
        "generate Python code for the task",
        "answer the question accurately",
        "create a short dialogue response",
    ]
    topics = [
        "machine learning",
        "climate change",
        "remote work",
        "customer support",
        "public health",
        "software debugging",
        "urban planning",
        "financial literacy",
        "renewable energy",
        "cybersecurity",
    ]
    extras = []
    i = 0
    while len(extras) < target:
        task = tasks[i % len(tasks)]
        topic = topics[(i // len(tasks)) % len(topics)]
        variant = i // (len(tasks) * len(topics))
        extras.append(f"{task} about {topic} variant {variant}")
        i += 1
    return extras[:target]


def build_dataset(source_path: Path, output_path: Path, target_entries: int = 10000) -> None:
    base_prompts = load_source_prompts(source_path)
    seen_originals: set[str] = set()
    pairs: list[tuple[str, str]] = []

    # 10 verbose variants per base prompt until we reach target
    variant_idx = 0
    base_cycle = 0
    while len(pairs) < target_entries:
        if base_cycle < len(base_prompts):
            base = base_prompts[base_cycle]
        else:
            # Extend with generated bases if needed (shouldn't happen with 1000*10)
            extra_needed = base_cycle - len(base_prompts) + 1
            extras = generate_extra_prompts(extra_needed)
            base = extras[-1]

        original = make_verbose(base, variant_idx)
        optimized = optimize_prompt(original, concise_target=base)

        if not optimized or not original:
            variant_idx += 1
            if variant_idx >= 10:
                variant_idx = 0
                base_cycle += 1
            continue

        if optimized == original:
            variant_idx += 1
            if variant_idx >= 10:
                variant_idx = 0
                base_cycle += 1
            continue

        if original not in seen_originals:
            seen_originals.add(original)
            pairs.append((original, optimized))

        variant_idx += 1
        if variant_idx >= 10:
            variant_idx = 0
            base_cycle += 1

        if base_cycle > len(base_prompts) * 20 and len(pairs) < target_entries:
            break

    pairs = pairs[:target_entries]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["original_prompt", "optimized_prompt"])
        writer.writeheader()
        for orig, opt in pairs:
            writer.writerow({"original_prompt": orig, "optimized_prompt": opt})

    # Stats
    orig_tokens = [count_tokens(o) for o, _ in pairs]
    opt_tokens = [count_tokens(p) for _, p in pairs]
    reduced = sum(1 for o, p in zip(orig_tokens, opt_tokens) if p < o)
    same = sum(1 for o, p in zip(orig_tokens, opt_tokens) if p == o)
    print(f"Wrote {len(pairs)} rows to {output_path}")
    print(f"Unique originals: {len(seen_originals)}")
    print(f"Reduced tokens: {reduced} ({100*reduced/len(pairs):.1f}%)")
    print(f"Same tokens: {same} ({100*same/len(pairs):.1f}%)")
    print(f"Avg original tokens: {sum(orig_tokens)/len(pairs):.1f}")
    print(f"Avg optimized tokens: {sum(opt_tokens)/len(pairs):.1f}")


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    build_dataset(
        source_path=root / "prompts_dataset.csv",
        output_path=root / "prompt_optimization_dataset.csv",
        target_entries=10000,
    )
