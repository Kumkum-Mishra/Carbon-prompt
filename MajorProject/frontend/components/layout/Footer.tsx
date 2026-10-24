import Link from "next/link";
import { Leaf } from "lucide-react";
import { APP_NAME, GITHUB_URL, NAV_LINKS } from "@/utils/constants";

export default function Footer() {
  return (
    <footer className="mt-auto border-t border-slate-200 bg-slate-50">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-10 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
        <div className="flex items-center gap-2 text-emerald-700">
          <Leaf className="h-5 w-5" strokeWidth={1.75} />
          <span className="font-semibold">{APP_NAME}</span>
        </div>
        <nav
          aria-label="Footer"
          className="flex flex-wrap gap-x-5 gap-y-2 text-sm text-slate-600"
        >
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="rounded-sm transition-colors duration-150 hover:text-emerald-700 focus-ring"
            >
              {link.label}
            </Link>
          ))}
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-sm transition-colors duration-150 hover:text-emerald-700 focus-ring"
          >
            GitHub
          </a>
        </nav>
        <p className="text-sm text-slate-500">
          © {new Date().getFullYear()} {APP_NAME}. Sustainable AI for everyone.
        </p>
      </div>
    </footer>
  );
}
