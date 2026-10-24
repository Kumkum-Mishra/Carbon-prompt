"""REST API routes for the Prompt Optimization module."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from optimizer.optimization_service import OptimizationService
from optimizer.schemas import OptimizeErrorResponse, OptimizeRequest

logger = logging.getLogger(__name__)

router = APIRouter()
_optimization_service = OptimizationService()


@router.post("/optimize")
async def optimize_prompt(request: Request) -> JSONResponse:
    """Optimize a prompt and return sustainability comparison metrics."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content=OptimizeErrorResponse(message="Invalid prompt.").model_dump(),
        )

    if not isinstance(body, dict) or "prompt" not in body:
        return JSONResponse(
            status_code=400,
            content=OptimizeErrorResponse(message="Invalid prompt.").model_dump(),
        )

    prompt_value = body.get("prompt")
    if prompt_value is None:
        return JSONResponse(
            status_code=400,
            content=OptimizeErrorResponse(message="Invalid prompt.").model_dump(),
        )

    if not isinstance(prompt_value, str):
        return JSONResponse(
            status_code=400,
            content=OptimizeErrorResponse(message="Invalid prompt.").model_dump(),
        )

    try:
        validated = OptimizeRequest(prompt=prompt_value)
    except ValidationError as exc:
        message = _extract_validation_message(exc)
        logger.warning("Validation error: %s", message)
        return JSONResponse(
            status_code=400,
            content=OptimizeErrorResponse(message=message).model_dump(),
        )

    try:
        result = _optimization_service.optimize_prompt(validated.prompt)
    except Exception:
        logger.exception("Unexpected error during optimization")
        return JSONResponse(
            status_code=500,
            content=OptimizeErrorResponse(message="Optimization failed.").model_dump(),
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
