from app.retriever import retrieve_documents


def main() -> None:
    query = "Why is the API Gateway returning 502 errors after release v2.3.1?"

    results = retrieve_documents(query=query, k=3)

    print(f"\nQuery: {query}\n")

    for index, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print(f"Result {index}")
        print(f"Score: {result['score']}")
        print(f"Document: {metadata.get('document')}")
        print(f"Chunk ID: {metadata.get('chunk_id')}")
        print("-" * 80)
        print(result["content"][:500])
        print("=" * 80)


if __name__ == "__main__":
    main()