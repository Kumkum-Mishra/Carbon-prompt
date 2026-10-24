import { render, screen } from "@testing-library/react";
import RecommendationCard from "@/components/analyze/RecommendationCard";

describe("RecommendationCard", () => {
  it("renders model and reasons", () => {
    render(
      <RecommendationCard
        recommendedModel="Gemini Pro"
        score={78.5}
        reasons={["Highest overall GMES", "Fastest response"]}
        topModels={[
          { model: "Gemini Pro", score: 78.5 },
          { model: "GPT-5", score: 74.25 },
        ]}
        category="Coding"
      />
    );
    expect(screen.getByText("Gemini Pro")).toBeInTheDocument();
    expect(screen.getByText("Highest overall GMES")).toBeInTheDocument();
    expect(screen.getByText("GPT-5")).toBeInTheDocument();
  });
});
