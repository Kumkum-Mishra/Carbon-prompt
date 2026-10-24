"""Unit tests for request schema validation."""

import pytest
from pydantic import ValidationError

from analyzer.config import MAX_PROMPT_LENGTH
from analyzer.schemas import AnalyzeRequest


class TestAnalyzeRequest:
    def test_valid_prompt(self) -> None:
        req = AnalyzeRequest(prompt="Write CNN code")
        assert req.prompt == "Write CNN code"

    def test_strips_not_applied_at_schema_level(self) -> None:
        req = AnalyzeRequest(prompt="  valid prompt  ")
        assert req.prompt == "  valid prompt  "

    def test_empty_prompt(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeRequest(prompt="")
        assert "Prompt cannot be empty." in str(exc_info.value)

    def test_whitespace_only(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeRequest(prompt="   ")
        assert "Prompt cannot be empty." in str(exc_info.value)

    def test_too_short(self) -> None:
        with pytest.raises(ValidationError):
            AnalyzeRequest(prompt="a")

    def test_too_long(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeRequest(prompt="x" * (MAX_PROMPT_LENGTH + 1))
        assert "Prompt exceeds maximum length." in str(exc_info.value)
