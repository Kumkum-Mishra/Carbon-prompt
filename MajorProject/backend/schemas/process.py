"""Pipeline request and response schemas."""

from pydantic import BaseModel, Field

from analyzer.schemas import AnalysisResult
from carbon.schemas import CarbonResult
from optimizer.schemas import OptimizationResult
from recommendation.schemas import RecommendationResult


class ProcessRequest(BaseModel):
    prompt: str = Field(..., description="Raw natural language prompt to process")


class PipelineCarbonComparison(BaseModel):
    original: CarbonResult
    optimized: CarbonResult


class PipelineData(BaseModel):
    analysis: AnalysisResult
    carbon: PipelineCarbonComparison
    optimization: OptimizationResult
    recommendation: RecommendationResult


class PipelineMetadata(BaseModel):
    processing_time_ms: float
    pipeline_version: str


class ProcessSuccessResponse(BaseModel):
    success: bool = True
    pipeline: PipelineData
    metadata: PipelineMetadata


class HealthModules(BaseModel):
    analyzer: str
    carbon: str
    optimizer: str
    recommendation: str


class HealthResponse(BaseModel):
    status: str
    version: str
    modules: HealthModules
