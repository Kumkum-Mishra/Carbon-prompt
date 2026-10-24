import type { ReactNode } from "react";
import { cn } from "@/utils/cn";

interface PageContainerProps {
  children: ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
}

export default function PageContainer({
  children,
  title,
  subtitle,
  className = "",
}: PageContainerProps) {
  return (
    <div
      className={cn(
        "mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-12 lg:px-8 lg:py-14",
        className
      )}
    >
      {(title || subtitle) && (
        <header className="mb-10">
          {title && (
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              {title}
            </h1>
          )}
          {subtitle && (
            <p className="mt-2 max-w-3xl text-base leading-[1.65] text-slate-600 sm:text-lg">
              {subtitle}
            </p>
          )}
        </header>
      )}
      {children}
    </div>
  );
}
