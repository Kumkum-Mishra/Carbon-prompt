"use client";

import { motion } from "framer-motion";
import { Award, BarChart3, Leaf, Sparkles, Zap } from "lucide-react";
import { fadeInUp, staggerContainer } from "@/design/motion";

const previewCards = [
  {
    icon: BarChart3,
    title: "Prompt Analysis",
    description: "Task type, prompt style, and token breakdown.",
  },
  {
    icon: Leaf,
    title: "Carbon Impact",
    description: "Before/after Green Carbon Score comparison.",
  },
  {
    icon: Zap,
    title: "Optimization",
    description: "A shorter, clearer rewrite of your prompt.",
  },
  {
    icon: Award,
    title: "Model Recommendation",
    description: "The best-fit model with reasons and alternatives.",
  },
];

export default function AnalyzeEmptyState() {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={staggerContainer(0.08)}
      className="rounded-[24px] border border-dashed border-slate-200 bg-slate-50/60 p-6 text-center sm:p-10"
    >
      <motion.div
        variants={fadeInUp}
        className="mx-auto inline-flex h-11 w-11 items-center justify-center rounded-full bg-emerald-50 text-emerald-600"
      >
        <Sparkles className="h-5 w-5" strokeWidth={1.75} />
      </motion.div>
      <motion.h2
        variants={fadeInUp}
        className="mt-4 text-lg font-semibold text-slate-900"
      >
        See your full prompt analysis here
      </motion.h2>
      <motion.p
        variants={fadeInUp}
        className="mx-auto mt-2 max-w-md text-sm leading-[1.65] text-slate-600"
      >
        Enter a prompt above and click Analyze to see its token cost, carbon
        score, optimized rewrite, and recommended model.
      </motion.p>

      <motion.div
        variants={fadeInUp}
        className="mt-8 grid gap-3 text-left sm:grid-cols-2 lg:grid-cols-4"
      >
        {previewCards.map((card) => (
          <div
            key={card.title}
            className="rounded-[16px] border border-slate-200 bg-white p-4"
          >
            <card.icon
              className="h-4 w-4 text-slate-400"
              strokeWidth={1.75}
            />
            <p className="mt-2 text-sm font-semibold text-slate-800">
              {card.title}
            </p>
            <p className="mt-1 text-xs leading-[1.5] text-slate-500">
              {card.description}
            </p>
          </div>
        ))}
      </motion.div>
    </motion.div>
  );
}
