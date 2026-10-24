"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { fadeInUp } from "@/design/motion";
import { architectureNodes } from "@/data/home";
import RevealSection from "./RevealSection";
import SectionHeading from "./SectionHeading";

export default function ArchitecturePreview() {
  return (
    <RevealSection className="bg-white px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <SectionHeading
          eyebrow="Under the Hood"
          title="A modular pipeline behind one API call"
          description="Each stage is an independent module. The backend orchestrates them into a single request-response cycle."
        />

        <motion.div
          variants={fadeInUp}
          className="mt-12 overflow-x-auto rounded-[24px] border border-slate-200 bg-slate-50 p-6 sm:p-8"
        >
          <div className="flex min-w-max items-center justify-center gap-2 sm:gap-3">
            {architectureNodes.map((node, index) => (
              <div key={node.label} className="flex items-center gap-2 sm:gap-3">
                <div className="flex flex-col items-center gap-2 rounded-[16px] border border-slate-200 bg-white px-4 py-3 shadow-sm">
                  <node.icon
                    className="h-5 w-5 text-emerald-600"
                    strokeWidth={1.75}
                  />
                  <span className="whitespace-nowrap text-xs font-medium text-slate-700">
                    {node.label}
                  </span>
                </div>
                {index < architectureNodes.length - 1 && (
                  <ArrowRight className="h-4 w-4 shrink-0 text-slate-300" />
                )}
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </RevealSection>
  );
}
