export function formatNumber(value: number, decimals = 2): string {
  return value.toLocaleString(undefined, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

export function formatPercent(value: number): string {
  return `${formatNumber(value, 2)}%`;
}

export function formatCarbonScore(value: number): string {
  if (value === 0) return "0";
  if (value < 0.001) return value.toFixed(6);
  return value.toFixed(4);
}

export function formatProcessingTime(ms: number): string {
  return `Completed in ${Math.round(ms)} ms`;
}
