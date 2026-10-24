"use client";

import { motion } from "framer-motion";
import { fadeInUp } from "@/design/motion";
import Badge from "@/components/ui/Badge";
import type { BadgeVariant } from "@/components/ui/Badge";

interface DatasetSectionHeaderProps {
  badge: string;
  badgeVariant?: BadgeVariant;
  title: string;
  description: string;
}

export default function DatasetSectionHeader({
  badge,
  badgeVariant = "green",
  title,
  description,
}: DatasetSectionHeaderProps) {
  return (
    <motion.div variants={fadeInUp} className="max-w-2xl">
      <Badge variant={badgeVariant}>{badge}</Badge>
      <h2 className="mt-3 text-2xl font-bold leading-[1.2] text-slate-900 sm:text-3xl">
        {title}
      </h2>
      <p className="mt-2 text-sm leading-[1.65] text-slate-600">
        {description}
      </p>
    </motion.div>
  );
}
