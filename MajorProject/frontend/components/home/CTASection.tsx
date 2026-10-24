"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Rocket } from "lucide-react";
import { fadeInUp } from "@/design/motion";
import RevealSection from "./RevealSection";

export default function CTASection() {
  return (
    <RevealSection className="bg-slate-50 px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <motion.div
        variants={fadeInUp}
        className="relative mx-auto max-w-6xl overflow-hidden rounded-[32px] bg-slate-950 px-8 py-16 text-center sm:px-16"
      >
        <div
          aria-hidden
          className="absolute left-1/2 top-1/2 h-[380px] w-[380px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-emerald-500/20 blur-[110px]"
        />

        <div className="relative">
          <div className="inline-flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/15 text-emerald-400">
            <Rocket className="h-5 w-5" strokeWidth={1.75} />
          </div>
          <h2 className="mt-6 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Start analyzing prompts
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-base leading-[1.65] text-slate-300">
            Paste a prompt and see its token cost, carbon score, optimized
            rewrite, and recommended model in seconds.
          </p>
          <div className="mt-8 flex justify-center">
            <Link
              href="/analyze"
              className="group inline-flex min-h-[48px] items-center gap-2 rounded-[10px] bg-emerald-600 px-7 py-3 text-sm font-semibold text-white transition-all duration-150 hover:-translate-y-0.5 hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-400 active:translate-y-0"
            >
              Analyze a Prompt
              <ArrowRight className="h-4 w-4 transition-transform duration-150 group-hover:translate-x-0.5" />
            </Link>
          </div>
        </div>
      </motion.div>
    </RevealSection>
  );
}
