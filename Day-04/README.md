
# ShramikSathi - Day 04

## Overview
FastAPI backend with Pandas analysis and intelligent FAQ search.

## Features
- GET /health
- GET /records?limit=10
- GET /records/{id}
- GET /search?q=gratuity
- POST /questions
- TF-IDF and Cosine Similarity Search
- Pandas data analysis

## How to Run

1. Install dependencies:

pip install -r Day-04/requirements.txt

2. Start the API:

uvicorn Day-04.app.main:app --reload

3. Open API documentation:

http://127.0.0.1:8000/docs

## Dataset
Uses 20 Labour Code FAQs from Day-03.

## Technologies
Python, FastAPI, Pandas, Scikit-learn, TF-IDF
