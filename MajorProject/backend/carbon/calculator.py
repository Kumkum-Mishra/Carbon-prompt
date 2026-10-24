"""Green Carbon Score calculation."""

from carbon.constants import MAX_GREEN_CARBON_SCORE, SCALING_CONSTANT_K, SCORE_DECIMAL_PLACES


class InvalidTokenCountError(Exception):
    """Raised when token count is not a positive integer."""


class CalculationError(Exception):
    """Raised when the Green Carbon Score cannot be calculated."""


def validate_token_count(token_count: int) -> None:
    if not isinstance(token_count, int) or isinstance(token_count, bool):
        raise InvalidTokenCountError("Token count must be a positive integer.")
    if token_count <= 0:
        raise InvalidTokenCountError("Token count must be a positive integer.")


def calculate_green_carbon_score(
    token_count: int,
    prompt_weight: float,
    task_weight: float,
    scaling_constant: float = SCALING_CONSTANT_K,
) -> float:
    """Apply the GCS formula and return a rounded score."""
    validate_token_count(token_count)

    try:
        score = token_count * prompt_weight * task_weight * scaling_constant
        if MAX_GREEN_CARBON_SCORE is not None:
            score = min(score, MAX_GREEN_CARBON_SCORE)
        return round(score, SCORE_DECIMAL_PLACES)
    except (TypeError, ValueError, OverflowError) as exc:
        raise CalculationError("Unable to calculate Green Carbon Score.") from exc
