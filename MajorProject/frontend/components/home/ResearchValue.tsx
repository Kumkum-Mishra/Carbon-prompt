"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { fadeInUp } from "@/design/motion";
import { researchInsights } from "@/data/home";
import RevealSection from "./RevealSection";
import SectionHeading from "./SectionHeading";

export default function ResearchValue() {
  return (
    <RevealSection className="bg-white px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <SectionHeading
          eyebrow="Research & Transparency"
          title="Built for scrutiny, not just demos"
          description="GreenPrompt AI is a research project first. Every score and recommendation is explained, not hidden."
        />

        <div className="mt-12 grid gap-6 sm:grid-cols-3">
          {researchInsights.map((item) => (
            <motion.div
              key={item.title}
              variants={fadeInUp}
              className="rounded-[16px] border border-slate-200 bg-slate-50 p-6"
            >
              <div className="inline-flex h-10 w-10 items-center justify-center rounded-[10px] bg-violet-50 text-violet-600">
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

        <motion.div variants={fadeInUp} className="mt-10 flex justify-center gap-6">
          <Link
            href="/mathematics"
            className="group inline-flex items-center gap-1.5 rounded-sm text-sm font-semibold text-emerald-700 transition-colors duration-150 hover:text-emerald-800 focus-ring"
          >
            Read the formulas
            <ArrowRight className="h-4 w-4 transition-transform duration-150 group-hover:translate-x-0.5" />
          </Link>
          <Link
            href="/datasets"
            className="group inline-flex items-center gap-1.5 rounded-sm text-sm font-semibold text-emerald-700 transition-colors duration-150 hover:text-emerald-800 focus-ring"
          >
            Explore the datasets
            <ArrowRight className="h-4 w-4 transition-transform duration-150 group-hover:translate-x-0.5" />
          </Link>
        </motion.div>
      </div>
    </RevealSection>
  );
}
