"use client";

import type { LucideIcon } from "lucide-react";
import CountUp from "react-countup";
import { motion } from "framer-motion";
import IconBox from "@/components/ui/IconBox";
import { fadeInUp } from "@/design/motion";
import { cn } from "@/utils/cn";

interface KPICardProps {
  icon: LucideIcon;
  label: string;
  value: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  description?: string;
}

export default function KPICard({
  icon,
  label,
  value,
  decimals = 0,
  prefix = "",
  suffix = "",
  description,
}: KPICardProps) {
  return (
    <motion.div
      variants={fadeInUp}
      className={cn(
        "rounded-card border border-slate-200 bg-white p-5 card-hover"
      )}
    >
      <div className="flex items-center gap-2.5">
        <IconBox icon={icon} />
        <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
          {label}
        </p>
      </div>
      <p className="mt-3 text-3xl font-bold tabular-nums text-slate-900">
        <CountUp
          end={value}
          decimals={decimals}
          duration={1.2}
          prefix={prefix}
          suffix={suffix}
          separator=","
        />
      </p>
      {description && (
        <p className="mt-1 text-xs leading-relaxed text-slate-500">
          {description}
        </p>
      )}
    </motion.div>
  );
}
