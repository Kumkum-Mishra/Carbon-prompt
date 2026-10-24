"""Map Prompt Analyzer task types to dataset categories."""

from recommendation.config import (
    CATEGORY_FALLBACK_CSV_KEY,
    CATEGORY_TO_CSV_KEY,
    CATEGORY_TO_DATASET_FILE,
    TASK_TYPE_TO_CATEGORY,
)


class UnknownCategoryError(Exception):
    """Raised when a task type cannot be mapped to a dataset category."""


def map_task_type_to_category(task_type: str) -> str:
    """Map a Prompt Analyzer task type to a dataset category."""
    if task_type not in TASK_TYPE_TO_CATEGORY:
        raise UnknownCategoryError("Category not recognized.")
    return TASK_TYPE_TO_CATEGORY[task_type]


def resolve_category(category: str | None, task_type: str) -> str:
    """Resolve the dataset category from explicit category or task type."""
    if category:
        if category in TASK_TYPE_TO_CATEGORY:
            return TASK_TYPE_TO_CATEGORY[category]
        normalized = _normalize_category_name(category)
        if normalized is not None:
            return normalized
        raise UnknownCategoryError("Category not recognized.")
    return map_task_type_to_category(task_type)


def get_csv_filter_key(category: str) -> str:
    """Return the CSV category key used to filter the unified dataset."""
    csv_key = CATEGORY_TO_CSV_KEY.get(category)
    if csv_key is None:
        raise UnknownCategoryError("Category not recognized.")
    return csv_key


def get_fallback_csv_key(category: str) -> str | None:
    """Return an alternate CSV key when the primary category has no models."""
    return CATEGORY_FALLBACK_CSV_KEY.get(category)


def get_dataset_filename(category: str) -> str:
    """Return the logical dataset filename for logging."""
    return CATEGORY_TO_DATASET_FILE.get(category, f"{category.lower()}_models.csv")


def _normalize_category_name(category: str) -> str | None:
    aliases = {
        "coding": "Coding",
        "math": "Math",
        "mathematics": "Math",
        "text": "Text",
        "writing": "Text",
        "image": "Image",
        "vision": "Vision",
        "search": "Search",
        "general": "Text",
    }
    if category in TASK_TYPE_TO_CATEGORY.values():
        return category
    return aliases.get(category.lower())
