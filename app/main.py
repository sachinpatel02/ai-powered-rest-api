from fastapi import FastAPI
from app.api.v1 import analyze, classify, extract, qa

app = FastAPI(
    title="AI Powered REST API",
    description="AI Powered text analysis using Gemini.",
    version="1.0.0",
)

app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])
app.include_router(classify.router, prefix="/api/v1", tags=["classify"])
app.include_router(extract.router, prefix="/api/v1", tags=["extract"])
app.include_router(qa.router, prefix="/api/v1", tags=["qa"])

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}