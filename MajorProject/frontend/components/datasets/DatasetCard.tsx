"use client";

import type { ReactNode } from "react";
import type { LucideIcon } from "lucide-react";
import { motion } from "framer-motion";
import IconBox from "@/components/ui/IconBox";
import { fadeInUp } from "@/design/motion";
import { cn } from "@/utils/cn";

interface DatasetCardProps {
  title: string;
  description: string;
  icon?: LucideIcon;
  children: ReactNode;
  className?: string;
  span?: "default" | "wide";
}

export default function DatasetCard({
  title,
  description,
  icon,
  children,
  className,
  span = "default",
}: DatasetCardProps) {
  return (
    <motion.div
      variants={fadeInUp}
      className={cn(
        "rounded-card border border-slate-200 bg-white p-6",
        span === "wide" && "lg:col-span-2",
        className
      )}
    >
      <div className="flex items-start gap-3">
        {icon && <IconBox icon={icon} />}
        <div>
          <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
          <p className="mt-0.5 text-sm text-slate-600">{description}</p>
        </div>
      </div>
      <div className="mt-5">{children}</div>
    </motion.div>
  );
}
