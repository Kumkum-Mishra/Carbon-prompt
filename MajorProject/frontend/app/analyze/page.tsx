"use client";

import { motion } from "framer-motion";
import AnalyzeEmptyState from "@/components/analyze/AnalyzeEmptyState";
import AnalyzeErrorState from "@/components/analyze/AnalyzeErrorState";
import PipelineLoader from "@/components/analyze/PipelineLoader";
import PromptInput from "@/components/analyze/PromptInput";
import ResultsPanel from "@/components/analyze/ResultsPanel";
import PageContainer from "@/components/layout/PageContainer";
import { fadeInUp, staggerDefault } from "@/design/motion";
import { useProcessPrompt } from "@/hooks/useProcessPrompt";

export default function AnalyzePage() {
  const {
    result,
    error,
    errorDetails,
    isLoading,
    loadingStep,
    submit,
    retry,
  } = useProcessPrompt();

  const showEmptyState = !result && !error && !isLoading;

  return (
    <PageContainer
      title="Prompt Analysis"
      subtitle="Analyze, optimize, and get model recommendations for your prompt in one workflow."
    >
      <motion.div
        initial="hidden"
        animate="visible"
        variants={staggerDefault()}
        className="space-y-10"
      >
        <PromptInput
          onSubmit={submit}
          isLoading={isLoading}
          optimizedPrompt={
            result && !isLoading
              ? result.pipeline.optimization.optimized_prompt
              : null
          }
        />

        {error && !isLoading && (
          <motion.div variants={fadeInUp}>
            <AnalyzeErrorState
              message={error}
              details={errorDetails ?? undefined}
              onRetry={retry}
            />
          </motion.div>
        )}

        {isLoading && <PipelineLoader step={loadingStep} />}

        {result && !isLoading && <ResultsPanel result={result} />}

        {showEmptyState && (
          <motion.div variants={fadeInUp}>
            <AnalyzeEmptyState />
          </motion.div>
        )}
      </motion.div>
    </PageContainer>
  );
}
