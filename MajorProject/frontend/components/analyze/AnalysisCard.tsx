import { BarChart3 } from "lucide-react";
import Badge from "@/components/ui/Badge";
import IconBox from "@/components/ui/IconBox";
import { cn } from "@/utils/cn";

export interface AnalysisCardProps {
  taskType: string;
  promptType: string;
  tokenCount: number;
  characterCount: number;
  wordCount: number;
}

export default function AnalysisCard({
  taskType,
  promptType,
  tokenCount,
  characterCount,
  wordCount,
}: AnalysisCardProps) {
  const stats = [
    { label: "Tokens", value: tokenCount, accent: true },
    { label: "Words", value: wordCount },
    { label: "Characters", value: characterCount },
  ];

  return (
    <div className="flex h-full flex-col rounded-card border border-slate-200 bg-white p-5">
      <div className="flex items-center gap-2.5">
        <IconBox icon={BarChart3} />
        <h3 className="text-base font-semibold text-slate-900">
          Prompt Analysis
        </h3>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        <Badge variant="violet">{promptType}</Badge>
        <Badge variant="blue">{taskType}</Badge>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2.5">
        {stats.map((stat) => (
          <div key={stat.label} className="rounded-inner bg-slate-50 px-3 py-2.5">
            <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
              {stat.label}
            </p>
            <p
              className={cn(
                "mt-0.5 text-xl font-bold tabular-nums",
                stat.accent ? "text-emerald-700" : "text-slate-900"
              )}
            >
              {stat.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
