"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { fadeInUp, staggerContainer, viewportOnce } from "@/design/motion";
import { formulas, workedExample } from "@/data/mathematics";
import InfoBadge from "./InfoBadge";

export default function WorkedExampleSection() {
  return (
    <motion.section
      id="worked-example"
      initial="hidden"
      whileInView="visible"
      viewport={viewportOnce}
      variants={staggerContainer(0.1)}
      className="scroll-mt-24 rounded-[16px] border border-slate-200 bg-white p-6 sm:p-8"
    >
      <motion.div variants={fadeInUp}>
        <InfoBadge variant="blue">Worked Example</InfoBadge>
        <h2 className="mt-3 text-2xl font-bold leading-[1.2] text-slate-900 sm:text-3xl">
          Following one prompt through the pipeline
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-[1.65] text-slate-600">
          The figures below are illustrative, but every step applies the exact
          formulas defined above.
        </p>
      </motion.div>

      <motion.div
        variants={fadeInUp}
        className="mt-5 grid gap-4 sm:grid-cols-[1fr_auto_1fr] sm:items-center"
      >
        <div className="rounded-[10px] bg-slate-50 p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
            Original Prompt
          </p>
          <p className="mt-1 text-sm leading-relaxed text-slate-800">
            &ldquo;{workedExample.prompt}&rdquo;
          </p>
        </div>
        <ArrowRight className="mx-auto hidden h-5 w-5 text-emerald-500 sm:block" />
        <div className="rounded-[10px] border border-emerald-100 bg-emerald-50 p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-emerald-700">
            Optimized Prompt
          </p>
          <p className="mt-1 text-sm leading-relaxed text-slate-800">
            &ldquo;{workedExample.optimizedPrompt}&rdquo;
          </p>
        </div>
      </motion.div>

      <div className="mt-6 space-y-3">
        {workedExample.steps.map((step) => {
          const relatedFormula = formulas.find((f) => f.id === step.formulaId);
          return (
            <motion.div
              key={step.label}
              variants={fadeInUp}
              className="flex flex-col gap-2 rounded-[10px] border border-slate-200 p-4 sm:flex-row sm:items-center sm:justify-between sm:gap-4"
            >
              <div>
                <p className="text-sm font-semibold text-slate-900">
                  {step.label}
                </p>
                <p className="mt-0.5 text-xs leading-[1.5] text-slate-500">
                  {step.detail}
                </p>
              </div>
              <div className="flex items-center gap-3 sm:shrink-0">
                <span className="whitespace-nowrap rounded-inner bg-slate-900 px-3 py-1.5 font-mono text-xs text-emerald-300">
                  {step.value}
                </span>
                {relatedFormula && (
                  <Link
                    href={`#${relatedFormula.id}`}
                    className="hidden whitespace-nowrap text-xs font-medium text-emerald-700 hover:text-emerald-800 sm:inline"
                  >
                    {relatedFormula.title.split(" (")[0]}
                  </Link>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>
    </motion.section>
  );
}
