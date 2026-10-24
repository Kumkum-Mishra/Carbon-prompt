# 13 — Final Project Documentation

**GreenPrompt AI — Complete Project Guide**  
Suitable for onboarding, viva preparation, research paper methods section, and recruiter walkthroughs.

*All technical statements below were verified against the repository on 17 July 2026.*

---

## 1. Project Overview

GreenPrompt AI is a full-stack system that helps users write **more efficient prompts** for large language models and choose **efficient models**.

Given a prompt, the system:

1. Analyzes structure and complexity (tokens, prompt strategy, task type)
2. Estimates a relative **Green Carbon Score (GCS)**
3. Generates a shorter optimized prompt using a fine-tuned **FLAN-T5-small** model
4. Recomputes carbon and reduction percentages
5. Recommends suitable LLMs using **GMES** over a curated metrics dataset

**Important definition:** GCS is a research-defined relative index, not a laboratory measurement of CO₂ emissions.

---

## 2. Folder Structure

```
MajorProject/
├── frontend/                 # Next.js UI
├── backend/                  # FastAPI services
├── training/                 # Model fine-tuning scripts
├── models/greenprompt_model/ # Saved seq2seq weights + metrics
├── Dataset/                  # CSV copies
├── Guide/                    # Audit & documentation (this folder)
├── PRD/                      # Product requirements
├── prompts_dataset.csv       # 1,000 source prompts
├── prompt_optimization_dataset.csv  # 10,000 train pairs
├── model_data.csv            # 770 model metrics
├── build_optimization_dataset.py
└── .env.example
```

---

## 3. Frontend Architecture

- **Framework:** Next.js 14 App Router, TypeScript, Tailwind, Framer Motion, Recharts
- **Pages:** `/` marketing, `/analyze` live demo, `/mathematics` formulas, `/datasets` charts
- **State:** `useProcessPrompt` local state only
- **API:** single live call `POST /process` from Analyze
- **Rendering:** cards for carbon, analysis/optimization, recommendations; word-level prompt diff

Details: [02_Frontend_Architecture.md](./02_Frontend_Architecture.md)

---

## 4. Backend Architecture

- **Framework:** FastAPI + Pydantic
- **Modules:** Analyzer, Carbon, Optimizer, Recommendation
- **Gateway:** `/process` orchestrates the full pipeline; individual endpoints exist for unit access
- **Default optimizer:** local trained model under `models/greenprompt_model`

Details: [03_Backend_Architecture.md](./03_Backend_Architecture.md)

---

## 5. Complete Workflow

User prompt → Analyze → Original GCS → Optimize (beam search + rank) → Optimized GCS → Recommend models → JSON → UI cards.

Sequence diagram: [09_Flowcharts.md](./09_Flowcharts.md) §11  
Narrative: [08_Full_Project_Flow.md](./08_Full_Project_Flow.md)

---

## 6. Machine Learning Models

| Model | Role |
|-------|------|
| Fine-tuned `google/flan-t5-small` (~77M) | Prompt rewriting |
| tiktoken `cl100k_base` | Token counting (not trainable) |
| Regex classifiers | Prompt/task typing (not ML) |
| GMES formulas | Ranking (not ML) |

Training data is **synthetic**: verbose wrappers + rule-based targets from `build_optimization_dataset.py`.

Reported BLEU/ROUGE from a **40-sample** fast eval are high because evaluation matches the same synthetic distribution — disclose this in papers.

Details: [04_Prompt_Optimization.md](./04_Prompt_Optimization.md)

---

## 7. Prompt Optimization

- Prefix: `Simplify this prompt while preserving meaning: `
- Generation: beam search (5 beams / 5 sequences), max 96 new tokens, no temperature sampling
- Ranking: lexical similarity + token/carbon gains + readability − type-change penalties
- Semantic floor: similarity ≥ 0.50 + preserve numbers/quotes

---

## 8. Carbon Prediction

\[
GCS = T \times W_p \times W_t \times 0.00001
\]

Weights live in YAML. Hand verification MATCHED implementation.

Details: [05_Carbon_Prediction.md](./05_Carbon_Prediction.md)

---

## 9. Model Recommendation

Load `model_data.csv` → parse → min-max normalize → cost efficiency → GMES mean → top 5.

Audit Coding top pick: **Grok 4.20 Beta Non-reasoning (80.35)**.

Details: [06_Model_Recommendation.md](./06_Model_Recommendation.md)

---

## 10. Training Process (Start to Finish)

1. Collect/curate 1,000 prompts (`prompts_dataset.csv`)
2. Expand to 10,000 pairs (`build_optimization_dataset.py`)
3. Split 80/10/10 seed 42
4. Fine-tune FLAN-T5-small 3 epochs (AdamW, LR 3e-4, warmup 0.06)
5. Save best checkpoint by eval loss
6. Optional `finish_evaluation.py` for demos + sample metrics
7. Deploy weights path for `TrainedModelProvider`

---

## 11. Inference Process

1. Load tokenizer + `AutoModelForSeq2SeqLM` from disk (lazy/singleton in provider)
2. Encode prefixed prompt
3. `generate` with beams
4. Decode & dedupe
5. Score candidates in OptimizationService
6. Return best comparison payload

---

## 12. Mathematics

Four formulas documented on `/mathematics` match backend code:

1. GCS  
2. Token reduction %  
3. Carbon reduction %  
4. Cost efficiency + GMES  

Verification report: [07_Mathematical_Verification.md](./07_Mathematical_Verification.md)

---

## 13. Datasets

| Dataset | Rows | Use |
|---------|------|-----|
| prompts_dataset.csv | 1,000 | Source prompts / stats |
| prompt_optimization_dataset.csv | 10,000 | Training pairs |
| model_data.csv | 770 | Recommendations |
| dataset-stats.json | snapshot | Frontend Datasets page |

Charts on `/datasets` are **static** but currently consistent with CSV aggregates.

---

## 14. API Flow

| Endpoint | Role |
|----------|------|
| POST `/process` | Full pipeline (frontend) |
| POST `/analyze` | Analysis only |
| POST `/carbon` | GCS only |
| POST `/optimize` | Optimization only |
| POST `/recommend` | Ranking only |
| GET `/health` | Module smoke |

---

## 15. Deployment Architecture (Practical)

**Local demo (as designed):**

```
Terminal A: cd backend && python main.py   # :8000
Terminal B: cd frontend && npm run dev     # :3000
Env: NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
     LLM_PROVIDER=trained_model
     TRAINED_MODEL_PATH=../models/greenprompt_model
```

**Production suggestions (not all implemented):**
- Separate model worker / GPU host
- Rate limiting & auth if public
- Regenerate dataset-stats in CI
- Deep health checks including model load
- Single shared config module

---

## 16. Advantages

1. End-to-end demonstrable pipeline for sustainability-aware prompting  
2. Transparent, simple, testable carbon index  
3. Real local seq2seq model (not only API wrappers)  
4. Data-driven model ranking  
5. Modular backend with strong unit-test density  
6. Clear UI separation of live demo vs methodology pages  

---

## 17. Limitations

1. GCS ≠ physical CO₂  
2. Synthetic optimization labels → limited generalization proof  
3. Heuristic classifiers & lexical similarity  
4. Static Mathematics/Datasets pages can drift  
5. Marketing copy inconsistencies (see Bug Report)  
6. CPU inference latency  
7. CSV model metrics may be stale  

---

## 18. Future Work

1. Human preference / LLM-as-judge eval on real prompts  
2. Embedding-based semantic similarity  
3. Learned carbon factors or energy models (CodeCarbon, etc.)  
4. Live pricing APIs for recommendation  
5. Show Wp/Wt/K in UI  
6. Full test-set evaluation & ONNX/runtime acceleration  
7. Unify static content with backend constants via codegen  

---

## 19. Research Contribution (Honest Framing)

**Contribution:** A reproducible software system combining (a) prompt compression via fine-tuned seq2seq, (b) a transparent multiplicative sustainability index for prompts, and (c) multi-criteria model recommendation (GMES).

**Not claimed by the code:** Absolute emission accounting; SOTA prompt optimization quality solely from synthetic BLEU.

---

## 20. Testing Methodology

- Unit tests for pure math and parsers  
- Route-level API tests  
- Pipeline tests with mock LLM provider  
- Frontend component tests  
- Audit: hand recalculation + CSV reconciliation + full suite execution  

Results: **224 backend + 16 frontend tests passed** (17 Jul 2026).

---

## 21. Validation Methodology

| Claim | Validation |
|-------|------------|
| GCS formula | Code + hand calc MATCH |
| Reduction % | Code + hand calc MATCH |
| GMES | Code + ranking smoke |
| Token counts | tiktoken live |
| Dataset charts | JSON vs CSV MATCH |
| Optimized text | Model weights + provider path verified |
| No random scores | Grep/review of production paths |

---

## 22. How to Explain in a Viva (60 seconds)

“GreenPrompt analyzes a prompt with tiktoken and rule-based classifiers, computes GCS as tokens times prompt and task weights times 1e-5, rewrites the prompt with a fine-tuned FLAN-T5 model using beam search and similarity ranking, then recommends models by GMES over a 770-row metrics CSV. The carbon score is a relative index for comparison, not measured CO₂. Training pairs were synthetically generated to teach de-verbosity.”

---

## 23. Document Index

Start at [00_INDEX.md](./00_INDEX.md) for the full audit package.
