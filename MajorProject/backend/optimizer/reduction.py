"""Reduction percentage calculations."""

import logging

from optimizer.config import PERCENT_DECIMAL_PLACES

logger = logging.getLogger(__name__)


def calculate_token_reduction_percent(
    original_tokens: int, optimized_tokens: int
) -> float:
    """Calculate percentage reduction in token count."""
    if original_tokens == 0:
        logger.warning("Original token count is zero; returning 0.0%% reduction.")
        return 0.0
    reduction = ((original_tokens - optimized_tokens) / original_tokens) * 100
    return round(reduction, PERCENT_DECIMAL_PLACES)


def calculate_carbon_reduction_percent(
    original_carbon: float, optimized_carbon: float
) -> float:
    """Calculate percentage reduction in Green Carbon Score."""
    if original_carbon == 0:
        logger.warning("Original carbon score is zero; returning 0.0%% reduction.")
        return 0.0
    reduction = ((original_carbon - optimized_carbon) / original_carbon) * 100
    return round(reduction, PERCENT_DECIMAL_PLACES)
