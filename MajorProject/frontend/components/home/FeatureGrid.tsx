"use client";

import { motion } from "framer-motion";
import { fadeInUp } from "@/design/motion";
import { featureItems } from "@/data/home";
import RevealSection from "./RevealSection";
import SectionHeading from "./SectionHeading";

export default function FeatureGrid() {
  return (
    <RevealSection className="bg-slate-50 px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <SectionHeading
          eyebrow="What It Does"
          title="Four modules, one unified pipeline"
          description="Each module is independently useful, and together they form the complete GreenPrompt AI experience."
        />

        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {featureItems.map((feature) => (
            <motion.div
              key={feature.title}
              variants={fadeInUp}
              className="group rounded-card border border-slate-200 bg-white p-6 transition-all duration-200 ease-out hover:-translate-y-0.5 hover:border-emerald-300 hover:shadow-card-hover"
            >
              <div className="inline-flex h-9 w-9 items-center justify-center rounded-inner bg-emerald-50 text-emerald-600 transition-colors duration-150 group-hover:bg-emerald-100">
                <feature.icon className="h-5 w-5" strokeWidth={1.75} />
              </div>
              <h3 className="mt-4 text-base font-semibold leading-[1.35] text-slate-900">
                {feature.title}
              </h3>
              <p className="mt-2 text-sm leading-[1.65] text-slate-600">
                {feature.description}
              </p>
              <span className="mt-4 inline-flex items-center rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600">
                {feature.metric}
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </RevealSection>
  );
}
