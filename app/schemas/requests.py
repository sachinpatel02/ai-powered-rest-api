from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)


class QARequest(BaseModel):
    context: str = Field(..., min_length=10, max_length=5000)
    question: str = Field(..., min_length=10, max_length=500)


class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000)
    labels: list[str] = Field(..., min_length=2, max_length=10)
