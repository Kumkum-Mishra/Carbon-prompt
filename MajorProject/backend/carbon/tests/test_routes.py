"""Integration tests for the POST /carbon endpoint."""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestCarbonRoute:
    def test_raw_prompt_triggers_analysis(self, client: TestClient) -> None:
        response = client.post("/carbon", json={"prompt": "Write Python code for CNN"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["carbon"]["task_type"] == "Coding"
        assert data["carbon"]["token_count"] > 0

    def test_pre_analyzed_input_skips_reanalysis(self, client: TestClient) -> None:
        response = client.post(
            "/carbon",
            json={
                "token_count": 9,
                "prompt_type": "Zero-shot",
                "task_type": "Coding",
                "prompt": "Write Python code for CNN",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["carbon"]["green_carbon_score"] == 0.000126

    def test_response_schema(self, client: TestClient) -> None:
        response = client.post(
            "/carbon",
            json={
                "token_count": 9,
                "prompt_type": "Zero-shot",
                "task_type": "Coding",
            },
        )
        carbon = response.json()["carbon"]
        assert set(carbon.keys()) == {
            "token_count",
            "prompt_type",
            "task_type",
            "prompt_weight",
            "task_weight",
            "scaling_constant",
            "green_carbon_score",
        }

    def test_missing_required_fields(self, client: TestClient) -> None:
        response = client.post("/carbon", json={"token_count": 9})
        assert response.status_code == 400
        assert response.json()["message"] == "Missing required analyzer fields."

    def test_empty_body(self, client: TestClient) -> None:
        response = client.post("/carbon", json={})
        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_unknown_prompt_type(self, client: TestClient) -> None:
        response = client.post(
            "/carbon",
            json={
                "token_count": 5,
                "prompt_type": "Unknown",
                "task_type": "Coding",
            },
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Prompt type not recognized."

    def test_unknown_task_type(self, client: TestClient) -> None:
        response = client.post(
            "/carbon",
            json={
                "token_count": 5,
                "prompt_type": "Zero-shot",
                "task_type": "Unknown",
            },
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Task type not recognized."

    def test_zero_token_count(self, client: TestClient) -> None:
        response = client.post(
            "/carbon",
            json={
                "token_count": 0,
                "prompt_type": "Zero-shot",
                "task_type": "Coding",
            },
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Token count must be a positive integer."

    def test_invalid_raw_prompt(self, client: TestClient) -> None:
        response = client.post("/carbon", json={"prompt": ""})
        assert response.status_code == 400
        assert response.json()["message"] == "Prompt cannot be empty."

    def test_few_shot_scoring_via_api(self, client: TestClient) -> None:
        response = client.post(
            "/carbon",
            json={
                "token_count": 10,
                "prompt_type": "Few-shot",
                "task_type": "Question Answering",
            },
        )
        data = response.json()
        assert data["carbon"]["prompt_weight"] == 1.2
        assert data["carbon"]["task_weight"] == 1.0
        assert data["carbon"]["green_carbon_score"] == 0.00012

    def test_chain_of_thought_mathematics(self, client: TestClient) -> None:
        response = client.post(
            "/carbon",
            json={
                "token_count": 8,
                "prompt_type": "Chain of Thought",
                "task_type": "Mathematics",
            },
        )
        data = response.json()
        assert data["carbon"]["green_carbon_score"] == 0.00018

    def test_analyzer_to_carbon_pipeline(self, client: TestClient) -> None:
        analyze_response = client.post(
            "/analyze", json={"prompt": "Write Python code for CNN"}
        )
        analysis = analyze_response.json()["analysis"]

        carbon_response = client.post(
            "/carbon",
            json={
                "token_count": analysis["token_count"],
                "prompt_type": analysis["prompt_type"],
                "task_type": analysis["task_type"],
            },
        )
        assert carbon_response.status_code == 200
        assert carbon_response.json()["success"] is True
