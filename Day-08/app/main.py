
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from rag import ask_question


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


app = FastAPI(
    title="ShramikSathi RAG API",
    description="Labour law question answering using RAG",
    version="1.0.0"
)

# Serve frontend static files
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500
    )


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


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
