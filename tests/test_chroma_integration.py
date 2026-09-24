from app.schemas.document import DocumentMetadata, SourceDocument
from app.processing.chunker import DocumentChunker
from app.vectorstore.chroma_store import ChromaVectorStore


def test_chunk_embedding_and_chroma_retrieval():
    source_document = SourceDocument(
        document_id="integration-test-001",
        content=(
            "Retrieval augmented generation combines "
            "information retrieval with a language model. "
            "The retrieval system finds relevant information "
            "from a knowledge base before generating an answer."
        ),
        metadata=DocumentMetadata(
            document_id="integration-test-001",
            source_type="pdf",
            source="integration_test.pdf",
            title="RAG Integration Test",
        ),
    )

    chunker = DocumentChunker(
        chunk_size=200,
        chunk_overlap=30,
    )

    chunks = chunker.chunk(source_document)

    assert len(chunks) > 0

    vector_store = ChromaVectorStore(
        collection_name="integration_test",
    )

    vector_store.add_documents(chunks)

    results = vector_store.similarity_search(
        "What is retrieval augmented generation?",
        k=1,
    )

    assert len(results) > 0

    result = results[0]

    assert "retrieval" in result.page_content.lower()
    assert "generation" in result.page_content.lower()

    assert (
        result.metadata["document_id"]
        == "integration-test-001"
    )