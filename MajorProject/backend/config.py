"""Application configuration loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).parent
_PROJECT_ROOT = _BACKEND_DIR.parent

load_dotenv(_PROJECT_ROOT / ".env")
load_dotenv(_BACKEND_DIR / ".env")

APP_NAME: str = os.getenv("APP_NAME", "GreenPrompt AI")
APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
PIPELINE_VERSION: str = os.getenv("PIPELINE_VERSION", "1.0")

MAX_PROMPT_LENGTH: int = int(os.getenv("MAX_PROMPT_LENGTH", "10000"))
DATASET_DIR: Path = Path(
    os.getenv("DATASET_DIR", str(_PROJECT_ROOT / "Dataset"))
).resolve()

LOG_DIR: Path = _BACKEND_DIR / "logs"
LOG_TO_FILE: bool = os.getenv("LOG_TO_FILE", "true").lower() == "true"
LOG_FULL_PROMPT: bool = os.getenv("LOG_FULL_PROMPT", "false").lower() == "true"

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", ""))
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "trained_model")
LLM_MODEL: str = os.getenv("LLM_MODEL", "")

CORS_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]

IS_PRODUCTION: bool = ENVIRONMENT == "production"
