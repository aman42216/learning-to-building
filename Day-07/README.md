
# Day-07: Semantic Search with ChromaDB

## Project Overview
Day-07 implements semantic search for ShramikSathi using document chunking, embeddings, ChromaDB and FastAPI.

The system searches official labour law PDFs and structured FAQ records to retrieve relevant information.

## Technologies Used
- Python 3.13
- FastAPI
- ChromaDB
- PyPDF
- ONNX Default Embedding Function
- Uvicorn

## Project Structure

```text
Day-07/
├── app/
│   ├── __init__.py
│   ├── chunking.py
│   ├── faq_chunking.py
│   ├── embed.py
│   ├── save_chunks.py
│   ├── vectorstore.py
│   ├── run_search.py
│   └── main.py
├── data/
│   └── processed/
│       └── chunks.json
├── chroma_db/
├── eval/
│   └── search_results.md
├── requirements.txt
└── README.md
```

## 1. Document Chunking
- Extracted text from official labour law PDFs using PyPDF.
- Applied overlapping word-based chunking.
- Chunk size: 1000 words.
- Chunk overlap: 200 words.
- Preserved source, page number and document title.
- Detected and skipped duplicate PDF files.

## 2. FAQ Chunking
- Loaded 20 structured FAQ records from Day-03.
- Created one question-answer chunk per FAQ.
- Preserved topic, code name, FAQ date and source URL.

## 3. Embedding Generation
- Used ChromaDB DefaultEmbeddingFunction.
- Generated 384-dimensional embeddings.
- Used local ONNX-based embedding functionality.

## 4. Vector Database
- Used ChromaDB PersistentClient.
- Collection name: shramiksathi_documents.
- Distance metric: Cosine similarity.
- Implemented upsert and stale-record synchronization.

## 5. Semantic Search
- Evaluated 10 questions from Day-05.
- Retrieved the top matching document chunks.
- Recorded chunk IDs, source, page, title and distance.
- Saved results in eval/search_results.md.

## 6. FastAPI Endpoint

GET /search/semantic?q=

Example:

```text
http://127.0.0.1:8000/search/semantic?q=minimum%20wage
```

Optional parameter:
- top_k: Number of search results (1–20).

The endpoint returns relevant content, metadata and distance.

## 7. Relevance Checking and Abstention
- Implemented a provisional cosine-distance threshold of 0.50.
- Returns answerable=false when no retrieved result meets the threshold.
- Prevents unrelated retrieved chunks from being presented as sufficiently relevant evidence.
- Threshold requires further evaluation against all 10 questions.

## 8. Run the Project

Install dependencies:

```bash
pip install -r Day-07/requirements.txt
```

Generate chunks:

```bash
python Day-07/app/save_chunks.py
```

Index documents:

```bash
python -c "import json, sys; sys.path.insert(0, 'Day-07/app'); from vectorstore import index_chunks; chunks=json.load(open('Day-07/data/processed/chunks.json', encoding='utf-8')); print('Indexed chunks:', index_chunks(chunks))"
```

Start FastAPI:

```bash
uvicorn main:app --app-dir Day-07/app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 9. Evaluation
- Total structured FAQs: 20
- Unique PDF chunks: 125
- FAQ chunks: 20
- Total indexed chunks: 145
- Evaluation questions: 10
- Persistent ChromaDB storage verified.
- Supported and unsupported query tests performed.

Detailed results: eval/search_results.md

## Conclusion
Day-07 implements a persistent semantic search system for ShramikSathi. It combines official PDF documents and structured FAQs, generates embeddings, retrieves relevant chunks and exposes semantic search through FastAPI.
