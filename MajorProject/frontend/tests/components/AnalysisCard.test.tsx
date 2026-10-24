import { render, screen } from "@testing-library/react";
import AnalysisCard from "@/components/analyze/AnalysisCard";

describe("AnalysisCard", () => {
  it("renders all analysis fields", () => {
    render(
      <AnalysisCard
        taskType="Coding"
        promptType="Zero-shot"
        tokenCount={9}
        characterCount={32}
        wordCount={6}
      />
    );
    expect(screen.getByText("Coding")).toBeInTheDocument();
    expect(screen.getByText("Zero-shot")).toBeInTheDocument();
    expect(screen.getByText("9")).toBeInTheDocument();
    expect(screen.getByText("32")).toBeInTheDocument();
    expect(screen.getByText("6")).toBeInTheDocument();
  });
});
