export type DiffSegmentType = "equal" | "add" | "remove";

export interface DiffSegment {
  type: DiffSegmentType;
  value: string;
}

/**
 * Tokenize into words, punctuation, and whitespace so "scalability." and
 * "scalability" / "issues." compare cleanly at the word level.
 */
export function tokenizeWords(text: string): string[] {
  return text.match(/\w+|[^\w\s]+|\s+/g) ?? [];
}

/**
 * Word-level Myers/LCS diff. Returns a single sequence of equal/add/remove
 * segments suitable for GitHub-style side-by-side rendering.
 */
export function diffWords(original: string, optimized: string): DiffSegment[] {
  const a = tokenizeWords(original);
  const b = tokenizeWords(optimized);
  const n = a.length;
  const m = b.length;

  const dp: number[][] = Array.from({ length: n + 1 }, () =>
    Array(m + 1).fill(0)
  );

  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      if (a[i] === b[j]) {
        dp[i][j] = dp[i + 1][j + 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
  }

  const raw: DiffSegment[] = [];
  let i = 0;
  let j = 0;
  while (i < n && j < m) {
    if (a[i] === b[j]) {
      raw.push({ type: "equal", value: a[i] });
      i += 1;
      j += 1;
    } else if (dp[i + 1][j] >= dp[i][j + 1]) {
      raw.push({ type: "remove", value: a[i] });
      i += 1;
    } else {
      raw.push({ type: "add", value: b[j] });
      j += 1;
    }
  }
  while (i < n) {
    raw.push({ type: "remove", value: a[i] });
    i += 1;
  }
  while (j < m) {
    raw.push({ type: "add", value: b[j] });
    j += 1;
  }

  return mergeAdjacent(raw);
}

function mergeAdjacent(segments: DiffSegment[]): DiffSegment[] {
  if (segments.length === 0) return segments;
  const merged: DiffSegment[] = [{ ...segments[0] }];
  for (let k = 1; k < segments.length; k++) {
    const prev = merged[merged.length - 1];
    const curr = segments[k];
    if (prev.type === curr.type) {
      prev.value += curr.value;
    } else {
      merged.push({ ...curr });
    }
  }
  return merged;
}

/** Segments visible in the Original pane (equal + removals). */
export function originalSideSegments(segments: DiffSegment[]): DiffSegment[] {
  return segments.filter((s) => s.type === "equal" || s.type === "remove");
}

/** Segments visible in the Optimized pane (equal + additions). */
export function optimizedSideSegments(segments: DiffSegment[]): DiffSegment[] {
  return segments.filter((s) => s.type === "equal" || s.type === "add");
}
