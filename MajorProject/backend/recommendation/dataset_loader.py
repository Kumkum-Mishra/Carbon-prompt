"""Load and cache model datasets from CSV."""

import csv
import logging
from dataclasses import dataclass
from pathlib import Path

from recommendation.category_mapper import (
    get_csv_filter_key,
    get_dataset_filename,
    get_fallback_csv_key,
)
from recommendation.config import UNIFIED_DATASET_PATH
from recommendation.normalizers import (
    normalize_higher_better,
    normalize_lower_better,
    parse_context,
    parse_cost,
    parse_latency,
    parse_speed,
)
from recommendation.scorer import ScoredModel, score_model

logger = logging.getLogger(__name__)

_REQUIRED_COLUMNS = {
    "full_name_of_model",
    "category",
    "speed",
    "latency",
    "context",
    "input_cost",
    "output_cost",
}


class DatasetNotFoundError(Exception):
    """Raised when the dataset file cannot be found."""


class EmptyDatasetError(Exception):
    """Raised when no models are available for a category."""


class DatasetLoadError(Exception):
    """Raised when dataset loading or validation fails."""


@dataclass(frozen=True)
class RawModelRow:
    model: str
    category: str
    speed: float | None
    latency: float | None
    context: float | None
    input_cost: float | None
    output_cost: float | None


_cache: dict[str, list[ScoredModel]] = {}


def load_models_for_category(
    category: str,
    *,
    dataset_path: Path | None = None,
) -> list[ScoredModel]:
    """Load, normalize, and score models for the given category."""
    if category in _cache:
        return _cache[category]

    path = dataset_path or UNIFIED_DATASET_PATH
    if not path.exists():
        raise DatasetNotFoundError("Dataset not found.")

    csv_key = get_csv_filter_key(category)
    raw_rows = _load_raw_rows(path, csv_key)

    if not raw_rows:
        fallback_key = get_fallback_csv_key(category)
        if fallback_key:
            logger.warning(
                "No models for category %s; falling back to %s",
                category,
                fallback_key,
            )
            raw_rows = _load_raw_rows(path, fallback_key)

    if not raw_rows:
        raise EmptyDatasetError(f"No models available for {category}.")

    scored_models = _normalize_and_score(raw_rows)
    _cache[category] = scored_models

    logger.info(
        "Loaded dataset %s with %d models for category %s",
        get_dataset_filename(category),
        len(scored_models),
        category,
    )
    return scored_models


def clear_dataset_cache() -> None:
    """Clear the in-memory dataset cache (primarily for tests)."""
    _cache.clear()


def _load_raw_rows(path: Path, csv_key: str) -> list[RawModelRow]:
    rows: list[RawModelRow] = []

    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise DatasetLoadError("Dataset is missing a header row.")

        missing_columns = _REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            raise DatasetLoadError(
                f"Dataset is missing required columns: {', '.join(sorted(missing_columns))}"
            )

        for row_number, row in enumerate(reader, start=2):
            if row.get("category", "").strip().lower() != csv_key:
                continue

            parsed = _parse_row(row)
            if parsed is None:
                continue
            rows.append(parsed)

    return rows


def _parse_row(row: dict[str, str]) -> RawModelRow | None:
    speed = parse_speed(row.get("speed", ""))
    latency = parse_latency(row.get("latency", ""))
    context = parse_context(row.get("context", ""))
    input_cost = parse_cost(row.get("input_cost", ""))
    output_cost = parse_cost(row.get("output_cost", ""))

    model_name = row.get("full_name_of_model", "").strip()
    if not model_name:
        return None

    metrics = [speed, latency, context, input_cost, output_cost]
    if sum(value is not None for value in metrics) < 1:
        return None

    return RawModelRow(
        model=model_name,
        category=row.get("category", "").strip(),
        speed=speed,
        latency=latency,
        context=context,
        input_cost=input_cost,
        output_cost=output_cost,
    )


def _normalize_column(
    values: list[float | None],
    *,
    lower_better: bool = False,
) -> list[float]:
    present_values = [value for value in values if value is not None]
    if not present_values:
        return [50.0 for _ in values]

    normalized_present = (
        normalize_lower_better(present_values)
        if lower_better
        else normalize_higher_better(present_values)
    )

    normalized: list[float] = []
    present_index = 0
    for value in values:
        if value is None:
            normalized.append(50.0)
        else:
            normalized.append(normalized_present[present_index])
            present_index += 1
    return normalized


def _normalize_and_score(rows: list[RawModelRow]) -> list[ScoredModel]:
    speeds = _normalize_column([row.speed for row in rows])
    latencies = _normalize_column([row.latency for row in rows], lower_better=True)
    contexts = _normalize_column([row.context for row in rows])
    input_costs = _normalize_column([row.input_cost for row in rows])
    output_costs = _normalize_column([row.output_cost for row in rows])

    return [
        score_model(
            model=row.model,
            speed=speeds[index],
            latency=latencies[index],
            context=contexts[index],
            input_cost=input_costs[index],
            output_cost=output_costs[index],
        )
        for index, row in enumerate(rows)
    ]
