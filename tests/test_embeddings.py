from app.vectorstore.embeddings import EmbeddingService


def test_embedding_service_requires_api_key(monkeypatch):
    monkeypatch.setattr(
        "app.vectorstore.embeddings.settings.GOOGLE_API_KEY",
        "",
    )

    try:
        EmbeddingService()
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "GOOGLE_API_KEY" in str(exc)