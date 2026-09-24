from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import settings
from app.schemas.document import SourceDocument
from app.vectorstore.embeddings import EmbeddingService


class ChromaVectorStore:
    """
    Persistent ChromaDB vector store for the RAG application.
    """

    def __init__(
        self,
        collection_name: str = "rag_documents",
    ):
        self.embedding_service = EmbeddingService()

        self.vector_store = Chroma(
            collection_name=collection_name,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embedding_service.model,
        )

    def add_documents(
        self,
        documents: list[SourceDocument],
    ) -> None:
        """
        Add source document chunks to ChromaDB.
        """

        if not documents:
            return

        langchain_documents = []
        ids = []

        for document in documents:
            langchain_documents.append(
                Document(
                    page_content=document.content,
                    metadata={
                        "document_id": document.document_id,
                        "source_type": document.metadata.source_type,
                        "source": document.metadata.source,
                        "title": document.metadata.title or "",
                        "chunk_index": document.metadata.chunk_index,
                        "page": document.metadata.page,
                        "timestamp_start": (
                            document.metadata.timestamp_start
                        ),
                        "timestamp_end": (
                            document.metadata.timestamp_end
                        ),
                    },
                )
            )

            ids.append(
                f"{document.document_id}_{document.metadata.chunk_index}"
            )

        self.vector_store.add_documents(
            documents=langchain_documents,
            ids=ids,
        )

    def similarity_search(
        self,
        query: str,
        k: int | None = None,
    ) -> list[Document]:
        """
        Retrieve the most similar chunks for a query.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        search_k = (
            k if k is not None else settings.TOP_K
        )

        return self.vector_store.similarity_search(
            query,
            k=search_k,
        )

    def mmr_search(
        self,
        query: str,
        k: int | None = None,
        fetch_k: int | None = None,
        document_id: str | None = None,
    ) -> list[Document]:
        """
        Retrieve diverse relevant chunks using MMR.

        If document_id is provided, retrieval is restricted
        to chunks belonging to that specific source.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        search_k = (
            k if k is not None else settings.TOP_K
        )

        candidate_k = (
            fetch_k
            if fetch_k is not None
            else settings.FETCH_K
        )

        search_filter = None

        if document_id:
            search_filter = {
                "document_id": document_id,
            }

        return self.vector_store.max_marginal_relevance_search(
            query,
            k=search_k,
            fetch_k=candidate_k,
            filter=search_filter,
        )