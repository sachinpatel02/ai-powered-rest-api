from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    sentiment: str  # "positive" | "negative" | "neutral"
    tone: str  # "formal" | "casual" | "aggressive" etc.
    summary: str  # 1-2 sentence summary
    readability: str  # "simple" | "moderate" | "complex"
    key_topics: list[str]  # up to 5 topics


class Entity(BaseModel):
    text: str  # the actual entity text
    type: str  # PERSON | DATE | LOCATION | ORG etc.


class ExtractResponse(BaseModel):
    entities: list[Entity]


class QAResponse(BaseModel):
    answer: str
    confidence: str  # "high" | "medium" | "low"
    found_in_context: bool  # did the answer come from context or model's own knowledge?


class ClassifyResponse(BaseModel):
    label: str  # the winning label
    confidence_score: float  # 0.0 - 1.0
    reasoning: str  # why this label was chosen — chain of thought output
