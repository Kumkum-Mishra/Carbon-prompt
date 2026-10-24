"""Application health check endpoint."""

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from carbon.prompt_weights import get_all_prompt_weights
from carbon.task_weights import get_all_task_weights
from config import APP_VERSION
from recommendation.config import UNIFIED_DATASET_PATH
from recommendation.dataset_loader import load_models_for_category
from schemas.process import HealthModules, HealthResponse
from services.module_registry import get_module_registry

logger = logging.getLogger(__name__)

router = APIRouter()


def _check_analyzer() -> str:
    registry = get_module_registry()
    result = registry.analyzer.analyze("Test prompt.")
    return "ok" if result.success else "error"


def _check_carbon() -> str:
    weights = get_all_prompt_weights()
    task_weights = get_all_task_weights()
    return "ok" if weights and task_weights else "error"


def _check_optimizer() -> str:
    registry = get_module_registry()
    provider = registry.optimizer._optimizer.provider_name
    return "ok" if provider else "error"


def _check_recommendation() -> str:
    if not UNIFIED_DATASET_PATH.exists():
        return "error"
    try:
        models = load_models_for_category("Coding", dataset_path=UNIFIED_DATASET_PATH)
        return "ok" if models else "error"
    except Exception:
        return "error"


@router.get("/health")
async def health_check() -> JSONResponse:
    """Return application and module health status."""
    modules = HealthModules(
        analyzer=_check_analyzer(),
        carbon=_check_carbon(),
        optimizer=_check_optimizer(),
        recommendation=_check_recommendation(),
    )

    all_ok = all(status == "ok" for status in modules.model_dump().values())
    response = HealthResponse(
        status="healthy" if all_ok else "degraded",
        version=APP_VERSION,
        modules=modules,
    )

    status_code = 200 if all_ok else 503
    if not all_ok:
        logger.warning("Health check degraded: %s", modules.model_dump())

    return JSONResponse(status_code=status_code, content=response.model_dump())
