"""Pydantic request and response schemas for the Prompt Analyzer."""

from pydantic import BaseModel, Field, field_validator

from analyzer.config import MAX_PROMPT_LENGTH, MIN_PROMPT_LENGTH


class AnalyzeRequest(BaseModel):
    prompt: str = Field(..., description="Raw natural language prompt to analyze")

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


class AnalysisResult(BaseModel):
    prompt: str
    prompt_type: str
    task_type: str
    category: str
    token_count: int
    character_count: int
    word_count: int


class SuccessResponse(BaseModel):
    success: bool = True
    analysis: AnalysisResult


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
