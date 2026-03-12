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


@router.post("/classify", response_model=ClassifyResponse,
             summary="Classify text into custom labels",
             response_description="The most appropriate label with confidence and reasoning"
             )
async def classify(request: ClassifyRequest):
    """
        Classify text into one of the caller-provided labels.

        Unlike hardcoded classifiers, this endpoint accepts any labels
        at runtime — making it reusable across completely different
        classification domains without any code changes.

        Returns:
        - **label** — the winning label from your provided list
        - **confidence_score** — 0.0 to 1.0
        - **reasoning** — one sentence chain-of-thought explanation

        Example use cases: support ticket routing, content categorization,
        intent detection, document tagging.
        """
    try:
        return await _call_gemini_classify(request.text, request.labels)
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Model returned invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
