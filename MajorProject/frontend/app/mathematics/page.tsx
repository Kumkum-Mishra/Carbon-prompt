"use client";

import FormulaCard from "@/components/mathematics/FormulaCard";
import FormulaNav from "@/components/mathematics/FormulaNav";
import LimitationsSection from "@/components/mathematics/LimitationsSection";
import WorkedExampleSection from "@/components/mathematics/WorkedExampleSection";
import PageContainer from "@/components/layout/PageContainer";
import { formulas } from "@/data/mathematics";

const navItems = [
  ...formulas.map((formula) => ({
    id: formula.id,
    label: formula.title.split(" (")[0],
  })),
  { id: "worked-example", label: "Worked Example" },
  { id: "limitations", label: "Limitations" },
];

export default function MathematicsPage() {
  return (
    <PageContainer
      title="Mathematics"
      subtitle="Formulas behind GreenPrompt AI: carbon scoring, optimization ranking, and dynamic model recommendation (DGMES)."
    >
      <div className="grid gap-8 lg:grid-cols-[220px_1fr] lg:gap-12">
        <FormulaNav items={navItems} variant="chips" className="lg:hidden" />
        <FormulaNav
          items={navItems}
          variant="sidebar"
          className="hidden lg:block"
        />

        <div className="space-y-8">
          {formulas.map((formula) => (
            <FormulaCard key={formula.id} {...formula} />
          ))}

          <WorkedExampleSection />
          <LimitationsSection />
        </div>
      </div>
    </PageContainer>
  );
}
