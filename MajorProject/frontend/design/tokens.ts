/**
 * Design tokens aligned with FRONTEND_DESIGN_ARCHITECTURE.md.
 * Prefer Tailwind classes that map to these values in components.
 */

export const radii = {
  sm: "6px",
  md: "10px",
  lg: "16px",
  xl: "24px",
  "2xl": "32px",
  full: "9999px",
} as const;

export const shadows = {
  card: "0 1px 2px 0 rgb(15 23 42 / 0.04)",
  cardHover: "0 4px 20px -4px rgb(15 23 42 / 0.08)",
  floating: "0 12px 40px -12px rgb(15 23 42 / 0.18)",
} as const;

export const focusRing =
  "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-500";

export const focusRingLight =
  "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-400";
