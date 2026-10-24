"use client";

import type { LucideIcon } from "lucide-react";
import { MapPin, Sigma } from "lucide-react";
import IconBox from "@/components/ui/IconBox";
import { highlightFormula } from "@/utils/formulaHighlight";
import ExampleCard from "./ExampleCard";
import InfoBadge from "./InfoBadge";
import VariableTable from "./VariableTable";

export interface FormulaVariable {
  symbol: string;
  description: string;
}

export interface FormulaCardProps {
  id?: string;
  icon?: LucideIcon;
  badge?: string;
  title: string;
  formula: string;
  variables: FormulaVariable[];
  explanation: string;
  example: string;
  usage?: string;
}

export default function FormulaCard({
  id,
  icon = Sigma,
  badge,
  title,
  formula,
  variables,
  explanation,
  example,
  usage,
}: FormulaCardProps) {
  return (
    <div
      id={id}
      className="scroll-mt-24 rounded-card border border-slate-200 bg-white p-6 sm:p-8"
    >
      <div className="flex flex-wrap items-center gap-3">
        <IconBox icon={icon} />
        <h3 className="text-2xl font-bold leading-[1.25] text-slate-900">
          {title}
        </h3>
        {badge && <InfoBadge>{badge}</InfoBadge>}
      </div>

      <pre className="mt-5 overflow-x-auto whitespace-pre-wrap break-words rounded-inner bg-slate-900 px-4 py-3.5 font-mono text-[15px] leading-relaxed text-slate-200">
        {highlightFormula(formula, variables)}
      </pre>

      <div className="mt-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
          Variables
        </p>
        <div className="mt-2">
          <VariableTable variables={variables} />
        </div>
      </div>

      <p className="mt-5 text-[15px] leading-[1.65] text-slate-700">
        {explanation}
      </p>

      <div className="mt-5">
        <ExampleCard>{example}</ExampleCard>
      </div>

      {usage && (
        <div className="mt-4 flex items-start gap-2 text-xs text-slate-500">
          <MapPin className="mt-0.5 h-3.5 w-3.5 shrink-0" strokeWidth={1.75} />
          <span>{usage}</span>
        </div>
      )}
    </div>
  );
}
