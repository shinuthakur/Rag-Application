
from typing import Any, Literal

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """
    Metadata associated with a source document/chunk.
    """

    document_id: str

    source_type: Literal[
        "pdf",
        "web",
        "youtube"
    ]

    source: str

    title: str | None = None

    chunk_index: int = 0

    page: int | None = None

    timestamp_start: float | None = None

    timestamp_end: float | None = None

    extra: dict[str, Any] = Field(
        default_factory=dict
    )


class SourceDocument(BaseModel):
    """
    Standard internal representation of any ingested source.
    """

    document_id: str

    content: str

    metadata: DocumentMetadata