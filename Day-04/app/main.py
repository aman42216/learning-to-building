
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path
from .smart_search import smart_search

app = FastAPI(
    title="ShramikSathi API",
    description="Labour Rights Assistant API"
)

# Load records from Day-03 JSON file
DATA_FILE = Path(__file__).resolve().parents[2] / "Day-03" / "data" / "records.json"


def load_records():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Request model for POST endpoint
class Question(BaseModel):
    question: str


# 1. Health Check API
@app.get("/health")
def health():
    return {"status": "healthy", "message": "ShramikSathi API is running"}


# 2. Get All Records with Limit
@app.get("/records")
def get_records(limit: int = 10):
    records = load_records()
    return records[:limit]


# 3. Get Record by ID
@app.get("/records/{id}")
def get_record(id: int):
    records = load_records()

    if id < 1 or id > len(records):
        raise HTTPException(status_code=404, detail="Record not found")

    return records[id - 1]


# 4. Search Records
@app.get("/search")
def search_records(q: str):
    results = smart_search(q)

    return {
        "query": q,
        "total_results": len(results),
        "results": results
    }

# 5. Submit User Question
@app.post("/questions")
def submit_question(data: Question):
    return {
        "message": "Question received successfully",
        "question": data.question
    }
