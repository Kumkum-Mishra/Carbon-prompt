"""Pydantic request and response schemas for prompt optimization."""

from pydantic import BaseModel, Field, field_validator

from optimizer.config import MAX_PROMPT_LENGTH, MIN_PROMPT_LENGTH


class OptimizeRequest(BaseModel):
    prompt: str = Field(..., description="Raw natural language prompt to optimize")

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


class OptimizationResult(BaseModel):
    original_prompt: str
    optimized_prompt: str
    original_tokens: int
    optimized_tokens: int
    token_reduction_percent: float
    original_carbon_score: float
    optimized_carbon_score: float
    carbon_reduction_percent: float
    original_task_type: str
    optimized_task_type: str
    original_prompt_type: str
    optimized_prompt_type: str


class OptimizeSuccessResponse(BaseModel):
    success: bool = True
    optimization: OptimizationResult


class OptimizeErrorResponse(BaseModel):
    success: bool = False
    message: str
