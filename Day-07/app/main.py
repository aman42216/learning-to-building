from fastapi import FastAPI, HTTPException, Query

from vectorstore import get_collection
from embed import semantic_search

app = FastAPI(
    title="ShramikSathi Semantic Search API",
    description="Semantic search across labour law documents and FAQs",
    version="1.0.0"
)

# Provisional threshold based on current evaluation
RELEVANCE_THRESHOLD = 0.50


@app.get("/")
def home():
    return {
        "message": "ShramikSathi Semantic Search API is running"
    }


@app.get("/search/semantic")
def search_semantic(
    q: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20)
):
    try:
        collection = get_collection()

        if collection.count() == 0:
            raise HTTPException(
                status_code=503,
                detail="Search database is empty"
            )

        results = semantic_search(collection, q, top_k=top_k)

        search_results = []

        for i, chunk_id in enumerate(results["ids"][0]):
            distance = results["distances"][0][i]

            if distance <= RELEVANCE_THRESHOLD:
                search_results.append({
                    "chunk_id": chunk_id,
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": round(distance, 4)
                })

        if not search_results:
            return {
                "query": q,
                "answerable": False,
                "message": "No sufficiently relevant information found in the knowledge base.",
                "total_results": 0,
                "results": []
            }

        return {
            "query": q,
            "answerable": True,
            "total_results": len(search_results),
            "results": search_results
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )