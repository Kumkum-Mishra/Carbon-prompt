import {
  diffWords,
  optimizedSideSegments,
  originalSideSegments,
} from "@/utils/wordDiff";

describe("wordDiff", () => {
  it("marks removals and keeps shared words", () => {
    const original =
      "Act as a senior backend engineer and carefully review this API design for scalability issues.";
    const optimized =
      "Act as a senior backend engineer and review this API design for scalability.";

    const segments = diffWords(original, optimized);
    const originalSide = originalSideSegments(segments);
    const optimizedSide = optimizedSideSegments(segments);

    const removed = originalSide
      .filter((s) => s.type === "remove")
      .map((s) => s.value.trim())
      .filter(Boolean);
    const added = optimizedSide
      .filter((s) => s.type === "add")
      .map((s) => s.value.trim())
      .filter(Boolean);

    expect(removed.join(" ")).toContain("carefully");
    expect(removed.join(" ")).toContain("issues");
    expect(added).toHaveLength(0);
    expect(optimizedSide.map((s) => s.value).join("")).toBe(optimized);
  });

  it("marks additions with green-side segments", () => {
    const segments = diffWords("Write CNN code", "Write a PyTorch CNN");
    const added = optimizedSideSegments(segments).filter((s) => s.type === "add");
    const removed = originalSideSegments(segments).filter((s) => s.type === "remove");

    expect(added.some((s) => s.value.includes("PyTorch") || s.value.includes("a"))).toBe(
      true
    );
    expect(removed.some((s) => s.value.includes("code"))).toBe(true);
  });
});
