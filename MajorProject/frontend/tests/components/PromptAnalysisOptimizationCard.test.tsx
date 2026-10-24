import { render, screen } from "@testing-library/react";
import PromptAnalysisOptimizationCard from "@/components/analyze/PromptAnalysisOptimizationCard";

describe("PromptAnalysisOptimizationCard", () => {
  it("renders merged analysis and optimization metrics", () => {
    render(
      <PromptAnalysisOptimizationCard
        taskType="Coding"
        promptType="Zero-shot"
        tokenCount={26}
        characterCount={32}
        wordCount={6}
        originalTokens={26}
        optimizedTokens={13}
        tokenReductionPercent={50}
        carbonReductionPercent={46.15}
      />
    );
    expect(screen.getByText("Coding")).toBeInTheDocument();
    expect(screen.getByText("Zero-shot")).toBeInTheDocument();
    expect(screen.getAllByText("26").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("13")).toBeInTheDocument();
    expect(screen.getByText("50.00%")).toBeInTheDocument();
    expect(screen.getByText("46.15%")).toBeInTheDocument();
    expect(screen.getByText("Analysis & Optimization")).toBeInTheDocument();
  });
});
