
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "Day-03" / "data" / "records.json"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


records = load_data()

documents = [
    record["question"] + " " + record["official_answer"]
    for record in records
]

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(documents)


def smart_search(query, limit=5):
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(
        query_vector, tfidf_matrix
    ).flatten()

    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices:
        if scores[index] <= 0:
            continue

        result = records[index].copy()
        result["similarity_score"] = round(
            float(scores[index]), 3
        )

        results.append(result)

        if len(results) >= limit:
            break

    return results

if __name__ == "__main__":
    print("\n===== SMART SEARCH TEST =====")

    results = smart_search("gratuity calculation")

    for result in results:
        print("\nQuestion:", result["question"])
        print("Score:", result["similarity_score"])