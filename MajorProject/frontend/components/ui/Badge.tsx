import type { ReactNode } from "react";
import { cn } from "@/utils/cn";

export type BadgeVariant = "green" | "blue" | "amber" | "slate" | "red" | "violet";

interface BadgeProps {
  variant?: BadgeVariant;
  children: ReactNode;
  className?: string;
}

const VARIANT_CLASSES: Record<BadgeVariant, string> = {
  green: "bg-emerald-50 text-emerald-700",
  blue: "bg-blue-50 text-blue-700",
  amber: "bg-amber-50 text-amber-700",
  slate: "bg-slate-100 text-slate-600",
  red: "bg-red-50 text-red-700",
  violet: "bg-violet-50 text-violet-700",
};

export default function Badge({
  variant = "slate",
  children,
  className,
}: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium",
        VARIANT_CLASSES[variant],
        className
      )}
    >
      {children}
    </span>
  );
}
