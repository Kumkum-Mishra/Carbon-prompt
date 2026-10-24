import type { ReactNode } from "react";

export interface FormulaVariable {
  symbol: string;
  description: string;
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

const OPERATOR_PATTERN = "[×xX*/+\\-=(),]";
const NUMBER_PATTERN = "\\d+(?:\\.\\d+)?";

/**
 * Lightweight syntax highlighting for formula strings: variable identifiers
 * (from the card's variable list), numeric constants, and operators each get
 * their own accent color. Formulas are simple expressions, so a small
 * tokenizer is enough — no dependency on a full code-highlighting library.
 */
export function highlightFormula(
  formula: string,
  variables: FormulaVariable[]
): ReactNode[] {
  const identifiers = Array.from(
    new Set(
      variables.flatMap((variable) =>
        variable.symbol.split(/\s*\/\s*/).map((part) => part.trim())
      )
    )
  )
    .filter(Boolean)
    .sort((a, b) => b.length - a.length);

  const identifierPattern = identifiers.map(escapeRegExp).join("|");
  const pattern = new RegExp(
    `(${identifierPattern ? `${identifierPattern}|` : ""}${NUMBER_PATTERN}|${OPERATOR_PATTERN})`,
    "g"
  );

  const identifierSet = new Set(identifiers);
  const numberRegex = new RegExp(`^${NUMBER_PATTERN}$`);
  const operatorRegex = new RegExp(`^${OPERATOR_PATTERN}$`);

  return formula
    .split(pattern)
    .filter((token) => token !== "" && token !== undefined)
    .map((token, index) => {
      if (identifierSet.has(token)) {
        return (
          <span key={index} className="font-semibold text-emerald-400">
            {token}
          </span>
        );
      }
      if (numberRegex.test(token)) {
        return (
          <span key={index} className="text-amber-400">
            {token}
          </span>
        );
      }
      if (operatorRegex.test(token)) {
        return (
          <span key={index} className="text-slate-400">
            {token}
          </span>
        );
      }
      return <span key={index}>{token}</span>;
    });
}
