
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from graph import run_graph


app = FastAPI(
    title="ShramikSathi Agent API",
    description="LangGraph Agent with RAG, Calculator and Approval",
    version="1.0"
)


# ==========================================
# REQUEST MODEL
# ==========================================

class AgentRequest(BaseModel):
    question: str = ""
    thread_id: str
    approved: Optional[bool] = None


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Welcome to ShramikSathi Agent API",
        "status": "running"
    }


# ==========================================
# AGENT ENDPOINT
# ==========================================

@app.post("/agent")
def agent_endpoint(request: AgentRequest):

    if request.approved is None and not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question is required for a new request."
        )

    try:
        result = run_graph(
            question=request.question,
            thread_id=request.thread_id,
            approved=request.approved
        )

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
