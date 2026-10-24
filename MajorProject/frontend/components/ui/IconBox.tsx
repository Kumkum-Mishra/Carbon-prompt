import type { LucideIcon } from "lucide-react";
import { cn } from "@/utils/cn";

interface IconBoxProps {
  icon: LucideIcon;
  className?: string;
  iconClassName?: string;
  size?: "sm" | "md" | "lg";
  tone?: "emerald" | "slate" | "amber" | "blue" | "red";
}

const BOX_SIZE = {
  sm: "h-8 w-8",
  md: "h-9 w-9",
  lg: "h-11 w-11",
} as const;

const ICON_SIZE = {
  sm: "h-4 w-4",
  md: "h-5 w-5",
  lg: "h-5 w-5",
} as const;

const TONE = {
  emerald: "bg-emerald-50 text-emerald-600",
  slate: "bg-slate-100 text-slate-600",
  amber: "bg-amber-50 text-amber-600",
  blue: "bg-blue-50 text-blue-600",
  red: "bg-red-50 text-red-600",
} as const;

export default function IconBox({
  icon: Icon,
  className,
  iconClassName,
  size = "md",
  tone = "emerald",
}: IconBoxProps) {
  return (
    <span
      className={cn(
        "inline-flex shrink-0 items-center justify-center rounded-inner",
        BOX_SIZE[size],
        TONE[tone],
        className
      )}
    >
      <Icon
        className={cn(ICON_SIZE[size], iconClassName)}
        strokeWidth={1.75}
      />
    </span>
  );
}
