"use client";

import { Leaf, Zap } from "lucide-react";
import { motion } from "framer-motion";
import type { ProcessSuccessResponse } from "@/types/api";
import { fadeInUp, staggerTight } from "@/design/motion";
import {
  formatNumber,
  formatPercent,
  formatProcessingTime,
} from "@/utils/formatters";
import CarbonCard from "./CarbonCard";
import PromptAnalysisOptimizationCard from "./PromptAnalysisOptimizationCard";
import RecommendationCard from "./RecommendationCard";

interface ResultsPanelProps {
  result: ProcessSuccessResponse;
}

export default function ResultsPanel({ result }: ResultsPanelProps) {
  const { pipeline, metadata } = result;
  const { analysis, carbon, optimization, recommendation } = pipeline;

  const recommendedModel = recommendation.recommended_model;
  const recommendedEntry =
    recommendation.top_models.find((model) => model.model === recommendedModel) ??
    recommendation.top_models[0];
  const modelSpeed = recommendedEntry?.speed;
  const carbonReduction = optimization.carbon_reduction_percent;
  const scoreLabel = recommendation.score_type ?? "DGMES";

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={staggerTight()}
      className="space-y-4"
    >
      <motion.div
        variants={fadeInUp}
        className="flex items-center justify-between gap-3"
      >
        <h2 className="text-lg font-semibold text-slate-900">Results</h2>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
          {formatProcessingTime(metadata.processing_time_ms)}
        </span>
      </motion.div>

      {/* Single dashboard row: Carbon | Analysis & Optimization | Recommendation */}
      <div className="grid grid-cols-1 items-stretch gap-4 md:grid-cols-2 xl:grid-cols-3">
        <motion.div variants={fadeInUp} className="min-h-0 min-w-0">
          <CarbonCard
            originalScore={carbon.original.green_carbon_score}
            optimizedScore={carbon.optimized.green_carbon_score}
            reductionPercent={optimization.carbon_reduction_percent}
          />
        </motion.div>

        <motion.div variants={fadeInUp} className="min-h-0 min-w-0">
          <PromptAnalysisOptimizationCard
            taskType={analysis.task_type}
            promptType={analysis.prompt_type}
            tokenCount={analysis.token_count}
            characterCount={analysis.character_count}
            wordCount={analysis.word_count}
            originalTokens={optimization.original_tokens}
            optimizedTokens={optimization.optimized_tokens}
            tokenReductionPercent={optimization.token_reduction_percent}
            carbonReductionPercent={optimization.carbon_reduction_percent}
          />
        </motion.div>

        <motion.div
          variants={fadeInUp}
          className="min-h-0 min-w-0 md:col-span-2 xl:col-span-1"
        >
          <RecommendationCard
            recommendedModel={recommendation.recommended_model}
            score={recommendation.score}
            scoreType={recommendation.score_type}
            reasons={recommendation.reason}
            topModels={recommendation.top_models}
            category={recommendation.category}
            weights={recommendation.weights}
          />
        </motion.div>
      </div>

      <motion.div
        variants={fadeInUp}
        className="grid grid-cols-1 gap-3 sm:grid-cols-2"
      >
        <div className="flex gap-3 rounded-card border border-slate-200 bg-white p-4">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-amber-50 text-amber-600">
            <Zap className="h-4 w-4" strokeWidth={1.75} />
          </div>
          <div className="min-w-0">
            <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
              Response speed
            </p>
            <p className="mt-1 text-sm leading-relaxed text-slate-700">
              <span className="font-semibold text-slate-900">
                {recommendedModel}
              </span>{" "}
              is expected to respond quickly, with a dataset speed score of{" "}
              <span className="font-semibold text-amber-700">
                {modelSpeed != null ? `${formatNumber(modelSpeed, 0)}/100` : "—"}
              </span>
              {recommendation.score != null && (
                <>
                  {" "}
                  and a {scoreLabel} of{" "}
                  <span className="font-semibold text-slate-900">
                    {formatNumber(recommendation.score)}
                  </span>
                </>
              )}
              .
            </p>
          </div>
        </div>

        <div className="flex gap-3 rounded-card border border-slate-200 bg-white p-4">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-emerald-50 text-emerald-600">
            <Leaf className="h-4 w-4" strokeWidth={1.75} />
          </div>
          <div className="min-w-0">
            <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
              Carbon savings
            </p>
            <p className="mt-1 text-sm leading-relaxed text-slate-700">
              Together, your optimized prompt and{" "}
              <span className="font-semibold text-slate-900">
                {recommendedModel}
              </span>{" "}
              reduce carbon impact by{" "}
              <span className="font-semibold text-emerald-700">
                {formatPercent(carbonReduction)}
              </span>
              .
            </p>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
