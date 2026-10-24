"""Unit tests for token counting."""

import pytest

from analyzer.tokenizer import TokenizerError, count_tokens


class TestTokenizer:
    def test_simple_prompt(self) -> None:
        count = count_tokens("Explain Artificial Intelligence.")
        assert count == 5

    def test_returns_integer(self) -> None:
        count = count_tokens("Hello world")
        assert isinstance(count, int)
        assert count > 0

    def test_empty_string(self) -> None:
        count = count_tokens("")
        assert count == 0

    def test_coding_prompt(self) -> None:
        count = count_tokens("Write CNN code")
        assert count == 3

    def test_tokenizer_error_on_invalid_encoding(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def raise_error(_: str) -> None:
            raise RuntimeError("encoding unavailable")

        monkeypatch.setattr("analyzer.tokenizer.tiktoken.get_encoding", raise_error)
        monkeypatch.setattr("analyzer.tokenizer._encoding", None)

        with pytest.raises(TokenizerError, match="Unable to calculate tokens."):
            count_tokens("test prompt")
