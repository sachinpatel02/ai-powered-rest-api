from json import JSONDecodeError

from fastapi import APIRouter, HTTPException, status
from google.genai import types
import json
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.gemini import client
from app.schemas.requests import AnalyzeRequest
from app.schemas.responses import AnalyzeResponse
from app.prompt.templates import ANALYZE_SYSTEM_PROMPT


router = APIRouter()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
async def _call_gemini_analyze(text: str) -> AnalyzeResponse:
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=ANALYZE_SYSTEM_PROMPT,
            temperature=settings.temperature,
            max_output_tokens=settings.max_output_tokens,
            response_mime_type="application/json",
            response_schema=AnalyzeResponse,
        )
    )
    data = json.loads(response.text)
    return AnalyzeResponse(**data)


@router.post("/analyze", response_model=AnalyzeResponse,
             summary="Analyze text",
             response_description="Structured analysis of the provided text"
             )
async def analyze_text(request: AnalyzeRequest):
    """
        Analyze a piece of text and return structured insights.

        Performs the following analysis:
        - **Sentiment** — positive, negative, or neutral
        - **Tone** — descriptive tone label (formal, casual, urgent, etc.)
        - **Summary** — concise 1-2 sentence summary
        - **Readability** — simple, moderate, or complex
        - **Key Topics** — up to 5 main topics identified

        Ideal for content moderation, customer feedback analysis, and
        automated content tagging pipelines.
        """
    try:
        return await _call_gemini_analyze(request.text)
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Model returned invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
