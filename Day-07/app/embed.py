
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


def get_embedding_function():
    """Initialize ChromaDB's local ONNX embedding model."""
    return DefaultEmbeddingFunction()


def generate_embeddings(texts):
    """Generate embeddings for a list of text chunks."""
    embedding_function = get_embedding_function()
    embeddings = embedding_function(texts)

    return [
        embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)
        for embedding in embeddings
    ]


def semantic_search(collection, query, top_k=5):
    """Find relevant chunks using semantic similarity."""

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")

    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results
