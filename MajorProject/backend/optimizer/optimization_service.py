"""Main orchestration layer for prompt optimization."""

import logging
from datetime import datetime, timezone

from analyzer.analyzer import PromptAnalyzer
from analyzer.utils import clean_prompt
from carbon.carbon_service import CarbonService
from optimizer.comparison import build_comparison
from optimizer.config import LOG_FULL_PROMPT, OPTIMIZER_NUM_CANDIDATES
from optimizer.optimizer import OptimizationFailedError, PromptOptimizer
from optimizer.providers.base import LLMProviderUnavailableError, LLMTimeoutError
from optimizer.ranking_engine import RankedCandidate, rank_candidate
from optimizer.schemas import (
    OptimizationResult,
    OptimizeErrorResponse,
    OptimizeSuccessResponse,
)

logger = logging.getLogger(__name__)


class OptimizationService:
    """Optimizes prompts and compares sustainability metrics."""

    def __init__(
        self,
        analyzer: PromptAnalyzer | None = None,
        carbon_service: CarbonService | None = None,
        optimizer: PromptOptimizer | None = None,
    ) -> None:
        self._analyzer = analyzer or PromptAnalyzer()
        self._carbon_service = carbon_service or CarbonService(analyzer=self._analyzer)
        self._optimizer = optimizer or PromptOptimizer()

    def optimize_prompt(
        self, raw_prompt: str
    ) -> OptimizeSuccessResponse | OptimizeErrorResponse:
        cleaned_prompt = clean_prompt(raw_prompt)

        original_analysis_result = self._analyzer.analyze(cleaned_prompt)
        if not original_analysis_result.success:
            return OptimizeErrorResponse(
                message="Unable to complete optimization analysis."
            )
        original_analysis = original_analysis_result.analysis

        try:
            candidate_texts = self._optimizer.optimize_candidates(
                cleaned_prompt,
                num_candidates=OPTIMIZER_NUM_CANDIDATES,
            )
        except LLMTimeoutError:
            return OptimizeErrorResponse(message="Optimization timed out.")
        except LLMProviderUnavailableError:
            return OptimizeErrorResponse(message="LLM provider unavailable.")
        except OptimizationFailedError:
            return OptimizeErrorResponse(message="Optimization failed.")
        except Exception:
            logger.exception("Unexpected error during LLM optimization")
            return OptimizeErrorResponse(message="Optimization failed.")

        original_carbon_result = self._carbon_service.estimate_from_analysis(
            token_count=original_analysis.token_count,
            prompt_type=original_analysis.prompt_type,
            task_type=original_analysis.task_type,
        )
        if not original_carbon_result.success:
            return OptimizeErrorResponse(
                message="Unable to complete optimization analysis."
            )

        best_candidate = self._rank_candidates(
            original_analysis=original_analysis,
            original_carbon=original_carbon_result.carbon,
            candidate_texts=candidate_texts,
        )
        if best_candidate is None:
            return OptimizeErrorResponse(
                message="Optimization failed semantic validation."
            )

        comparison = build_comparison(
            original_analysis=original_analysis,
            optimized_analysis=best_candidate.analysis,
            original_carbon_score=original_carbon_result.carbon.green_carbon_score,
            optimized_carbon_score=best_candidate.carbon.green_carbon_score,
        )

        self._log_optimization(comparison, best_candidate=best_candidate)

        return OptimizeSuccessResponse(
            optimization=OptimizationResult(
                original_prompt=comparison.original_prompt,
                optimized_prompt=comparison.optimized_prompt,
                original_tokens=comparison.original_tokens,
                optimized_tokens=comparison.optimized_tokens,
                token_reduction_percent=comparison.token_reduction_percent,
                original_carbon_score=comparison.original_carbon_score,
                optimized_carbon_score=comparison.optimized_carbon_score,
                carbon_reduction_percent=comparison.carbon_reduction_percent,
                original_task_type=comparison.original_task_type,
                optimized_task_type=comparison.optimized_task_type,
                original_prompt_type=comparison.original_prompt_type,
                optimized_prompt_type=comparison.optimized_prompt_type,
            )
        )

    def _rank_candidates(
        self,
        *,
        original_analysis,
        original_carbon,
        candidate_texts: list[str],
    ) -> RankedCandidate | None:
        ranked: list[RankedCandidate] = []
        for candidate_text in candidate_texts:
            cleaned_candidate = clean_prompt(candidate_text)
            if not cleaned_candidate:
                continue

            candidate_analysis_result = self._analyzer.analyze(cleaned_candidate)
            if not candidate_analysis_result.success:
                continue
            candidate_analysis = candidate_analysis_result.analysis

            candidate_carbon_result = self._carbon_service.estimate_from_analysis(
                token_count=candidate_analysis.token_count,
                prompt_type=candidate_analysis.prompt_type,
                task_type=candidate_analysis.task_type,
            )
            if not candidate_carbon_result.success:
                continue

            ranked_candidate = rank_candidate(
                original_analysis=original_analysis,
                original_carbon=original_carbon,
                candidate_analysis=candidate_analysis,
                candidate_carbon=candidate_carbon_result.carbon,
            )
            if ranked_candidate is not None:
                ranked.append(ranked_candidate)

        # If all generated candidates are rejected, keep the original prompt.
        # This preserves meaning and avoids returning a harmful rewrite.
        if not ranked:
            original_candidate = rank_candidate(
                original_analysis=original_analysis,
                original_carbon=original_carbon,
                candidate_analysis=original_analysis,
                candidate_carbon=original_carbon,
            )
            return original_candidate

        return max(ranked, key=lambda candidate: candidate.score)

    def _log_optimization(self, comparison, best_candidate: RankedCandidate) -> None:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": self._optimizer.provider_name,
            "model": self._optimizer.model_name,
            "candidate_score": best_candidate.score,
            "semantic_similarity": best_candidate.semantic_similarity,
            "readability_score": best_candidate.readability_score,
            "original_tokens": comparison.original_tokens,
            "optimized_tokens": comparison.optimized_tokens,
            "original_carbon_score": comparison.original_carbon_score,
            "optimized_carbon_score": comparison.optimized_carbon_score,
            "token_reduction_percent": comparison.token_reduction_percent,
            "carbon_reduction_percent": comparison.carbon_reduction_percent,
        }
        if LOG_FULL_PROMPT:
            log_data["original_prompt"] = comparison.original_prompt
            log_data["optimized_prompt"] = comparison.optimized_prompt

        logger.info("Prompt optimization completed: %s", log_data)
