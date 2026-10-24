"""Tests for GET /health endpoint."""

import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestHealthRoute:
    def test_health_check(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code in (200, 503)
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "modules" in data
        assert set(data["modules"].keys()) == {
            "analyzer",
            "carbon",
            "optimizer",
            "recommendation",
        }

    def test_health_modules_status(self, client: TestClient) -> None:
        response = client.get("/health")
        modules = response.json()["modules"]
        for status in modules.values():
            assert status in ("ok", "error")

    def test_healthy_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        if response.json()["status"] == "healthy":
            assert response.status_code == 200
