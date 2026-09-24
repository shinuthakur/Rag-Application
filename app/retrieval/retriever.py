from langchain_core.documents import Document

from app.config import settings
from app.vectorstore.chroma_store import ChromaVectorStore


class Retriever:
    def __init__(
        self,
        vector_store: ChromaVectorStore | None = None,
    ):
        self.vector_store = (
            vector_store
            if vector_store is not None
            else ChromaVectorStore()
        )

    def retrieve(
        self,
        query: str,
        document_id: str | None = None,
    ) -> list[Document]:

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        return self.vector_store.mmr_search(
            query=query,
            k=settings.TOP_K,
            fetch_k=settings.FETCH_K,
            document_id=document_id,
        )