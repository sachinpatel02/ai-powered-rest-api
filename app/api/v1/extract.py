from json import JSONDecodeError
from fastapi import APIRouter, HTTPException, status
from google.genai import types
import json

from app.core.config import settings
from app.core.gemini import client

from app.schemas.requests import ExtractRequest
from app.schemas.responses import ExtractResponse
from app.prompt.templates import EXTRACT_SYSTEM_PROMPT

router = APIRouter()


async def _call_gemini_extract(text: str) -> ExtractResponse:
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=EXTRACT_SYSTEM_PROMPT,
            temperature=settings.temperature,
            max_output_tokens=settings.max_output_tokens,
            response_mime_type="application/json",
            response_schema=ExtractResponse,
        )
    )
    data = json.loads(response.text)
    return ExtractResponse(**data)


@router.post("/extract", response_model=ExtractResponse,
             summary="Extract named entities",
             response_description="All named entities found in the text"
             )
async def extract_text(request: ExtractRequest):
    """
        Extract all named entities from the provided text.

        Identifies and classifies the following entity types:
        - **PERSON** — people and public figures
        - **ORGANIZATION** — companies, institutions, agencies
        - **LOCATION** — cities, countries, landmarks
        - **DATE** — dates, times, periods
        - **PRODUCT** — products, software, services
        - **EVENT** — named events, conferences, incidents
        - **OTHER** — any other notable named entity

        Useful for knowledge extraction, document indexing, and
        automated metadata generation.
        """
    try:
        return await _call_gemini_extract(request.text)
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Model returned invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
