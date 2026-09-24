import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Central configuration for the RAG application.
    """

    # --------------------------------------------------
    # API
    # --------------------------------------------------

    GOOGLE_API_KEY: str = os.getenv(
        "GOOGLE_API_KEY",
        "",
    )

    # --------------------------------------------------
    # Models
    # --------------------------------------------------

    LLM_MODEL: str = os.getenv(
        "LLM_MODEL",
        "gemini-3.6-flash",
    )

    LLM_FALLBACK_MODEL: str = os.getenv(
        "LLM_FALLBACK_MODEL",
        "gemini-3.5-flash",
    )

    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "gemini-embedding-001",
    )

    # --------------------------------------------------
    # Vector database
    # --------------------------------------------------

    CHROMA_PERSIST_DIRECTORY: str = os.getenv(
        "CHROMA_PERSIST_DIRECTORY",
        "./chroma_db",
    )

    # --------------------------------------------------
    # Chunking
    # --------------------------------------------------

    CHUNK_SIZE: int = int(
        os.getenv(
            "CHUNK_SIZE",
            "800",
        )
    )

    CHUNK_OVERLAP: int = int(
        os.getenv(
            "CHUNK_OVERLAP",
            "150",
        )
    )

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    TOP_K: int = int(
        os.getenv(
            "TOP_K",
            "5",
        )
    )

    FETCH_K: int = int(
        os.getenv(
            "FETCH_K",
            "10",
        )
    )


settings = Settings()