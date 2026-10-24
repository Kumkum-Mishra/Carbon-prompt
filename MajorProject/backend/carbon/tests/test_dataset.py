"""Unit tests for reference dataset loading."""

from pathlib import Path

import pytest

from carbon.dataset import DatasetLoadError, load_carbon_prompt_dataset


class TestDataset:
    def test_load_default_dataset(self) -> None:
        records = load_carbon_prompt_dataset()
        assert len(records) >= 1
        first = records[0]
        assert first.prompt
        assert first.prompt_type
        assert first.task_type
        assert first.token_count > 0
        assert first.carbon_score >= 0

    def test_reference_example_row(self) -> None:
        records = load_carbon_prompt_dataset()
        coding_record = next(
            record for record in records if record.prompt == "Write Python code for CNN"
        )
        assert coding_record.prompt_type == "Zero-shot"
        assert coding_record.task_type == "Coding"
        assert coding_record.token_count == 9
        assert coding_record.carbon_score == 0.000126

    def test_missing_dataset_raises(self, tmp_path: Path) -> None:
        with pytest.raises(DatasetLoadError):
            load_carbon_prompt_dataset(tmp_path / "missing.csv")
