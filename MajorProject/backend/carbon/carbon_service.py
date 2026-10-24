"""Main orchestration layer for carbon estimation."""

import logging
from datetime import datetime, timezone

from analyzer.analyzer import PromptAnalyzer
from carbon.calculator import (
    CalculationError,
    InvalidTokenCountError,
    calculate_green_carbon_score,
)
from carbon.constants import SCALING_CONSTANT_K
from carbon.prompt_weights import UnknownPromptTypeError, get_prompt_weight
from carbon.schemas import CarbonErrorResponse, CarbonResult, CarbonSuccessResponse
from carbon.task_weights import UnknownTaskTypeError, get_task_weight

logger = logging.getLogger(__name__)


class CarbonService:
    """Estimates Green Carbon Score from analyzer output or raw prompts."""

    def __init__(self, analyzer: PromptAnalyzer | None = None) -> None:
        self._analyzer = analyzer or PromptAnalyzer()

    def estimate_from_raw_prompt(
        self, prompt: str
    ) -> CarbonSuccessResponse | CarbonErrorResponse:
        analysis_result = self._analyzer.analyze(prompt)
        if not analysis_result.success:
            return CarbonErrorResponse(message=analysis_result.message)

        analysis = analysis_result.analysis
        return self.estimate_from_analysis(
            token_count=analysis.token_count,
            prompt_type=analysis.prompt_type,
            task_type=analysis.task_type,
        )

    def estimate_from_analysis(
        self,
        *,
        token_count: int,
        prompt_type: str,
        task_type: str,
    ) -> CarbonSuccessResponse | CarbonErrorResponse:
        try:
            prompt_weight = get_prompt_weight(prompt_type)
        except UnknownPromptTypeError as exc:
            logger.warning("Unknown prompt type: %s", prompt_type)
            return CarbonErrorResponse(message=str(exc))

        try:
            task_weight = get_task_weight(task_type)
        except UnknownTaskTypeError as exc:
            logger.warning("Unknown task type: %s", task_type)
            return CarbonErrorResponse(message=str(exc))

        try:
            green_carbon_score = calculate_green_carbon_score(
                token_count=token_count,
                prompt_weight=prompt_weight,
                task_weight=task_weight,
                scaling_constant=SCALING_CONSTANT_K,
            )
        except InvalidTokenCountError as exc:
            logger.warning("Invalid token count: %s", token_count)
            return CarbonErrorResponse(message=str(exc))
        except CalculationError as exc:
            logger.error("Calculation error: %s", exc)
            return CarbonErrorResponse(message=str(exc))

        self._log_estimation(
            prompt_type=prompt_type,
            task_type=task_type,
            token_count=token_count,
            prompt_weight=prompt_weight,
            task_weight=task_weight,
            green_carbon_score=green_carbon_score,
        )

        return CarbonSuccessResponse(
            carbon=CarbonResult(
                token_count=token_count,
                prompt_type=prompt_type,
                task_type=task_type,
                prompt_weight=prompt_weight,
                task_weight=task_weight,
                scaling_constant=SCALING_CONSTANT_K,
                green_carbon_score=green_carbon_score,
            )
        )

    def _log_estimation(
        self,
        *,
        prompt_type: str,
        task_type: str,
        token_count: int,
        prompt_weight: float,
        task_weight: float,
        green_carbon_score: float,
    ) -> None:
        logger.info(
            "Carbon estimation completed: %s",
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "prompt_type": prompt_type,
                "task_type": task_type,
                "token_count": token_count,
                "prompt_weight": prompt_weight,
                "task_weight": task_weight,
                "green_carbon_score": green_carbon_score,
            },
        )
