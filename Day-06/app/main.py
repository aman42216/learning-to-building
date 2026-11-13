
import json
import importlib.util
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .llm import generate_response


# --------------------------------
# 1. PROJECT PATHS
# --------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parent

PROMPT_FILE = BASE_DIR / "prompts" / "system_prompt.txt"

SEARCH_FILE = (
    PROJECT_ROOT
    / "Day-04"
    / "app"
    / "smart_search.py"
)


# --------------------------------
# 2. IMPORT EXISTING SMART SEARCH
# --------------------------------

spec = importlib.util.spec_from_file_location(
    "smart_search_module",
    SEARCH_FILE
)

if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load smart_search module")

search_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_module)

smart_search = search_module.smart_search


# --------------------------------
# 3. FASTAPI APPLICATION
# --------------------------------

app = FastAPI(
    title="ShramikSathi Day-06",
    description="AI-powered Labour Rights Chat API",
    version="0.1.0"
)


# --------------------------------
# 4. REQUEST MODEL
# --------------------------------

class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000
    )


# --------------------------------
# 5. LOAD SYSTEM PROMPT
# --------------------------------

def load_system_prompt():

    if not PROMPT_FILE.exists():
        raise FileNotFoundError("System prompt file not found")

    with open(PROMPT_FILE, "r", encoding="utf-8") as file:
        return file.read()


# --------------------------------
# 6. CHAT ENDPOINT
# --------------------------------

@app.post("/chat")
def chat(data: ChatRequest):

    question = data.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Search relevant official FAQ records
    results = smart_search(question, limit=3)

    # No relevant information found
    if not results or results[0]["similarity_score"] < 0.10:

        return {
            "answer": (
                "Sorry, our current official FAQ dataset "
                "does not contain enough information to "
                "answer this question reliably."
            ),
            "confidence": "low",
            "follow_up": (
                "Would you like to ask about wages, "
                "gratuity or social security?"
            )
        }

    # Prepare context from official FAQ records
    context = "\n\n".join(
        (
            f"Question: {item['question']}\n"
            f"Official Answer: {item['official_answer']}"
        )
        for item in results
    )

    # Load system prompt
    system_prompt = load_system_prompt()

    # Prepare user prompt
    response_prompt = f"""
User Question:
{question}

Relevant Official FAQ Information:
{context}

Instructions:
1. Answer using relevant official information.
2. Do not invent labour laws or legal rules.
3. If the context is insufficient, clearly say so.
4. Keep the answer simple and helpful.

Return ONLY valid JSON in this format:

{{
    "answer": "Your answer here",
    "confidence": "high, medium or low",
    "follow_up": "One relevant follow-up question"
}}
"""

    try:

        # Generate response using Groq
        result = generate_response(
            response_prompt,
            system_prompt
        )

        result = result.strip()

        # Remove Markdown code fences if present
        if result.startswith("```"):
            result = result.replace("```json", "", 1)
            result = result.replace("```", "").strip()

        # Parse JSON response
        parsed_result = json.loads(result)

        answer = parsed_result.get("answer", "")
        confidence = str(
            parsed_result.get("confidence", "low")
        ).lower()

        follow_up = parsed_result.get("follow_up", "")

        if confidence not in ["high", "medium", "low"]:
            confidence = "low"

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Invalid answer returned by AI")

        if not isinstance(follow_up, str):
            follow_up = ""

        return {
            "answer": answer,
            "confidence": confidence,
            "follow_up": follow_up
        }

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=502,
            detail="AI returned an invalid JSON response"
        )

    except Exception:

        raise HTTPException(
            status_code=502,
            detail="Unable to generate AI response"
        )
