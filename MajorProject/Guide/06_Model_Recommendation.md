# 06 — Model Recommendation Documentation

---

## 1. Purpose

Given a task type (from analysis or explicit input), recommend the best LLM(s) from `model_data.csv` using the **Green Model Efficiency Score (GMES)**.

---

## 2. Dataset

| Item | Value |
|------|-------|
| File | `model_data.csv` (project root) |
| Rows | 770 |
| Columns | `full_name_of_model`, `category`, `speed`, `latency`, `context`, `input_cost`, `output_cost` |
| Categories | text 291, coding 286, vision 85, image 73, search 35 |

Verified against `frontend/data/dataset-stats.json` during audit — counts MATCH.

---

## 3. Category Mapping

Analyzer task types map to CSV categories (`recommendation/config.py`):

| Task type | Category filter |
|-----------|-----------------|
| Coding | coding |
| Mathematics | math (fallback coding) |
| Writing / Summarization / Translation / QA / Reasoning / General | text |
| Image Generation | image (fallback text) |
| Vision Analysis | vision |
| Search | search |

---

## 4. Metric Parsing

| Field | Example | Parse |
|-------|---------|-------|
| speed | `56 tps` | first float |
| latency | `1.6s` | first float |
| context | `200K` | amount × K/M/B |
| cost | `$5.00` | strip `$`, float |
| null | `null` | missing |

Rows need a model name + at least one parseable metric.

---

## 5. Normalization (0–100)

Higher-is-better (speed, context, raw costs before efficiency flip):

\[
100 \times \frac{v - \min}{\max - \min}
\]

Lower-is-better (latency):

\[
100 \times \frac{\max - v}{\max - \min}
\]

If all equal → 100. Missing → imputed **50.0**.

---

## 6. Scoring Formulas

### Cost Efficiency

\[
\text{CostEfficiency} = 100 - \frac{\text{input\_cost\_norm} + \text{output\_cost\_norm}}{2}
\]

(Inputs are already normalized expense scores: higher = more expensive.)

### GMES

\[
\text{GMES} = \frac{\text{Speed} + \text{Latency} + \text{Context} + \text{CostEfficiency}}{4}
\]

All four terms are 0–100 normalized scores (latency score is higher when raw latency is lower).

---

## 7. Ranking Algorithm

Sort key (descending priority):
1. GMES
2. Cost efficiency
3. Speed
4. Context
5. Model name (alphabetical)

Return top **N = 5**.

**No randomness.** Same CSV + same category → same ranking.

### Audit smoke test (Coding)

| Rank | Model | GMES (score) |
|------|-------|--------------|
| 1 | Grok 4.20 Beta Non-reasoning | 80.35 |
| 2 | Grok 4.1 Fast Non-Reasoning | 78.73 |
| 3 | Grok 4 Fast Non-Reasoning | 78.38 |
| 4 | Grok 4 Fast Reasoning | 77.84 |
| 5 | Llama 3.1 8B Turbo | 76.46 |

Why #1 over #2: higher composite GMES (primarily stronger normalized speed while keeping excellent latency/context/cost).

---

## 8. Reason Generation

Template heuristics (`reason_generator.py`):
- Always includes “Highest overall GMES”
- Adds up to 3 more if top model ties category max on speed/latency/context/cost_efficiency
- Not personalized NLP

Frontend shows only first **2** reasons.

---

## 9. API

`POST /recommend` with prompt or task_type → `RecommendationService`.

In `/process`, recommendation uses **optimized** task type.

---

## 10. Limitations

1. Dataset completeness/accuracy of vendor metrics is external.
2. Missing metrics → 50.0 can distort ranking.
3. Math/Image fallbacks may recommend adjacent-domain models.
4. GMES equal-weights four axes — no learned preference.
5. No live API pricing refresh.

---

## 11. Verdict

Recommendations are **data-driven and deterministic**. They are not random. They are only as trustworthy as `model_data.csv` and the equal-weight GMES design.
