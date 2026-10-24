import { render, screen } from "@testing-library/react";
import CarbonCard from "@/components/analyze/CarbonCard";

describe("CarbonCard", () => {
  it("displays reduction percentage", () => {
    render(
      <CarbonCard
        originalScore={0.000126}
        optimizedScore={0.000084}
        reductionPercent={33.33}
      />
    );
    expect(screen.getByText("33.33%")).toBeInTheDocument();
    expect(screen.getByText("Original GCS")).toBeInTheDocument();
    expect(screen.getByText("Optimized GCS")).toBeInTheDocument();
  });
});
