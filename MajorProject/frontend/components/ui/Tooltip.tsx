"use client";

import { useId, useState } from "react";
import { Info } from "lucide-react";
import { cn } from "@/utils/cn";

interface TooltipProps {
  label: string;
  className?: string;
}

/**
 * Compact, keyboard-accessible tooltip for short clarifications
 * (e.g. "GCS is a relative sustainability score, not measured CO2.").
 */
export default function Tooltip({ label, className }: TooltipProps) {
  const [open, setOpen] = useState(false);
  const id = useId();

  return (
    <span className="relative inline-flex">
      <button
        type="button"
        aria-describedby={open ? id : undefined}
        aria-label={label}
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
        onFocus={() => setOpen(true)}
        onBlur={() => setOpen(false)}
        onKeyDown={(event) => {
          if (event.key === "Escape") setOpen(false);
        }}
        className={cn(
          "inline-flex items-center justify-center rounded-full text-slate-400 transition-colors duration-150 hover:text-slate-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-500",
          className
        )}
      >
        <Info className="h-3.5 w-3.5" strokeWidth={1.75} />
      </button>
      {open && (
        <span
          id={id}
          role="tooltip"
          className="absolute bottom-full left-1/2 z-20 mb-2 w-56 -translate-x-1/2 rounded-md bg-slate-900 px-3 py-2 text-xs leading-snug text-white shadow-lg"
        >
          {label}
        </span>
      )}
    </span>
  );
}