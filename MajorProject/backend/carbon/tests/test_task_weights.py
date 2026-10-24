"""Unit tests for task weight lookup."""

import pytest

from carbon.task_weights import UnknownTaskTypeError, get_all_task_weights, get_task_weight


class TestTaskWeights:
    def test_coding_weight(self) -> None:
        assert get_task_weight("Coding") == 1.4

    def test_mathematics_weight(self) -> None:
        assert get_task_weight("Mathematics") == 1.5

    def test_writing_weight(self) -> None:
        assert get_task_weight("Writing") == 1.2

    def test_unknown_task_type(self) -> None:
        with pytest.raises(UnknownTaskTypeError, match="Task type not recognized."):
            get_task_weight("Unknown Task")

    def test_all_supported_types_present(self) -> None:
        weights = get_all_task_weights()
        assert "Coding" in weights
        assert "Mathematics" in weights
        assert "General" in weights
        assert len(weights) == 11
