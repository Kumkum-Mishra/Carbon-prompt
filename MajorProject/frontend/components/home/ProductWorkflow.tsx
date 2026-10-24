"use client";

import { motion } from "framer-motion";
import { ArrowDown, ArrowRight } from "lucide-react";
import { fadeInUp } from "@/design/motion";
import { workflowSteps } from "@/data/home";
import RevealSection from "./RevealSection";
import SectionHeading from "./SectionHeading";

export default function ProductWorkflow() {
  return (
    <RevealSection className="bg-white px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <SectionHeading
          eyebrow="How It Works"
          title="One pipeline, four steps"
          description="Every prompt flows through the same transparent pipeline, from raw input to a model recommendation."
        />

        <div className="mt-14 flex flex-col items-stretch gap-4 sm:hidden">
          {workflowSteps.map((step, index) => (
            <motion.div key={step.title} variants={fadeInUp}>
              <WorkflowCard step={step} index={index} />
              {index < workflowSteps.length - 1 && (
                <div className="flex justify-center py-2">
                  <ArrowDown className="h-4 w-4 text-slate-300" />
                </div>
              )}
            </motion.div>
          ))}
        </div>

        <div className="mt-14 hidden items-center gap-3 sm:flex">
          {workflowSteps.map((step, index) => (
            <div key={step.title} className="flex flex-1 items-center gap-3">
              <motion.div variants={fadeInUp} className="flex-1">
                <WorkflowCard step={step} index={index} />
              </motion.div>
              {index < workflowSteps.length - 1 && (
                <ArrowRight className="hidden h-4 w-4 shrink-0 text-slate-300 lg:block" />
              )}
            </div>
          ))}
        </div>
      </div>
    </RevealSection>
  );
}

function WorkflowCard({
  step,
  index,
}: {
  step: (typeof workflowSteps)[number];
  index: number;
}) {
  return (
    <div className="h-full rounded-[16px] border border-slate-200 bg-slate-50 p-5 transition-colors duration-150 hover:border-emerald-300">
      <div className="flex items-center gap-3">
        <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-xs font-semibold text-white">
          {index + 1}
        </span>
        <step.icon className="h-5 w-5 text-emerald-600" strokeWidth={1.75} />
      </div>
      <h3 className="mt-4 text-base font-semibold text-slate-900">
        {step.title}
      </h3>
      <p className="mt-1 text-sm leading-[1.6] text-slate-600">
        {step.description}
      </p>
    </div>
  );
}
