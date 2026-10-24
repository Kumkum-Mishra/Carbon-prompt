"use client";

import {
  Bar,
  BarChart,
  Cell,
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Award, CheckCircle2 } from "lucide-react";
import Badge from "@/components/ui/Badge";
import IconBox from "@/components/ui/IconBox";
import Tooltip from "@/components/ui/Tooltip";
import { formatNumber } from "@/utils/formatters";

export interface RecommendationCardProps {
  recommendedModel: string;
  score: number;
  scoreType?: string;
  reasons: string[];
  topModels: Array<{ model: string; score: number }>;
  category: string;
  weights?: {
    speed: number;
    latency: number;
    context: number;
    cost_efficiency: number;
  };
}

function longestLabelLength(labels: string[]): number {
  return labels.reduce((max, label) => Math.max(max, label.length), 0);
}

export default function RecommendationCard({
  recommendedModel,
  score,
  scoreType = "GMES",
  reasons,
  topModels,
  category,
  weights,
}: RecommendationCardProps) {
  const chartData = topModels.slice(0, 4).map((model) => ({
    name: model.model,
    score: model.score,
  }));

  const yAxisWidth = Math.min(
    Math.max(longestLabelLength(chartData.map((d) => d.name)) * 7, 72),
    160
  );

  return (
    <div className="flex h-full min-w-0 flex-col rounded-card border border-slate-200 bg-white p-5">
      <div className="flex items-center gap-2.5">
        <IconBox icon={Award} />
        <h3 className="text-base font-semibold text-slate-900">
          Model Recommendation
        </h3>
        <Tooltip label={`${scoreType} combines speed, latency, context, and cost efficiency using prompt-specific weights when available.`} />
      </div>

      <div className="mt-4 flex flex-1 flex-col gap-3">
        <div className="rounded-inner bg-emerald-50 px-3 py-3">
          <p className="text-[11px] font-medium uppercase tracking-wide text-emerald-700">
            Recommended Model
          </p>
          <p className="mt-1 break-words text-base font-bold leading-snug text-slate-900 sm:text-lg">
            {recommendedModel}
          </p>
          <div className="mt-2 flex flex-wrap items-center gap-2 text-sm text-slate-600">
            <span>
              {scoreType}:{" "}
              <span className="font-semibold text-emerald-700">
                {formatNumber(score)}
              </span>
            </span>
            <Badge variant="slate">{category}</Badge>
          </div>
        </div>

        {weights && (
          <p className="text-xs text-slate-500">
            Weights — speed {formatNumber(weights.speed, 2)}, latency{" "}
            {formatNumber(weights.latency, 2)}, context{" "}
            {formatNumber(weights.context, 2)}, cost{" "}
            {formatNumber(weights.cost_efficiency, 2)}
          </p>
        )}

        {reasons.length > 0 && (
          <div>
            <p className="text-[11px] font-medium uppercase tracking-wide text-slate-500">
              Why this model?
            </p>
            <ul className="mt-1.5 space-y-1">
              {reasons.slice(0, 2).map((reason) => (
                <li
                  key={reason}
                  className="flex items-start gap-2 text-sm leading-snug text-slate-700"
                >
                  <CheckCircle2
                    className="mt-0.5 h-3.5 w-3.5 shrink-0 text-emerald-600"
                    strokeWidth={1.75}
                  />
                  <span className="break-words">{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {chartData.length > 1 && (
          <div className="mt-auto min-h-[72px] w-full flex-1">
            <p className="mb-1.5 text-[11px] font-medium uppercase tracking-wide text-slate-500">
              Top Scores
            </p>
            <ResponsiveContainer width="100%" height={chartData.length * 26 + 8}>
              <BarChart
                data={chartData}
                layout="vertical"
                margin={{ top: 0, right: 8, left: 0, bottom: 0 }}
              >
                <XAxis type="number" hide />
                <YAxis
                  dataKey="name"
                  type="category"
                  width={yAxisWidth}
                  tickLine={false}
                  axisLine={false}
                  tick={{ fontSize: 11, fill: "#334155" }}
                  interval={0}
                />
                <RechartsTooltip
                  formatter={(value: number) => [formatNumber(value), scoreType]}
                  contentStyle={{ fontSize: 12, borderRadius: 8 }}
                  cursor={{ fill: "rgba(16,185,129,0.06)" }}
                />
                <Bar
                  dataKey="score"
                  radius={[0, 4, 4, 0]}
                  isAnimationActive
                  animationDuration={700}
                  barSize={10}
                >
                  {chartData.map((entry) => (
                    <Cell
                      key={entry.name}
                      fill={
                        entry.name === recommendedModel ? "#10b981" : "#cbd5e1"
                      }
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {topModels.length > 1 && (
          <ul className="mt-2 space-y-1 border-t border-slate-100 pt-2">
            {topModels
              .filter((m) => m.model !== recommendedModel)
              .slice(0, 2)
              .map((model) => (
                <li
                  key={model.model}
                  className="flex items-center justify-between gap-2 text-xs"
                >
                  <span className="min-w-0 break-words text-slate-600">
                    {model.model}
                  </span>
                  <span className="shrink-0 tabular-nums text-slate-400">
                    {formatNumber(model.score)}
                  </span>
                </li>
              ))}
          </ul>
        )}
      </div>
    </div>
  );
}
