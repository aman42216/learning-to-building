import json
import hashlib
from pathlib import Path


FAQ_FILE = Path("Day-03/data/records.json")


def process_faq_records():
    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    chunks = []

    for index, record in enumerate(records, start=1):

        question = record["question"].strip()
        answer = record["official_answer"].strip()

        content = f"Question: {question}\nAnswer: {answer}"

        chunk_id = hashlib.sha256(
            f"{index}:{content}".encode("utf-8")
        ).hexdigest()

        chunks.append({
            "id": chunk_id,
            "text": content,
            "metadata": {
                "source": "records.json",
                "page": 0,
                "title": record["topic"],
                "topic": record["topic"],
                "code_name": record["code_name"],
                "faq_date": record["faq_date"],
                "source_url": record["source_url"],
                "chunk_index": index - 1
            }
        })

    return chunks


if __name__ == "__main__":
    results = process_faq_records()

    print("Total FAQ chunks:", len(results))
    print("First chunk metadata:", results[0]["metadata"])
    print("First chunk preview:", results[0]["text"])