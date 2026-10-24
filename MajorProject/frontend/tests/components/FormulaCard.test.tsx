import { render, screen } from "@testing-library/react";
import FormulaCard from "@/components/mathematics/FormulaCard";

describe("FormulaCard", () => {
  it("renders formula and explanation", () => {
    render(
      <FormulaCard
        title="Green Carbon Score"
        formula="GCS = TokenCount × PromptWeight × TaskWeight × K"
        variables={[
          { symbol: "TokenCount", description: "Input tokens" },
        ]}
        explanation="Relative computational impact metric."
        example="9 × 1.0 × 1.4 × 0.00001 = 0.000126"
      />
    );
    expect(screen.getByText("Green Carbon Score")).toBeInTheDocument();

    // The formula is syntax-highlighted, so its text is split across
    // multiple <span> elements. Match against the containing element's
    // full text content instead of a single text node.
    expect(
      screen.getByText(
        (_, element) =>
          element?.tagName.toLowerCase() === "pre" &&
          element.textContent === "GCS = TokenCount × PromptWeight × TaskWeight × K"
      )
    ).toBeInTheDocument();
    expect(screen.getByText("Relative computational impact metric.")).toBeInTheDocument();
  });
});
