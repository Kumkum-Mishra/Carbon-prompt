# 10 — Complete Testing Report

**Audit date:** 17 July 2026

---

## 1. Automated Suite Results

| Suite | Command | Result |
|-------|---------|--------|
| Backend | `pytest analyzer/tests carbon/tests recommendation/tests optimizer/tests tests/ -q` | **224 passed** in ~3s |
| Frontend | `npm test` | **10 suites / 16 tests passed** |

---

## 2. Prompt Analysis Testing

| Case | Input | Observed | Expected | Pass? |
|------|-------|----------|----------|-------|
| Normal QA | `What is the capital of Japan?` | 29 chars, 6 words, 7 tokens, Zero-shot / Question Answering | Real counts + heuristic type | Pass |
| Verbose | neural network explain prompt | 66 chars, 12 words, 13 tokens, Zero-shot / QA | Real | Pass |
| Coding CoT-ish | linked list + “step by step” | Coding classified | Heuristic | Pass |
| Persona + code | “You are a senior engineer…” | Persona Prompting / Coding | Pass |
| Translation long | “Translate to French…” ×50 | Translation, 300 tokens | Pass |
| Special chars | `!!!@@@###` | 9 chars, 4 tokens, General | Pass |
| Code snippet | `def foo():…` | General (no strong coding keyword hit) | Acceptable classifier limit | Note |
| Empty string | `""` | Analyzer returns zeros / Zero-shot General | Route requires min 2 chars | Service vs route gap |
| Single char | `"a"` | Accepted by analyzer service | Route min length 2 | Gap |

**Conclusion:** Counts are computed, not hardcoded. Classification is regex-based and imperfect on edge code without keywords.

---

## 3. Prompt Optimization Testing

| Area | Result |
|------|--------|
| Unit tests (ranking, reduction, routes, mock provider) | Covered in 224 pytest |
| Default provider | `trained_model` |
| Mock provider | Test-only fixed strings |
| Demo JSON | Real model outputs (politeness stripping) |
| Live model E2E in CI | Not observed as mandatory test (slow/heavy) |

**Edge:** If generation yields no unique candidates, provider returns original prompt (silent no-op).

---

## 4. Carbon Calculation Testing

| Test | Result |
|------|--------|
| Formula unit tests in `carbon/tests` | Pass (part of 224) |
| Manual 9×1.0×1.4×1e-5 | 0.000126 MATCH |
| Manual 24×1.0×1.2×1e-5 | 0.000288 MATCH |
| Manual 26×1.2×1.6×1e-5 | 0.000499 MATCH |
| Manual 100×1.5×1.5×1e-5 | 0.00225 MATCH |
| token_count 0 / negative / bool | Raises InvalidTokenCountError |
| Unknown prompt/task type | Errors (YAML lookup) |

**No fake numbers detected.**

---

## 5. Model Recommendation Testing

| Test | Result |
|------|--------|
| Unit tests normalizers/scorer/ranking | Pass |
| Coding smoke | Top: Grok 4.20 Beta Non-reasoning, score 80.35 |
| Determinism | Same inputs → same ranking |
| Dataset size | 770 models MATCH JSON |

---

## 6. Frontend Testing

Covered: FormulaCard, wordDiff, api service, Navbar, PromptInput, CarbonCard, RecommendationCard, legacy Analysis/Optimization cards.

**Gaps:** ResultsPanel, useProcessPrompt, PipelineLoader, Datasets page, Mathematics integration, health check usage, E2E browser flow.

---

## 7. API / Integration

| Endpoint | Test coverage |
|----------|---------------|
| `/health` | Integration tests present |
| `/process` | Integration with mock optimizer |
| Module routes | Present per module |
| Live trained model in `/process` | Not required in default pytest path |

---

## 8. Edge Case Matrix

| Scenario | Analysis | Optimize | Carbon | Recommend |
|----------|----------|----------|--------|-----------|
| Empty prompt | Service soft; route 400 | Route 400 | Route 400 | Route 400 |
| Very long (within 10k) | Works | May be slow on CPU model | Works | Works |
| Over max length | 400 | 400 | 400 | N/A |
| Special characters | Tokenizes | May little-change | Works | Via task |
| Programming | Often Coding | Depends on model | Higher Wt | coding models |
| Reasoning / CoT keywords | May shift types | Type-change penalties in rank | Weights may change | Category map |
| Few-shot patterns | Prompt-type classifier | Same | Higher Wp | — |

---

## 9. Validation Methodology Used in Audit

1. Static code review of formulas and data flow  
2. Hand recalculation vs function output  
3. CSV vs frontend JSON reconciliation  
4. Full pytest + Jest execution  
5. Recommendation smoke ranking printout  

---

## 10. Overall Testing Verdict

Core math and backend modules are **well tested and consistent**. Frontend unit coverage is **narrow but green**. Highest residual risk: **untested live model inference performance/quality** in automated CI and **marketing page consistency** (not covered by tests).
