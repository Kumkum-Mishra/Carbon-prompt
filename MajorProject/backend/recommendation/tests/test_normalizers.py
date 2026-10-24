"""Unit tests for metric parsing and normalization."""

from recommendation.normalizers import (
    normalize_higher_better,
    normalize_lower_better,
    parse_context,
    parse_cost,
    parse_latency,
    parse_speed,
)


class TestNormalizers:
    def test_parse_speed(self) -> None:
        assert parse_speed("56 tps") == 56.0

    def test_parse_latency(self) -> None:
        assert parse_latency("1.6s") == 1.6

    def test_parse_context_k(self) -> None:
        assert parse_context("200K") == 200_000.0

    def test_parse_context_m(self) -> None:
        assert parse_context("1M") == 1_000_000.0

    def test_parse_cost(self) -> None:
        assert parse_cost("$5.00") == 5.0

    def test_parse_null_returns_none(self) -> None:
        assert parse_speed("null") is None
        assert parse_latency("null") is None

    def test_normalize_higher_better(self) -> None:
        assert normalize_higher_better([0, 50, 100]) == [0.0, 50.0, 100.0]

    def test_normalize_lower_better(self) -> None:
        assert normalize_lower_better([1.0, 2.0, 3.0]) == [100.0, 50.0, 0.0]

    def test_normalize_equal_values(self) -> None:
        assert normalize_higher_better([5, 5, 5]) == [100.0, 100.0, 100.0]
