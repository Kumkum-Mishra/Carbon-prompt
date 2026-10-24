"""Parse and normalize raw model metric values."""

import re


def parse_speed(value: str) -> float | None:
    """Parse speed strings such as '56 tps'."""
    if not value or value.strip().lower() == "null":
        return None
    match = re.search(r"([\d.]+)", value)
    return float(match.group(1)) if match else None


def parse_latency(value: str) -> float | None:
    """Parse latency strings such as '1.6s'."""
    if not value or value.strip().lower() == "null":
        return None
    match = re.search(r"([\d.]+)", value)
    return float(match.group(1)) if match else None


def parse_context(value: str) -> float | None:
    """Parse context strings such as '200K' or '1M'."""
    if not value or value.strip().lower() == "null":
        return None
    normalized = value.strip().upper().replace(",", "")
    match = re.match(r"([\d.]+)\s*([KMB])?", normalized)
    if not match:
        return None
    amount = float(match.group(1))
    suffix = match.group(2)
    multipliers = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}
    return amount * multipliers.get(suffix, 1)


def parse_cost(value: str) -> float | None:
    """Parse cost strings such as '$5.00'."""
    if not value or value.strip().lower() == "null":
        return None
    match = re.search(r"([\d.]+)", value.replace("$", ""))
    return float(match.group(1)) if match else None


def normalize_higher_better(values: list[float]) -> list[float]:
    """Normalize values to 0-100 where higher raw values score higher."""
    if not values:
        return []
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        return [100.0 for _ in values]
    return [round(100 * (value - minimum) / (maximum - minimum), 2) for value in values]


def normalize_lower_better(values: list[float]) -> list[float]:
    """Normalize values to 0-100 where lower raw values score higher."""
    if not values:
        return []
    minimum = min(values)
    maximum = max(values)
    if maximum == minimum:
        return [100.0 for _ in values]
    return [
        round(100 * (maximum - value) / (maximum - minimum), 2) for value in values
    ]
