import json
import time
from pathlib import Path

from app.retriever import retrieve_documents

EVAL_FILE = Path("data/eval_sets/retrieval_eval.jsonl")


def load_eval_cases() -> list[dict]:
    cases = []

    with EVAL_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                cases.append(json.loads(line))

    return cases


def evaluate_retrieval(k: int = 3) -> dict:
    cases = load_eval_cases()

    total_cases = len(cases)
    passed_cases = 0
    total_latency = 0.0
    results = []

    for case in cases:
        question = case["question"]
        expected_sources = set(case["expected_sources"])

        start_time = time.perf_counter()
        retrieved = retrieve_documents(query=question, k=k)
        latency = time.perf_counter() - start_time

        retrieved_sources = {
            item["metadata"].get("document")
            for item in retrieved
        }

        matched_sources = expected_sources.intersection(retrieved_sources)
        passed = len(matched_sources) > 0

        if passed:
            passed_cases += 1

        total_latency += latency

        results.append(
            {
                "question": question,
                "expected_sources": sorted(expected_sources),
                "retrieved_sources": sorted(retrieved_sources),
                "matched_sources": sorted(matched_sources),
                "passed": passed,
                "latency_seconds": round(latency, 3),
            }
        )

    recall_at_k = passed_cases / total_cases if total_cases else 0.0
    avg_latency = total_latency / total_cases if total_cases else 0.0

    return {
        "k": k,
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "recall_at_k": round(recall_at_k, 3),
        "average_latency_seconds": round(avg_latency, 3),
        "results": results,
    }


def main() -> None:
    report = evaluate_retrieval(k=3)

    print("\nRetrieval Evaluation Report")
    print("=" * 40)
    print(f"Total cases: {report['total_cases']}")
    print(f"Passed cases: {report['passed_cases']}")
    print(f"Recall@{report['k']}: {report['recall_at_k']}")
    print(f"Average latency: {report['average_latency_seconds']}s")
    print("=" * 40)

    for result in report["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"\n[{status}] {result['question']}")
        print(f"Expected: {result['expected_sources']}")
        print(f"Retrieved: {result['retrieved_sources']}")
        print(f"Matched: {result['matched_sources']}")
        print(f"Latency: {result['latency_seconds']}s")


if __name__ == "__main__":
    main()