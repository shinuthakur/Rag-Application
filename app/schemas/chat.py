from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question about the ingested source.",
    )

    document_id: str = Field(
        ...,
        min_length=1,
        description="ID of the source the user is asking about.",
    )


class ChatResponse(BaseModel):
    answer: str