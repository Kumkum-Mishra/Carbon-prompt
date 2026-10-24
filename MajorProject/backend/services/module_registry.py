"""Registry providing shared module service instances."""

from analyzer.analyzer import PromptAnalyzer
from carbon.carbon_service import CarbonService
from optimizer.optimization_service import OptimizationService
from optimizer.optimizer import PromptOptimizer
from recommendation.recommendation_service import RecommendationService


class ModuleRegistry:
    """Initialize and provide access to all backend module services."""

    def __init__(self) -> None:
        self.analyzer = PromptAnalyzer()
        self.carbon = CarbonService(analyzer=self.analyzer)
        self.optimizer = OptimizationService(
            analyzer=self.analyzer,
            carbon_service=self.carbon,
            optimizer=PromptOptimizer(),
        )
        self.recommendation = RecommendationService(analyzer=self.analyzer)


_registry: ModuleRegistry | None = None


def get_module_registry() -> ModuleRegistry:
    """Return the shared module registry singleton."""
    global _registry
    if _registry is None:
        _registry = ModuleRegistry()
    return _registry


def reset_module_registry() -> None:
    """Reset the registry (primarily for tests)."""
    global _registry
    _registry = None
