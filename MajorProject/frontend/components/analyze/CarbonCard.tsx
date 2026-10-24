"use client";

import {
  Bar,
  BarChart,
  Cell,
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  XAxis,
} from "recharts";
import { Leaf } from "lucide-react";
import IconBox from "@/components/ui/IconBox";
import Tooltip from "@/components/ui/Tooltip";
import { formatCarbonScore, formatPercent } from "@/utils/formatters";

export interface CarbonCardProps {
  originalScore: number;
  optimizedScore: number;
  reductionPercent: number;
}

export default function CarbonCard({
  originalScore,
  optimizedScore,
  reductionPercent,
}: CarbonCardProps) {
  const chartData = [
    { name: "Before", score: originalScore },
    { name: "After", score: optimizedScore },
  ];

  return (
    <div className="flex h-full min-w-0 flex-col rounded-card border border-slate-200 bg-white p-5">
      <div className="flex items-center gap-2.5">
        <IconBox icon={Leaf} />
        <h3 className="text-base font-semibold text-slate-900">Carbon Impact</h3>
        <Tooltip label="GCS is a relative sustainability score, not a measured CO2 value." />
      </div>

      <div className="mt-4 flex flex-1 flex-col gap-3">
        <div className="grid grid-cols-2 gap-2">
          <div className="rounded-inner bg-slate-50 px-3 py-2.5">
            <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
              Original GCS
            </p>
            <p className="mt-0.5 text-base font-bold tabular-nums text-slate-900 sm:text-lg">
              {formatCarbonScore(originalScore)}
            </p>
          </div>
          <div className="rounded-inner bg-emerald-50 px-3 py-2.5">
            <p className="text-[11px] font-medium uppercase tracking-wide text-emerald-700">
              Optimized GCS
            </p>
            <p className="mt-0.5 text-base font-bold tabular-nums text-emerald-800 sm:text-lg">
              {formatCarbonScore(optimizedScore)}
            </p>
          </div>
        </div>

        <div className="min-h-[88px] flex-1 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{ top: 4, right: 4, left: 4, bottom: 0 }}
            >
              <XAxis
                dataKey="name"
                tickLine={false}
                axisLine={false}
                tick={{ fontSize: 11, fill: "#64748b" }}
              />
              <RechartsTooltip
                formatter={(value: number) => [formatCarbonScore(value), "GCS"]}
                contentStyle={{ fontSize: 12, borderRadius: 8 }}
                cursor={{ fill: "rgba(16,185,129,0.06)" }}
              />
              <Bar
                dataKey="score"
                radius={[6, 6, 0, 0]}
                isAnimationActive
                animationDuration={700}
              >
                <Cell fill="#94a3b8" />
                <Cell fill="#10b981" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-auto rounded-inner border border-emerald-100 bg-emerald-50 px-3 py-2.5 text-center">
          <p className="text-xs text-emerald-700">Carbon Reduction</p>
          <p className="text-lg font-bold tabular-nums text-emerald-800 sm:text-xl">
            {formatPercent(reductionPercent)}
          </p>
        </div>
      </div>
    </div>
  );
}
