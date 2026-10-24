"use client";

import type { ReactNode } from "react";
import { motion } from "framer-motion";
import { staggerContainer, viewportOnce } from "@/design/motion";
import { cn } from "@/utils/cn";

interface RevealSectionProps {
  children: ReactNode;
  className?: string;
  stagger?: number;
}

/**
 * Scroll-reveal wrapper: fades and lifts children into view once,
 * staggering direct motion children. Keeps every Home section
 * consistent without repeating viewport/variant wiring.
 */
export default function RevealSection({
  children,
  className,
  stagger = 0.12,
}: RevealSectionProps) {
  return (
    <motion.section
      initial="hidden"
      whileInView="visible"
      viewport={viewportOnce}
      variants={staggerContainer(stagger)}
      className={cn(className)}
    >
      {children}
    </motion.section>
  );
}
