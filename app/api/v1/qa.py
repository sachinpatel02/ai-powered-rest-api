from json import JSONDecodeError
from fastapi import APIRouter, HTTPException, status
from google.genai import types
import json
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.gemini import client

from app.schemas.requests import QARequest
from app.schemas.responses import QAResponse
from app.prompt.templates import QA_SYSTEM_PROMPT

router = APIRouter()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
async def _call_gemini_qa(context: str, question: str) -> QAResponse:
    message = f"context: {context}, question: {question}"
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=message,
        config=types.GenerateContentConfig(
            system_instruction=QA_SYSTEM_PROMPT,
            temperature=settings.temperature,
            max_output_tokens=settings.max_output_tokens,
            response_mime_type="application/json",
            response_schema=QAResponse,
        )
    )
    data = json.loads(response.text)
    return QAResponse(**data)


@router.post("/qa", response_model=QAResponse,
             summary="Answer a question from context",
             response_description="Answer grounded in the provided context"
             )
async def qa(request: QARequest):
    """
        Answer a question strictly based on the provided context.

        Key behaviors:
        - Answers are grounded in the context — model will not fabricate
        - `found_in_context` flag tells you if the answer came from context
          or the model's general knowledge
        - `confidence` reflects how clearly the answer appears in the text

        Ideal for document Q&A, support ticket resolution, and
        contract/policy question answering systems.
        """
    try:
        return await _call_gemini_qa(request.context, request.question)
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Model returned invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
