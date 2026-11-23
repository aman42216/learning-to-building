
# ShramikSathi â€“ Labour Rights Information Assistant

# ShramikSathi

[![ShramikSathi CI](https://github.com/aman42216/learning-to-building/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/aman42216/learning-to-building/actions/workflows/ci.yml)

**Live API / Swagger Docs:** 
https://learning-to-building-wo8y.onrender.com/docs

**Live API:** https://learning-to-building-wo8y.onrender.com

**Health Check:** https://learning-to-building-wo8y.onrender.com/health

## 1. Project Overview

ShramikSathi is a Python-based Labour Rights Information Assistant developed to help Indian workers understand their labour rights in simple language.

The project provides information about wages, gratuity, leave, contract labour, employee benefits and social security through a collection of frequently asked questions.

## 2. Problem Statement

Many Indian workers find it difficult to understand labour laws because official documents and legal information can be lengthy and complicated.

ShramikSathi aims to make labour-related information easier to access by organizing official FAQs and providing a simple question-answering system.

## 3. Target Users

The main users of ShramikSathi are:

- Factory and industrial workers
- Contract workers
- Daily-wage workers
- Private-sector employees
- Workers seeking information about wages, gratuity and social security

## 4. Key Features

- Search labour-related FAQs.
- View official answers.
- Access information about different Labour Codes.
- Calculate illustrative gratuity estimates.
- Retrieve information from structured JSON records.
- Provide AI-powered answers using Groq API in later development stages.

## 5. Data Sources

The project uses labour-related information from official government sources:

- Ministry of Labour and Employment: https://labour.gov.in/
- Official Labour Codes and government FAQ documents.
- Labour-related PDF documents used for data extraction and processing.

## 6. Technology Stack

- Python
- JSON
- FastAPI
- Pandas
- Scikit-learn
- Groq API
- Git and GitHub

## 7. Project Development Structure

This project is developed step by step during the Python training program.

- Day-01: Python Basics and Git/GitHub
- Day-02: Collections, Functions and Project Layout
- Day-03: PDF Data Extraction and Processing
- Day-04: FastAPI and Smart Search
- Day-05: LLM Fundamentals and Documentation
- Day-06: Groq API Integration and Prompt Evaluation

## 8. Project Goal

The goal of ShramikSathi is to make labour-rights information more understandable and accessible to Indian workers through Python and AI-based technologies.

---
**Project Name:** ShramikSathi
**Domain:** Python, Artificial Intelligence and Labour Rights Information


## Day-11: Testing and Docker Deployment

### Testing
- Created 18 automated pytest tests.
- Tested FAQ records and semantic search.
- Tested FastAPI health and ask endpoints.
- Tested Agent calculator functionality.
- All 18 tests passed.

Run tests:
```bash
python -m pytest -v
```

### Docker Deployment
The ShramikSathi application runs using Docker Compose.

Services:
- RAG API: http://localhost:8008
- Agent API: http://localhost:8009
- Streamlit UI: http://localhost:8501

### Run with Docker

1. Install Docker Desktop.
2. Configure `Day-06/.env` with your Groq API key.
3. Build Docker images:

```bash
docker compose build
```

4. Start all services:

```bash
docker compose up -d
```

5. Stop services:

```bash
docker compose down
```

### ChromaDB
- Persistent Docker volume: `chroma_data`
- Automatically indexes 145 document chunks during RAG API startup.

### Docker Files
- `Dockerfile`
- `.dockerignore`
- `docker-compose.yml`
- `requirements.txt`

## Production Notes

### Performance Monitoring

| Metric | First Request | Cached Request |
|---|---:|---:|
| RAG Latency | 6980.17 ms | 0.03 ms |
| LLM Latency | 2611.63 ms | Not Called |
| Prompt Tokens | 2056 | 0 |
| Completion Tokens | 411 | 0 |
| Cache Status | MISS | HIT |

Note: These are sample measurements from a local test run.
Performance may vary depending on API response time and system conditions.

### Production Features
- Request latency logging
- LLM token usage tracking
- Response caching
- Input length validation
- Prompt injection protection