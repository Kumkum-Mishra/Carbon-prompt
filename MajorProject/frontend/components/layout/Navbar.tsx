"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useId, useRef, useState } from "react";
import { Github, Leaf, Menu, X } from "lucide-react";
import { APP_NAME, GITHUB_URL, NAV_LINKS } from "@/utils/constants";
import { cn } from "@/utils/cn";

export default function Navbar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const menuId = useId();
  const menuButtonRef = useRef<HTMLButtonElement>(null);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  useEffect(() => {
    setMobileOpen(false);
  }, [pathname]);

  useEffect(() => {
    if (!mobileOpen) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setMobileOpen(false);
        menuButtonRef.current?.focus();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [mobileOpen]);

  const linkClass = (active: boolean) =>
    cn(
      "rounded-inner px-3 py-2 text-sm font-medium transition-colors duration-150 focus-ring",
      active
        ? "bg-emerald-50 text-emerald-700"
        : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
    );

  return (
    <nav
      className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/90 backdrop-blur-md"
      aria-label="Primary"
    >
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="flex items-center gap-2 font-semibold text-emerald-700 transition-colors duration-150 hover:text-emerald-800 focus-ring rounded-inner"
        >
          <Leaf className="h-5 w-5" strokeWidth={1.75} />
          <span>{APP_NAME}</span>
        </Link>

        <div className="hidden items-center gap-1 md:flex">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              aria-current={isActive(link.href) ? "page" : undefined}
              className={linkClass(isActive(link.href))}
            >
              {link.label}
            </Link>
          ))}
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="ml-1 inline-flex items-center gap-1.5 rounded-inner px-3 py-2 text-sm font-medium text-slate-600 transition-colors duration-150 hover:bg-slate-50 hover:text-slate-900 focus-ring"
          >
            <Github className="h-4 w-4" strokeWidth={1.75} />
            GitHub
          </a>
          <Link
            href="/analyze"
            className="ml-2 inline-flex min-h-[40px] items-center rounded-inner bg-emerald-600 px-4 py-2 text-sm font-semibold text-white transition-all duration-150 hover:-translate-y-0.5 hover:bg-emerald-500 focus-ring active:translate-y-0"
          >
            Analyze Prompt
          </Link>
        </div>

        <button
          ref={menuButtonRef}
          type="button"
          className="inline-flex h-11 w-11 items-center justify-center rounded-inner text-slate-600 transition-colors duration-150 hover:bg-slate-50 focus-ring md:hidden"
          onClick={() => setMobileOpen((open) => !open)}
          aria-label={mobileOpen ? "Close menu" : "Open menu"}
          aria-expanded={mobileOpen}
          aria-controls={menuId}
        >
          {mobileOpen ? (
            <X className="h-5 w-5" strokeWidth={1.75} />
          ) : (
            <Menu className="h-5 w-5" strokeWidth={1.75} />
          )}
        </button>
      </div>

      {mobileOpen && (
        <div
          id={menuId}
          className="border-t border-slate-200 bg-white px-4 py-3 md:hidden"
        >
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              aria-current={isActive(link.href) ? "page" : undefined}
              className={cn(
                "block rounded-inner px-3 py-3 text-base font-medium transition-colors duration-150 focus-ring",
                isActive(link.href)
                  ? "bg-emerald-50 text-emerald-700"
                  : "text-slate-700 hover:bg-slate-50"
              )}
            >
              {link.label}
            </Link>
          ))}
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-1 flex items-center gap-2 rounded-inner px-3 py-3 text-base font-medium text-slate-700 transition-colors duration-150 hover:bg-slate-50 focus-ring"
          >
            <Github className="h-4 w-4" strokeWidth={1.75} />
            GitHub
          </a>
          <Link
            href="/analyze"
            onClick={() => setMobileOpen(false)}
            className="mt-2 flex min-h-[44px] items-center justify-center rounded-inner bg-emerald-600 px-3 py-3 text-base font-semibold text-white transition-colors duration-150 hover:bg-emerald-500 focus-ring"
          >
            Analyze Prompt
          </Link>
        </div>
      )}
    </nav>
  );
}
