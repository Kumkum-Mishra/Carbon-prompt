"""Unit tests for task type to category mapping."""

import pytest

from recommendation.category_mapper import (
    UnknownCategoryError,
    get_csv_filter_key,
    map_task_type_to_category,
    resolve_category,
)


class TestCategoryMapper:
    def test_coding(self) -> None:
        assert map_task_type_to_category("Coding") == "Coding"

    def test_mathematics(self) -> None:
        assert map_task_type_to_category("Mathematics") == "Math"

    def test_writing(self) -> None:
        assert map_task_type_to_category("Writing") == "Text"

    def test_image_generation(self) -> None:
        assert map_task_type_to_category("Image Generation") == "Image"

    def test_vision_analysis(self) -> None:
        assert map_task_type_to_category("Vision Analysis") == "Vision"

    def test_search(self) -> None:
        assert map_task_type_to_category("Search") == "Search"

    def test_general(self) -> None:
        assert map_task_type_to_category("General") == "Text"

    def test_unknown_task_type(self) -> None:
        with pytest.raises(UnknownCategoryError, match="Category not recognized."):
            map_task_type_to_category("Unknown")

    def test_resolve_with_explicit_category(self) -> None:
        assert resolve_category("Coding", "General") == "Coding"

    def test_csv_filter_key(self) -> None:
        assert get_csv_filter_key("Coding") == "coding"
        assert get_csv_filter_key("Text") == "text"
