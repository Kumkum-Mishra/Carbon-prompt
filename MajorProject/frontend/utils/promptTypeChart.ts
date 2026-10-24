const FEATURED_PROMPT_TYPES = [
  { key: "Zero Shot", label: "Zero Shot" },
  { key: "One Shot", label: "One Shot" },
  { key: "Few Shot", label: "Few Shot" },
  { key: "Chain Of Thought", label: "Chain of Thought" },
  { key: "Role Prompting", label: "Role Prompting" },
  { key: "Persona Prompting", label: "Persona Prompting" },
  { key: "Tree Of Thought", label: "Tree of Thought" },
  { key: "React", label: "ReAct" },
  { key: "Structured Prompt", label: "Structured Prompt" },
] as const;

const FEATURED_KEYS = new Set(
  FEATURED_PROMPT_TYPES.map((promptType) => promptType.key)
);

export const PROMPT_TYPE_CHART_COLORS = [
  "#14532d",
  "#166534",
  "#15803d",
  "#16a34a",
  "#22c55e",
  "#4ade80",
  "#65a30d",
  "#84cc16",
  "#a3e635",
  "#78716c",
] as const;

export function groupPromptTypeDistribution(
  distribution: Record<string, number>
): { name: string; value: number }[] {
  const grouped: { name: string; value: number }[] = FEATURED_PROMPT_TYPES.map(
    ({ key, label }) => ({
      name: label,
      value: distribution[key] ?? 0,
    })
  );

  const otherValue = Object.entries(distribution).reduce(
    (sum, [key, value]) =>
      (FEATURED_KEYS as Set<string>).has(key) ? sum : sum + value,
    0
  );

  grouped.push({ name: "Other Types", value: otherValue });

  return grouped;
}
