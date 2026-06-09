from app.ingestion import ingest_documents


def main() -> None:
    result = ingest_documents()

    print("Document ingestion completed")
    print(f"Documents loaded: {result['documents_loaded']}")
    print(f"Chunks created: {result['chunks_created']}")
    print(f"Qdrant collection: {result['collection']}")


if __name__ == "__main__":
    main()