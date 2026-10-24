# GreenPrompt AI Backend

Green AI and Sustainable Prompt Engineering System — unified REST API backend.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env
```

## Run the Server

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or:

```bash
python main.py
```

## Run Tests

```bash
cd backend
pytest -v
```

## API Documentation

When the server is running:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/analyze` | POST | Analyze prompt metadata |
| `/carbon` | POST | Estimate Green Carbon Score |
| `/optimize` | POST | Optimize prompt for sustainability |
| `/recommend` | POST | Recommend best LLM |
| `/process` | POST | Run complete pipeline |
| `/health` | GET | Application health check |

## Complete Pipeline

`POST /process` executes:

1. Prompt Analyzer (original)
2. Carbon Estimation (original)
3. Prompt Optimization with the local trained model
4. Carbon Estimation (optimized)
5. Model Recommendation

The optimizer flow is:

1. Generate 3-5 candidate rewrites with `models/greenprompt_model`
2. Reject candidates that lose explicit constraints or drift too far from the original meaning
3. Estimate carbon for valid candidates
4. Rank by semantic similarity, token reduction, readability, and carbon reduction
5. Return the best prompt to the dashboard

## Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `APP_NAME` | GreenPrompt AI | Application name |
| `APP_VERSION` | 1.0.0 | Application version |
| `ENVIRONMENT` | development | Environment name |
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 8000 | Server port |
| `LOG_LEVEL` | INFO | Logging level |
| `LLM_PROVIDER` | trained_model | Optimizer provider (`trained_model`, `rule_based`, `openai`, `anthropic`, `gemini`, `mock`) |
| `TRAINED_MODEL_PATH` | models/greenprompt_model | Local fine-tuned FLAN-T5 model directory |
| `TRAINED_MODEL_DEVICE` | auto | `auto`, `cpu`, `mps`, or `cuda` |
| `OPTIMIZER_NUM_CANDIDATES` | 5 | Number of optimized candidates to generate/rank |
| `OPTIMIZER_NUM_BEAMS` | 5 | Beam-search width for candidate generation |
| `SEMANTIC_SIMILARITY_THRESHOLD` | 0.50 | Minimum similarity required before ranking |
| `OPENAI_API_KEY` | — | OpenAI API key |
| `ANTHROPIC_API_KEY` | — | Anthropic API key |
| `GOOGLE_API_KEY` | — | Google Gemini API key |
| `MAX_PROMPT_LENGTH` | 10000 | Maximum prompt length |
| `CORS_ORIGINS` | * | Allowed CORS origins |

See `.env.example` in the project root for the full list.

## Project Structure

```
backend/
├── app.py                 # FastAPI application
├── main.py                # Entry point
├── config.py              # Environment configuration
├── routes/                # Gateway routes (/process, /health)
├── services/              # Pipeline orchestration
├── schemas/               # Shared response schemas
├── utils/                 # Logging, errors, timing
├── analyzer/              # PRD 1
├── carbon/                # PRD 2
├── optimizer/             # PRD 3
├── recommendation/        # PRD 4
├── logs/                  # Application logs
└── tests/                 # Gateway tests
```
