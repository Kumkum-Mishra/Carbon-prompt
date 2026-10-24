export interface AnalysisResult {
  prompt: string;
  prompt_type: string;
  task_type: string;
  category: string;
  token_count: number;
  character_count: number;
  word_count: number;
}

export interface CarbonResult {
  token_count: number;
  prompt_type: string;
  task_type: string;
  prompt_weight: number;
  task_weight: number;
  scaling_constant: number;
  green_carbon_score: number;
}

export interface OptimizationResult {
  original_prompt: string;
  optimized_prompt: string;
  original_tokens: number;
  optimized_tokens: number;
  token_reduction_percent: number;
  original_carbon_score: number;
  optimized_carbon_score: number;
  carbon_reduction_percent: number;
  original_task_type: string;
  optimized_task_type: string;
  original_prompt_type: string;
  optimized_prompt_type: string;
}

export interface TopModel {
  model: string;
  score: number;
  speed: number;
  latency: number;
  context: number;
  cost_efficiency: number;
  baseline_gmes?: number;
}

export interface RecommendationWeights {
  speed: number;
  latency: number;
  context: number;
  cost_efficiency: number;
}

export interface RecommendationFeatures {
  input_tokens: number;
  expected_output_tokens: number;
  total_tokens: number;
  urgency: boolean;
  cost_sensitive: boolean;
  detail_level: string;
}

export interface RecommendationResult {
  category: string;
  task_type: string;
  recommended_model: string;
  score: number;
  score_type?: string;
  baseline_gmes?: number;
  weights?: RecommendationWeights;
  features?: RecommendationFeatures;
  top_models: TopModel[];
  reason: string[];
}

export interface PipelineData {
  analysis: AnalysisResult;
  carbon: {
    original: CarbonResult;
    optimized: CarbonResult;
  };
  optimization: OptimizationResult;
  recommendation: RecommendationResult;
}

export interface PipelineMetadata {
  processing_time_ms: number;
  pipeline_version: string;
}

export interface ProcessSuccessResponse {
  success: true;
  pipeline: PipelineData;
  metadata: PipelineMetadata;
}

export interface ApiErrorResponse {
  success: false;
  message: string;
  details?: string;
}

export type ProcessResponse = ProcessSuccessResponse | ApiErrorResponse;

export interface HealthResponse {
  status: string;
  version: string;
  modules: Record<string, string>;
}
