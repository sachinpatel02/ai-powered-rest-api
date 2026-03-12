from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000,
                      description="The text to analyze. Minimum 10 characters, maximum 5000.",
                      examples=["FastAPI is an amazing framework. I love building APIs with it every day."]
                      )


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000,
                      description="Text from which to extract named entities.",
                      examples=[
                          "Sundar Pichai, CEO of Google, announced a partnership with Samsung in Seoul on March 5th 2024."]
                      )


class QARequest(BaseModel):
    context: str = Field(..., min_length=10, max_length=5000,
                         description="The reference text the question should be answered from.",
                         examples=[
                             "FastAPI was created by Sebastián Ramírez in 2018. It is built on Starlette and Pydantic."]
                         )
    question: str = Field(..., min_length=10, max_length=500,
                          description="The question to answer based on the context.",
                          examples=["Who created FastAPI and when?"]
                          )


class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000,
                      description="The text to classify.",
                      examples=[
                          "I cannot reset my password and have been trying for 2 hours. This is very frustrating."]
                      )
    labels: list[str] = Field(..., min_length=2, max_length=10,
                              description="List of possible labels to classify into. Minimum 2 labels required.",
                              examples=[["technical_issue", "billing", "complaint", "general_inquiry"]]
                              )
