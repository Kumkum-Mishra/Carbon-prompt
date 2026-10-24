import { cn } from "@/utils/cn";
import type { DiffSegment } from "@/utils/wordDiff";

interface PromptDiffViewProps {
  segments: DiffSegment[];
  side: "original" | "optimized";
  className?: string;
}

/**
 * Renders word-level diff tokens.
 * Original: removals = red strikethrough.
 * Optimized: additions = soft green background.
 */
export default function PromptDiffView({
  segments,
  side,
  className,
}: PromptDiffViewProps) {
  return (
    <p
      className={cn(
        "whitespace-pre-wrap break-words text-[15px] leading-[1.65] text-slate-800",
        className
      )}
      aria-label={side === "original" ? "Original prompt with changes" : "Optimized prompt with changes"}
    >
      {segments.map((segment, index) => {
        if (segment.type === "equal") {
          return <span key={index}>{segment.value}</span>;
        }
        if (side === "original" && segment.type === "remove") {
          return (
            <span
              key={index}
              className="rounded-sm bg-red-50 text-red-600 line-through decoration-red-400/80"
            >
              {segment.value}
            </span>
          );
        }
        if (side === "optimized" && segment.type === "add") {
          return (
            <span
              key={index}
              className="rounded-sm bg-emerald-100/90 px-0.5 text-emerald-900"
            >
              {segment.value}
            </span>
          );
        }
        return null;
      })}
    </p>
  );
}
