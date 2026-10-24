"""Main orchestration layer for model recommendation."""

import logging
from datetime import datetime, timezone

from analyzer.analyzer import PromptAnalyzer
from recommendation.category_mapper import (
    UnknownCategoryError,
    get_dataset_filename,
    resolve_category,
)
from recommendation.config import TOP_N_MODELS, get_recommendation_scoring_mode
from recommendation.dataset_loader import (
    DatasetNotFoundError,
    EmptyDatasetError,
    load_models_for_category,
)
from recommendation.feature_extractor import (
    PromptFeatures,
    extract_prompt_features,
    features_to_dict,
)
from recommendation.priority_engine import (
    MetricPriorities,
    compute_priorities,
    priorities_to_dict,
)
from recommendation.ranking import rank_models
from recommendation.reason_generator import generate_reasons
from recommendation.schemas import (
    RecommendErrorResponse,
    RecommendationFeatures,
    RecommendationPriorities,
    RecommendationResult,
    RecommendationWeights,
    RecommendSuccessResponse,
    TopModelResult,
)
from recommendation.scorer import ScoredModel
from recommendation.weight_normalizer import (
    MetricWeights,
    normalize_weights,
    weights_to_dict,
)

logger = logging.getLogger(__name__)


class RecommendationService:
    """Recommends LLMs based on prompt category and GMES/DGMES scoring."""

    def __init__(self, analyzer: PromptAnalyzer | None = None) -> None:
        self._analyzer = analyzer or PromptAnalyzer()

    def recommend_from_raw_prompt(
        self, prompt: str
    ) -> RecommendSuccessResponse | RecommendErrorResponse:
        analysis_result = self._analyzer.analyze(prompt)
        if not analysis_result.success:
            return RecommendErrorResponse(message=analysis_result.message)

        return self.recommend_from_task_type(
            task_type=analysis_result.analysis.task_type,
            category=analysis_result.analysis.category,
            prompt=prompt,
            input_tokens=analysis_result.analysis.token_count,
        )

    def recommend_from_task_type(
        self,
        *,
        task_type: str,
        category: str | None = None,
        prompt: str | None = None,
        input_tokens: int | None = None,
    ) -> RecommendSuccessResponse | RecommendErrorResponse:
        try:
            resolved_category = resolve_category(category, task_type)
        except UnknownCategoryError as exc:
            logger.warning("Unknown category for task type %s: %s", task_type, exc)
            return RecommendErrorResponse(message=str(exc))

        try:
            models = load_models_for_category(resolved_category)
        except DatasetNotFoundError as exc:
            logger.error("Dataset not found for category %s", resolved_category)
            return RecommendErrorResponse(message=str(exc))
        except EmptyDatasetError as exc:
            logger.warning("Empty dataset for category %s", resolved_category)
            return RecommendErrorResponse(message=str(exc))
        except Exception:
            logger.exception("Unexpected dataset loading error")
            return RecommendErrorResponse(message="Dataset not found.")

        weights, features, priorities = self._resolve_scoring_context(
            task_type=task_type,
            prompt=prompt,
            input_tokens=input_tokens,
        )
        use_dynamic = (
            get_recommendation_scoring_mode() == "dynamic_dgmes" and weights is not None
        )

        ranked_models = rank_models(
            models,
            top_n=TOP_N_MODELS,
            weights=weights if use_dynamic else None,
        )
        top_model = ranked_models[0]
        reasons = generate_reasons(
            top_model,
            models,
            weights=weights if use_dynamic else None,
            features=features,
        )

        score_type = "DGMES" if use_dynamic else "GMES"
        top_score = top_model.dgmes if use_dynamic else top_model.gmes

        self._log_recommendation(
            task_type=task_type,
            category=resolved_category,
            dataset_file=get_dataset_filename(resolved_category),
            model_count=len(models),
            recommended_model=top_model.model,
            top_score=top_score,
            score_type=score_type,
            weights=weights,
        )

        return RecommendSuccessResponse(
            recommendation=RecommendationResult(
                category=resolved_category,
                task_type=task_type,
                recommended_model=top_model.model,
                score=top_score,
                score_type=score_type,
                baseline_gmes=top_model.gmes,
                weights=(
                    RecommendationWeights(**weights_to_dict(weights))
                    if weights is not None
                    else None
                ),
                features=(
                    RecommendationFeatures(**features_to_dict(features))
                    if features is not None
                    else None
                ),
                priorities=(
                    RecommendationPriorities(**priorities_to_dict(priorities))
                    if priorities is not None
                    else None
                ),
                top_models=[
                    TopModelResult(
                        model=model.model,
                        score=model.dgmes if use_dynamic else model.gmes,
                        speed=model.speed,
                        latency=model.latency,
                        context=model.context,
                        cost_efficiency=model.cost_efficiency,
                        baseline_gmes=model.gmes,
                    )
                    for model in ranked_models
                ],
                reason=reasons,
            )
        )

    def _resolve_scoring_context(
        self,
        *,
        task_type: str,
        prompt: str | None,
        input_tokens: int | None,
    ) -> tuple[MetricWeights | None, PromptFeatures | None, MetricPriorities | None]:
        if get_recommendation_scoring_mode() != "dynamic_dgmes":
            return None, None, None

        if prompt is None or input_tokens is None:
            logger.info(
                "Dynamic DGMES requested without prompt context; falling back to GMES."
            )
            return None, None, None

        features = extract_prompt_features(
            prompt=prompt,
            task_type=task_type,
            input_tokens=input_tokens,
        )
        priorities = compute_priorities(features)
        weights = normalize_weights(priorities)
        return weights, features, priorities

    def _log_recommendation(
        self,
        *,
        task_type: str,
        category: str,
        dataset_file: str,
        model_count: int,
        recommended_model: str,
        top_score: float,
        score_type: str,
        weights: MetricWeights | None,
    ) -> None:
        payload: dict[str, object] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_type": task_type,
            "category": category,
            "dataset_file": dataset_file,
            "model_count": model_count,
            "recommended_model": recommended_model,
            "score_type": score_type,
            "top_score": top_score,
        }
        if weights is not None:
            payload["weights"] = weights_to_dict(weights)

        logger.info("Model recommendation completed: %s", payload)
