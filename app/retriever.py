from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from app.config import settings


def get_vector_store() -> QdrantVectorStore:
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )

    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
    )


def retrieve_documents(query: str, k: int = 3) -> list[dict]:
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(query=query, k=k)

    retrieved = []
    for document, score in results:
        retrieved.append(
            {
                "content": document.page_content,
                "score": float(score),
                "metadata": document.metadata,
            }
        )

    return retrieved