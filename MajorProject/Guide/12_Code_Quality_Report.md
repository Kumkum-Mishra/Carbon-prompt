# 12 — Code Quality Report

---

## 1. Strengths

1. **Clear modular boundaries** — analyzer, carbon, optimizer, recommendation are separable packages with schemas and tests.
2. **Deterministic core math** — GCS/GMES/reductions are pure functions with unit tests.
3. **Typed API contracts** — Pydantic backend + TypeScript frontend types for `/process`.
4. **Provider pattern** — optimizer can swap trained/rule/API/mock backends.
5. **Honest UI tooltip** on CarbonCard about relative GCS.
6. **224 backend tests** covering formulas and routes.
7. **Pipeline orchestration** is readable (`pipeline_service.py`).

---

## 2. Weaknesses

1. Config duplication (root vs optimizer).
2. Static frontend docs can drift from YAML/CSV.
3. Marketing pages not treated as “source of truth” governed content.
4. ML eval methodology weak for research claims.
5. Dead frontend components + weak pipeline test assertion.
6. Health check incomplete for heavy dependency (torch model).
7. Semantic similarity is lexical, named as if deeper NLP.

---

## 3. Maintainability

| Aspect | Rating | Notes |
|--------|--------|-------|
| Backend structure | Good | Package-per-domain |
| Frontend structure | Good | App router + components |
| Shared constants FE/BE | Weak | Formulas duplicated in TS docs |
| Training reproducibility | Good | seed 42, config file |
| Docs in repo | Improving | This Guide folder |

---

## 4. Testing Quality

| Layer | Quality |
|-------|---------|
| Formula unit tests | Strong |
| Route tests | Good |
| Pipeline with mock optimizer | Adequate |
| Live model regression | Weak / missing |
| Frontend component tests | Adequate but narrow |
| Visual/E2E | Missing |

---

## 5. Code Smells

- `assert … or True` in pipeline tests  
- Unused `checkHealth` client helper  
- Orphaned analyze cards  
- Silent exception swallow on ONNX export  
- Recommendation category argument redundancy  

---

## 6. Security & Ops Hygiene

- Env-based secrets for external LLMs — good pattern  
- Ensure `.env` not committed (`.env.example` present)  
- Public demo deployment needs rate limits (not present)  

---

## 7. Recommendations

1. Introduce a single `shared` constants document or codegen for K/weights examples.  
2. Add a script to regenerate `dataset-stats.json` from CSVs.  
3. Add CI job: pytest + jest + optional model smoke (skip if no weights).  
4. Replace marketing hardcodes with named fixtures.  
5. Document research limitations next to metrics JSON.  

---

## 8. Overall Quality Verdict

**Engineering quality for a major project is solid** on architecture and formula correctness.  
**Research quality requires careful disclosure** of synthetic training and relative carbon scoring.  
**Product polish** needs consistency fixes on static pages and deeper health/observability.
