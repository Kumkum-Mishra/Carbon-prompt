"""Unit tests for carbon service orchestration."""

import pytest

from analyzer.analyzer import PromptAnalyzer
from carbon.carbon_service import CarbonService


@pytest.fixture
def service() -> CarbonService:
    return CarbonService()


class TestCarbonService:
    def test_estimate_from_analysis(self, service: CarbonService) -> None:
        result = service.estimate_from_analysis(
            token_count=9,
            prompt_type="Zero-shot",
            task_type="Coding",
        )
        assert result.success is True
        assert result.carbon.green_carbon_score == 0.000126
        assert result.carbon.prompt_weight == 1.0
        assert result.carbon.task_weight == 1.4
        assert result.carbon.scaling_constant == 0.00001

    def test_estimate_from_raw_prompt(self, service: CarbonService) -> None:
        result = service.estimate_from_raw_prompt("Write Python code for CNN")
        assert result.success is True
        assert result.carbon.task_type == "Coding"
        assert result.carbon.token_count > 0
        assert result.carbon.green_carbon_score > 0

    def test_unknown_prompt_type(self, service: CarbonService) -> None:
        result = service.estimate_from_analysis(
            token_count=5,
            prompt_type="Invalid Prompt Type",
            task_type="Coding",
        )
        assert result.success is False
        assert result.message == "Prompt type not recognized."

    def test_unknown_task_type(self, service: CarbonService) -> None:
        result = service.estimate_from_analysis(
            token_count=5,
            prompt_type="Zero-shot",
            task_type="Invalid Task Type",
        )
        assert result.success is False
        assert result.message == "Task type not recognized."

    def test_zero_token_count(self, service: CarbonService) -> None:
        result = service.estimate_from_analysis(
            token_count=0,
            prompt_type="Zero-shot",
            task_type="Coding",
        )
        assert result.success is False
        assert result.message == "Token count must be a positive integer."

    def test_negative_token_count(self, service: CarbonService) -> None:
        result = service.estimate_from_analysis(
            token_count=-3,
            prompt_type="Zero-shot",
            task_type="Coding",
        )
        assert result.success is False
        assert result.message == "Token count must be a positive integer."

    def test_invalid_raw_prompt(self, service: CarbonService) -> None:
        result = service.estimate_from_raw_prompt("")
        assert result.success is False

    def test_pipeline_with_analyzer(self) -> None:
        analyzer = PromptAnalyzer()
        carbon = CarbonService(analyzer=analyzer)
        analysis = analyzer.analyze("Write Python code for CNN")
        assert analysis.success is True

        result = carbon.estimate_from_analysis(
            token_count=analysis.analysis.token_count,
            prompt_type=analysis.analysis.prompt_type,
            task_type=analysis.analysis.task_type,
        )
        assert result.success is True
        expected = round(
            analysis.analysis.token_count
            * result.carbon.prompt_weight
            * result.carbon.task_weight
            * result.carbon.scaling_constant,
            6,
        )
        assert result.carbon.green_carbon_score == expected
