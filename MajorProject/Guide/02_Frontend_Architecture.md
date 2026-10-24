# 02 — Frontend Architecture Document

**Stack:** Next.js 14 (App Router), React client components, TypeScript, Tailwind, Framer Motion, Recharts, Axios, Jest + Testing Library.

---

## 1. Routing

| Route | File | Live API? |
|-------|------|-----------|
| `/` | `frontend/app/page.tsx` | No — marketing |
| `/analyze` | `frontend/app/analyze/page.tsx` | **Yes** — `POST /process` |
| `/mathematics` | `frontend/app/mathematics/page.tsx` | No — static formulas |
| `/datasets` | `frontend/app/datasets/page.tsx` | No — static JSON |

Root layout: `app/layout.tsx` → `AppShell` (Navbar + PageTransition + Footer).

Nav links: `utils/constants.ts` — Home, Analyze, Mathematics, Datasets.

---

## 2. Page Hierarchy

```
RootLayout
└── AppShell
    ├── Navbar
    ├── main / PageTransition
    │   ├── Home sections (Hero, Problem, Workflow, Features, Metrics, Architecture, Tech, Research)
    │   ├── Analyze (PromptInput + loader/error/results)
    │   ├── Mathematics (FormulaNav + FormulaCards + WorkedExample + Limitations)
    │   └── Datasets (KPI cards + charts + ResearchNotes)
    └── Footer
```

---

## 3. Component Map (Analyze)

| Component | Role |
|-----------|------|
| `PromptInput` | Prompt form, samples, word-diff vs optimized |
| `PipelineLoader` | Cosmetic 4-step progress |
| `ResultsPanel` | Wires three result cards |
| `CarbonCard` | Before/after GCS + reduction % + bar chart |
| `PromptAnalysisOptimizationCard` | Analysis + optimization metrics |
| `RecommendationCard` | Top model, GMES, reasons, bar chart |
| `AnalyzeEmptyState` / `AnalyzeErrorState` | Pre/post error UI |

**Orphaned (implemented but unused on pages):** `AnalysisCard`, `OptimizationCard`, `ResultsOverview`, `CTASection`.

---

## 4. State Management

Pattern: **local React state only** (no Redux/Zustand/React Query).

`hooks/useProcessPrompt.ts` owns:
- `result`, `error`, `isLoading`, `loadingStep`, `lastPrompt`
- `submit`, `retry`, `reset`

Loading steps advance every **800 ms** client-side — **not** tied to real backend stages (cosmetic).

---

## 5. API Layer

`services/api.ts`:
- Base URL: `NEXT_PUBLIC_API_BASE_URL` or `http://localhost:8000`
- Timeout: 60s
- `processPrompt(prompt)` → `POST /process`
- `checkHealth()` → `GET /health` (**defined, never called from UI**)

Types: `types/api.ts` mirrors backend pipeline schema including `prompt_weight`, `task_weight`, `scaling_constant` — **typed but not displayed**.

---

## 6. How Displayed Values Reach the UI

```
User prompt
  → PromptInput local state
  → useProcessPrompt.submit()
  → api.processPrompt()
  → ProcessSuccessResponse
  → ResultsPanel
       ├─ CarbonCard(original GCS, optimized GCS, carbon_reduction_percent)
       ├─ PromptAnalysisOptimizationCard(analysis + optimization fields)
       └─ RecommendationCard(recommendation.*)
  → PromptInput shows optimized_prompt for diff
```

**Frontend does not recompute GCS or GMES.** It only formats:
- `formatCarbonScore` — 6 decimals if &lt; 0.001 else 4
- `formatPercent` — 2 decimals
- `formatNumber`

---

## 7. Mathematics Page

Source: `data/mathematics.ts` (static).

Documents four formulas matching backend:
1. GCS
2. Token reduction %
3. Carbon reduction %
4. Cost efficiency + GMES

Worked example uses task label **"Explanation"** (weight 1.2) — **not** in backend task taxonomy (closest: Writing 1.2). Arithmetic of the example is correct; the label is illustrative.

---

## 8. Datasets Page

Source: `data/dataset-stats.json` (static snapshot).

Verified against CSV during audit:
- 1,000 prompts, average tokens **46.98** — MATCH
- 770 models, category counts MATCH

Charts:
- Prompt-type pie (groups rare types into “Other”)
- Task-type bar — **only top 8 of 10** (`.slice(0, 8)`)
- Model category bar + summary tiles

---

## 9. Animations & Responsive Behavior

- Framer Motion page transitions (`design/motion.ts`)
- CountUp-style home metrics
- Responsive Navbar (mobile menu)
- FormulaNav: sticky sidebar desktop, chips mobile
- Charts via Recharts `ResponsiveContainer`

---

## 10. Frontend Integrity Issues

| Issue | Severity |
|-------|----------|
| Home “10,000+ Prompts Benchmarked” vs Datasets 1,000 rows | Major consistency |
| Hero token/carbon numbers ≠ Mathematics worked example for similar prompt | Major marketing |
| GCS factor breakdown not shown on Analyze | Transparency gap |
| Fake loading step timer | Minor UX |
| Reasons truncated to 2; models chart to 4 | Minor |
| Dead components still tested | Code hygiene |

Full list: [11_Bug_Report.md](./11_Bug_Report.md).
