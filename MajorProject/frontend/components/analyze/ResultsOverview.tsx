"use client";

import { motion } from "framer-motion";
import CountUp from "react-countup";
import { ArrowDownRight, Award, Gauge, Hash } from "lucide-react";
import { fadeInUp } from "@/design/motion";

interface ResultsOverviewProps {
  originalTokens: number;
  optimizedTokens: number;
  tokenReductionPercent: number;
  carbonReductionPercent: number;
  recommendedModel: string;
}

export default function ResultsOverview({
  originalTokens,
  optimizedTokens,
  tokenReductionPercent,
  carbonReductionPercent,
  recommendedModel,
}: ResultsOverviewProps) {
  const metrics = [
    {
      icon: Hash,
      label: "Original Tokens",
      value: originalTokens,
      decimals: 0,
      suffix: "",
    },
    {
      icon: Hash,
      label: "Optimized Tokens",
      value: optimizedTokens,
      decimals: 0,
      suffix: "",
    },
    {
      icon: ArrowDownRight,
      label: "Token Reduction",
      value: tokenReductionPercent,
      decimals: 1,
      suffix: "%",
    },
    {
      icon: Gauge,
      label: "Carbon Reduction",
      value: carbonReductionPercent,
      decimals: 1,
      suffix: "%",
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
      {metrics.map((metric) => (
        <motion.div
          key={metric.label}
          variants={fadeInUp}
          className="rounded-card border border-slate-200 bg-white p-4"
        >
          <div className="flex items-center gap-1.5 text-slate-500">
            <metric.icon className="h-3.5 w-3.5" strokeWidth={1.75} />
            <p className="text-[11px] font-medium leading-tight">{metric.label}</p>
          </div>
          <p className="mt-1.5 text-xl font-bold tabular-nums text-slate-900 sm:text-2xl">
            <CountUp
              end={metric.value}
              decimals={metric.decimals}
              duration={1}
              suffix={metric.suffix}
            />
          </p>
        </motion.div>
      ))}

      <motion.div
        variants={fadeInUp}
        className="rounded-card border border-emerald-200 bg-emerald-50 p-4 col-span-2 sm:col-span-1"
      >
        <div className="flex items-center gap-1.5 text-emerald-700">
          <Award className="h-3.5 w-3.5" strokeWidth={1.75} />
          <p className="text-[11px] font-medium leading-tight">Recommended</p>
        </div>
        <p className="mt-1.5 truncate text-base font-bold text-emerald-900 sm:text-lg">
          {recommendedModel}
        </p>
      </motion.div>
    </div>
  );
}
