# 09 — Flowcharts for Every Module

All diagrams are Mermaid. They reflect **implemented** code paths.

---

## 1. Overall Project

```mermaid
flowchart LR
  subgraph UI[Frontend Next.js]
    Home
    Analyze
    Math[Mathematics]
    Data[Datasets]
  end
  subgraph API[Backend FastAPI]
    Process
    Modules[Analyzer Carbon Optimizer Recommend]
  end
  subgraph Assets[Assets]
    Model[FLAN-T5 fine-tune]
    CSV[model_data.csv]
    YAML[weight YAMLs]
  end
  Analyze -->|POST /process| Process
  Process --> Modules
  Modules --> Model
  Modules --> CSV
  Modules --> YAML
  Home -.->|static| Home
  Math -.->|static| Math
  Data -.->|static JSON| Data
```

---

## 2. Frontend Architecture

```mermaid
flowchart TB
  Layout[RootLayout + AppShell]
  Layout --> Nav[Navbar]
  Layout --> Pages
  Layout --> Footer
  Pages --> HomePage
  Pages --> AnalyzePage
  Pages --> MathPage
  Pages --> DatasetsPage
  AnalyzePage --> Hook[useProcessPrompt]
  Hook --> API[services/api.processPrompt]
  Hook --> Results[ResultsPanel]
  Results --> CarbonCard
  Results --> AnalysisOptCard
  Results --> RecCard[RecommendationCard]
```

---

## 3. Backend Architecture

```mermaid
flowchart TB
  App[app.py] --> R1[/analyze]
  App --> R2[/carbon]
  App --> R3[/optimize]
  App --> R4[/recommend]
  App --> R5[/process]
  App --> R6[/health]
  R5 --> PS[PipelineService]
  PS --> Registry[ModuleRegistry]
  Registry --> A[PromptAnalyzer]
  Registry --> C[CarbonService]
  Registry --> O[OptimizationService]
  Registry --> Rec[RecommendationService]
```

---

## 4. Prompt Analysis

```mermaid
flowchart TD
  In[Raw prompt] --> Clean[clean_prompt strip]
  Clean --> Tok[tiktoken cl100k_base count]
  Clean --> Task[classify_task regex]
  Clean --> PType[classify_prompt_type regex]
  Clean --> Chars[len cleaned]
  Clean --> Words[split word count]
  Tok --> Out[AnalysisResult]
  Task --> Out
  PType --> Out
  Chars --> Out
  Words --> Out
```

---

## 5. Prompt Optimization

```mermaid
flowchart TD
  P[Prompt] --> An[Analyze original]
  P --> Gen[Provider generate candidates]
  Gen --> TM[TrainedModelProvider beam=5]
  TM --> Cands[Unique candidates]
  Cands --> Loop[For each candidate]
  Loop --> ReAn[Re-analyze + carbon]
  ReAn --> Rank[ranking_engine score]
  Rank --> Filter{similarity ≥ 0.50 and constraints?}
  Filter -->|yes| Pool[Candidate pool]
  Filter -->|no| Drop[Reject]
  Pool --> Best[Select best score]
  Best --> Cmp[comparison + reduction %]
```

---

## 6. Carbon Calculation

```mermaid
flowchart TD
  T[token_count] --> Val{positive int?}
  Val -->|no| Err[InvalidTokenCountError]
  Val -->|yes| Wp[get_prompt_weight]
  PT[prompt_type] --> Wp
  TT[task_type] --> Wt[get_task_weight]
  Wp --> Mul[T × Wp × Wt × K]
  Wt --> Mul
  K[K=1e-5] --> Mul
  Mul --> Round[round 6 decimals]
  Round --> GCS[green_carbon_score]
```

---

## 7. Model Recommendation

```mermaid
flowchart TD
  Task[task_type] --> Map[category_mapper]
  Map --> Load[load model_data.csv filter]
  Load --> Parse[parse speed latency context costs]
  Parse --> Norm[min-max normalize 0-100]
  Norm --> CE[cost_efficiency]
  CE --> GMES[mean of 4 dims]
  GMES --> Sort[sort GMES CE speed context name]
  Sort --> Top5[top 5]
  Top5 --> Reasons[template reasons]
```

---

## 8. Training Pipeline

```mermaid
flowchart TD
  CSV1[prompts_dataset.csv] --> Build[build_optimization_dataset.py]
  Build --> CSV2[prompt_optimization_dataset.csv]
  CSV2 --> Split[80/10/10 seed 42]
  Split --> Tok[Tokenize + prefix]
  Tok --> Train[Seq2SeqTrainer 3 epochs]
  Train --> Save[models/greenprompt_model]
  Save --> Eval[finish_evaluation 40 samples]
  Eval --> Metrics[evaluation_metrics.json]
```

---

## 9. Inference Pipeline (Trained Model)

```mermaid
flowchart TD
  Text[User prompt] --> Pref[Prefix + text]
  Pref --> Enc[Tokenizer encode]
  Enc --> Gen[model.generate beams]
  Gen --> Dec[Batch decode]
  Dec --> Dedup[Deduplicate]
  Dedup --> Out[Candidate strings]
```

---

## 10. Dataset Flow

```mermaid
flowchart LR
  PD[prompts_dataset.csv] --> Build
  Build --> POD[prompt_optimization_dataset.csv]
  POD --> Train
  MD[model_data.csv] --> Rec[Recommendation]
  PD --> StatsJSON[dataset-stats.json manual snapshot]
  MD --> StatsJSON
  StatsJSON --> DatasetsPage
```

---

## 11. API Flow

```mermaid
sequenceDiagram
  participant U as Browser
  participant F as Next.js
  participant B as FastAPI
  participant M as Local Model
  participant C as CSV/YAML
  U->>F: Submit prompt
  F->>B: POST /process
  B->>B: Analyze
  B->>C: Load weights
  B->>B: GCS original
  B->>M: Beam generate
  B->>B: Rank + GCS optimized
  B->>C: Rank models
  B-->>F: ProcessSuccessResponse
  F-->>U: Cards + diff
```

---

## 12. User Flow

```mermaid
flowchart TD
  Start[Land on Home] --> Learn[Read problem / workflow]
  Learn --> Go[Go to Analyze]
  Go --> Type[Enter prompt]
  Type --> Wait[See loader steps]
  Wait --> View[View carbon / analysis / recommendation]
  View --> Diff[Inspect optimized prompt diff]
  View --> Math[Optional: Mathematics page]
  View --> Data[Optional: Datasets page]
```
