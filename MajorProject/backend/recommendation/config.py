"""Configuration for the Model Recommendation module."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

TOP_N_MODELS: int = 5
GMES_DECIMAL_PLACES: int = 2
DGMES_DECIMAL_PLACES: int = 2
COST_EFFICIENCY_DECIMAL_PLACES: int = 1
WEIGHT_DECIMAL_PLACES: int = 4

# equal_gmes = fixed equal weights; dynamic_dgmes = prompt-dependent weights (PRD 9)
RECOMMENDATION_SCORING_MODE: str = os.getenv(
    "RECOMMENDATION_SCORING_MODE", "dynamic_dgmes"
)


def get_recommendation_scoring_mode() -> str:
    """Read scoring mode at call time so tests and env changes apply immediately."""
    return os.getenv("RECOMMENDATION_SCORING_MODE", RECOMMENDATION_SCORING_MODE)

# Dynamic weighting constants (PRD 9)
T_CONTEXT_REF: int = int(os.getenv("T_CONTEXT_REF", "80000"))
CONTEXT_PRIORITY_FLOOR: float = 0.05
T_OUT_SPEED_LOW: int = 100
T_OUT_SPEED_HIGH: int = 500
SPEED_PRIORITY_LOW: float = 0.25
SPEED_PRIORITY_MEDIUM: float = 0.55
SPEED_PRIORITY_HIGH: float = 1.0
LATENCY_PRIORITY_HIGH: float = 1.0
LATENCY_PRIORITY_LOW: float = 0.30
T_TOTAL_COST_LOW: int = 500
T_TOTAL_COST_HIGH: int = 5000
COST_PRIORITY_LOW: float = 0.20
COST_PRIORITY_MEDIUM: float = 0.50
COST_PRIORITY_HIGH: float = 1.0
COST_SENSITIVITY_BOOST: float = 0.25
T_OUT_MIN: int = 20
T_OUT_MAX: int = 20000
TOKENS_PER_WORD: float = 1.3

TASK_OUTPUT_BASE_TOKENS: dict[str, int] = {
    "Question Answering": 80,
    "Search": 120,
    "Summarization": 250,
    "Translation": 200,
    "Writing": 600,
    "Reasoning": 400,
    "Coding": 350,
    "Mathematics": 200,
    "General": 150,
    "Vision Analysis": 200,
    "Image Generation": 60,
}

DETAIL_LOW_KEYWORDS: tuple[str, ...] = (
    "brief",
    "short",
    "tl;dr",
    "one sentence",
    "concise",
)

DETAIL_HIGH_KEYWORDS: tuple[str, ...] = (
    "detailed",
    "comprehensive",
    "step by step",
    "step-by-step",
    "in depth",
    "in-depth",
    "long form",
    "long-form",
    "thorough",
    "extensive",
)
UNIFIED_DATASET_PATH: Path = PROJECT_ROOT / "model_data.csv"
DATA_DIR: Path = Path(__file__).parent / "data"

TASK_TYPE_TO_CATEGORY: dict[str, str] = {
    "Coding": "Coding",
    "Mathematics": "Math",
    "Writing": "Text",
    "Summarization": "Text",
    "Translation": "Text",
    "Question Answering": "Text",
    "Reasoning": "Text",
    "Image Generation": "Image",
    "Vision Analysis": "Vision",
    "Search": "Search",
    "General": "Text",
}

CATEGORY_TO_CSV_KEY: dict[str, str] = {
    "Coding": "coding",
    "Math": "math",
    "Text": "text",
    "Image": "image",
    "Vision": "vision",
    "Search": "search",
}

CATEGORY_FALLBACK_CSV_KEY: dict[str, str] = {
    "Math": "coding",
    "Image": "text",
}

CATEGORY_TO_DATASET_FILE: dict[str, str] = {
    "Coding": "coding_models.csv",
    "Math": "math_models.csv",
    "Text": "text_models.csv",
    "Image": "image_models.csv",
    "Vision": "vision_models.csv",
    "Search": "search_models.csv",
}

SUPPORTED_TASK_TYPES: list[str] = list(TASK_TYPE_TO_CATEGORY.keys())
