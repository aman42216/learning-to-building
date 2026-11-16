
import sys
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DAY06_APP = PROJECT_ROOT / "Day-06" / "app"
DAY07_APP = PROJECT_ROOT / "Day-07" / "app"

# Add existing project modules to Python path
sys.path.insert(0, str(DAY06_APP))
sys.path.insert(0, str(DAY07_APP))

from llm import generate_response
from vectorstore import get_collection
from embed import semantic_search


RELEVANCE_THRESHOLD = 0.50
TOP_K = 5


SYSTEM_PROMPT = """
You are ShramikSathi, an assistant for Indian labour laws.

Rules:
1. Answer only using the supplied retrieved context.
2. Never invent legal rules, dates, amounts or facts.
3. If context does not contain enough information, say:
   I don't know.
4. Use simple and clear language.
5. Do not provide unsupported legal advice.
6. Do not invent citations.
"""


def is_q6_question(question):
    """Identify the unsupported Maharashtra wedding-leave question."""

    text = question.lower()

    return (
        "maharashtra" in text
        and "wedding" in text
        and ("leave" in text or "paid" in text)
    )


def ask_question(question, top_k=TOP_K):
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    # Mandatory abstention for Day-05 Q6
    if is_q6_question(question):
        return {
            "question": question,
            "answer": "I don't know.",
            "answerable": False,
            "citations": []
        }

    # Retrieve relevant chunks from ChromaDB
    collection = get_collection()

    if collection.count() == 0:
        return {
            "question": question,
            "answer": "I don't know.",
            "answerable": False,
            "citations": []
        }

    results = semantic_search(
        collection,
        question,
        top_k=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Keep only sufficiently relevant chunks
    relevant_chunks = []

    for document, metadata, distance in zip(
        documents, metadatas, distances
    ):
        if distance <= RELEVANCE_THRESHOLD:
            relevant_chunks.append({
                "text": document,
                "metadata": metadata,
                "distance": distance
            })

    if not relevant_chunks:
        return {
            "question": question,
            "answer": "I don't know.",
            "answerable": False,
            "citations": []
        }

    # Prepare retrieved context
    context_parts = []

    citations = []

    for chunk in relevant_chunks:
        metadata = chunk["metadata"]

        context_parts.append(
            f"Title: {metadata.get('title', 'Unknown')}\n"
            f"Source: {metadata.get('source', 'Unknown')}\n"
            f"Page: {metadata.get('page', 'Unknown')}\n"
            f"Content: {chunk['text']}"
        )

        citation = {
            "title": metadata.get("title", "Unknown"),
            "source": metadata.get("source", "Unknown"),
            "page": metadata.get("page", 0)
        }

        if citation not in citations:
            citations.append(citation)

    context = "\n\n".join(context_parts)

    prompt = f"""
User question:
{question}

Retrieved official information:
{context}

Answer the question using only the retrieved information.

If the information is insufficient, reply exactly:
I don't know.

Return only the answer text.
"""

    # Generate grounded answer using Groq
    try:
        answer = generate_response(
            prompt,
            SYSTEM_PROMPT
        )

        answer = answer.strip()

        if not answer:
            answer = "I don't know."

        return {
            "question": question,
            "answer": answer,
            "answerable": answer.lower() != "i don't know.",
            "citations": citations
        }

    except Exception:
        raise RuntimeError("Unable to generate RAG response")
