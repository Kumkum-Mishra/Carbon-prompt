# GreenPrompt AI — Technical Audit Guide Index

**Audit date:** 17 July 2026  
**Scope:** Full repository at project root (frontend, backend, training, models, datasets)  
**Method:** Source-code inspection, formula recalculation, pytest/Jest execution — no assumptions accepted without verification  

## Deliverables

| # | Document | File |
|---|----------|------|
| 1 | Complete Technical Audit Report | [01_Complete_Technical_Audit_Report.md](./01_Complete_Technical_Audit_Report.md) |
| 2 | Frontend Architecture Document | [02_Frontend_Architecture.md](./02_Frontend_Architecture.md) |
| 3 | Backend Architecture Document | [03_Backend_Architecture.md](./03_Backend_Architecture.md) |
| 4 | Prompt Optimization Documentation | [04_Prompt_Optimization.md](./04_Prompt_Optimization.md) |
| 5 | Carbon Prediction Documentation | [05_Carbon_Prediction.md](./05_Carbon_Prediction.md) |
| 6 | Model Recommendation Documentation | [06_Model_Recommendation.md](./06_Model_Recommendation.md) |
| 7 | Mathematical Verification Report | [07_Mathematical_Verification.md](./07_Mathematical_Verification.md) |
| 8 | Full Project Flow Document | [08_Full_Project_Flow.md](./08_Full_Project_Flow.md) |
| 9 | Flowcharts (all modules) | [09_Flowcharts.md](./09_Flowcharts.md) |
| 10 | Complete Testing Report | [10_Complete_Testing_Report.md](./10_Complete_Testing_Report.md) |
| 11 | Bug Report | [11_Bug_Report.md](./11_Bug_Report.md) |
| 12 | Code Quality Report | [12_Code_Quality_Report.md](./12_Code_Quality_Report.md) |
| 13 | Final Project Documentation | [13_Final_Project_Documentation.md](./13_Final_Project_Documentation.md) |

## Executive Verdict (one paragraph)

GreenPrompt AI’s **runtime calculations are real and deterministic**: Green Carbon Score (GCS), token/carbon reduction percentages, and GMES ranking are implemented in code and match hand calculation. Prompt analysis uses **tiktoken** plus rule-based classifiers (not hardcoded display numbers). Prompt optimization defaults to a **fine-tuned FLAN-T5-small** model with beam search — not a placeholder string generator. Recommendation scores come from **`model_data.csv`**. However: carbon scores are a **relative index** (not measured CO₂); training labels are **synthetic/rule-based** so published BLEU/ROUGE metrics are inflated; the Mathematics/Datasets pages are **static documentation**; and the Home page contains **marketing numbers that conflict** with the datasets page.

## Test Snapshot

| Suite | Result |
|-------|--------|
| Backend pytest | **224 passed** |
| Frontend Jest | **16 passed** (10 suites) |
| Manual GCS recalculation | **All MATCH** |
| Dataset JSON vs CSV | **MATCH** (1000 prompts, avg tokens 46.98, 770 models) |
