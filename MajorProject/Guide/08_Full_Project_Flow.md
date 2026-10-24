# 08 — Full Project Flow Document

---

## 1. End-to-End User Flow (Analyze)

```
User opens /analyze
  → enters prompt (or picks sample)
  → clicks Analyze / Optimize
  → frontend POST /process { prompt }
  → backend PipelineService
  → response rendered in ResultsPanel + optimized diff
```

---

## 2. Detailed Backend Pipeline

```
1) Prompt Analysis
   clean_prompt → count_tokens(tiktoken) → classify_task → classify_prompt_type
   → character_count, word_count

2) Original Carbon
   Wp = prompt_weights[prompt_type]
   Wt = task_weights[task_type]
   GCS_orig = T_orig × Wp × Wt × 1e-5

3) Prompt Optimization
   TrainedModelProvider beam search (or alternate provider)
   → N candidates
   → ranking_engine (similarity, reductions, readability, constraints)
   → best optimized_prompt
   → re-analyze optimized → T_opt, types_opt
   → GCS_opt_internal for comparison
   → token_reduction_%, carbon_reduction_%

4) Optimized Carbon (pipeline re-estimate)
   GCS_opt = T_opt × Wp_opt × Wt_opt × 1e-5

5) Model Recommendation
   map optimized task_type → category
   load model_data.csv rows
   normalize metrics → CostEfficiency → GMES
   rank top 5 → reasons

6) Response assembly
   pipeline { analysis, carbon{original,optimized}, optimization, recommendation }
   metadata { processing_time_ms, pipeline_version }
```

---

## 3. Frontend Rendering Flow

```
useProcessPrompt stores ProcessSuccessResponse
  → ResultsPanel maps fields
     CarbonCard ← carbon.original/optimized.green_carbon_score
                ← optimization.carbon_reduction_percent
     PromptAnalysisOptimizationCard ← analysis + optimization metrics
     RecommendationCard ← recommendation
  → PromptInput.optimizedPrompt ← optimization.optimized_prompt
  → PromptDiffView highlights word changes
```

---

## 4. Parallel Static Flows (no API)

### Home
Static marketing sections from `data/home.ts` + Hero hardcoded visuals.

### Mathematics
Static formulas from `data/mathematics.ts`.

### Datasets
Static charts from `data/dataset-stats.json` (snapshot of CSVs).

---

## 5. Training / Offline Flow

```
prompts_dataset.csv
  → build_optimization_dataset.py
  → prompt_optimization_dataset.csv
  → train_prompt_optimizer.py
  → models/greenprompt_model/
  → finish_evaluation.py → metrics + demos
  → TrainedModelProvider loads weights at runtime
```

---

## 6. Data Artifacts Touching Runtime

| Artifact | Used by |
|----------|---------|
| `models/greenprompt_model/*` | Optimizer (default) |
| `model_data.csv` | Recommendation |
| `prompt_weights.yaml` / `task_weights.yaml` | Carbon |
| tiktoken encoding | Analyzer |
| Frontend JSON/TS data files | Docs pages only |

---

## 7. Error Paths

| Stage | Typical failure | User sees |
|-------|-----------------|-----------|
| Empty/short prompt | Validation | 400 / frontend validation |
| Model missing | Provider unavailable | Pipeline 500 / optimize error |
| Unknown types (pre-analyzed carbon) | 400 | Error message |
| Empty category models | Dataset error | 400/500 |
| Network down | Axios error | AnalyzeErrorState |

---

## 8. Deployment Shape (as implemented)

```
Browser (Next.js :3000)
   │  NEXT_PUBLIC_API_BASE_URL
   ▼
FastAPI (uvicorn :8000)
   ├── local torch model dir
   ├── YAML weights
   └── model_data.csv
```

No container/orchestration files were required for this audit’s correctness conclusions. See Final Documentation for suggested deployment notes.
