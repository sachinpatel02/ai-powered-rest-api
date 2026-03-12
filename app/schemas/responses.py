from pydantic import BaseModel, Field


class AnalyzeResponse(BaseModel):
    sentiment: str = Field(description="Overall sentiment: positive, negative, or neutral")
    tone: str = Field(description="Tone of the text e.g. formal, casual, urgent")
    summary: str = Field(description="1-2 sentence summary of the text")
    readability: str = Field(description="Readability level: simple, moderate, or complex")
    key_topics: list[str] = Field(description="Up to 5 key topics identified in the text")


class Entity(BaseModel):
    text: str = Field(description="The exact entity text as it appears")
    type: str = Field(description="Entity type: PERSON, ORGANIZATION, LOCATION, DATE, PRODUCT, EVENT, OTHER")


class ExtractResponse(BaseModel):
    entities: list[Entity] = Field(description="List of all named entities found in the text")


class QAResponse(BaseModel):
    answer: str = Field(description="Answer to the question")
    confidence: str = Field(description="Confidence level: high, medium, or low")
    found_in_context: bool = Field(description="True if answer is grounded in the provided context")


class ClassifyResponse(BaseModel):
    label: str = Field(description="The most appropriate label from the provided list")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0")
    reasoning: str = Field(description="One sentence explaining why this label was chosen")
