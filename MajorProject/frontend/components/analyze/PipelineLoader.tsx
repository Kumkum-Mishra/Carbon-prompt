"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";
import { fadeInUp, staggerContainer } from "@/design/motion";
import { pipelineSteps } from "@/data/analyze";
import Skeleton from "@/components/ui/Skeleton";
import { cn } from "@/utils/cn";

interface PipelineLoaderProps {
  step: number;
}

export default function PipelineLoader({ step }: PipelineLoaderProps) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={staggerContainer(0.08)}
      role="status"
      aria-live="polite"
      className="space-y-8"
    >
      <motion.div
        variants={fadeInUp}
        className="rounded-[24px] border border-slate-200 bg-white p-6 sm:p-8"
      >
        <div className="grid grid-cols-2 gap-4 sm:flex sm:items-center sm:justify-between">
          {pipelineSteps.map((meta, index) => {
            const state =
              index < step ? "done" : index === step ? "active" : "pending";
            return (
              <div key={meta.label} className="flex items-center gap-3">
                <span
                  className={cn(
                    "flex h-9 w-9 shrink-0 items-center justify-center rounded-full border text-sm font-semibold transition-colors duration-200",
                    state === "done" &&
                      "border-emerald-600 bg-emerald-600 text-white",
                    state === "active" &&
                      "border-emerald-500 bg-emerald-50 text-emerald-600",
                    state === "pending" &&
                      "border-slate-200 bg-slate-50 text-slate-400"
                  )}
                >
                  {state === "done" ? (
                    <Check className="h-4 w-4" />
                  ) : (
                    <meta.icon
                      className={cn(
                        "h-4 w-4",
                        state === "active" && "animate-pulse"
                      )}
                      strokeWidth={1.75}
                    />
                  )}
                </span>
                <span
                  className={cn(
                    "text-sm font-medium",
                    state === "pending" ? "text-slate-400" : "text-slate-800"
                  )}
                >
                  {meta.label.replace(/\.\.\.$/, "")}
                </span>
              </div>
            );
          })}
        </div>

        <div className="mt-5 h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${((step + 1) / pipelineSteps.length) * 100}%` }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
            className="h-full rounded-full bg-emerald-500"
          />
        </div>
      </motion.div>

      <motion.div
        variants={fadeInUp}
        className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
        aria-hidden
      >
        {Array.from({ length: 4 }).map((_, index) => (
          <div
            key={index}
            className="rounded-[16px] border border-slate-200 bg-white p-5"
          >
            <Skeleton className="h-4 w-24" />
            <Skeleton className="mt-3 h-7 w-16" />
            <Skeleton className="mt-3 h-3 w-full" />
          </div>
        ))}
      </motion.div>

      <motion.div variants={fadeInUp} className="grid gap-6 lg:grid-cols-2">
        {Array.from({ length: 4 }).map((_, index) => (
          <div
            key={index}
            className="rounded-[16px] border border-slate-200 bg-white p-6"
          >
            <Skeleton className="h-5 w-40" />
            <div className="mt-5 space-y-3">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-5/6" />
              <Skeleton className="h-4 w-2/3" />
            </div>
          </div>
        ))}
      </motion.div>
    </motion.div>
  );
}
