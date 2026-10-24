"use client";

import { ArrowDownRight, ArrowRight, BarChart3, Leaf } from "lucide-react";
import Badge from "@/components/ui/Badge";
import IconBox from "@/components/ui/IconBox";
import { formatPercent } from "@/utils/formatters";
import { cn } from "@/utils/cn";

export interface PromptAnalysisOptimizationCardProps {
  taskType: string;
  promptType: string;
  tokenCount: number;
  characterCount: number;
  wordCount: number;
  originalTokens: number;
  optimizedTokens: number;
  tokenReductionPercent: number;
  carbonReductionPercent: number;
}

export default function PromptAnalysisOptimizationCard({
  taskType,
  promptType,
  tokenCount,
  characterCount,
  wordCount,
  originalTokens,
  optimizedTokens,
  tokenReductionPercent,
  carbonReductionPercent,
}: PromptAnalysisOptimizationCardProps) {
  const stats = [
    { label: "Tokens", value: tokenCount, accent: true },
    { label: "Words", value: wordCount },
    { label: "Characters", value: characterCount },
  ];

  return (
    <div className="flex h-full min-w-0 flex-col rounded-card border border-slate-200 bg-white p-5">
      <div className="flex items-center gap-2.5">
        <IconBox icon={BarChart3} />
        <h3 className="text-base font-semibold leading-tight text-slate-900">
          Analysis &amp; Optimization
        </h3>
      </div>

      <div className="mt-4 flex flex-1 flex-col gap-3">
        {/* Section 1: classification */}
        <div className="grid grid-cols-2 gap-2.5">
          <div className="rounded-inner bg-slate-50 px-3 py-2.5">
            <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
              Prompt Type
            </p>
            <div className="mt-1.5">
              <Badge variant="violet">{promptType}</Badge>
            </div>
          </div>
          <div className="rounded-inner bg-slate-50 px-3 py-2.5">
            <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
              Task Type
            </p>
            <div className="mt-1.5">
              <Badge variant="blue">{taskType}</Badge>
            </div>
          </div>
        </div>

        {/* Section 2: input stats */}
        <div className="grid grid-cols-3 gap-2">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className="rounded-inner bg-slate-50 px-2.5 py-2.5 text-center sm:px-3"
            >
              <p className="text-[10px] font-medium uppercase tracking-wide text-slate-500 sm:text-[11px]">
                {stat.label}
              </p>
              <p
                className={cn(
                  "mt-0.5 text-lg font-bold tabular-nums sm:text-xl",
                  stat.accent ? "text-emerald-700" : "text-slate-900"
                )}
              >
                {stat.value}
              </p>
            </div>
          ))}
        </div>

        {/* Section 3: before → after */}
        <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-2 rounded-inner border border-slate-100 bg-slate-50/80 px-2 py-3 sm:gap-3 sm:px-3">
          <div className="text-center">
            <p className="text-[10px] font-medium uppercase tracking-wide text-slate-500 sm:text-[11px]">
              Before
            </p>
            <p className="mt-0.5 text-xl font-bold tabular-nums text-slate-900 sm:text-2xl">
              {originalTokens}
            </p>
            <p className="text-[10px] text-slate-500 sm:text-xs">tokens</p>
          </div>
          <ArrowRight
            className="h-4 w-4 shrink-0 text-emerald-500"
            strokeWidth={1.75}
            aria-hidden
          />
          <div className="text-center">
            <p className="text-[10px] font-medium uppercase tracking-wide text-emerald-700 sm:text-[11px]">
              After
            </p>
            <p className="mt-0.5 text-xl font-bold tabular-nums text-emerald-800 sm:text-2xl">
              {optimizedTokens}
            </p>
            <p className="text-[10px] text-emerald-700/80 sm:text-xs">tokens</p>
          </div>
        </div>

        {/* Section 4: reductions */}
        <div className="mt-auto grid grid-cols-2 gap-2">
          <div className="rounded-inner bg-slate-50 px-3 py-2.5">
            <div className="flex items-center gap-1 text-slate-500">
              <ArrowDownRight className="h-3.5 w-3.5 shrink-0" strokeWidth={1.75} />
              <p className="text-[10px] font-medium uppercase tracking-wide sm:text-[11px]">
                Token Reduction
              </p>
            </div>
            <p className="mt-1 text-lg font-bold tabular-nums text-emerald-700 sm:text-xl">
              {formatPercent(tokenReductionPercent)}
            </p>
          </div>
          <div className="rounded-inner border border-emerald-100 bg-emerald-50 px-3 py-2.5">
            <div className="flex items-center gap-1 text-emerald-700">
              <Leaf className="h-3.5 w-3.5 shrink-0" strokeWidth={1.75} />
              <p className="text-[10px] font-medium uppercase tracking-wide sm:text-[11px]">
                Carbon Reduction
              </p>
            </div>
            <p className="mt-1 text-lg font-bold tabular-nums text-emerald-800 sm:text-xl">
              {formatPercent(carbonReductionPercent)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
