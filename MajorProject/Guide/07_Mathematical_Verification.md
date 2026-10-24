# 07 — Complete Mathematical Verification Report

---

## 1. Scope

Verify every formula shown on the Mathematics page against backend implementation and hand calculation. Confirm Analyze UI displays values from those formulas (not invented locally).

---

## 2. Formula 1 — Green Carbon Score

### Documented (`frontend/data/mathematics.ts`)

```
GCS = TokenCount × PromptWeight × TaskWeight × K
K = 0.00001
Example: 9 × 1.0 × 1.4 × 0.00001 = 0.000126
```

### Implemented (`backend/carbon/calculator.py` + `constants.py`)

```python
score = token_count * prompt_weight * task_weight * scaling_constant
return round(score, 6)  # SCORE_DECIMAL_PLACES = 6
# SCALING_CONSTANT_K = 0.00001
```

### Verification

| Check | Result |
|-------|--------|
| Symbol definitions | Match |
| Example arithmetic | Match |
| Backend vs hand calc (4 cases) | All MATCH |
| Units | Unitless index (documented correctly in Limitations) |

**Verdict: CORRECT**

---

## 3. Formula 2 — Token Reduction

### Documented

```
((OriginalTokens - OptimizedTokens) / OriginalTokens) × 100
Example: ((26 - 13) / 26) × 100 = 50.0%
```

### Implemented (`backend/optimizer/reduction.py`)

```python
round((original - optimized) / original * 100, 2)
# if original == 0 → 0.0
```

Hand: `(26-13)/26*100 = 50.0` — MATCH.

**Verdict: CORRECT**

---

## 4. Formula 3 — Carbon Reduction

### Documented

```
((OriginalCarbon - OptimizedCarbon) / OriginalCarbon) × 100
Example: ((0.00039 - 0.00021) / 0.00039) × 100 = 46.15%
```

### Implemented

Same structure as token reduction on carbon floats, 2 decimals.

Hand: `(0.00039-0.00021)/0.00039*100 = 46.1538… → 46.15` — MATCH.

**Verdict: CORRECT**

---

## 5. Formula 4 — GMES

### Documented

```
CostEfficiency = 100 - ((InputCost + OutputCost) / 2)
GMES = (Speed + Latency + Context + CostEfficiency) / 4
```

### Implemented (`backend/recommendation/scorer.py`)

Identical arithmetic on **normalized** 0–100 metric scores.

PRD-style check: CE from (80,70) → 25.0; GMES (90+88+100+25)/4 = 75.75 — wait, earlier audit said 74.25 with CE from 80/70:

`(80+70)/2 = 75`; `100-75 = 25`; `(90+88+100+25)/4 = 75.75`.

Audit agent example used CE=19 for GPT-like → different inputs. Formula itself MATCHES docs.

**Verdict: CORRECT** (inputs must be normalized scores, which Mathematics page implies via variable names Speed/Latency/Context).

---

## 6. Worked Example Audit

Source: `data/mathematics.ts` worked example.

| Step | Claim | Math | Notes |
|------|-------|------|-------|
| GCS | 24×1.0×1.2×1e-5=0.000288 | OK | Task labeled Explanation — not in backend taxonomy |
| Token red | 50% | OK | Illustrative |
| Carbon red | 50% | OK if weights unchanged | |
| GMES | 86.25 from (92+90+88+75)/4 | OK | Illustrative numbers |

**Frontend/backend live match:** formulas match; example labels are pedagogical.

---

## 7. Analyze Page — Display vs Formula

| Displayed number | Computed where | Matches formula? |
|------------------|----------------|------------------|
| Token count | Backend analyzer | Yes (tiktoken) |
| GCS before/after | Backend carbon | Yes |
| Token reduction % | Backend reduction | Yes |
| Carbon reduction % | Backend reduction | Yes |
| GMES / model score | Backend scorer | Yes |

Frontend only formats; does not alter formula results (except display rounding for GCS ≥ 0.001 → 4 decimals).

---

## 8. Datasets Page Averages

| Metric | JSON | CSV recompute | Result |
|--------|------|---------------|--------|
| totalPrompts | 1000 | 1000 | MATCH |
| averageTokenCount | 46.98 | 46.98 | MATCH |
| totalModels | 770 | 770 | MATCH |
| category counts | Text/Coding/… | Counter match | MATCH |

averageCarbonScore 0.000108 is a **precomputed snapshot** in JSON (not recomputed by frontend at runtime). Not a live formula call — acceptable for a static page if regenerated when data changes.

---

## 9. Scaling & Units Summary

| Quantity | Unit | Scaling |
|----------|------|---------|
| GCS | unitless | ×1e-5 |
| Reduction | percent | ×100 |
| GMES | 0–100 score | min-max then mean |
| Costs in GMES path | normalized then inverted for efficiency | |

---

## 10. Mismatches Found

| Item | Severity | Detail |
|------|----------|--------|
| Task “Explanation” on Math page | Minor/Medium | Not a live classifier label |
| Home Hero numbers vs Math worked example | Major | Marketing inconsistency |
| Home 10,000+ vs Datasets 1,000 | Major | Different meanings not clarified |
| Analyze hides Wp/Wt/K | Medium | Docs show factors; UI shows final only |
| Dual carbon fields in response | Low | Scores from `carbon.*`, % from `optimization.*` |

No formula implementation bugs found in calculator/scorer/reduction.
