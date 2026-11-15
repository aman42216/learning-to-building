import chromadb
from pathlib import Path

from embed import get_embedding_function

DB_PATH = Path("Day-07/chroma_db")
COLLECTION_NAME = "shramiksathi_documents"


def get_collection():
    DB_PATH.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    embedding_function = get_embedding_function()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


def index_chunks(chunks):
    collection = get_collection()

    if not chunks:
        raise ValueError("No chunks available for indexing")

    # Find old chunks that are no longer in the source data
    existing = collection.get(include=["metadatas"])

    new_ids = {chunk["id"] for chunk in chunks}

    stale_ids = [
        chunk_id
        for chunk_id in existing["ids"]
        if chunk_id not in new_ids
    ]

    # Remove stale chunks
    if stale_ids:
        collection.delete(ids=stale_ids)

    # Insert or update current chunks
    collection.upsert(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks]
    )

    return collection.count()