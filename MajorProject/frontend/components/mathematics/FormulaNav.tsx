"use client";

import type { MouseEvent } from "react";
import { useEffect, useState } from "react";
import { cn } from "@/utils/cn";

export interface FormulaNavItem {
  id: string;
  label: string;
}

interface FormulaNavProps {
  items: FormulaNavItem[];
  className?: string;
  variant: "sidebar" | "chips";
}

function useActiveSection(ids: string[]): string {
  const [activeId, setActiveId] = useState(ids[0] ?? "");

  useEffect(() => {
    const elements = ids
      .map((id) => document.getElementById(id))
      .filter((el): el is HTMLElement => Boolean(el));

    if (elements.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) {
          setActiveId(visible[0].target.id);
        }
      },
      { rootMargin: "-15% 0px -70% 0px", threshold: 0 }
    );

    elements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, [ids]);

  return activeId;
}

export default function FormulaNav({ items, className, variant }: FormulaNavProps) {
  const activeId = useActiveSection(items.map((item) => item.id));

  const handleClick = (id: string) => (event: MouseEvent) => {
    event.preventDefault();
    document.getElementById(id)?.scrollIntoView({
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ? "auto"
        : "smooth",
      block: "start",
    });
  };

  if (variant === "chips") {
    return (
      <nav
        aria-label="Formula sections"
        className={cn("flex gap-2 overflow-x-auto pb-1", className)}
      >
        {items.map((item) => (
          <a
            key={item.id}
            href={`#${item.id}`}
            onClick={handleClick(item.id)}
            className={cn(
              "shrink-0 whitespace-nowrap rounded-full border px-3 py-1.5 text-sm font-medium transition-colors duration-150 focus-ring",
              activeId === item.id
                ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                : "border-slate-200 bg-white text-slate-600 hover:border-emerald-200 hover:text-emerald-700"
            )}
            aria-current={activeId === item.id ? "location" : undefined}
          >
            {item.label}
          </a>
        ))}
      </nav>
    );
  }

  return (
    <nav
      aria-label="Formula sections"
      className={cn("sticky top-24 self-start", className)}
    >
      <p className="px-3 text-xs font-semibold uppercase tracking-wide text-slate-400">
        On this page
      </p>
      <ul className="mt-2 space-y-1">
        {items.map((item) => (
          <li key={item.id}>
            <a
              href={`#${item.id}`}
              onClick={handleClick(item.id)}
              aria-current={activeId === item.id ? "page" : undefined}
              className={cn(
                "block rounded-inner px-3 py-2 text-sm font-medium transition-colors duration-150 focus-ring",
                activeId === item.id
                  ? "bg-emerald-50 text-emerald-700"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              )}
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
