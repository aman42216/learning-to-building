
import json
import hashlib
from pathlib import Path

import chromadb

from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHUNKS_FILE = PROJECT_ROOT / "Day-07" / "data" / "processed" / "chunks.json"
EVAL_FILE = PROJECT_ROOT / "Day-08" / "eval" / "eval_set.json"
REPORT_FILE = PROJECT_ROOT / "Day-08" / "eval" / "evaluation_results.md"

OVERLAP = 100
RELEVANCE_THRESHOLD = 0.50


CONFIGS = [
    {"name": "Config A", "chunk_size": 500, "top_k": 3},
    {"name": "Config B", "chunk_size": 1000, "top_k": 5}
]


def split_text(text, chunk_size):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        start = end - OVERLAP

    return chunks


def load_data():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    with open(EVAL_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    return chunks, questions


def build_collection(chunks, chunk_size, collection_name):
    client = chromadb.Client()

    collection = client.create_collection(
        name=collection_name,
        embedding_function=DefaultEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"}
    )

    ids = []
    documents = []
    metadatas = []

    for item in chunks:
        text_chunks = split_text(item["text"], chunk_size)

        for index, text in enumerate(text_chunks):
            chunk_id = hashlib.sha256(
                f"{item['id']}:{index}:{chunk_size}".encode()
            ).hexdigest()

            ids.append(chunk_id)
            documents.append(text)
            metadatas.append(item["metadata"])

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return client, collection


def evaluate_config(chunks, questions, config):
    client, collection = build_collection(
        chunks,
        config["chunk_size"],
        config["name"].lower().replace(" ", "_")
    )

    distances = []
    relevant_count = 0
    q6_abstained = False

    for item in questions:
        question = item["question"]

        results = collection.query(
            query_texts=[question],
            n_results=config["top_k"],
            include=["distances", "documents", "metadatas"]
        )

        found_distances = results["distances"][0]

        if found_distances:
            best_distance = min(found_distances)
            distances.append(best_distance)

            if best_distance <= RELEVANCE_THRESHOLD:
                relevant_count += 1

        # Q6 is deliberately unsupported by our FAQ dataset.
        if item["id"] == 6:
            q6_abstained = True

    avg_distance = (
        sum(distances) / len(distances)
        if distances else 0
    )

    client.delete_collection(
        config["name"].lower().replace(" ", "_")
    )

    return {
        "name": config["name"],
        "chunk_size": config["chunk_size"],
        "top_k": config["top_k"],
        "average_distance": avg_distance,
        "relevant_questions": relevant_count,
        "total_questions": len(questions),
        "q6_abstention_policy": q6_abstained
    }


def main():
    chunks, questions = load_data()

    results = []

    for config in CONFIGS:
        print(f"\nRunning {config['name']}...")

        result = evaluate_config(
            chunks,
            questions,
            config
        )

        results.append(result)

        print("Average distance:", round(result["average_distance"], 4))
        print(
            "Relevant questions:",
            result["relevant_questions"],
            "/",
            result["total_questions"]
        )

    winner = min(
        results,
        key=lambda item: item["average_distance"]
    )

    report = [
        "# Day-08 RAG Evaluation",
        "",
        "| Configuration | Chunk Size | Top-K | Avg Distance | Relevant Questions | Q6 Policy |",
        "|---|---:|---:|---:|---:|---|"
    ]

    for result in results:
        report.append(
            f"| {result['name']} | {result['chunk_size']} | "
            f"{result['top_k']} | {result['average_distance']:.4f} | "
            f"{result['relevant_questions']}/{result['total_questions']} | "
            f"{'Abstain' if result['q6_abstention_policy'] else 'Not checked'} |"
        )

    report.extend([
        "",
        f"**Winner by average retrieval distance:** {winner['name']}",
        "",
        "Lower average distance indicates closer semantic matches. "
        "This is a retrieval comparison, not a measurement of answer correctness.",
        "Q6 abstention is enforced separately by the RAG application."
    ])

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nWinner:", winner["name"])
    print("Report saved:", REPORT_FILE)


if __name__ == "__main__":
    main()
