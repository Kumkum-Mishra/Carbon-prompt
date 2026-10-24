# 05 — Carbon Prediction Documentation

> This is the most critical module for viva/research honesty.

---

## 1. What “Carbon” Means Here

GreenPrompt does **not** measure physical CO₂ (grams, kWh, PUE, grid intensity).

It computes a **Green Carbon Score (GCS)** — a relative, unitless index proportional to token count and configured weights.

The Analyze UI tooltip correctly says GCS is relative, not measured CO₂.

---

## 2. Exact Formula (Source of Truth)

Implemented in `backend/carbon/calculator.py`:

\[
\text{GCS} = \mathrm{round}\big(T \times W_p \times W_t \times K,\ 6\big)
\]

Optional cap `MAX_GREEN_CARBON_SCORE` exists but is **`None`** (disabled).

### Variables

| Symbol | Name | Source |
|--------|------|--------|
| \(T\) | Token count | tiktoken `cl100k_base` (or provided integer) |
| \(W_p\) | Prompt weight | `carbon/config/prompt_weights.yaml` |
| \(W_t\) | Task weight | `carbon/config/task_weights.yaml` |
| \(K\) | Scaling constant | `SCALING_CONSTANT_K = 0.00001` in `carbon/constants.py` |

### Prompt weights

| Prompt type | Weight |
|-------------|--------|
| Zero-shot | 1.00 |
| One-shot | 1.10 |
| Few-shot | 1.20 |
| Chain of Thought | 1.50 |
| Role Prompting | 1.15 |
| Persona Prompting | 1.20 |
| Tree of Thought | 1.70 |
| ReAct | 1.60 |
| Structured Prompt | 1.25 |
| Other | 1.00 |

### Task weights

| Task type | Weight |
|-----------|--------|
| Coding | 1.40 |
| Mathematics | 1.50 |
| Reasoning | 1.60 |
| Writing | 1.20 |
| Summarization | 1.10 |
| Translation | 1.10 |
| Question Answering | 1.00 |
| Vision Analysis | 1.50 |
| Image Generation | 1.80 |
| Search | 1.20 |
| General | 1.00 |

Unknown types → error (no silent default).

---

## 3. Related Displayed Metrics

### Original / Optimized GCS
Computed twice in `/process`: once for original analysis fields, once for optimized tokens + optimized classified types.

### Token reduction %

\[
\frac{T_{\text{orig}} - T_{\text{opt}}}{T_{\text{orig}}} \times 100
\]

Rounded to 2 decimals (`optimizer/reduction.py`). Zero original → 0.0.

### Carbon reduction %

\[
\frac{C_{\text{orig}} - C_{\text{opt}}}{C_{\text{orig}}} \times 100
\]

If prompt/task type changes between original and optimized, carbon % can diverge from token % even with proportional token change (weights differ).

---

## 4. Manual Verification (Audit Execution)

| Tokens | Prompt | Task | Wp | Wt | Manual GCS | API GCS | Result |
|--------|--------|------|----|----|------------|---------|--------|
| 9 | Zero-shot | Coding | 1.0 | 1.4 | 0.000126 | 0.000126 | MATCH |
| 24 | Zero-shot | Writing | 1.0 | 1.2 | 0.000288 | 0.000288 | MATCH |
| 26 | Few-shot | Reasoning | 1.2 | 1.6 | 0.000499 | 0.000499 | MATCH |
| 100 | Chain of Thought | Mathematics | 1.5 | 1.5 | 0.00225 | 0.00225 | MATCH |

Mathematics page example `9 × 1.0 × 1.4 × 0.00001 = 0.000126` — **MATCH**.

Worked example `24 × 1.0 × 1.2 × 0.00001 = 0.000288` — **MATCH** arithmetically (task label “Explanation” is not a live backend type).

---

## 5. Fake / Random / Placeholder Check

| Check | Result |
|-------|--------|
| `random()` in carbon path | Not present |
| Hardcoded GCS in API | Not present |
| Weights from YAML | Static config (intentional) |
| K arbitrary scale | Yes — not physical units |
| Reference CSV `carbon/data/carbon_prompt_dataset.csv` | Formula-consistent; **not used at runtime** |

---

## 6. Frontend Display Mapping

| UI field | API field |
|----------|-----------|
| Before score | `pipeline.carbon.original.green_carbon_score` |
| After score | `pipeline.carbon.optimized.green_carbon_score` |
| Reduction % | `pipeline.optimization.carbon_reduction_percent` |

**Not shown in UI (but present in API):** `prompt_weight`, `task_weight`, `scaling_constant`, per-side token counts in CarbonCard.

**Potential inconsistency:** carbon scores come from pipeline re-estimate; reduction % comes from optimizer comparison object. They should match under normal conditions; both use the same calculator.

---

## 7. Service Flow

```
token_count + prompt_type + task_type
  → get_prompt_weight / get_task_weight
  → calculate_green_carbon_score
  → CarbonResult
```

Validation: token_count must be positive `int` (bool rejected).

---

## 8. Research Framing

**Correct claim:** “We define GCS as a multiplicative index of token load and prompting/task intensity weights.”

**Incorrect claim:** “The system measures carbon dioxide emissions of LLM inference.”

Weights encode domain assumptions (e.g. Image Generation 1.80 &gt; QA 1.00). They are research design choices, not measured emission factors.
