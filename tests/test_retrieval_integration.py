from app.processing.chunker import DocumentChunker
from app.retrieval.retriever import Retriever
from app.schemas.document import DocumentMetadata, SourceDocument
from app.vectorstore.chroma_store import ChromaVectorStore


def test_real_retrieval_pipeline():
    source_document = SourceDocument(
        document_id="retrieval-test-001",
        content=(
            "Retrieval augmented generation combines "
            "information retrieval with a language model. "

            "A retrieval system searches a knowledge base "
            "to find information relevant to a user's question. "

            "The retrieved information is then provided to "
            "a language model as context for generating an answer. "

            "This approach can help a language model answer "
            "questions using information from external sources."
        ),
        metadata=DocumentMetadata(
            document_id="retrieval-test-001",
            source_type="pdf",
            source="retrieval_test.pdf",
            title="Retrieval Test",
        ),
    )

    chunker = DocumentChunker(
        chunk_size=180,
        chunk_overlap=30,
    )

    chunks = chunker.chunk(source_document)

    vector_store = ChromaVectorStore(
        collection_name="retrieval_integration_test",
    )

    vector_store.add_documents(chunks)

    retriever = Retriever(
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        "How does retrieval augmented generation use external information?"
    )

    assert len(results) > 0

    combined_text = " ".join(
        document.page_content
        for document in results
    ).lower()

    assert "retrieval" in combined_text
    assert "information" in combined_text