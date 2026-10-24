"use client";

import { motion } from "framer-motion";
import { fadeInUp } from "@/design/motion";
import { technologies } from "@/data/home";
import RevealSection from "./RevealSection";
import SectionHeading from "./SectionHeading";

export default function TechStack() {
  return (
    <RevealSection className="bg-slate-50 px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <SectionHeading
          eyebrow="Technology"
          title="Built on a modern, research-grade stack"
        />

        <motion.div
          variants={fadeInUp}
          className="mt-10 flex flex-wrap justify-center gap-3"
        >
          {technologies.map((tech) => (
            <span
              key={tech}
              className="rounded-full border border-slate-200 bg-white px-4 py-1.5 text-sm font-medium text-slate-700 shadow-sm"
            >
              {tech}
            </span>
          ))}
        </motion.div>
      </div>
    </RevealSection>
  );
}
