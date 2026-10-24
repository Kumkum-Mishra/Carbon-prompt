"""Comparison logic for original vs optimized prompts."""

import logging
from dataclasses import dataclass

from analyzer.schemas import AnalysisResult
from optimizer.reduction import (
    calculate_carbon_reduction_percent,
    calculate_token_reduction_percent,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ComparisonMetrics:
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


def build_comparison(
    *,
    original_analysis: AnalysisResult,
    optimized_analysis: AnalysisResult,
    original_carbon_score: float,
    optimized_carbon_score: float,
) -> ComparisonMetrics:
    """Build comparison metrics from analyzer and carbon results."""
    if original_analysis.task_type != optimized_analysis.task_type:
        logger.warning(
            "Task type changed during optimization: %s -> %s",
            original_analysis.task_type,
            optimized_analysis.task_type,
        )

    if original_analysis.prompt_type != optimized_analysis.prompt_type:
        logger.warning(
            "Prompt type changed during optimization: %s -> %s",
            original_analysis.prompt_type,
            optimized_analysis.prompt_type,
        )

    return ComparisonMetrics(
        original_prompt=original_analysis.prompt,
        optimized_prompt=optimized_analysis.prompt,
        original_tokens=original_analysis.token_count,
        optimized_tokens=optimized_analysis.token_count,
        token_reduction_percent=calculate_token_reduction_percent(
            original_analysis.token_count,
            optimized_analysis.token_count,
        ),
        original_carbon_score=original_carbon_score,
        optimized_carbon_score=optimized_carbon_score,
        carbon_reduction_percent=calculate_carbon_reduction_percent(
            original_carbon_score,
            optimized_carbon_score,
        ),
        original_task_type=original_analysis.task_type,
        optimized_task_type=optimized_analysis.task_type,
        original_prompt_type=original_analysis.prompt_type,
        optimized_prompt_type=optimized_analysis.prompt_type,
    )
