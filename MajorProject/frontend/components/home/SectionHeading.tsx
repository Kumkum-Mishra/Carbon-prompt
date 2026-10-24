"use client";

import { motion } from "framer-motion";
import { fadeInUp } from "@/design/motion";
import { cn } from "@/utils/cn";

interface SectionHeadingProps {
  eyebrow: string;
  title: string;
  description?: string;
  align?: "center" | "left";
  tone?: "light" | "dark";
}

export default function SectionHeading({
  eyebrow,
  title,
  description,
  align = "center",
  tone = "light",
}: SectionHeadingProps) {
  return (
    <motion.div
      variants={fadeInUp}
      className={cn(
        "mx-auto max-w-2xl",
        align === "center" ? "text-center" : "text-left lg:mx-0"
      )}
    >
      <span
        className={cn(
          "text-xs font-semibold uppercase tracking-wider",
          tone === "dark" ? "text-emerald-400" : "text-emerald-600"
        )}
      >
        {eyebrow}
      </span>
      <h2
        className={cn(
          "mt-3 text-3xl font-bold leading-[1.2] tracking-tight sm:text-4xl",
          tone === "dark" ? "text-white" : "text-slate-900"
        )}
      >
        {title}
      </h2>
      {description && (
        <p
          className={cn(
            "mt-4 text-base leading-[1.65]",
            tone === "dark" ? "text-slate-300" : "text-slate-600"
          )}
        >
          {description}
        </p>
      )}
    </motion.div>
  );
}
