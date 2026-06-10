from app.retriever import retrieve_documents


def test_retriever_returns_relevant_docs() -> None:
    results = retrieve_documents(
        query="Why is the API Gateway returning 502 errors after release v2.3.1?",
        k=3,
    )

    documents = {result["metadata"].get("document") for result in results}

    assert "api_gateway_502_runbook.md" in documents