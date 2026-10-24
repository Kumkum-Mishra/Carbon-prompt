"""Pydantic request and response schemas for carbon estimation."""

from pydantic import BaseModel, Field


class CarbonResult(BaseModel):
    token_count: int
    prompt_type: str
    task_type: str
    prompt_weight: float
    task_weight: float
    scaling_constant: float
    green_carbon_score: float


class CarbonSuccessResponse(BaseModel):
    success: bool = True
    carbon: CarbonResult


class CarbonErrorResponse(BaseModel):
    success: bool = False
    message: str


class PreAnalyzedCarbonRequest(BaseModel):
    token_count: int = Field(..., description="Input token count from analyzer")
    prompt_type: str = Field(..., description="Detected prompt engineering strategy")
    task_type: str = Field(..., description="Detected task category")
    prompt: str | None = Field(default=None, description="Optional original prompt text")
