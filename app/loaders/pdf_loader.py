import uuid
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from app.loaders.base_loader import BaseLoader
from app.schemas.document import (
    DocumentMetadata,
    SourceDocument,
)


class PDFLoader(BaseLoader):
    """
    Loader for PDF documents.
    """

    def load(self, source: str) -> SourceDocument:
        """
        Load a PDF and convert it into a SourceDocument.
        """

        file_path = Path(source)

        if not file_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {source}"
            )

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(
                "The supplied file is not a PDF."
            )

        loader = PyPDFLoader(str(file_path))

        pages = loader.load()

        if not pages:
            raise ValueError(
                "The PDF contains no readable content."
            )

        content_parts = []

        for page in pages:
            content_parts.append(page.page_content)

        content = "\n\n".join(content_parts)

        document_id = str(uuid.uuid4())

        metadata = DocumentMetadata(
            document_id=document_id,
            source_type="pdf",
            source=str(file_path),
            title=file_path.name,
        )

        return SourceDocument(
            document_id=document_id,
            content=content,
            metadata=metadata,
        )