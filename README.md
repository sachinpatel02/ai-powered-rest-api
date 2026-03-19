# Text Intelligence API -- Multi-endpoint NLP Service

An async REST API for AI-powered text analysis built with **FastAPI** and **Google Gemini**.
Provides structured NLP capabilities via clean, documented endpoints — production-ready
with retry logic, Pydantic validation, and full test coverage.

---

## Features

| Endpoint | Description |
|---|---|
| `POST /api/v1/analyze` | Sentiment, tone, summary, readability, key topics |
| `POST /api/v1/extract` | Named entity recognition (people, orgs, locations, dates) |
| `POST /api/v1/qa` | Question answering grounded in provided context |
| `POST /api/v1/classify` | Dynamic text classification into caller-provided labels |

---

## Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — async Python web framework
- **[Google Gemini](https://ai.google.dev/)** — LLM for all inference
- **[Pydantic](https://docs.pydantic.dev/)** — request/response validation and structured outputs
- **[Tenacity](https://tenacity.readthedocs.io/)** — retry logic with exponential backoff
- **[pytest](https://pytest.org/) + [httpx](https://www.python-httpx.org/)** — async test suite

---

## Project Structure
```
text-intelligence-api/
├── app/
│   ├── main.py                  # FastAPI app, router registration
│   ├── core/
│   │   ├── config.py            # Settings via pydantic-settings
│   │   └── gemini.py            # Gemini client (single instance)
│   ├── api/
│   │   └── v1/
│   │       ├── analyze.py
│   │       ├── extract.py
│   │       ├── qa.py
│   │       └── classify.py
│   ├── schemas/
│   │   ├── requests.py          # Pydantic input models
│   │   └── responses.py         # Pydantic output models
│   └── prompts/
│       └── templates.py         # All system prompts
├── tests/
│   ├── conftest.py
│   ├── test_analyze.py
│   ├── test_extract.py
│   ├── test_qa.py
│   └── test_classify.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- Google Gemini API key — get one free at [aistudio.google.com](https://aistudio.google.com)

### Installation
```bash
# Clone the repo
git clone https://github.com/sachinpatel02/ai-powered-rest-api
cd ai-powered-rest-api

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Running the API
```bash
uvicorn app.main:app --reload
```

API is now running at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## API Usage

### Analyze Text
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI is an amazing framework. I love building APIs with it every day."}'
```
```json
{
  "sentiment": "positive",
  "tone": "enthusiastic",
  "summary": "The author expresses strong appreciation for FastAPI as a framework for building APIs.",
  "readability": "simple",
  "key_topics": ["FastAPI", "APIs", "web frameworks"]
}
```

### Extract Entities
```bash
curl -X POST http://localhost:8000/api/v1/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "Sundar Pichai, CEO of Google, announced a partnership with Samsung in Seoul on March 5th 2024."}'
```
```json
{
  "entities": [
    {"text": "Sundar Pichai", "type": "PERSON"},
    {"text": "Google", "type": "ORGANIZATION"},
    {"text": "Samsung", "type": "ORGANIZATION"},
    {"text": "Seoul", "type": "LOCATION"},
    {"text": "March 5th 2024", "type": "DATE"}
  ]
}
```

### Question Answering
```bash
curl -X POST http://localhost:8000/api/v1/qa \
  -H "Content-Type: application/json" \
  -d '{
    "context": "FastAPI was created by Sebastián Ramírez in 2018. It is built on Starlette and Pydantic.",
    "question": "Who created FastAPI and when?"
  }'
```
```json
{
  "answer": "FastAPI was created by Sebastián Ramírez in 2018.",
  "confidence": "high",
  "found_in_context": true
}
```

### Classify Text
```bash
curl -X POST http://localhost:8000/api/v1/classify \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I cannot reset my password and have been trying for 2 hours.",
    "labels": ["technical_issue", "billing", "complaint", "general_inquiry"]
  }'
```
```json
{
  "label": "technical_issue",
  "confidence_score": 0.85,
  "reasoning": "The user describes a login/password problem which is a technical issue."
}
```

---

## Running Tests
```bash
pytest tests/ -v
```

---

## Environment Variables

| Variable | Required | Default            | Description |
|---|---|--------------------|---|
| `GEMINI_API_KEY` | Yes | —                  | Your Google Gemini API key |
| `GEMINI_MODEL` | No | `gemini-2.5-flash` | Gemini model to use |
| `TEMPERATURE` | No | `0.3`              | Model temperature (0.0–1.0) |
| `MAX_OUTPUT_TOKENS` | No | `1024`             | Max tokens per response |

---

## Design Decisions

**Prompts as templates** — All system prompts live in `prompts/templates.py` rather than inline in routes. This makes them easy to iterate, version, and test independently.

**Single Gemini client** — Initialized once in `core/gemini.py` and reused across all requests, same pattern as a database connection pool.

**Structured outputs** — Responses use `response_schema` with Pydantic models, guaranteeing valid JSON structure rather than relying on prompt instructions alone.

**Retry with backoff** — All Gemini calls are wrapped with `tenacity` for automatic retry on rate limits and transient failures.

---

## License

MIT
