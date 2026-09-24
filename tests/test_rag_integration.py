from langchain_core.documents import Document

from app.rag.generator import RAGGenerator


def test_rag_generation():
    documents = [
        Document(
            page_content=(
                "Retrieval augmented generation combines "
                "information retrieval with a language model. "
                "The retrieval system finds relevant information "
                "from an external knowledge base and provides "
                "that information to the language model."
            ),
            metadata={
                "document_id": "rag-test-001",
                "source_type": "pdf",
                "source": "rag_test.pdf",
                "chunk_index": 0,
            },
        )
    ]

    generator = RAGGenerator()

    answer = generator.generate(
        question="What does retrieval augmented generation combine?",
        documents=documents,
    )

    assert answer
    assert "retrieval" in answer.lower()
    assert "language model" in answer.lower()