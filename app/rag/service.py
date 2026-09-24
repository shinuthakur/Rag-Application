from langchain_core.documents import Document

from app.config import settings
from app.rag.generator import RAGGenerator
from app.retrieval.retriever import Retriever


class RAGService:
    """
    Orchestrates the complete question-answering pipeline.

    Question
        ↓
    Retriever
        ↓
    Relevant Documents
        ↓
    RAG Generator
        ↓
    Answer
    """

    def __init__(
        self,
        retriever: Retriever | None = None,
        generator: RAGGenerator | None = None,
    ):
        self.retriever = (
            retriever
            if retriever is not None
            else Retriever()
        )

        self.generator = (
            generator
            if generator is not None
            else RAGGenerator()
        )

    def ask(
        self,
        question: str,
        document_id: str | None = None,
    ) -> str:
        """
        Answer a question using retrieved information.

        If document_id is provided, retrieval is restricted
        to that specific ingested source.
        """

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        documents: list[Document] = (
            self.retriever.retrieve(
                query=question,
                document_id=document_id,
            )
        )

        answer = self.generator.generate(
            question=question,
            documents=documents,
        )

        return answer