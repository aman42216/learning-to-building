
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "faqs.json"


def load_records():
    """Load FAQ records from JSON file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            records = data.get("faqs", data.get("data", []))
        else:
            records = data

        return records if isinstance(records, list) else []

    except (FileNotFoundError, json.JSONDecodeError):
        return []



def search(records, query):
    """Search FAQ records with priority for question and topic matches."""
    query_words = set(query.lower().split())

    stop_words = {
        "what", "is", "are", "the", "a", "an", "of",
        "to", "in", "for", "how", "can", "i", "my",
        "do", "does", "tell", "me", "about", "please"
    }

    query_words -= stop_words
    results = []

    for record in records:
        question = str(record.get("question", "")).lower()
        topic = str(record.get("topic", "")).lower()
        keywords = " ".join(record.get("keywords", [])).lower()
        answer = str(record.get("official_answer", "")).lower()

        score = 0

        for word in query_words:
            if word in question:
                score += 3
            if word in topic:
                score += 4
            if word in keywords:
                score += 3
            if word in answer:
                score += 1

        if score > 0:
            results.append((score, record))

    results.sort(key=lambda item: item[0], reverse=True)
    return [record for score, record in results]



def count_by(records, field):
    """Count records grouped by a field."""
    counts = {}

    for record in records:
        value = record.get(field, "Not specified")
        counts[value] = counts.get(value, 0) + 1

    return counts


def get_by_id(records, record_id):
    """Find a record using its ID."""
    for record in records:
        if record.get("id") == record_id:
            return record

    return None
