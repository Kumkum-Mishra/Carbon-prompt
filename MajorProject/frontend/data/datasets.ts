export interface ResearchNote {
  title: string;
  body: string;
}

export const researchNotes: ResearchNote[] = [
  {
    title: "Reference datasets, not live telemetry",
    body: "The carbon prompt dataset and model dataset are curated reference sets used to calibrate GreenPrompt AI's formulas. They represent a snapshot for benchmarking, not a live feed of production traffic.",
  },
  {
    title: "Prompt type coverage",
    body: "Prompting strategies are intentionally imbalanced: common strategies (Zero-shot, Few-shot, Chain-of-Thought, etc.) are heavily sampled, while advanced/academic strategies (Self-Consistency, Meta Prompting, Analogical Prompting) have smaller sample sizes for comparison.",
  },
  {
    title: "Model dataset scope",
    body: "The model dataset spans five categories — Text, Coding, Vision, Image, and Search — with performance figures (speed, latency, context window, cost) drawn from published provider specifications available at collection time.",
  },
  {
    title: "How this feeds the formulas",
    body: "Carbon prompt statistics inform the Green Carbon Score baseline, and model dataset statistics feed the Green Model Efficiency Score used for model recommendations. See the Mathematics page for the full derivations.",
  },
];
