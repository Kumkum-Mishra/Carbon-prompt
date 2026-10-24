"""Unit tests for recommendation service orchestration."""

import os

import pytest

from recommendation.dataset_loader import clear_dataset_cache
from recommendation.recommendation_service import RecommendationService


@pytest.fixture(autouse=True)
def clear_cache() -> None:
    clear_dataset_cache()
    yield
    clear_dataset_cache()


@pytest.fixture
def service() -> RecommendationService:
    return RecommendationService()


class TestRecommendationService:
    def test_recommend_from_task_type_coding(self, service: RecommendationService) -> None:
        result = service.recommend_from_task_type(task_type="Coding")
        assert result.success is True
        assert result.recommendation.category == "Coding"
        assert result.recommendation.recommended_model
        assert len(result.recommendation.top_models) <= 5
        assert result.recommendation.reason

    def test_recommend_from_task_type_text(self, service: RecommendationService) -> None:
        result = service.recommend_from_task_type(task_type="Writing")
        assert result.success is True
        assert result.recommendation.category == "Text"

    def test_recommend_from_task_type_math(self, service: RecommendationService) -> None:
        result = service.recommend_from_task_type(task_type="Mathematics")
        assert result.success is True
        assert result.recommendation.category == "Math"

    def test_recommend_from_raw_prompt(self, service: RecommendationService) -> None:
        result = service.recommend_from_raw_prompt("Write Python code for CNN using PyTorch")
        assert result.success is True
        assert result.recommendation.task_type == "Coding"
        assert result.recommendation.category == "Coding"

    def test_unknown_task_type(self, service: RecommendationService) -> None:
        result = service.recommend_from_task_type(task_type="Unknown")
        assert result.success is False
        assert result.message == "Category not recognized."

    def test_top_model_has_highest_score(self, service: RecommendationService) -> None:
        result = service.recommend_from_task_type(task_type="Coding")
        top_models = result.recommendation.top_models
        assert top_models[0].score >= top_models[-1].score

    def test_image_generation_prompt(self, service: RecommendationService) -> None:
        result = service.recommend_from_raw_prompt("Generate an image of a sunset.")
        assert result.success is True
        assert result.recommendation.category == "Image"

    def test_search_prompt(self, service: RecommendationService) -> None:
        result = service.recommend_from_raw_prompt("Search for the latest AI news.")
        assert result.success is True
        assert result.recommendation.category == "Search"

    def test_dynamic_dgmes_returns_weights(self, service: RecommendationService) -> None:
        result = service.recommend_from_raw_prompt(
            "Quickly tell me: What is the capital of Japan?"
        )
        assert result.success is True
        assert result.recommendation.score_type == "DGMES"
        assert result.recommendation.weights is not None
        assert result.recommendation.features is not None
        assert result.recommendation.priorities is not None
        total = (
            result.recommendation.weights.speed
            + result.recommendation.weights.latency
            + result.recommendation.weights.context
            + result.recommendation.weights.cost_efficiency
        )
        assert abs(total - 1.0) < 1e-6

    def test_equal_gmes_mode(self, service: RecommendationService, monkeypatch) -> None:
        monkeypatch.setenv("RECOMMENDATION_SCORING_MODE", "equal_gmes")
        result = service.recommend_from_raw_prompt("What is AI?")
        assert result.success is True
        assert result.recommendation.score_type == "GMES"
        assert result.recommendation.weights is None
