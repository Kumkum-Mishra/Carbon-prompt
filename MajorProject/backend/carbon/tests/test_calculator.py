"""Unit tests for Green Carbon Score calculation."""

import pytest

from carbon.calculator import (
    CalculationError,
    InvalidTokenCountError,
    calculate_green_carbon_score,
)
from carbon.constants import SCALING_CONSTANT_K


class TestCalculator:
    def test_formula_accuracy(self) -> None:
        score = calculate_green_carbon_score(
            token_count=9,
            prompt_weight=1.0,
            task_weight=1.4,
            scaling_constant=SCALING_CONSTANT_K,
        )
        assert score == 0.000126

    def test_zero_shot_coding(self) -> None:
        score = calculate_green_carbon_score(9, 1.0, 1.4)
        assert score == 0.000126

    def test_few_shot_scoring(self) -> None:
        score = calculate_green_carbon_score(10, 1.2, 1.0)
        assert score == 0.00012

    def test_chain_of_thought_scoring(self) -> None:
        score = calculate_green_carbon_score(8, 1.5, 1.5)
        assert score == 0.00018

    def test_mathematics_task_scoring(self) -> None:
        score = calculate_green_carbon_score(10, 1.0, 1.5)
        assert score == 0.00015

    def test_writing_task_scoring(self) -> None:
        score = calculate_green_carbon_score(10, 1.0, 1.2)
        assert score == 0.00012

    def test_large_token_count(self) -> None:
        score = calculate_green_carbon_score(100_000, 1.0, 1.0)
        assert score == 1.0

    def test_zero_token_count_rejection(self) -> None:
        with pytest.raises(InvalidTokenCountError):
            calculate_green_carbon_score(0, 1.0, 1.0)

    def test_negative_token_count_rejection(self) -> None:
        with pytest.raises(InvalidTokenCountError):
            calculate_green_carbon_score(-5, 1.0, 1.0)

    def test_non_integer_token_count_rejection(self) -> None:
        with pytest.raises(InvalidTokenCountError):
            calculate_green_carbon_score(1.5, 1.0, 1.0)  # type: ignore[arg-type]

    def test_scaling_constant_application(self) -> None:
        score_default = calculate_green_carbon_score(10, 1.0, 1.0)
        score_custom = calculate_green_carbon_score(10, 1.0, 1.0, scaling_constant=0.00002)
        assert score_custom == score_default * 2

    def test_result_rounded_to_six_decimal_places(self) -> None:
        score = calculate_green_carbon_score(7, 1.1, 1.1, scaling_constant=0.00001)
        assert score == round(7 * 1.1 * 1.1 * 0.00001, 6)
