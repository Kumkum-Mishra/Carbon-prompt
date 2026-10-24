"use client";

import { ArrowDownRight, ArrowRight, Leaf, Zap } from "lucide-react";
import IconBox from "@/components/ui/IconBox";
import { formatPercent } from "@/utils/formatters";
import { cn } from "@/utils/cn";

export interface OptimizationCardProps {
  originalTokens: number;
  optimizedTokens: number;
  tokenReductionPercent: number;
  carbonReductionPercent: number;
}

export default function OptimizationCard({
  originalTokens,
  optimizedTokens,
  tokenReductionPercent,
  carbonReductionPercent,
}: OptimizationCardProps) {
  const tokenDelta = originalTokens - optimizedTokens;
  const tokenBarWidth = Math.min(Math.max(tokenReductionPercent, 0), 100);

  return (
    <div className="flex h-full flex-col rounded-card border border-slate-200 bg-white p-5">
      <div className="flex items-center gap-2.5">
        <IconBox icon={Zap} />
        <h3 className="text-base font-semibold text-slate-900">
          Optimization Summary
        </h3>
      </div>

      {/* Before vs After token comparison */}
      <div className="mt-4 grid grid-cols-[1fr_auto_1fr] items-center gap-3">
        <div className="rounded-inner bg-slate-50 px-3 py-3 text-center">
          <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
            Before
          </p>
          <p className="mt-1 text-2xl font-bold tabular-nums text-slate-900">
            {originalTokens}
          </p>
          <p className="text-xs text-slate-500">tokens</p>
        </div>

        <ArrowRight
          className="h-4 w-4 text-emerald-500"
          strokeWidth={1.75}
          aria-hidden
        />

        <div className="rounded-inner border border-emerald-100 bg-emerald-50 px-3 py-3 text-center">
          <p className="text-[11px] font-medium uppercase tracking-wide text-emerald-700">
            After
          </p>
          <p className="mt-1 text-2xl font-bold tabular-nums text-emerald-800">
            {optimizedTokens}
          </p>
          <p className="text-xs text-emerald-700/80">tokens</p>
        </div>
      </div>

      {/* Visual reduction bar */}
      <div className="mt-4">
        <div className="flex items-center justify-between text-xs text-slate-500">
          <span>Token savings</span>
          <span className="font-medium tabular-nums text-emerald-700">
            −{tokenDelta} tokens
          </span>
        </div>
        <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-100">
          <div
            className={cn(
              "h-full rounded-full bg-emerald-500 transition-all duration-700 ease-out"
            )}
            style={{ width: `${tokenBarWidth}%` }}
          />
        </div>
      </div>

      {/* Improvement indicators */}
      <div className="mt-4 grid grid-cols-2 gap-2.5">
        <div className="rounded-inner bg-slate-50 px-3 py-3">
          <div className="flex items-center gap-1.5 text-slate-500">
            <ArrowDownRight className="h-3.5 w-3.5" strokeWidth={1.75} />
            <p className="text-[11px] font-medium uppercase tracking-wide">
              Token Reduction
            </p>
          </div>
          <p className="mt-1 text-xl font-bold tabular-nums text-emerald-700">
            {formatPercent(tokenReductionPercent)}
          </p>
        </div>
        <div className="rounded-inner border border-emerald-100 bg-emerald-50 px-3 py-3">
          <div className="flex items-center gap-1.5 text-emerald-700">
            <Leaf className="h-3.5 w-3.5" strokeWidth={1.75} />
            <p className="text-[11px] font-medium uppercase tracking-wide">
              Carbon Reduction
            </p>
          </div>
          <p className="mt-1 text-xl font-bold tabular-nums text-emerald-800">
            {formatPercent(carbonReductionPercent)}
          </p>
        </div>
      </div>
    </div>
  );
}
