"""Complete GreenPrompt AI pipeline orchestration."""

import logging

from config import PIPELINE_VERSION
from schemas.process import (
    PipelineCarbonComparison,
    PipelineData,
    PipelineMetadata,
    ProcessSuccessResponse,
)
from services.module_registry import ModuleRegistry, get_module_registry
from utils.errors import ErrorResponse
from utils.timing import measure_time

logger = logging.getLogger(__name__)


class PipelineService:
    """Orchestrates the full Analyzer → Carbon → Optimize → Carbon → Recommend flow."""

    def __init__(self, registry: ModuleRegistry | None = None) -> None:
        self._registry = registry or get_module_registry()

    def process_prompt(
        self, prompt: str
    ) -> ProcessSuccessResponse | ErrorResponse:
        with measure_time() as timing:
            analysis_result = self._registry.analyzer.analyze(prompt)
            if not analysis_result.success:
                return self._pipeline_error(
                    "Pipeline failed at analysis step.",
                    analysis_result.message,
                )
            analysis = analysis_result.analysis

            original_carbon_result = self._registry.carbon.estimate_from_analysis(
                token_count=analysis.token_count,
                prompt_type=analysis.prompt_type,
                task_type=analysis.task_type,
            )
            if not original_carbon_result.success:
                return self._pipeline_error(
                    "Pipeline failed at carbon estimation step.",
                    original_carbon_result.message,
                )

            optimization_result = self._registry.optimizer.optimize_prompt(prompt)
            if not optimization_result.success:
                return self._pipeline_error(
                    "Pipeline failed at optimization step.",
                    optimization_result.message,
                )
            optimization = optimization_result.optimization

            optimized_carbon_result = self._registry.carbon.estimate_from_analysis(
                token_count=optimization.optimized_tokens,
                prompt_type=optimization.optimized_prompt_type,
                task_type=optimization.optimized_task_type,
            )
            if not optimized_carbon_result.success:
                return self._pipeline_error(
                    "Pipeline failed at optimized carbon estimation step.",
                    optimized_carbon_result.message,
                )

            recommendation_result = self._registry.recommendation.recommend_from_task_type(
                task_type=optimization.optimized_task_type,
                category=optimization.optimized_task_type,
                prompt=prompt,
                input_tokens=analysis.token_count,
            )
            if not recommendation_result.success:
                return self._pipeline_error(
                    "Pipeline failed at recommendation step.",
                    recommendation_result.message,
                )

            logger.info(
                "Pipeline completed: task_type=%s recommended_model=%s tokens=%d->%d provider=%s",
                analysis.task_type,
                recommendation_result.recommendation.recommended_model,
                optimization.original_tokens,
                optimization.optimized_tokens,
                self._registry.optimizer._optimizer.provider_name,
            )

            response = ProcessSuccessResponse(
                pipeline=PipelineData(
                    analysis=analysis,
                    carbon=PipelineCarbonComparison(
                        original=original_carbon_result.carbon,
                        optimized=optimized_carbon_result.carbon,
                    ),
                    optimization=optimization,
                    recommendation=recommendation_result.recommendation,
                ),
                metadata=PipelineMetadata(
                    processing_time_ms=0.0,
                    pipeline_version=PIPELINE_VERSION,
                ),
            )

        # Elapsed time is finalized in measure_time()'s finally block, so set it after the with.
        response.metadata.processing_time_ms = round(timing["elapsed_ms"], 2)
        return response

    def _pipeline_error(self, message: str, details: str) -> ErrorResponse:
        logger.warning("Pipeline failure: %s (%s)", message, details)
        return ErrorResponse(message=message, details=details)
