import type { FormulaVariable } from "@/data/mathematics";

interface VariableTableProps {
  variables: FormulaVariable[];
}

export default function VariableTable({ variables }: VariableTableProps) {
  return (
    <div className="overflow-x-auto rounded-[10px] border border-slate-200">
      <table className="w-full text-left text-sm">
        <caption className="sr-only">Variable definitions</caption>
        <thead>
          <tr className="border-b border-slate-200 bg-slate-50">
            <th scope="col" className="px-3 py-2 text-xs font-medium uppercase tracking-wide text-slate-500">
              Symbol
            </th>
            <th scope="col" className="px-3 py-2 text-xs font-medium uppercase tracking-wide text-slate-500">
              Meaning
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {variables.map((variable) => (
            <tr key={variable.symbol}>
              <td className="whitespace-nowrap px-3 py-2 align-top font-mono text-sm font-medium text-emerald-700">
                {variable.symbol}
              </td>
              <td className="px-3 py-2 align-top text-slate-600">
                {variable.description}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
