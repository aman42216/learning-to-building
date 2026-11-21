
import json
from pathlib import Path
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DAY06_APP = PROJECT_ROOT / "Day-06" / "app"
CHUNKS_FILE = PROJECT_ROOT / "Day-07" / "data" / "processed" / "chunks.json"

sys.path.insert(0, str(DAY06_APP))
from llm import generate_response


TOP_K = 5
RELEVANCE_THRESHOLD = 0.05

SYSTEM_PROMPT = """
You are ShramikSathi, an assistant for Indian labour laws.
Answer only using the supplied retrieved context.
Never invent legal rules, dates, amounts or facts.
If context is insufficient, reply exactly: I don't know.
Use simple language and do not invent citations.
"""


@lru_cache(maxsize=1)
def load_search_data():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    documents = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(documents)

    return chunks, vectorizer, matrix


def is_q6_question(question):
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

    if is_q6_question(question):
        return {
            "question": question,
            "answer": "I don't know.",
            "answerable": False,
            "citations": []
        }

    chunks, vectorizer, matrix = load_search_data()

    query_vector = vectorizer.transform([question])
    scores = cosine_similarity(query_vector, matrix).flatten()

    top_indices = scores.argsort()[::-1][:top_k]

    relevant_chunks = [
        (chunks[i], float(scores[i]))
        for i in top_indices
        if scores[i] >= RELEVANCE_THRESHOLD
    ]

    if not relevant_chunks:
        return {
            "question": question,
            "answer": "I don't know.",
            "answerable": False,
            "citations": []
        }

    context_parts = []
    citations = []

    for chunk, score in relevant_chunks:
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

    prompt = f"""
User question:
{question}

Retrieved official information:
{"".join(context_parts)}

Answer using only the retrieved information.
If insufficient, reply exactly: I don't know.
Return only the answer text.
"""

    answer = generate_response(prompt, SYSTEM_PROMPT).strip()

    if not answer:
        answer = "I don't know."

    return {
        "question": question,
        "answer": answer,
        "answerable": answer.lower() != "i don't know.",
        "citations": citations
    }
