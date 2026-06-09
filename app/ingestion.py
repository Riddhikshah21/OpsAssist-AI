from pathlib import Path
from uuid import uuid4

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


DOCS_DIR = Path("data/docs")


def load_markdown_docs(docs_dir: Path = DOCS_DIR) -> list[Document]:
    documents: list[Document] = []

    for file_path in docs_dir.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        metadata = {
            "document": file_path.name,
            "source_path": str(file_path),
            "source_type": "documentation",
        }

        documents.append(Document(page_content=text, metadata=metadata))

    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )

    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"{chunk.metadata['document']}::chunk_{index}"
        chunk.metadata["id"] = str(uuid4())

    return chunks


def ingest_documents() -> dict[str, int | str]:
    documents = load_markdown_docs()
    chunks = chunk_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        force_recreate=True,
    )

    return {
        "documents_loaded": len(documents),
        "chunks_created": len(chunks),
        "collection": settings.qdrant_collection,
    }