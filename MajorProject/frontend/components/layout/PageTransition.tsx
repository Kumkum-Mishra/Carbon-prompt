"use client";

import type { ReactNode } from "react";
import { motion } from "framer-motion";
import { pageTransition } from "@/design/motion";

interface PageTransitionProps {
  children: ReactNode;
  className?: string;
}

/**
 * Architecture §11.4 page wrapper: opacity 0→1, y 8→0, ~300ms.
 * Respects MotionConfig reducedMotion from the root layout.
 */
export default function PageTransition({
  children,
  className,
}: PageTransitionProps) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={pageTransition}
      className={className}
    >
      {children}
    </motion.div>
  );
}
