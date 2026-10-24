import type { ReactNode } from "react";
import { Calculator } from "lucide-react";
import { cn } from "@/utils/cn";

interface ExampleCardProps {
  label?: string;
  children: ReactNode;
  className?: string;
}

export default function ExampleCard({
  label = "Example",
  children,
  className,
}: ExampleCardProps) {
  return (
    <div
      className={cn(
        "rounded-[10px] border border-emerald-100 bg-emerald-50 p-4",
        className
      )}
    >
      <p className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-emerald-700">
        <Calculator className="h-3.5 w-3.5" strokeWidth={1.75} />
        {label}
      </p>
      <p className="mt-1.5 whitespace-pre-wrap break-words font-mono text-sm leading-relaxed text-slate-800">
        {children}
      </p>
    </div>
  );
}
