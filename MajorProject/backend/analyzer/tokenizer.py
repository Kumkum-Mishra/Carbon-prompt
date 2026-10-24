"""Token counting using tiktoken."""

import tiktoken

from analyzer.config import TOKENIZER_ENCODING


class TokenizerError(Exception):
    """Raised when tokenization fails."""


_encoding: tiktoken.Encoding | None = None


def _get_encoding() -> tiktoken.Encoding:
    global _encoding
    if _encoding is None:
        try:
            _encoding = tiktoken.get_encoding(TOKENIZER_ENCODING)
        except Exception as exc:
            raise TokenizerError("Unable to calculate tokens.") from exc
    return _encoding


def count_tokens(prompt: str) -> int:
    """Return the exact input token count for the given prompt."""
    try:
        encoding = _get_encoding()
        return len(encoding.encode(prompt))
    except TokenizerError:
        raise
    except Exception as exc:
        raise TokenizerError("Unable to calculate tokens.") from exc
