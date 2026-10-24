"""Unit tests for reduction percentage calculations."""

import logging

from optimizer.reduction import (
    calculate_carbon_reduction_percent,
    calculate_token_reduction_percent,
)


class TestReduction:
    def test_token_reduction(self) -> None:
        assert calculate_token_reduction_percent(26, 13) == 50.0

    def test_carbon_reduction(self) -> None:
        assert calculate_carbon_reduction_percent(0.00039, 0.00021) == 46.15

    def test_zero_original_tokens(self, caplog) -> None:
        with caplog.at_level(logging.WARNING):
            result = calculate_token_reduction_percent(0, 5)
        assert result == 0.0

    def test_zero_original_carbon(self, caplog) -> None:
        with caplog.at_level(logging.WARNING):
            result = calculate_carbon_reduction_percent(0.0, 0.0001)
        assert result == 0.0

    def test_negative_token_reduction(self) -> None:
        assert calculate_token_reduction_percent(10, 15) == -50.0

    def test_negative_carbon_reduction(self) -> None:
        assert calculate_carbon_reduction_percent(0.0001, 0.00015) == -50.0

    def test_no_reduction(self) -> None:
        assert calculate_token_reduction_percent(10, 10) == 0.0
