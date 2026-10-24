import { render, screen } from "@testing-library/react";
import OptimizationCard from "@/components/analyze/OptimizationCard";

describe("OptimizationCard", () => {
  it("shows before/after token comparison and reductions", () => {
    render(
      <OptimizationCard
        originalTokens={9}
        optimizedTokens={6}
        tokenReductionPercent={33.33}
        carbonReductionPercent={40}
      />
    );
    expect(screen.getByText("9")).toBeInTheDocument();
    expect(screen.getByText("6")).toBeInTheDocument();
    expect(screen.getByText("33.33%")).toBeInTheDocument();
    expect(screen.getByText("40.00%")).toBeInTheDocument();
    expect(screen.getByText("−3 tokens")).toBeInTheDocument();
    expect(screen.queryByText(/Write CNN/)).not.toBeInTheDocument();
  });
});
