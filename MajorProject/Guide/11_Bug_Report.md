# 11 — Bug Report

Issues found during the 17 July 2026 source audit. Every item references observed code/behavior.

---

## Critical

*None found that return random/fake GCS/GMES in production APIs.*

---

## Major

### M1 — Home marketing conflicts with Datasets page
- **Problem:** Home claims “10,000+ Prompts Benchmarked”; Datasets shows 1,000 prompt rows.
- **Why:** Static `data/home.ts` vs `dataset-stats.json` (and CSV).
- **Impact:** Damages trust in viva/demo.
- **Fix:** Clarify 10k = optimization *pairs*; 1k = source prompts — or change copy.
- **Priority:** P1

### M2 — Hero visual numbers ≠ Mathematics worked example
- **Problem:** Same neural-network theme uses different token/carbon figures (Hero ~42→24, −42.8% vs Math 24→12, 50%).
- **Why:** Hardcoded marketing visuals.
- **Impact:** Inconsistent demo narrative.
- **Fix:** Share one canonical example object across Home/Math/Analyze samples.
- **Priority:** P1

### M3 — Circular ML evaluation overstated if cited naively
- **Problem:** BLEU ~94 / ROUGE ~0.99 from 40 synthetic test samples matching rule-based labels.
- **Why:** Training targets from same rule engine as construction script.
- **Impact:** Research overclaim risk.
- **Fix:** Disclose; add human/LLM-judge eval on real prompts; full 1000-sample eval.
- **Priority:** P1 (research integrity)

### M4 — Analyze UI hides GCS factors
- **Problem:** API returns Wp, Wt, K, token_count; UI shows only final GCS.
- **Why:** CarbonCard design omission.
- **Impact:** Hard to explain live results vs Mathematics page.
- **Fix:** Expandable breakdown in CarbonCard.
- **Priority:** P1

### M5 — Optimizer health check is shallow
- **Problem:** `/health` marks optimizer OK if `provider_name` is non-empty; does not load weights.
- **Why:** `_check_optimizer` implementation.
- **Impact:** “healthy” while `/optimize` can still fail.
- **Fix:** Attempt lightweight model path existence / load probe.
- **Priority:** P1

---

## Minor / Logic

### L1 — Dual `LLM_PROVIDER` defaults
- Root `backend/config.py` → `rule_based`; `optimizer/config.py` → `trained_model`.
- **Impact:** Operator confusion.
- **Fix:** Single shared config.
- **Priority:** P2

### L2 — `MAX_PROMPT_LENGTH` env unused by modules
- Root reads env; analyzer/optimizer hardcode 10000.
- **Priority:** P2

### L3 — Pipeline recommendation passes redundant category
- `category=optimization.optimized_task_type` duplicates task mapping intent.
- **Priority:** P3

### L4 — Optimized type changes not shown in UI
- ResultsPanel shows original classification; carbon may use optimized types.
- **Priority:** P2

### L5 — Carbon scores vs reduction % from different response branches
- `pipeline.carbon.*` vs `optimization.carbon_reduction_percent`.
- Usually consistent; theoretically can diverge if paths differ.
- **Priority:** P2

### L6 — Missing metric imputation = 50.0
- Can inflate mediocre incomplete rows.
- **Priority:** P2

### L7 — Category fallbacks (Math→coding, Image→text)
- May recommend adjacent domain.
- **Priority:** P2

### L8 — Analyzer service accepts empty/1-char; routes enforce min 2
- Inconsistent layers.
- **Priority:** P3

### L9 — Task classifier overlaps
- Multi-intent prompts may misclassify by regex order.
- **Priority:** P2

### L10 — Trained model silent no-op fallback
- Empty candidates → return original without error.
- **Priority:** P2

### L11 — System prompt ignored by trained model provider
- Loaded but unused.
- **Priority:** P3

### L12 — Weak test `assert ... or True` in pipeline service tests
- Always passes token-reduction assertion.
- **Priority:** P2

### L13 — Datasets task chart `.slice(0, 8)`
- Hides 2 of 10 categories without note.
- **Priority:** P3

### L14 — Recommendation reasons/models truncated in UI
- 2 reasons, 4 bars.
- **Priority:** P3

### L15 — Fake loading step timer (800 ms)
- Not synced to backend stages.
- **Priority:** P3

### L16 — `checkHealth()` unused in UI
- **Priority:** P3

### L17 — Dead components (AnalysisCard, OptimizationCard, ResultsOverview, CTASection)
- **Priority:** P3

### L18 — ONNX export missing after training
- Silent failure path.
- **Priority:** P3

### L19 — Full 1000-sample test eval not completed in training log
- Metrics rewritten by fast sample script.
- **Priority:** P2

### L20 — Mathematics “Explanation” task label
- Not in backend taxonomy.
- **Priority:** P3

---

## UI

| ID | Issue | Priority |
|----|-------|----------|
| U1 | Marketing number conflicts (M1/M2) | P1 |
| U2 | No GCS breakdown | P1 |
| U3 | Cosmetic pipeline loader | P3 |
| U4 | Chart truncation | P3 |
| U5 | Recharts zero-size warning in Jest (test env) | P3 |

---

## Backend

| ID | Issue | Priority |
|----|-------|----------|
| B1 | Shallow optimizer health | P1 |
| B2 | Config dual defaults | P2 |
| B3 | Pipeline failures always 500 | P2 |
| B4 | Inconsistent error schemas across modules | P3 |

---

## ML

| ID | Issue | Priority |
|----|-------|----------|
| ML1 | Synthetic circular labels | P1 |
| ML2 | Tiny eval sample (40) | P1 |
| ML3 | Similarity heuristic ≠ embeddings | P2 (limitation) |
| ML4 | Train eval generation ≠ prod beams | P2 |

---

## Performance

| ID | Issue | Priority |
|----|-------|----------|
| P1 | CPU inference can be slow for `/process` | P2 |
| P2 | Model loaded in-process; no separate inference service | P3 |

---

## Security

| ID | Issue | Priority |
|----|-------|----------|
| S1 | CORS/config from env — ensure production lockdown | P2 |
| S2 | Prompt logging flag `LOG_FULL_PROMPT` — PII risk if enabled | P2 |
| S3 | External LLM providers need API key hygiene | P2 |
| S4 | No auth on public optimize endpoints (expected for demo; not multi-tenant safe) | P2 if deployed public |

---

## Scalability

| ID | Issue | Priority |
|----|-------|----------|
| SC1 | Sync FastAPI + local torch in request path | P2 |
| SC2 | Recommendation loads/filters CSV in process | P3 |
| SC3 | No queue/worker for generation | P2 |

---

## Suggested Fix Order

1. Align Home/Hero/Datasets copy and examples  
2. Show GCS breakdown on Analyze  
3. Deepen `/health` model check  
4. Unify LLM provider config  
5. Add real-prompt human eval for optimizer  
6. Remove dead code; fix weak tests  
