"use client";

import { motion } from "framer-motion";
import CountUp from "react-countup";
import { fadeInUp } from "@/design/motion";
import { metricPreviewItems } from "@/data/home";
import RevealSection from "./RevealSection";
import SectionHeading from "./SectionHeading";

export default function MetricsPreview() {
  return (
    <RevealSection className="relative overflow-hidden bg-slate-950 px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div
        aria-hidden
        className="absolute left-1/2 top-1/2 h-[420px] w-[420px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-emerald-500/10 blur-[100px]"
      />

      <div className="relative mx-auto max-w-6xl">
        <SectionHeading
          eyebrow="Sustainability Impact"
          title="See the impact in numbers"
          description="Example results from optimizing prompts across the GreenPrompt AI benchmark dataset."
          tone="dark"
        />

        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {metricPreviewItems.map((metric) => (
            <motion.div
              key={metric.label}
              variants={fadeInUp}
              className="rounded-[16px] border border-white/10 bg-white/[0.04] p-6 backdrop-blur"
            >
              <p className="text-sm font-medium text-slate-400">
                {metric.label}
              </p>
              <p className="mt-2 text-3xl font-bold tabular-nums text-white sm:text-4xl">
                <CountUp
                  end={metric.value}
                  decimals={metric.decimals ?? 0}
                  duration={1.4}
                  suffix={metric.suffix}
                  enableScrollSpy
                  scrollSpyOnce
                />
              </p>
              <p className="mt-1 text-xs leading-[1.4] text-slate-500">
                {metric.helper}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </RevealSection>
  );
}