"""Unit tests for dataset loading."""

from pathlib import Path

import pytest

from recommendation.config import UNIFIED_DATASET_PATH
from recommendation.dataset_loader import (
    DatasetNotFoundError,
    clear_dataset_cache,
    load_models_for_category,
)


@pytest.fixture(autouse=True)
def clear_cache() -> None:
    clear_dataset_cache()
    yield
    clear_dataset_cache()


class TestDatasetLoader:
    def test_load_coding_models(self) -> None:
        models = load_models_for_category("Coding")
        assert len(models) > 0
        assert all(model.gmes >= 0 for model in models)

    def test_load_text_models(self) -> None:
        models = load_models_for_category("Text")
        assert len(models) > 0

    def test_load_image_models(self) -> None:
        models = load_models_for_category("Image")
        assert len(models) > 0

    def test_load_vision_models(self) -> None:
        models = load_models_for_category("Vision")
        assert len(models) > 0

    def test_load_search_models(self) -> None:
        models = load_models_for_category("Search")
        assert len(models) > 0

    def test_load_math_models_fallback(self) -> None:
        models = load_models_for_category("Math")
        assert len(models) > 0

    def test_cache_reuse(self) -> None:
        first = load_models_for_category("Coding")
        second = load_models_for_category("Coding")
        assert first is second

    def test_missing_dataset(self, tmp_path: Path) -> None:
        with pytest.raises(DatasetNotFoundError, match="Dataset not found."):
            load_models_for_category("Coding", dataset_path=tmp_path / "missing.csv")

    def test_unified_dataset_exists(self) -> None:
        assert UNIFIED_DATASET_PATH.exists()

    def test_models_have_required_fields(self) -> None:
        model = load_models_for_category("Coding")[0]
        assert model.model
        assert model.speed >= 0
        assert model.latency >= 0
        assert model.context >= 0
        assert model.cost_efficiency >= 0
        assert model.gmes >= 0
