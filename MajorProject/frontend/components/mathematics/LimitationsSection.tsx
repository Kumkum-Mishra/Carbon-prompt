"use client";

import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";
import { fadeInUp, staggerContainer, viewportOnce } from "@/design/motion";
import { limitations } from "@/data/mathematics";
import InfoBadge from "./InfoBadge";

export default function LimitationsSection() {
  return (
    <motion.section
      id="limitations"
      initial="hidden"
      whileInView="visible"
      viewport={viewportOnce}
      variants={staggerContainer(0.08)}
      className="scroll-mt-24 rounded-[16px] border border-amber-200 bg-amber-50/40 p-6 sm:p-8"
    >
      <motion.div variants={fadeInUp}>
        <InfoBadge variant="amber">Good to Know</InfoBadge>
        <h2 className="mt-3 text-2xl font-bold leading-[1.2] text-slate-900 sm:text-3xl">
          Limitations &amp; assumptions
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-[1.65] text-slate-600">
          These metrics are designed for comparison and guidance, not as
          absolute environmental measurements.
        </p>
      </motion.div>

      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        {limitations.map((item) => (
          <motion.div
            key={item.title}
            variants={fadeInUp}
            className="flex gap-3 rounded-[10px] border border-amber-200 bg-white p-4"
          >
            <AlertTriangle
              className="mt-0.5 h-4 w-4 shrink-0 text-amber-500"
              strokeWidth={1.75}
            />
            <div>
              <p className="text-sm font-semibold text-slate-900">
                {item.title}
              </p>
              <p className="mt-1 text-sm leading-[1.6] text-slate-600">
                {item.description}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.section>
  );
}
