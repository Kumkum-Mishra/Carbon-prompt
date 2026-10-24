import Badge from "@/components/ui/Badge";
import type { BadgeVariant } from "@/components/ui/Badge";

interface InfoBadgeProps {
  children: string;
  variant?: BadgeVariant;
}

/**
 * Thin, named wrapper around the shared Badge primitive for the small
 * category labels used throughout the Mathematics page (e.g. "Core Metric").
 */
export default function InfoBadge({ children, variant = "violet" }: InfoBadgeProps) {
  return <Badge variant={variant}>{children}</Badge>;
}
