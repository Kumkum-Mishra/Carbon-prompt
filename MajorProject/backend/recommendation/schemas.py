"""Pydantic request and response schemas for model recommendation."""

from pydantic import BaseModel, Field, field_validator

from analyzer.config import MAX_PROMPT_LENGTH, MIN_PROMPT_LENGTH
from recommendation.config import SUPPORTED_TASK_TYPES


class RecommendRequest(BaseModel):
    prompt: str = Field(..., description="Raw natural language prompt")

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Invalid prompt.")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Prompt cannot be empty.")
        if len(cleaned) < MIN_PROMPT_LENGTH:
            raise ValueError("Invalid prompt.")
        if len(cleaned) > MAX_PROMPT_LENGTH:
            raise ValueError("Prompt exceeds maximum length.")
        return value


class PreAnalyzedRecommendRequest(BaseModel):
    task_type: str = Field(..., description="Detected task category")
    category: str | None = Field(default=None, description="Optional dataset category override")

    @field_validator("task_type")
    @classmethod
    def validate_task_type(cls, value: str) -> str:
        if value not in SUPPORTED_TASK_TYPES:
            raise ValueError("Category not recognized.")
        return value


class TopModelResult(BaseModel):
    model: str
    score: float
    speed: float
    latency: float
    context: float
    cost_efficiency: float
    baseline_gmes: float | None = None


class RecommendationWeights(BaseModel):
    speed: float
    latency: float
    context: float
    cost_efficiency: float


class RecommendationFeatures(BaseModel):
    input_tokens: int
    expected_output_tokens: int
    total_tokens: int
    urgency: bool
    cost_sensitive: bool
    detail_level: str


class RecommendationPriorities(BaseModel):
    speed: float
    latency: float
    context: float
    cost_efficiency: float


class RecommendationResult(BaseModel):
    category: str
    task_type: str
    recommended_model: str
    score: float
    score_type: str = "GMES"
    baseline_gmes: float | None = None
    weights: RecommendationWeights | None = None
    features: RecommendationFeatures | None = None
    priorities: RecommendationPriorities | None = None
    top_models: list[TopModelResult]
    reason: list[str]


class RecommendSuccessResponse(BaseModel):
    success: bool = True
    recommendation: RecommendationResult


class RecommendErrorResponse(BaseModel):
    success: bool = False
    message: str
