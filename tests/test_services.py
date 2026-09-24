from app.rag.service import RAGService
from app.services.ingestion_service import IngestionService
from app.schemas.document import (
    DocumentMetadata,
    SourceDocument,
)


class FakeChunker:
    def chunk(self, document):
        return [document]


class FakeVectorStore:
    def __init__(self):
        self.documents = []

    def add_documents(self, documents):
        self.documents.extend(documents)


class FakeLoader:
    def load(self, source):
        return SourceDocument(
            document_id="test-service-001",
            content="Test document content.",
            metadata=DocumentMetadata(
                document_id="test-service-001",
                source_type="web",
                source=source,
                title="Test Document",
            ),
        )


class FakeRetriever:
    def retrieve(self, question):
        return []


class FakeGenerator:
    def generate(self, question, documents):
        return "Test answer."


def test_ingestion_service():
    service = IngestionService(
        chunker=FakeChunker(),
        vector_store=FakeVectorStore(),
    )

    # Replace detection/loader later with dependency injection.
    # This test focuses on the service structure.
    assert service.chunker is not None
    assert service.vector_store is not None


def test_rag_service():
    service = RAGService(
        retriever=FakeRetriever(),
        generator=FakeGenerator(),
    )

    answer = service.ask(
        "What is this document about?"
    )

    assert answer == "Test answer."