
import json
import re
import sys
import importlib.util
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BASE_DIR.parent

# Import Groq wrapper
LLM_FILE = BASE_DIR / "app" / "llm.py"

llm_spec = importlib.util.spec_from_file_location(
    "llm_module", LLM_FILE
)
llm_module = importlib.util.module_from_spec(llm_spec)
llm_spec.loader.exec_module(llm_module)

generate_response = llm_module.generate_response

# Import existing smart search
SEARCH_FILE = (
    PROJECT_ROOT / "Day-04" / "app" / "smart_search.py"
)

search_spec = importlib.util.spec_from_file_location(
    "search_module", SEARCH_FILE
)
search_module = importlib.util.module_from_spec(search_spec)
search_spec.loader.exec_module(search_module)

smart_search = search_module.smart_search

# Load 10 user questions
QUESTIONS_FILE = (
    PROJECT_ROOT / "Day-05" / "docs" / "user_questions.md"
)

with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
    content = file.read()

questions = re.findall(r"^\d+\.\s+(.+)$", content, re.MULTILINE)

# Load system prompt
PROMPT_FILE = BASE_DIR / "prompts" / "system_prompt.txt"

with open(PROMPT_FILE, "r", encoding="utf-8") as file:
    system_prompt = file.read()

results = []

print("\n===== SHRAMIKSATHI PROMPT EVALUATION =====")

for index, question in enumerate(questions, start=1):

    print(f"\nTesting Question {index}/10: {question}")

    # Version 1: Basic prompt
    prompt_v1 = f"""
Answer this Indian labour-related question simply:

{question}

Do not invent legal information.
"""

    # Version 2: Dataset-grounded prompt
    matches = smart_search(question, limit=3)

    context = "\n\n".join(
        f"Question: {item['question']}\n"
        f"Official Answer: {item['official_answer']}"
        for item in matches
    )

    if not matches or matches[0]["similarity_score"] < 0.10:
        context = "No sufficiently relevant FAQ information found."

    prompt_v2 = f"""
User Question:
{question}

Official FAQ Context:
{context}

Answer only using relevant official information.
If information is insufficient, clearly say so.
Do not invent laws or legal rules.
"""

    try:
        answer_v1 = generate_response(prompt_v1, system_prompt)
        answer_v2 = generate_response(prompt_v2, system_prompt)

        results.append({
            "question": question,
            "version_1": answer_v1,
            "version_2": answer_v2
        })

        print("Version 1: Completed")
        print("Version 2: Completed")

    except Exception as error:
        print("Error:", error)

        results.append({
            "question": question,
            "version_1": "ERROR",
            "version_2": "ERROR"
        })

# Save evaluation results
OUTPUT_FILE = BASE_DIR / "eval" / "evaluation_results.json"

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print("\nEvaluation completed!")
print("Results saved to:", OUTPUT_FILE)
print("Questions processed:", len(results))
