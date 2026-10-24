"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Leaf, Sparkles } from "lucide-react";
import { fadeInUp, staggerContainer } from "@/design/motion";
import { APP_NAME } from "@/utils/constants";

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-slate-950">
      {/* Ambient background: dark base + soft green radial glow + faint grid */}
      <div
        aria-hidden
        className="absolute inset-0"
        style={{
          backgroundImage:
            "linear-gradient(to right, rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.05) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
          maskImage:
            "radial-gradient(ellipse 80% 60% at 50% 0%, black 40%, transparent 100%)",
        }}
      />
      <div
        aria-hidden
        className="absolute left-1/2 top-[-10%] h-[560px] w-[560px] -translate-x-1/2 rounded-full bg-emerald-500/20 blur-[120px]"
      />

      <div className="relative mx-auto grid max-w-6xl gap-16 px-4 py-24 sm:px-6 lg:grid-cols-2 lg:items-center lg:gap-12 lg:py-32 xl:px-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={staggerContainer(0.12)}
          className="text-center lg:text-left"
        >
          <motion.div
            variants={fadeInUp}
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm font-medium text-emerald-300 backdrop-blur"
          >
            <Leaf className="h-3.5 w-3.5" strokeWidth={2} />
            Sustainable Prompt Engineering
          </motion.div>

          <motion.h1
            variants={fadeInUp}
            className="mt-6 text-[2.75rem] font-bold leading-[1.05] tracking-tight text-white sm:text-6xl lg:text-[4.25rem]"
          >
            Write prompts that think fast,{" "}
            <span className="text-emerald-400">cost less</span>, and run
            greener.
          </motion.h1>

          <motion.p
            variants={fadeInUp}
            className="mx-auto mt-6 max-w-[640px] text-lg leading-[1.7] text-slate-300 lg:mx-0"
          >
            {APP_NAME} analyzes your prompt, estimates its computational
            impact, rewrites it for efficiency, and recommends the best model
            for the job &mdash; all in one pipeline.
          </motion.p>

          <motion.div
            variants={fadeInUp}
            className="mt-10 flex flex-wrap items-center justify-center gap-4 lg:justify-start"
          >
            <Link
              href="/analyze"
              className="group inline-flex min-h-[48px] items-center gap-2 rounded-[10px] bg-emerald-600 px-6 py-3 text-sm font-semibold text-white shadow-[0_0_0_1px_rgba(16,185,129,0.4)] transition-all duration-150 hover:-translate-y-0.5 hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-400 active:translate-y-0"
            >
              <Sparkles className="h-4 w-4" strokeWidth={2} />
              Analyze a Prompt
              <ArrowRight className="h-4 w-4 transition-transform duration-150 group-hover:translate-x-0.5" />
            </Link>
            <Link
              href="/mathematics"
              className="inline-flex min-h-[48px] items-center rounded-[10px] border border-white/15 bg-white/5 px-6 py-3 text-sm font-semibold text-slate-200 backdrop-blur transition-all duration-150 hover:-translate-y-0.5 hover:border-white/25 hover:bg-white/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-400 active:translate-y-0"
            >
              View Methodology
            </Link>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24, scale: 0.97 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.55, delay: 0.25, ease: [0.16, 1, 0.3, 1] }}
        >
          <HeroVisualPanel />
        </motion.div>
      </div>
    </section>
  );
}

function HeroVisualPanel() {
  return (
    <div className="relative mx-auto max-w-md rounded-[24px] border border-white/10 bg-white/[0.04] p-6 shadow-2xl backdrop-blur-xl">
      <div
        aria-hidden
        className="absolute -right-6 -top-6 h-16 w-16 rounded-full bg-emerald-400/30 blur-2xl"
      />

      <div className="flex items-center justify-between">
        <span className="inline-flex items-center gap-1.5 text-xs font-medium uppercase tracking-wide text-slate-400">
          <Sparkles className="h-3.5 w-3.5 text-emerald-400" />
          Live Optimization Preview
        </span>
      </div>

      <div className="mt-5 rounded-[16px] border border-white/10 bg-slate-900/60 p-4">
        <div className="flex items-center justify-between">
          <p className="text-xs font-medium text-slate-400">
            Original Prompt
          </p>
          <span className="rounded-full bg-amber-500/15 px-2 py-0.5 text-[11px] font-semibold text-amber-400">
            42 tokens
          </span>
        </div>
        <p className="mt-2 text-sm leading-relaxed text-slate-300">
          &ldquo;Can you please explain in great detail, with many examples,
          how neural networks work and also discuss all their
          applications?&rdquo;
        </p>
      </div>

      <div className="my-3 flex items-center justify-center gap-2">
        <motion.div
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
          className="h-1.5 w-1.5 rounded-full bg-emerald-400"
        />
        <span className="text-xs font-medium text-emerald-400">
          Optimizing prompt&hellip;
        </span>
      </div>

      <div className="rounded-[16px] border border-emerald-500/30 bg-emerald-500/[0.08] p-4">
        <div className="flex items-center justify-between">
          <p className="text-xs font-medium text-emerald-300">
            Optimized Prompt
          </p>
          <span className="rounded-full bg-emerald-500/20 px-2 py-0.5 text-[11px] font-semibold text-emerald-300">
            24 tokens
          </span>
        </div>
        <p className="mt-2 text-sm leading-relaxed text-white">
          &ldquo;Explain how neural networks work, with examples and
          applications.&rdquo;
        </p>
      </div>

      <div className="mt-5">
        <div className="flex items-center justify-between text-xs font-medium text-slate-400">
          <span>Green Carbon Score</span>
          <span className="text-emerald-400">-42.8%</span>
        </div>
        <div className="mt-2 space-y-1.5">
          <GcsBar label="Before" widthPercent={100} color="bg-slate-500" />
          <GcsBar
            label="After"
            widthPercent={57}
            color="bg-emerald-500"
            delay={0.2}
          />
        </div>
      </div>
    </div>
  );
}

function GcsBar({
  label,
  widthPercent,
  color,
  delay = 0,
}: {
  label: string;
  widthPercent: number;
  color: string;
  delay?: number;
}) {
  return (
    <div className="flex items-center gap-2">
      <span className="w-12 shrink-0 text-[11px] text-slate-500">
        {label}
      </span>
      <div className="h-2 flex-1 overflow-hidden rounded-full bg-white/5">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${widthPercent}%` }}
          transition={{ duration: 0.8, delay: 0.6 + delay, ease: [0.16, 1, 0.3, 1] }}
          className={`h-full rounded-full ${color}`}
        />
      </div>
    </div>
  );
}
