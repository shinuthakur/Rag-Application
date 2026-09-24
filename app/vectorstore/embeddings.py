from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import settings


class EmbeddingService:
    """
    Provides the embedding model used by the RAG application.
    """

    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not configured."
            )

        self.model = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """
        if not texts:
            return []

        return self.model.embed_documents(texts)

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single query.
        """
        if not text.strip():
            raise ValueError(
                "Query text cannot be empty."
            )

        return self.model.embed_query(text)