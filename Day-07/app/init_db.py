
import json
from pathlib import Path
from vectorstore import index_chunks

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNKS_FILE = PROJECT_ROOT / "Day-07/data/processed/chunks.json"


def main():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    total = index_chunks(chunks)
    print(f"ChromaDB initialized successfully: {total} chunks")


if __name__ == "__main__":
    main()
