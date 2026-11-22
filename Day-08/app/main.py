
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag import ask_question


app = FastAPI(
    title="ShramikSathi RAG API",
    description="Labour law question answering using RAG",
    version="1.0.0"
)


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500
    )


@app.get("/")
def home():
    return {
        "message": "ShramikSathi RAG API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ShramikSathi RAG API"
    }


@app.post("/ask")
def ask(data: AskRequest):
    question = data.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        return ask_question(question)

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to process the question"
        )
