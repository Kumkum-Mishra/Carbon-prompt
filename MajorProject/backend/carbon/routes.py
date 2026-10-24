"""REST API routes for the Carbon Estimation module."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from analyzer.schemas import AnalyzeRequest
from carbon.carbon_service import CarbonService
from carbon.schemas import CarbonErrorResponse, PreAnalyzedCarbonRequest

logger = logging.getLogger(__name__)

router = APIRouter()
_carbon_service = CarbonService()


@router.post("/carbon")
async def estimate_carbon(request: Request) -> JSONResponse:
    """Estimate Green Carbon Score from a raw prompt or pre-analyzed input."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content=CarbonErrorResponse(
                message="Missing required analyzer fields."
            ).model_dump(),
        )

    if not isinstance(body, dict):
        return JSONResponse(
            status_code=400,
            content=CarbonErrorResponse(
                message="Missing required analyzer fields."
            ).model_dump(),
        )

    has_prompt = "prompt" in body and body.get("prompt") is not None
    has_token_count = "token_count" in body and body.get("token_count") is not None
    has_prompt_type = "prompt_type" in body and body.get("prompt_type") is not None
    has_task_type = "task_type" in body and body.get("task_type") is not None

    has_pre_analyzed_fields = has_token_count or has_prompt_type or has_task_type

    if has_pre_analyzed_fields:
        if not (has_token_count and has_prompt_type and has_task_type):
            return JSONResponse(
                status_code=400,
                content=CarbonErrorResponse(
                    message="Missing required analyzer fields."
                ).model_dump(),
            )

        try:
            validated = PreAnalyzedCarbonRequest.model_validate(body)
        except ValidationError:
            return JSONResponse(
                status_code=400,
                content=CarbonErrorResponse(
                    message="Missing required analyzer fields."
                ).model_dump(),
            )

        try:
            result = _carbon_service.estimate_from_analysis(
                token_count=validated.token_count,
                prompt_type=validated.prompt_type,
                task_type=validated.task_type,
            )
        except Exception:
            logger.exception("Unexpected error during carbon estimation")
            return JSONResponse(
                status_code=500,
                content=CarbonErrorResponse(
                    message="Unable to calculate Green Carbon Score."
                ).model_dump(),
            )
    elif has_prompt:
        prompt_value = body.get("prompt")
        if not isinstance(prompt_value, str):
            return JSONResponse(
                status_code=400,
                content=CarbonErrorResponse(message="Invalid prompt.").model_dump(),
            )

        try:
            AnalyzeRequest(prompt=prompt_value)
        except ValidationError as exc:
            message = _extract_validation_message(exc)
            return JSONResponse(
                status_code=400,
                content=CarbonErrorResponse(message=message).model_dump(),
            )

        try:
            result = _carbon_service.estimate_from_raw_prompt(prompt_value)
        except Exception:
            logger.exception("Unexpected error during carbon estimation")
            return JSONResponse(
                status_code=500,
                content=CarbonErrorResponse(
                    message="Unable to calculate Green Carbon Score."
                ).model_dump(),
            )
    else:
        return JSONResponse(
            status_code=400,
            content=CarbonErrorResponse(
                message="Missing required analyzer fields."
            ).model_dump(),
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
