import type { LucideIcon } from "lucide-react";
import {
  BarChart3,
  Cpu,
  FlaskConical,
  Gauge,
  Layers,
  LineChart,
  Search,
  ShieldCheck,
  Sparkles,
  Wand2,
} from "lucide-react";

export interface InsightItem {
  icon: LucideIcon;
  title: string;
  description: string;
}

export const problemInsights: InsightItem[] = [
  {
    icon: Layers,
    title: "Every Token Has a Cost",
    description:
      "Each prompt token consumes real compute cycles on inference hardware, and that cost compounds at scale.",
  },
  {
    icon: Cpu,
    title: "More Tokens, More Compute",
    description:
      "Longer, noisier prompts increase inference time and energy draw without improving output quality.",
  },
  {
    icon: Wand2,
    title: "Prompt Style Matters",
    description:
      "Chain-of-Thought, few-shot, and other strategies carry very different computational weight.",
  },
];

export interface WorkflowStep {
  icon: LucideIcon;
  title: string;
  description: string;
}

export const workflowSteps: WorkflowStep[] = [
  {
    icon: Search,
    title: "Analyze",
    description: "Detect task type, prompt style, and token usage.",
  },
  {
    icon: Gauge,
    title: "Estimate",
    description: "Calculate a Green Carbon Score for the prompt.",
  },
  {
    icon: Wand2,
    title: "Optimize",
    description: "Rewrite the prompt shorter and clearer, same intent.",
  },
  {
    icon: Cpu,
    title: "Recommend",
    description: "Rank models by speed, latency, context, and cost.",
  },
];

export interface FeatureItem {
  icon: LucideIcon;
  title: string;
  description: string;
  metric: string;
}

export const featureItems: FeatureItem[] = [
  {
    icon: BarChart3,
    title: "Prompt Analyzer",
    description:
      "Classifies task type and prompt strategy, then counts tokens with precision.",
    metric: "Token-level precision",
  },
  {
    icon: Gauge,
    title: "Carbon Estimation",
    description:
      "Estimates the relative computational impact of a prompt using the Green Carbon Score.",
    metric: "Relative GCS scoring",
  },
  {
    icon: Wand2,
    title: "Prompt Optimizer",
    description:
      "Rewrites prompts to reduce tokens and complexity while preserving intent.",
    metric: "Up to 40% shorter",
  },
  {
    icon: Cpu,
    title: "Model Recommendation",
    description:
      "Ranks AI models by speed, latency, context window, and cost efficiency.",
    metric: "4-factor GMES ranking",
  },
];

export interface MetricPreviewItem {
  label: string;
  value: number;
  suffix: string;
  helper: string;
  decimals?: number;
}

export const metricPreviewItems: MetricPreviewItem[] = [
  {
    label: "Token Reduction",
    value: 33.3,
    suffix: "%",
    helper: "Compared with the original prompt",
    decimals: 1,
  },
  {
    label: "Carbon Reduction",
    value: 28.4,
    suffix: "%",
    helper: "Lower Green Carbon Score after optimization",
    decimals: 1,
  },
  {
    label: "Avg. GMES Score",
    value: 87.4,
    suffix: "",
    helper: "Speed, latency, context, and cost combined",
    decimals: 1,
  },
  {
    label: "Prompts Benchmarked",
    value: 10000,
    suffix: "+",
    helper: "Across the research dataset",
    decimals: 0,
  },
];

export interface ArchitectureNode {
  icon: LucideIcon;
  label: string;
}

export const architectureNodes: ArchitectureNode[] = [
  { icon: Sparkles, label: "Prompt Input" },
  { icon: Search, label: "Analyzer" },
  { icon: Gauge, label: "Carbon Engine" },
  { icon: Wand2, label: "Optimizer" },
  { icon: Cpu, label: "Recommender" },
  { icon: LineChart, label: "Results" },
];

export const technologies = [
  "Next.js",
  "React",
  "TypeScript",
  "Tailwind CSS",
  "Framer Motion",
  "FastAPI",
  "Python",
  "Recharts",
];

export const researchInsights: InsightItem[] = [
  {
    icon: ShieldCheck,
    title: "GCS is a Relative Score",
    description:
      "The Green Carbon Score compares prompts against each other. It is not a direct CO2 measurement.",
  },
  {
    icon: FlaskConical,
    title: "Dataset-Driven Rankings",
    description:
      "Model scores are computed from benchmarked dataset metrics, not vendor marketing claims.",
  },
  {
    icon: Sparkles,
    title: "Context-Aware Optimization",
    description:
      "Optimization preserves intent first. Token reduction follows only when it is safe to do so.",
  },
];
