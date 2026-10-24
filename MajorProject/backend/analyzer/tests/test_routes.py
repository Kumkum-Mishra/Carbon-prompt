"""Integration tests for the POST /analyze endpoint."""

import pytest
from fastapi.testclient import TestClient

from analyzer.config import MAX_PROMPT_LENGTH, PROMPT_TYPES, TASK_CATEGORIES
from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestAnalyzeRoute:
    def test_valid_prompt(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": "Write CNN code"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "analysis" in data

    def test_response_contains_required_fields(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": "Write Python code for CNN."})
        data = response.json()
        analysis = data["analysis"]
        assert isinstance(analysis["token_count"], int)
        assert analysis["task_type"] in TASK_CATEGORIES
        assert analysis["prompt_type"] in PROMPT_TYPES
        assert analysis["category"] == analysis["task_type"]
        assert "character_count" in analysis
        assert "word_count" in analysis

    def test_missing_prompt(self, client: TestClient) -> None:
        response = client.post("/analyze", json={})
        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_null_prompt(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": None})
        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_non_string_prompt(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": 12345})
        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_empty_prompt(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": ""})
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Prompt cannot be empty."

    def test_whitespace_only_prompt(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": "   "})
        assert response.status_code == 400
        assert response.json()["message"] == "Prompt cannot be empty."

    def test_prompt_too_short(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": "a"})
        assert response.status_code == 400
        assert response.json()["success"] is False

    def test_prompt_too_long(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": "x" * (MAX_PROMPT_LENGTH + 1)})
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Prompt exceeds maximum length."

    def test_valid_coding_prompt(self, client: TestClient) -> None:
        response = client.post(
            "/analyze", json={"prompt": "Write Python code to implement CNN."}
        )
        data = response.json()
        assert data["analysis"]["task_type"] == "Coding"

    def test_valid_role_prompt(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": "Act as a software engineer."})
        data = response.json()
        assert data["analysis"]["prompt_type"] == "Role Prompting"

    def test_valid_chain_of_thought_prompt(self, client: TestClient) -> None:
        response = client.post("/analyze", json={"prompt": "Think step by step."})
        data = response.json()
        assert data["analysis"]["prompt_type"] == "Chain of Thought"

    def test_invalid_json_body(self, client: TestClient) -> None:
        response = client.post(
            "/analyze",
            content="not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400
        assert response.json()["success"] is False
