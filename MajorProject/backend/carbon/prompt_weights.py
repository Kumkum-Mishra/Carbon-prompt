"""Prompt-type weight lookup."""

from pathlib import Path

import yaml

_CONFIG_PATH = Path(__file__).parent / "config" / "prompt_weights.yaml"
_weights: dict[str, float] | None = None


class UnknownPromptTypeError(Exception):
    """Raised when a prompt type is not recognized."""


def _load_weights() -> dict[str, float]:
    global _weights
    if _weights is None:
        with _CONFIG_PATH.open(encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        _weights = {str(key): float(value) for key, value in raw.items()}
    return _weights


def get_prompt_weight(prompt_type: str) -> float:
    """Return the configured weight for the given prompt type."""
    weights = _load_weights()
    if prompt_type not in weights:
        raise UnknownPromptTypeError("Prompt type not recognized.")
    return weights[prompt_type]


def get_all_prompt_weights() -> dict[str, float]:
    """Return a copy of all configured prompt weights."""
    return dict(_load_weights())
