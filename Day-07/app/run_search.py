import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from vectorstore import get_collection
from embed import semantic_search

QUESTIONS_FILE = Path("Day-05/docs/user_questions.md")
OUTPUT_FILE = Path("Day-07/eval/search_results.md")


def load_questions():
    questions = []

    with open(QUESTIONS_FILE, encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line[:1].isdigit() and ". " in line:
                questions.append(line.split(". ", 1)[1])

    return questions


def main():
    collection = get_collection()
    questions = load_questions()

    report = ["# ShramikSathi Semantic Search Results\n"]
    report.append(f"Total questions: {len(questions)}\n")

    for number, question in enumerate(questions, start=1):
        results = semantic_search(collection, question, top_k=3)

        report.append(f"\n## {number}. {question}\n")

        ids = results["ids"][0]

        if not ids:
            report.append("No relevant results found.\n")
            continue

        for i, chunk_id in enumerate(ids):
            metadata = results["metadatas"][0][i]
            distance = results["distances"][0][i]
            document = results["documents"][0][i]

            report.append(f"- Chunk ID: {chunk_id}\n")
            report.append(f"  - Source: {metadata['source']}\n")
            report.append(f"  - Page: {metadata['page']}\n")
            report.append(f"  - Title: {metadata['title']}\n")
            report.append(f"  - Distance: {distance:.4f}\n")
            report.append(f"  - Preview: {document[:250]}\n")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("".join(report), encoding="utf-8")

    print("Questions evaluated:", len(questions))
    print("Report saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()