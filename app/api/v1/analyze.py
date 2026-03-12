from json import JSONDecodeError

from fastapi import APIRouter, HTTPException, status
from google.genai import types
import json

from app.core.config import settings
from app.core.gemini import client
from app.schemas.requests import AnalyzeRequest
from app.schemas.responses import AnalyzeResponse
from app.prompt.templates import ANALYZE_SYSTEM_PROMPT

router = APIRouter()


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

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    try:
        return await _call_gemini_analyze(request.text)
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Model returned invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
