"""Integration tests for POST /process endpoint."""

import pytest
from fastapi.testclient import TestClient

from app import app
from optimizer.optimizer import PromptOptimizer
from optimizer.providers.mock_provider import MockLLMProvider
from recommendation.dataset_loader import clear_dataset_cache
from routes.process import _pipeline_service
from services.module_registry import reset_module_registry


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def mock_optimizer() -> None:
    reset_module_registry()
    clear_dataset_cache()
    _pipeline_service._registry.optimizer._optimizer = PromptOptimizer(
        provider=MockLLMProvider(optimized_prompt="Write a PyTorch CNN implementation.")
    )
    yield
    reset_module_registry()
    clear_dataset_cache()


class TestProcessRoute:
    def test_valid_prompt(self, client: TestClient) -> None:
        response = client.post("/process", json={"prompt": "Write CNN code using PyTorch."})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "pipeline" in data
        assert "metadata" in data

    def test_pipeline_response_schema(self, client: TestClient) -> None:
        response = client.post("/process", json={"prompt": "Write CNN code using PyTorch."})
        pipeline = response.json()["pipeline"]
        assert set(pipeline.keys()) == {
            "analysis",
            "carbon",
            "optimization",
            "recommendation",
        }
        assert set(pipeline["carbon"].keys()) == {"original", "optimized"}
        assert pipeline["analysis"]["task_type"] == "Coding"
        assert pipeline["recommendation"]["recommended_model"]

    def test_metadata_includes_timing(self, client: TestClient) -> None:
        response = client.post("/process", json={"prompt": "Write CNN code using PyTorch."})
        metadata = response.json()["metadata"]
        assert "processing_time_ms" in metadata
        assert "pipeline_version" in metadata
        assert metadata["processing_time_ms"] >= 0

    def test_empty_prompt(self, client: TestClient) -> None:
        response = client.post("/process", json={"prompt": ""})
        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_missing_prompt(self, client: TestClient) -> None:
        response = client.post("/process", json={})
        assert response.status_code == 400

    def test_processing_time_header(self, client: TestClient) -> None:
        response = client.post("/process", json={"prompt": "Write CNN code using PyTorch."})
        assert "X-Processing-Time-Ms" in response.headers

    def test_pipeline_failure_on_optimization(self, client: TestClient) -> None:
        _pipeline_service._registry.optimizer._optimizer = PromptOptimizer(
            provider=MockLLMProvider(optimized_prompt="")
        )
        response = client.post("/process", json={"prompt": "Write CNN code using PyTorch."})
        assert response.status_code == 500
        data = response.json()
        assert data["success"] is False
        assert "optimization" in data["message"].lower()
