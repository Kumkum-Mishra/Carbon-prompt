"""Integration tests for the POST /optimize endpoint."""

import pytest
from fastapi.testclient import TestClient

from analyzer.analyzer import PromptAnalyzer
from carbon.carbon_service import CarbonService
from main import app
from optimizer.optimization_service import OptimizationService
from optimizer.optimizer import PromptOptimizer
from optimizer.providers.mock_provider import MockLLMProvider
from optimizer.routes import _optimization_service


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def mock_optimizer_service() -> None:
    _optimization_service._optimizer = PromptOptimizer(
        provider=MockLLMProvider(
            optimized_prompt=(
                "Explain artificial intelligence with examples and its "
                "applications across industries."
            )
        )
    )
    _optimization_service._analyzer = PromptAnalyzer()
    _optimization_service._carbon_service = CarbonService(
        analyzer=_optimization_service._analyzer
    )


class TestOptimizeRoute:
    def test_valid_prompt(self, client: TestClient) -> None:
        response = client.post(
            "/optimize",
            json={
                "prompt": (
                    "Can you please explain artificial intelligence in great detail "
                    "with lots of examples?"
                )
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "optimization" in data

    def test_response_schema(self, client: TestClient) -> None:
        response = client.post("/optimize", json={"prompt": "Explain AI in detail."})
        optimization = response.json()["optimization"]
        assert set(optimization.keys()) == {
            "original_prompt",
            "optimized_prompt",
            "original_tokens",
            "optimized_tokens",
            "token_reduction_percent",
            "original_carbon_score",
            "optimized_carbon_score",
            "carbon_reduction_percent",
            "original_task_type",
            "optimized_task_type",
            "original_prompt_type",
            "optimized_prompt_type",
        }

    def test_empty_prompt(self, client: TestClient) -> None:
        response = client.post("/optimize", json={"prompt": ""})
        assert response.status_code == 400
        assert response.json()["message"] == "Prompt cannot be empty."

    def test_whitespace_only_prompt(self, client: TestClient) -> None:
        response = client.post("/optimize", json={"prompt": "   "})
        assert response.status_code == 400
        assert response.json()["message"] == "Prompt cannot be empty."

    def test_missing_prompt(self, client: TestClient) -> None:
        response = client.post("/optimize", json={})
        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_non_string_prompt(self, client: TestClient) -> None:
        response = client.post("/optimize", json={"prompt": 123})
        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_llm_failure(self, client: TestClient) -> None:
        _optimization_service._optimizer = PromptOptimizer(
            provider=MockLLMProvider(optimized_prompt="")
        )
        response = client.post("/optimize", json={"prompt": "Explain AI in detail."})
        assert response.status_code == 400
        assert response.json()["message"] == "Optimization failed."

    def test_complete_pipeline_metrics(self, client: TestClient) -> None:
        response = client.post(
            "/optimize",
            json={
                "prompt": (
                    "Can you please explain artificial intelligence in great detail "
                    "with lots of examples and also discuss its applications in "
                    "different industries?"
                )
            },
        )
        data = response.json()["optimization"]
        reduced = data["original_tokens"] > data["optimized_tokens"]
        constrained = any(
            marker in data["optimized_prompt"].lower()
            for marker in ("word", "bullet", "simple", "fluff", "core idea")
        )
        assert reduced or constrained
        assert data["original_carbon_score"] > 0
        assert data["optimized_carbon_score"] > 0

    def test_rule_based_provider_integration(self, client: TestClient) -> None:
        from optimizer.providers.rule_based_provider import RuleBasedProvider

        _optimization_service._optimizer = PromptOptimizer(provider=RuleBasedProvider())
        response = client.post(
            "/optimize",
            json={"prompt": "Can you please explain artificial intelligence in detail?"},
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
