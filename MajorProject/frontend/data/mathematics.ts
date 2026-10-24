import type { LucideIcon } from "lucide-react";
import { Cpu, Gauge, Leaf, Scale, SlidersHorizontal, Zap } from "lucide-react";

export interface FormulaVariable {
  symbol: string;
  description: string;
}

export interface FormulaEntry {
  id: string;
  icon: LucideIcon;
  badge: string;
  title: string;
  formula: string;
  variables: FormulaVariable[];
  explanation: string;
  example: string;
  usage: string;
}

/**
 * Formulas mirror the live backend implementations in:
 * carbon/, optimizer/reduction.py, optimizer/ranking_engine.py,
 * recommendation/scorer.py, and recommendation/* weighting modules.
 */
export const formulas: FormulaEntry[] = [
  {
    id: "gcs",
    icon: Leaf,
    badge: "Core Metric",
    title: "Green Carbon Score (GCS)",
    formula: "GCS = TokenCount × PromptWeight × TaskWeight × K",
    variables: [
      { symbol: "TokenCount", description: "Number of input tokens in the prompt (tiktoken)" },
      {
        symbol: "PromptWeight",
        description: "Weight for prompting strategy (Zero-shot=1.0, Few-shot=1.2, CoT=1.5, …)",
      },
      {
        symbol: "TaskWeight",
        description: "Weight for task type (QA=1.0, Writing=1.2, Coding=1.4, Reasoning=1.6, …)",
      },
      { symbol: "K", description: "Scaling constant (0.00001)" },
    ],
    explanation:
      "The Green Carbon Score estimates the relative computational impact of a prompt. It combines token count with weights for the prompting strategy and task type, scaled by constant K. Higher scores indicate greater relative impact. This is a comparative metric, not a direct CO₂ measurement.",
    example: "9 tokens × 1.0 × 1.4 × 0.00001 = 0.000126",
    usage: "Used by the Carbon Estimation module to score every prompt, before and after optimization.",
  },
  {
    id: "token-reduction",
    icon: Zap,
    badge: "Comparative",
    title: "Token Reduction",
    formula: "TokenReduction(%) = ((OriginalTokens - OptimizedTokens) / OriginalTokens) × 100",
    variables: [
      { symbol: "OriginalTokens", description: "Token count before optimization" },
      { symbol: "OptimizedTokens", description: "Token count after optimization" },
    ],
    explanation:
      "Measures how many fewer input tokens the optimized prompt uses compared to the original. Higher percentages indicate greater token savings and improved sustainability.",
    example: "((26 - 13) / 26) × 100 = 50.0%",
    usage: "Calculated by the Prompt Optimizer to report savings after rewriting a prompt.",
  },
  {
    id: "carbon-reduction",
    icon: Gauge,
    badge: "Comparative",
    title: "Carbon Reduction",
    formula: "CarbonReduction(%) = ((OriginalCarbon - OptimizedCarbon) / OriginalCarbon) × 100",
    variables: [
      { symbol: "OriginalCarbon", description: "Green Carbon Score before optimization" },
      { symbol: "OptimizedCarbon", description: "Green Carbon Score after optimization" },
    ],
    explanation:
      "Measures the percentage decrease in Green Carbon Score after optimization. Higher percentages indicate greater sustainability improvement from prompt refinement.",
    example: "((0.00039 - 0.00021) / 0.00039) × 100 = 46.15%",
    usage: "Reported alongside Token Reduction to summarize the sustainability gain of optimization.",
  },
  {
    id: "candidate-score",
    icon: Scale,
    badge: "Optimization",
    title: "Optimizer Candidate Score",
    formula:
      "CandidateScore = 0.45×Similarity + 0.25×TokenGain + 0.15×Readability + 0.15×CarbonGain − Penalties",
    variables: [
      {
        symbol: "Similarity",
        description: "Lexical similarity between original and candidate (reject if < 0.50)",
      },
      {
        symbol: "TokenGain",
        description: "Normalized token-reduction component (capped)",
      },
      {
        symbol: "Readability",
        description: "Heuristic clarity score for the rewritten prompt",
      },
      {
        symbol: "CarbonGain",
        description: "Normalized carbon-reduction component (capped)",
      },
      {
        symbol: "Penalties",
        description: "Task-type change (−0.12) and prompt-type change (−0.04) when classifications shift",
      },
    ],
    explanation:
      "After the trained optimizer generates rewrite candidates, each candidate is re-analyzed and scored. The highest CandidateScore is kept. If every candidate fails similarity or constraint checks, the original prompt is retained.",
    example: "0.45×0.60 + 0.25×0.63 + 0.15×1.0 + 0.15×0.63 = 0.66 (before penalties)",
    usage: "Used inside the Prompt Optimizer to choose among beam-search rewrite candidates.",
  },
  {
    id: "gmes",
    icon: Cpu,
    badge: "Baseline Ranking",
    title: "Green Model Efficiency Score (GMES)",
    formula:
      "CostEfficiency = 100 − ((InputCost + OutputCost) / 2)\nGMES = (Speed + Latency + Context + CostEfficiency) / 4",
    variables: [
      { symbol: "Speed", description: "Normalized speed score (0–100, higher is better)" },
      {
        symbol: "Latency",
        description: "Normalized latency score (0–100, lower raw latency = higher score)",
      },
      { symbol: "Context", description: "Normalized context window score (0–100)" },
      {
        symbol: "InputCost / OutputCost",
        description: "Normalized cost scores (0–100, higher = more expensive)",
      },
      { symbol: "CostEfficiency", description: "100 minus average normalized cost" },
    ],
    explanation:
      "GMES is the equal-weight baseline for model ranking. It averages four normalized metrics with weights of 0.25 each. Model metric values come from model_data.csv and do not change with the prompt. GMES remains available for comparison and ablation; live Analyze defaults to DGMES.",
    example: "GPT-5: (90 + 88 + 100 + 19) / 4 = 74.25 · Gemini Pro: (95 + 94 + 96 + 29) / 4 = 78.5",
    usage: "Equal-weight baseline in Model Recommendation (mode = equal_gmes). Also returned as baseline_gmes alongside DGMES.",
  },
  {
    id: "dgmes",
    icon: SlidersHorizontal,
    badge: "Dynamic Ranking",
    title: "Dynamic GMES (DGMES)",
    formula:
      "P_C = max(0.05, min(1, T_in / 80000))\nP_S = 0.25 | 0.55 | 1.0  (by expected output size)\nP_L = 1.0 if urgent else 0.30\nP_E = 0.20 | 0.50 | 1.0  (by total tokens; +0.25 if cost-sensitive)\n\nw_i = P_i / ΣP\n\nDGMES = w_S·Speed + w_L·Latency + w_C·Context + w_E·CostEfficiency",
    variables: [
      { symbol: "T_in", description: "Input token count from the analyzer" },
      {
        symbol: "P_S / P_L / P_C / P_E",
        description: "Priorities for speed, latency, context, and cost (derived from the prompt)",
      },
      {
        symbol: "w_S / w_L / w_C / w_E",
        description: "Normalized weights that sum to 1",
      },
      {
        symbol: "Speed / Latency / Context / CostEfficiency",
        description: "Same static normalized model metrics used by GMES (unchanged by the prompt)",
      },
    ],
    explanation:
      "DGMES keeps every model metric fixed and only changes how much each metric matters for the current prompt. Features such as input tokens, expected output size, urgency keywords (quick, fast, …), and cost keywords (cheap, budget, …) produce priorities, which are normalized into weights. This is the default recommendation score in Analyze.",
    example:
      "Priorities 0.55, 1.0, 0.5, 1.0 → weights 0.180, 0.328, 0.164, 0.328 → FastCheap DGMES = 83.36",
    usage: "Default Model Recommendation path (RECOMMENDATION_SCORING_MODE=dynamic_dgmes).",
  },
];

export interface WorkedExampleStep {
  label: string;
  formulaId: string;
  value: string;
  detail: string;
}

/**
 * A single illustrative prompt walked through the live formula set.
 * Figures are for demonstration and use the formulas above.
 */
export const workedExample = {
  prompt:
    "Can you please explain in great detail, with many examples, how neural networks work and also discuss all their applications?",
  optimizedPrompt: "Explain how neural networks work, with examples and applications.",
  steps: [
    {
      label: "1. Analyze",
      formulaId: "gcs",
      value: "24 tokens · Zero-shot · Writing",
      detail: "The prompt analyzer counts tokens and detects prompt style and task type.",
    },
    {
      label: "2. Estimate (GCS)",
      formulaId: "gcs",
      value: "24 × 1.0 × 1.2 × 0.00001 = 0.000288",
      detail: "PromptWeight 1.0 (Zero-shot) and TaskWeight 1.2 (Writing) are applied.",
    },
    {
      label: "3. Optimize",
      formulaId: "token-reduction",
      value: "((24 - 12) / 24) × 100 = 50.0%",
      detail: "The rewritten prompt uses 12 tokens instead of 24, a 50% reduction.",
    },
    {
      label: "4. Rank rewrite candidates",
      formulaId: "candidate-score",
      value: "Best CandidateScore kept",
      detail: "Beam candidates are scored for similarity, token gain, readability, and carbon gain.",
    },
    {
      label: "5. Re-estimate (GCS)",
      formulaId: "carbon-reduction",
      value: "((0.000288 - 0.000144) / 0.000288) × 100 = 50.0%",
      detail: "Fewer tokens directly lower the optimized Green Carbon Score.",
    },
    {
      label: "6. Recommend (DGMES)",
      formulaId: "dgmes",
      value: "w_L≈0.38 · DGMES ranks models",
      detail: "Prompt features set dynamic weights; models are ranked by DGMES, not equal-weight GMES alone.",
    },
  ] satisfies WorkedExampleStep[],
};

export interface LimitationEntry {
  title: string;
  description: string;
}

export const limitations: LimitationEntry[] = [
  {
    title: "GCS is relative, not measured CO₂",
    description:
      "The Green Carbon Score compares prompts against each other using token count and weights. It is not a direct measurement of emitted carbon.",
  },
  {
    title: "Model metrics are static; weights are dynamic",
    description:
      "Speed, latency, context, and cost values come from model_data.csv and do not change with the prompt. DGMES only changes how much each metric matters.",
  },
  {
    title: "Expected output size is a heuristic",
    description:
      "DGMES cost and speed priorities use an estimated output length from task type, detail keywords, and explicit word counts — not a measured generation.",
  },
  {
    title: "Recommendations are scoped to available models",
    description:
      "Model Recommendation can only rank models present in its dataset. A better-suited model outside that dataset would not be suggested.",
  },
  {
    title: "Optimization does not guarantee reduction",
    description:
      "The optimizer prioritizes preserving intent. Some prompts are already concise and may see little or no token or carbon reduction.",
  },
];
