# Carbon-prompt

Carbon-prompt is a carbon-aware prompt engineering framework for sustainable
large language model (LLM) inference. It analyzes prompts, estimates their
carbon impact, generates more efficient prompt alternatives, and recommends
models based on quality and sustainability criteria.

## Features

- Prompt analysis and metadata extraction
- Carbon and energy-impact estimation
- Sustainability-focused prompt optimization
- LLM recommendation and ranking
- End-to-end processing pipeline
- FastAPI REST backend
- Next.js dashboard frontend
- Automated backend and frontend tests

## Project Structure

```text
MajorProject/
├── backend/       # FastAPI application and processing pipeline
├── frontend/      # Next.js dashboard
├── Dataset/       # Datasets used by the application
├── training/      # Model-training scripts
└── build_optimization_dataset.py
```

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- npm

## Backend Setup

From the `MajorProject` directory:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example ..\.env
```

Start the API:

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API documentation is available at:

- http://localhost:8000/docs
- http://localhost:8000/redoc

Run backend tests:

```powershell
pytest -v
```

## Frontend Setup

In a second terminal, from the `MajorProject` directory:

```powershell
cd frontend
npm install
npm run dev
```

Open the dashboard at http://localhost:3000.

The frontend API URL can be configured with
`NEXT_PUBLIC_API_BASE_URL` in `frontend/.env.local`. The default backend URL
is `http://localhost:8000`.

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/health` | GET | Check application health |
| `/analyze` | POST | Analyze prompt metadata |
| `/carbon` | POST | Estimate carbon impact |
| `/optimize` | POST | Optimize a prompt |
| `/recommend` | POST | Recommend an LLM |
| `/process` | POST | Run the complete pipeline |

The `/process` endpoint runs prompt analysis, carbon estimation, optimization,
optimized-prompt estimation, and model recommendation in one request.

## Configuration

Copy `MajorProject/.env.example` to `MajorProject/.env` and adjust settings
for your environment. API keys must be kept local and must never be committed
to Git.

The trained model files are intentionally excluded from this repository because
of their size. To use the trained-model optimizer, place the model locally at
the path configured by `TRAINED_MODEL_PATH`, or select another supported
optimizer provider in `.env`.

## Repository Exclusions

Research documents, evaluation materials, experiments, paper files, guides,
large model artifacts, generated build files, dependencies, caches, and local
environment files are excluded through `.gitignore`.

## License

This project is provided for academic and research purposes.
