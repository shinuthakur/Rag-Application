from pydantic import BaseModel, Field


class IngestionRequest(BaseModel):
    source: str = Field(
        ...,
        min_length=1,
        description="PDF path, webpage URL, or YouTube URL.",
    )


class IngestionResponse(BaseModel):
    document_id: str
    source_type: str
    source: str
    title: str | None = None
    message: str