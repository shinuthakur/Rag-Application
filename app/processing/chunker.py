from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.schemas.document import DocumentMetadata, SourceDocument


class DocumentChunker:
    """
    Split a SourceDocument into smaller documents suitable
    for embedding and retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def chunk(
        self,
        document: SourceDocument,
    ) -> list[SourceDocument]:
        """
        Split a SourceDocument into smaller SourceDocuments.
        """

        chunks = self.splitter.split_text(document.content)

        chunked_documents = []

        for index, chunk_text in enumerate(chunks):
            metadata = DocumentMetadata(
                document_id=document.document_id,
                source_type=document.metadata.source_type,
                source=document.metadata.source,
                title=document.metadata.title,
                chunk_index=index,
                page=document.metadata.page,
                timestamp_start=document.metadata.timestamp_start,
                timestamp_end=document.metadata.timestamp_end,
                extra=document.metadata.extra.copy(),
            )

            chunked_documents.append(
                SourceDocument(
                    document_id=document.document_id,
                    content=chunk_text,
                    metadata=metadata,
                )
            )

        return chunked_documents