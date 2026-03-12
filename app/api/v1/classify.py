from json import JSONDecodeError
from os.path import join

from fastapi import APIRouter, HTTPException, status
from google.genai import types
import json

from app.core.config import settings
from app.core.gemini import client

from app.schemas.requests import ClassifyRequest
from app.schemas.responses import ClassifyResponse
from app.prompt.templates import CLASSIFY_SYSTEM_PROMPT

router = APIRouter()

async def _call_gemini_classify(text: str, labels: list[str]) -> ClassifyResponse:
    l = " label: ".join(labels)
    message = f"text: {text}, List of labels: {l}"
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=message,
        config=types.GenerateContentConfig(
            system_instruction=CLASSIFY_SYSTEM_PROMPT,
            temperature=settings.temperature,
            max_output_tokens=settings.max_output_tokens,
            response_mime_type="application/json",
            response_schema=ClassifyResponse,
        )
    )
    data = json.loads(response.text)
    return ClassifyResponse(**data)

@router.post("/classify", response_model=ClassifyResponse)
async def classify(request: ClassifyRequest):
    try:
        return await _call_gemini_classify(request.text, request.labels)
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Model returned invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))