"""REST API routes for the Model Recommendation module."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from analyzer.schemas import AnalyzeRequest
from recommendation.recommendation_service import RecommendationService
from recommendation.schemas import (
    PreAnalyzedRecommendRequest,
    RecommendErrorResponse,
    RecommendRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter()
_recommendation_service = RecommendationService()


@router.post("/recommend")
async def recommend_model(request: Request) -> JSONResponse:
    """Recommend the best LLM for a prompt or pre-analyzed task type."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content=RecommendErrorResponse(
                message="Missing required analyzer fields."
            ).model_dump(),
        )

    if not isinstance(body, dict):
        return JSONResponse(
            status_code=400,
            content=RecommendErrorResponse(
                message="Missing required analyzer fields."
            ).model_dump(),
        )

    has_prompt = "prompt" in body and body.get("prompt") is not None
    has_task_type = "task_type" in body and body.get("task_type") is not None

    if has_task_type:
        try:
            validated = PreAnalyzedRecommendRequest.model_validate(body)
        except ValidationError as exc:
            message = _extract_validation_message(exc)
            return JSONResponse(
                status_code=400,
                content=RecommendErrorResponse(message=message).model_dump(),
            )

        try:
            result = _recommendation_service.recommend_from_task_type(
                task_type=validated.task_type,
                category=validated.category,
            )
        except Exception:
            logger.exception("Unexpected error during model recommendation")
            return JSONResponse(
                status_code=500,
                content=RecommendErrorResponse(
                    message="Unable to generate recommendation."
                ).model_dump(),
            )
    elif has_prompt:
        prompt_value = body.get("prompt")
        if not isinstance(prompt_value, str):
            return JSONResponse(
                status_code=400,
                content=RecommendErrorResponse(message="Invalid prompt.").model_dump(),
            )

        try:
            AnalyzeRequest(prompt=prompt_value)
        except ValidationError as exc:
            message = _extract_validation_message(exc)
            return JSONResponse(
                status_code=400,
                content=RecommendErrorResponse(message=message).model_dump(),
            )

        try:
            result = _recommendation_service.recommend_from_raw_prompt(prompt_value)
        except Exception:
            logger.exception("Unexpected error during model recommendation")
            return JSONResponse(
                status_code=500,
                content=RecommendErrorResponse(
                    message="Unable to generate recommendation."
                ).model_dump(),
            )
    else:
        return JSONResponse(
            status_code=400,
            content=RecommendErrorResponse(
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
        return msg or "Missing required analyzer fields."
    return "Missing required analyzer fields."
