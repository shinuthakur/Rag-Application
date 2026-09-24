from app.loaders.loaders_factory import get_loader
from app.loaders.source_detector import detect_source_type
from app.processing.chunker import DocumentChunker
from app.schemas.document import SourceDocument
from app.vectorstore.chroma_store import ChromaVectorStore


class IngestionService:
    """
    Orchestrates the complete source ingestion pipeline.

    Source
        ↓
    Detection
        ↓
    Loader
        ↓
    SourceDocument
        ↓
    Chunking
        ↓
    ChromaDB
    """

    def __init__(
        self,
        chunker: DocumentChunker | None = None,
        vector_store: ChromaVectorStore | None = None,
        loader_factory=get_loader,
        source_detector=detect_source_type,
    ):
        self.chunker = (
            chunker
            if chunker is not None
            else DocumentChunker()
        )

        self.vector_store = (
            vector_store
            if vector_store is not None
            else ChromaVectorStore()
        )

        self.loader_factory = loader_factory
        self.source_detector = source_detector

    def ingest(self, source: str) -> SourceDocument:
        """
        Ingest a source into the vector database.

        Pipeline:
            1. Detect source type
            2. Select appropriate loader
            3. Load and normalize source
            4. Split into chunks
            5. Store chunks in ChromaDB

        Returns:
            The original normalized SourceDocument.
        """

        if not source.strip():
            raise ValueError("Source cannot be empty.")

        # 1. Detect source type
        source_type = self.source_detector(source)

        # 2. Get appropriate loader
        loader = self.loader_factory(source_type)

        # 3. Load and normalize source
        document = loader.load(source)

        # 4. Split into chunks
        chunks = self.chunker.chunk(document)

        # 5. Store chunks in ChromaDB
        self.vector_store.add_documents(chunks)

        return document