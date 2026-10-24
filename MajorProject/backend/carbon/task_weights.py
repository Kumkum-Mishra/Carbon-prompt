"""Task-type weight lookup."""

from pathlib import Path

import yaml

_CONFIG_PATH = Path(__file__).parent / "config" / "task_weights.yaml"
_weights: dict[str, float] | None = None


class UnknownTaskTypeError(Exception):
    """Raised when a task type is not recognized."""


def _load_weights() -> dict[str, float]:
    global _weights
    if _weights is None:
        with _CONFIG_PATH.open(encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        _weights = {str(key): float(value) for key, value in raw.items()}
    return _weights


def get_task_weight(task_type: str) -> float:
    """Return the configured weight for the given task type."""
    weights = _load_weights()
    if task_type not in weights:
        raise UnknownTaskTypeError("Task type not recognized.")
    return weights[task_type]


def get_all_task_weights() -> dict[str, float]:
    """Return a copy of all configured task weights."""
    return dict(_load_weights())
