import type { ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "@/utils/cn";

export type ButtonVariant = "primary" | "secondary" | "ghost" | "danger" | "outline";
export type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  children: ReactNode;
  isLoading?: boolean;
}

const VARIANT_CLASSES: Record<ButtonVariant, string> = {
  primary:
    "bg-emerald-600 text-white shadow-[0_0_0_1px_rgba(16,185,129,0.35)] hover:-translate-y-0.5 hover:bg-emerald-500 active:translate-y-0",
  secondary:
    "border border-slate-200 bg-white text-slate-700 hover:-translate-y-0.5 hover:border-slate-300 hover:bg-slate-50 active:translate-y-0",
  outline:
    "border border-white/15 bg-white/5 text-slate-200 backdrop-blur hover:-translate-y-0.5 hover:border-white/25 hover:bg-white/10 active:translate-y-0",
  ghost:
    "text-emerald-700 hover:bg-emerald-50 hover:text-emerald-800",
  danger:
    "bg-red-600 text-white hover:-translate-y-0.5 hover:bg-red-500 active:translate-y-0",
};

const SIZE_CLASSES: Record<ButtonSize, string> = {
  sm: "min-h-[36px] rounded-inner px-3 py-1.5 text-xs font-semibold",
  md: "min-h-[44px] rounded-inner px-5 py-2.5 text-sm font-semibold",
  lg: "min-h-[48px] rounded-inner px-6 py-3 text-sm font-semibold",
};

export default function Button({
  variant = "primary",
  size = "md",
  children,
  className,
  disabled,
  isLoading,
  type = "button",
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      disabled={disabled || isLoading}
      className={cn(
        "inline-flex items-center justify-center gap-2 transition-all duration-150 ease-out",
        "focus-ring disabled:pointer-events-none disabled:opacity-50",
        VARIANT_CLASSES[variant],
        SIZE_CLASSES[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
