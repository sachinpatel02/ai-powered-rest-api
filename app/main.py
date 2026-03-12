from fastapi import FastAPI
from app.api.v1 import analyze, classify, extract, qa

description = f"""
AI-powered text analysis API built with FastAPI and Google Gemini.
## Features
- **Analyze** — sentiment, tone, summary, readability, key topics
- **Extract** — named entity recognition (people, orgs, locations, dates)
- **Q&A** — answer questions grounded in provided context
- **Classify** — categorize text into any custom labels

## Notes
- All endpoints accept plain text input (max 5000 characters)
- Responses are structured JSON, validated with Pydantic
- Built with async throughout — safe for high concurrency
"""
app = FastAPI(
    title="AI Powered REST API for Text Analysis",
    description=description,
    version="1.0.0",
    contact={
        "name": "Sachin Patel",
        "url": "https://github.com/sachinpatel02/simple-auth-service"
    }
)

app.include_router(analyze.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(classify.router, prefix="/api/v1", tags=["Classification"])
app.include_router(extract.router, prefix="/api/v1", tags=["Extraction"])
app.include_router(qa.router, prefix="/api/v1", tags=["Q&A"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
