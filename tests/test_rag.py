from langchain_core.documents import Document

from app.rag.generator import RAGGenerator


def test_generator_rejects_empty_question():
    generator = RAGGenerator.__new__(RAGGenerator)

    try:
        generator.generate("", [])
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Question cannot be empty." in str(exc)


def test_generator_handles_no_documents():
    generator = RAGGenerator.__new__(RAGGenerator)

    result = generator.generate(
        "What is RAG?",
        [],
    )

    assert (
        result
        == "I could not find the answer in the provided source."
    )