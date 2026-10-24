"""Reference dataset loader for carbon estimation benchmarking."""

import csv
from dataclasses import dataclass
from pathlib import Path

_DEFAULT_DATASET_PATH = Path(__file__).parent / "data" / "carbon_prompt_dataset.csv"
_REQUIRED_COLUMNS = {
    "Prompt",
    "Prompt Type",
    "Task Type",
    "Token Count",
    "Carbon Score",
}


@dataclass(frozen=True)
class CarbonPromptRecord:
    prompt: str
    prompt_type: str
    task_type: str
    token_count: int
    carbon_score: float


class DatasetLoadError(Exception):
    """Raised when the reference dataset cannot be loaded."""


def load_carbon_prompt_dataset(
    path: Path | None = None,
) -> list[CarbonPromptRecord]:
    """Load the reference carbon prompt dataset from CSV."""
    dataset_path = path or _DEFAULT_DATASET_PATH

    if not dataset_path.exists():
        raise DatasetLoadError(f"Dataset not found: {dataset_path}")

    records: list[CarbonPromptRecord] = []

    with dataset_path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise DatasetLoadError("Dataset is missing a header row.")

        missing_columns = _REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            raise DatasetLoadError(
                f"Dataset is missing required columns: {', '.join(sorted(missing_columns))}"
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                records.append(
                    CarbonPromptRecord(
                        prompt=row["Prompt"],
                        prompt_type=row["Prompt Type"],
                        task_type=row["Task Type"],
                        token_count=int(row["Token Count"]),
                        carbon_score=float(row["Carbon Score"]),
                    )
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise DatasetLoadError(
                    f"Invalid dataset row at line {row_number}."
                ) from exc

    return records
