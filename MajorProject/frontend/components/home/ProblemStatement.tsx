"use client";

import { motion } from "framer-motion";
import { fadeInUp } from "@/design/motion";
import { problemInsights } from "@/data/home";
import RevealSection from "./RevealSection";
import SectionHeading from "./SectionHeading";

export default function ProblemStatement() {
  return (
    <RevealSection className="bg-slate-50 px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <SectionHeading
          eyebrow="The Problem"
          title="Prompts have a computational cost"
          description="Unoptimized prompts quietly waste tokens and compute. GreenPrompt AI makes that cost visible before it adds up."
        />

        <div className="mt-12 grid gap-6 sm:grid-cols-3">
          {problemInsights.map((item) => (
            <motion.div
              key={item.title}
              variants={fadeInUp}
              className="rounded-[16px] border border-slate-200 bg-white p-6"
            >
              <div className="inline-flex h-10 w-10 items-center justify-center rounded-[10px] bg-emerald-50 text-emerald-600">
                <item.icon className="h-5 w-5" strokeWidth={1.75} />
              </div>
              <h3 className="mt-4 text-lg font-semibold leading-[1.35] text-slate-900">
                {item.title}
              </h3>
              <p className="mt-2 text-sm leading-[1.65] text-slate-600">
                {item.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </RevealSection>
  );
}
