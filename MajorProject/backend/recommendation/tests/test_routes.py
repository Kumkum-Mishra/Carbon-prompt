"""Integration tests for the POST /recommend endpoint."""

import pytest
from fastapi.testclient import TestClient

from main import app
from recommendation.dataset_loader import clear_dataset_cache


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_cache() -> None:
    clear_dataset_cache()
    yield
    clear_dataset_cache()


class TestRecommendRoute:
    def test_raw_prompt(self, client: TestClient) -> None:
        response = client.post("/recommend", json={"prompt": "Write CNN code"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["recommendation"]["task_type"] == "Coding"

    def test_pre_analyzed_input(self, client: TestClient) -> None:
        response = client.post(
            "/recommend",
            json={"task_type": "Coding", "category": "Coding"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["recommendation"]["category"] == "Coding"

    def test_response_schema(self, client: TestClient) -> None:
        response = client.post("/recommend", json={"task_type": "Coding"})
        recommendation = response.json()["recommendation"]
        assert {
            "category",
            "task_type",
            "recommended_model",
            "score",
            "score_type",
            "baseline_gmes",
            "weights",
            "features",
            "priorities",
            "top_models",
            "reason",
        }.issubset(set(recommendation.keys()))
        assert set(recommendation["top_models"][0].keys()) == {
            "model",
            "score",
            "speed",
            "latency",
            "context",
            "cost_efficiency",
            "baseline_gmes",
        }

    def test_missing_fields(self, client: TestClient) -> None:
        response = client.post("/recommend", json={})
        assert response.status_code == 400
        assert response.json()["message"] == "Missing required analyzer fields."

    def test_unknown_task_type(self, client: TestClient) -> None:
        response = client.post("/recommend", json={"task_type": "Unknown"})
        assert response.status_code == 400
        assert response.json()["message"] == "Category not recognized."

    def test_empty_prompt(self, client: TestClient) -> None:
        response = client.post("/recommend", json={"prompt": ""})
        assert response.status_code == 400
        assert response.json()["message"] == "Prompt cannot be empty."

    def test_translation_uses_text_category(self, client: TestClient) -> None:
        response = client.post(
            "/recommend",
            json={"prompt": "Translate this paragraph into Hindi."},
        )
        data = response.json()
        assert data["recommendation"]["category"] == "Text"

    def test_analyzer_to_recommend_pipeline(self, client: TestClient) -> None:
        analyze_response = client.post(
            "/analyze", json={"prompt": "Write Python code for CNN"}
        )
        analysis = analyze_response.json()["analysis"]

        recommend_response = client.post(
            "/recommend",
            json={
                "task_type": analysis["task_type"],
                "category": analysis["category"],
            },
        )
        assert recommend_response.status_code == 200
        assert recommend_response.json()["success"] is True

    def test_top_models_sorted_by_score(self, client: TestClient) -> None:
        response = client.post("/recommend", json={"task_type": "Coding"})
        top_models = response.json()["recommendation"]["top_models"]
        scores = [model["score"] for model in top_models]
        assert scores == sorted(scores, reverse=True)

    def test_reasons_present(self, client: TestClient) -> None:
        response = client.post(
            "/recommend",
            json={"prompt": "Quickly search for the latest AI news."},
        )
        reasons = response.json()["recommendation"]["reason"]
        assert len(reasons) >= 1
        assert any("GMES" in reason or "DGMES" in reason for reason in reasons)
