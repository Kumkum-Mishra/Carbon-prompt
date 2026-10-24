"""Configuration for the Prompt Optimization module."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = Path(__file__).resolve().parents[1]

# Load project .env before reading optimizer settings so LLM_PROVIDER is reliable.
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(BACKEND_DIR / ".env")

MAX_PROMPT_LENGTH: int = 10_000
MIN_PROMPT_LENGTH: int = 2
LOG_FULL_PROMPT: bool = os.getenv("LOG_FULL_PROMPT", "false").lower() == "true"

LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "trained_model")
LLM_MODEL: str = os.getenv("LLM_MODEL", "")
LLM_TIMEOUT_SECONDS: float = float(os.getenv("LLM_TIMEOUT_SECONDS", "30"))
LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "1"))

_raw_model_path = os.getenv(
    "TRAINED_MODEL_PATH", str(PROJECT_ROOT / "models" / "greenprompt_model")
)
_model_path = Path(_raw_model_path)
if not _model_path.is_absolute():
    _model_path = PROJECT_ROOT / _model_path
TRAINED_MODEL_PATH: Path = _model_path.resolve()
TRAINED_MODEL_DEVICE: str = os.getenv("TRAINED_MODEL_DEVICE", "auto")
OPTIMIZER_NUM_CANDIDATES: int = int(os.getenv("OPTIMIZER_NUM_CANDIDATES", "5"))
OPTIMIZER_NUM_BEAMS: int = int(os.getenv("OPTIMIZER_NUM_BEAMS", "5"))
OPTIMIZER_MAX_NEW_TOKENS: int = int(os.getenv("OPTIMIZER_MAX_NEW_TOKENS", "96"))
OPTIMIZER_TASK_PREFIX: str = os.getenv(
    "OPTIMIZER_TASK_PREFIX",
    "Simplify this prompt while preserving meaning: ",
)
SEMANTIC_SIMILARITY_THRESHOLD: float = float(
    os.getenv("SEMANTIC_SIMILARITY_THRESHOLD", "0.50")
)
# When true, merge rule-based output-constraint candidates alongside the
# primary provider (e.g. FLAN-T5). Does not replace the trained model.
ENABLE_CONSTRAINT_RULES: bool = (
    os.getenv("ENABLE_CONSTRAINT_RULES", "true").lower() == "true"
)

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

SYSTEM_PROMPT_PATH: Path = (
    Path(__file__).parent / "prompts" / "optimizer_system_prompt.txt"
)

DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "gemini": "gemini-2.0-flash",
    "trained_model": str(TRAINED_MODEL_PATH),
    "rule_based": "rule-based",
    "mock": "mock",
}

PERCENT_DECIMAL_PLACES: int = 2
