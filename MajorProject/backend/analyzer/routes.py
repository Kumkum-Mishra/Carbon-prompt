"""REST API routes for the Prompt Analyzer module."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from analyzer.analyzer import PromptAnalyzer
from analyzer.schemas import AnalyzeRequest, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter()
_analyzer = PromptAnalyzer()


@router.post("/analyze")
async def analyze_prompt(request: Request) -> JSONResponse:
    """Analyze a raw prompt and return structured metadata."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(message="Invalid prompt.").model_dump(),
        )

    if body is None or "prompt" not in body:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(message="Invalid prompt.").model_dump(),
        )

    prompt_value = body.get("prompt")
    if prompt_value is None:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(message="Invalid prompt.").model_dump(),
        )

    if not isinstance(prompt_value, str):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(message="Invalid prompt.").model_dump(),
        )

    try:
        validated = AnalyzeRequest(prompt=prompt_value)
    except ValidationError as exc:
        message = _extract_validation_message(exc)
        logger.warning("Validation error: %s", message)
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(message=message).model_dump(),
        )

    try:
        result = _analyzer.analyze(validated.prompt)
    except Exception:
        logger.exception("Unexpected error during prompt analysis")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(message="Unable to analyze prompt.").model_dump(),
        )

    status_code = 200 if result.success else 400
    return JSONResponse(status_code=status_code, content=result.model_dump())


def _extract_validation_message(exc: ValidationError) -> str:
    for error in exc.errors():
        msg = error.get("msg", "")
        if msg.startswith("Value error, "):
            return msg.removeprefix("Value error, ")
        return msg or "Invalid prompt."
    return "Invalid prompt."
