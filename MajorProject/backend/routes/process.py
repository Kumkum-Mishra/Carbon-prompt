"""Complete pipeline endpoint."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from analyzer.schemas import AnalyzeRequest
from services.pipeline_service import PipelineService
from utils.errors import ErrorResponse, build_error_response

logger = logging.getLogger(__name__)

router = APIRouter()
_pipeline_service = PipelineService()


@router.post("/process")
async def process_prompt(request: Request) -> JSONResponse:
    """Run the complete GreenPrompt AI processing pipeline."""
    try:
        body = await request.json()
    except Exception:
        return build_error_response("Invalid request body.", status_code=400)

    if not isinstance(body, dict) or "prompt" not in body:
        return build_error_response("Prompt cannot be empty.", status_code=400)

    prompt_value = body.get("prompt")
    if prompt_value is None or not isinstance(prompt_value, str):
        return build_error_response("Invalid prompt.", status_code=400)

    try:
        validated = AnalyzeRequest(prompt=prompt_value)
    except ValidationError as exc:
        message = _extract_validation_message(exc)
        return build_error_response(message, status_code=400)

    try:
        result = _pipeline_service.process_prompt(validated.prompt)
    except Exception:
        logger.exception("Unexpected pipeline error")
        return build_error_response("Internal server error.", status_code=500)

    if isinstance(result, ErrorResponse):
        return build_error_response(
            result.message,
            status_code=500,
            details=result.details,
        )

    return JSONResponse(status_code=200, content=result.model_dump())


def _extract_validation_message(exc: ValidationError) -> str:
    for error in exc.errors():
        msg = error.get("msg", "")
        if msg.startswith("Value error, "):
            return msg.removeprefix("Value error, ")
        return msg or "Invalid prompt."
    return "Invalid prompt."
