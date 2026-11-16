
# ShramikSathi — Day 08: Retrieval-Augmented Generation (RAG)

## Overview
Day-08 upgrades ShramikSathi with Retrieval-Augmented Generation (RAG). It retrieves relevant labour-law information from the Day-07 ChromaDB vector database and generates grounded answers using the Groq LLM.

## Technologies
- Python
- FastAPI
- ChromaDB
- Groq API
- Pydantic

## Features
1. Retrieves relevant chunks from ChromaDB.
2. Generates answers using retrieved context.
3. Provides citations with title, source and page.
4. Abstains with "I don't know" when information is insufficient.
5. Includes a dedicated abstention rule for the Maharashtra wedding-leave question (Q6).

## API

### POST /ask

Example request:

```json
{
  "question": "What is minimum wage?"
}
```

The response contains:
- question
- answer
- answerable
- citations

## Evaluation

Evaluation dataset: 15 questions.

Two configurations were compared:

| Configuration | Chunk Size | Top-K | Average Distance | Relevant Questions |
|---|---:|---:|---:|---:|
| Config A | 500 | 3 | 0.3662 | 13/15 |
| Config B | 1000 | 5 | 0.3695 | 13/15 |

### Winner: Config A

Config A achieved a lower average retrieval distance of 0.3662 compared with 0.3695 for Config B. Both configurations retrieved 13 out of 15 questions within the relevance threshold of 0.50.

Lower distance indicates closer semantic matches. This evaluation measures retrieval performance, not final LLM answer correctness.

## RAG Test Results

| Test | Expected Behaviour | Result |
|---|---|---|
| Minimum wage | Grounded answer with citation | PASS |
| Q6 wedding leave | "I don't know." | PASS |

## Run the API

From the project root:

```powershell
uvicorn main:app --app-dir Day-08/app --reload
```

Swagger documentation:

http://127.0.0.1:8000/docs

## Run Evaluation

```powershell
python Day-08/eval/run_eval.py
```

Evaluation report: `eval/evaluation_results.md`
