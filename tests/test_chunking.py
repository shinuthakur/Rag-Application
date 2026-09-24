from app.processing.chunker import DocumentChunker
from app.schemas.document import DocumentMetadata, SourceDocument


def create_test_document() -> SourceDocument:
    metadata = DocumentMetadata(
        document_id="test-doc-123",
        source_type="pdf",
        source="test.pdf",
        title="Test PDF",
    )

    return SourceDocument(
        document_id="test-doc-123",
        content=(
            "This is the first paragraph. "
            "It contains some information about the document.\n\n"
            "This is the second paragraph. "
            "It contains more information that should be split "
            "into smaller chunks when the document becomes large."
        ),
        metadata=metadata,
    )


def test_document_chunking():
    document = create_test_document()

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) > 1

    for index, chunk in enumerate(chunks):
        assert chunk.document_id == document.document_id
        assert chunk.metadata.document_id == document.document_id
        assert chunk.metadata.source_type == "pdf"
        assert chunk.metadata.source == "test.pdf"
        assert chunk.metadata.chunk_index == index
        assert chunk.content


def test_chunk_indices_are_sequential():
    document = create_test_document()

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.chunk(document)

    indices = [
        chunk.metadata.chunk_index
        for chunk in chunks
    ]

    assert indices == list(range(len(chunks)))