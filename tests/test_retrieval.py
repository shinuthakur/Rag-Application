from app.retrieval.retriever import Retriever


def test_retriever_rejects_empty_query():
    retriever = Retriever.__new__(Retriever)

    try:
        retriever.retrieve("")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Query cannot be empty." in str(exc)