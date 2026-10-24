# 01 — Complete Technical Audit Report

**Project:** GreenPrompt AI  
**Audit role:** Senior AI Research / Software / ML / QA / Architect / Code Reviewer  
**Date:** 17 July 2026  
**Rule:** Every claim below was verified against source code or executed tests.

---

## 1. Project Purpose

GreenPrompt AI analyzes a user prompt, estimates a relative **Green Carbon Score (GCS)**, generates a shorter **optimized prompt** via a local seq2seq model, recomputes carbon, and recommends an LLM from a CSV catalog using **GMES** (Green Model Efficiency Score).

It is suitable for major-project demonstration if limitations (synthetic training labels; relative carbon index; static docs pages) are disclosed honestly.

---

## 2. Repository Map

| Path | Role |
|------|------|
| `frontend/` | Next.js 14 App Router UI |
| `backend/` | FastAPI gateway + analyzer, carbon, optimizer, recommendation |
| `training/` | FLAN-T5 fine-tuning + evaluation scripts |
| `models/greenprompt_model/` | Saved fine-tuned weights + metrics |
| `prompts_dataset.csv` | 1,000 labeled source prompts |
| `prompt_optimization_dataset.csv` | 10,000 synthetic train pairs |
| `model_data.csv` | 770 models for recommendation |
| `Dataset/` | Copies of prompts + model CSVs |
| `build_optimization_dataset.py` | Builds synthetic optimization pairs |
| `PRD/` | Product requirements (not runtime) |
| `Guide/` | This audit documentation |

---

## 3. Module Purpose Inventory

### 3.1 Backend gateway

| Module | Purpose |
|--------|---------|
| `backend/main.py` | Uvicorn entry |
| `backend/app.py` | FastAPI app, CORS, timing middleware, global 500 handler |
| `backend/config.py` | Root env (CORS, keys, unused `LLM_PROVIDER=rule_based` default) |
| `backend/routes/health.py` | Module smoke health |
| `backend/routes/process.py` | Full pipeline `POST /process` |
| `backend/services/pipeline_service.py` | Analyze → Carbon → Optimize → Carbon → Recommend |
| `backend/services/module_registry.py` | Shared service singletons for `/process` |
| `backend/schemas/process.py` | Pipeline request/response models |
| `backend/utils/*` | Errors, logging, timing |

### 3.2 Analyzer

| Module | Purpose |
|--------|---------|
| `analyzer/analyzer.py` | Orchestrates clean → tokenize → classify → counts |
| `analyzer/tokenizer.py` | tiktoken `cl100k_base` |
| `analyzer/task_classifier.py` | Regex task categories |
| `analyzer/prompt_type_classifier.py` | Regex prompt strategies |
| `analyzer/utils.py` | Strip/clean, word count |
| `analyzer/routes.py` | `POST /analyze` |
| `analyzer/schemas.py` | Request/response validation |

### 3.3 Carbon

| Module | Purpose |
|--------|---------|
| `carbon/calculator.py` | GCS = tokens × Wp × Wt × K |
| `carbon/constants.py` | K = 1e-5, 6 decimal places |
| `carbon/prompt_weights.py` / `task_weights.py` | YAML weight loaders |
| `carbon/carbon_service.py` | Weight lookup + GCS |
| `carbon/routes.py` | `POST /carbon` |
| `carbon/dataset.py` | Reference CSV (tests only, not runtime) |

### 3.4 Optimizer

| Module | Purpose |
|--------|---------|
| `optimizer/optimization_service.py` | Analyze → candidates → rank → comparison |
| `optimizer/optimizer.py` | Provider coordinator + retries |
| `optimizer/providers/trained_model_provider.py` | FLAN-T5 beam search (default) |
| `optimizer/providers/rule_based_provider.py` | Regex filler strip |
| `optimizer/providers/mock_provider.py` | Test-only fixed output |
| `optimizer/providers/openai|anthropic|gemini_provider.py` | External APIs |
| `optimizer/ranking_engine.py` | Similarity + scoring of candidates |
| `optimizer/reduction.py` | Token/carbon % formulas |
| `optimizer/comparison.py` | Before/after assembly |
| `optimizer/routes.py` | `POST /optimize` |

### 3.5 Recommendation

| Module | Purpose |
|--------|---------|
| `recommendation/dataset_loader.py` | Load/filter/normalize `model_data.csv` |
| `recommendation/normalizers.py` | Parse metrics + min-max 0–100 |
| `recommendation/scorer.py` | Cost efficiency + GMES |
| `recommendation/ranking.py` | Sort top-N |
| `recommendation/category_mapper.py` | Task → CSV category |
| `recommendation/reason_generator.py` | Template reasons |
| `recommendation/routes.py` | `POST /recommend` |

### 3.6 Frontend

| Area | Purpose |
|------|---------|
| `app/page.tsx` | Marketing home (static) |
| `app/analyze/page.tsx` | Live pipeline UI (`POST /process`) |
| `app/mathematics/page.tsx` | Formula documentation (static) |
| `app/datasets/page.tsx` | Dataset charts from JSON snapshot (static) |
| `hooks/useProcessPrompt.ts` | Analyze-page state + API call |
| `services/api.ts` | Axios client |
| `data/*` | Static content / formula text / dataset-stats |

### 3.7 Training / models

| Area | Purpose |
|------|---------|
| `training/train_prompt_optimizer.py` | Fine-tune FLAN-T5-small |
| `training/evaluate_model.py` | BLEU/ROUGE/BERTScore helpers |
| `training/finish_evaluation.py` | Fast 40-sample eval + demos |
| `models/greenprompt_model/` | Saved weights, tokenizer, metrics |

---

## 4. Are Outputs Fake / Random / Placeholder?

| Output | Verdict | Evidence |
|--------|---------|----------|
| Character / word / token counts | **Real** | `len()`, `split()`, tiktoken encode |
| Prompt/task type | **Heuristic real** | Regex classifiers — not random, but not ML |
| GCS | **Real formula** | Hand-checked MATCH (see §7 doc) |
| Optimized prompt (default) | **Real model** | `TrainedModelProvider` loads `model.safetensors` |
| Token/carbon reduction % | **Real formula** | `(O-N)/O × 100` |
| Model recommendation | **Data-driven** | CSV + GMES arithmetic |
| Mock provider | **Test only** | Not production default |
| Home page metrics | **Marketing static** | Not from API |
| Mathematics examples | **Static docs** | Match formulas but illustrative labels |
| Datasets charts | **Static JSON** | Verified equal to CSV aggregates |

**No production API path uses `random()` for scores.**

---

## 5. Critical Scientific Honesty Notes

1. **GCS is not measured CO₂.** It is `tokens × weights × 0.00001` — a relative sustainability index. The UI CarbonCard tooltip states this correctly; Home marketing sometimes implies stronger environmental measurement.
2. **Optimizer training is circular.** Labels come from `build_optimization_dataset.py` rule-based `optimize_prompt()`. Evaluation against the same distribution yields BLEU ~94 on 40 samples — not proof of real-world quality.
3. **Semantic similarity is not embeddings.** Ranking uses `SequenceMatcher` + Jaccard word overlap (threshold 0.50).
4. **Datasets/Mathematics pages do not call the backend.** They will drift if YAML weights or CSVs change unless JSON/TS files are regenerated.

---

## 6. Endpoint Summary

| Method | Path | Real computation? |
|--------|------|-------------------|
| GET | `/health` | Smoke checks (optimizer only checks provider name string) |
| POST | `/process` | Full real pipeline |
| POST | `/analyze` | Real |
| POST | `/carbon` | Real formula |
| POST | `/optimize` | Real model/providers |
| POST | `/recommend` | Real CSV + GMES |

Full I/O detail: [03_Backend_Architecture.md](./03_Backend_Architecture.md).

---

## 7. Verification Performed During This Audit

1. Read all major backend/frontend/training modules (via exhaustive file review).
2. Recalculated GCS for multiple (tokens, Wp, Wt) tuples — **all MATCH**.
3. Compared `frontend/data/dataset-stats.json` to live CSV — **MATCH**.
4. Ran backend pytest — **224 passed**.
5. Ran frontend Jest — **16 passed**.
6. Ran recommendation for Coding — top model **Grok 4.20 Beta Non-reasoning**, GMES **80.35** (deterministic from CSV).

---

## 8. Overall Quality Scorecard

| Area | Score | Notes |
|------|-------|-------|
| Formula correctness | High | GCS/GMES/reduction verified |
| API honesty | High | No fake runtime scores |
| ML scientific rigor | Medium-Low | Synthetic labels; tiny eval sample |
| Frontend ↔ backend consistency | Medium | Analyze live; Home/Math/Datasets static + some conflicts |
| Test coverage | Medium-High backend; Medium frontend | Missing live model E2E in CI |
| Production readiness | Medium | Needs config cleanup, health depth, UI transparency |

---

## 9. Recommendations for Viva / Paper / Recruiters

**Say clearly:**
- GCS is a **weighted token-based index**, not life-cycle CO₂.
- Optimization model is a **fine-tuned FLAN-T5-small** trained on **synthetic de-verbosity pairs**.
- Recommendations rank models from a **curated metrics CSV** via GMES.
- Live demo path is `/analyze` → `POST /process`.

**Do not claim:**
- Absolute carbon emissions in grams.
- State-of-the-art NLP optimization quality based on BLEU 94 alone.
- That Datasets page charts refresh live from the CSV.

---

## 10. Related Documents

Continue with architecture docs (02–03), domain docs (04–06), math verification (07), flows (08–09), testing/bugs/quality (10–12), and the full narrative (13).
