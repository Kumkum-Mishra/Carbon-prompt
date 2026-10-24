"""Tests for gateway configuration."""

from config import APP_NAME, APP_VERSION, MAX_PROMPT_LENGTH, PIPELINE_VERSION


class TestConfig:
    def test_app_name(self) -> None:
        assert APP_NAME == "GreenPrompt AI"

    def test_app_version(self) -> None:
        assert APP_VERSION

    def test_max_prompt_length(self) -> None:
        assert MAX_PROMPT_LENGTH > 0

    def test_pipeline_version(self) -> None:
        assert PIPELINE_VERSION
