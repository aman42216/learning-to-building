# ShramikSathi – Interview Preparation

## 1. 60-Second Project Pitch

Hello, my project is ShramikSathi, a Labour Rights Information Assistant developed using Python and Generative AI.

The main objective of this project is to help Indian workers understand labour-related information such as minimum wages, gratuity, leave, contract labour and social security in simple language.

I collected labour-related information from official government PDFs, extracted the text, cleaned the data and divided it into smaller chunks.

I developed a Retrieval-Augmented Generation pipeline that retrieves relevant information and uses the Groq LLM API to generate answers based on the retrieved context.

I used Python, FastAPI, Scikit-learn, ChromaDB, Groq API and Docker during development.

I also implemented response caching, input validation, prompt-injection protection, latency monitoring and token-usage logging.

The project includes automated testing using Pytest and CI/CD using GitHub Actions.

My goal is to make official labour-rights information easier for workers to access and understand.

## 2. Ten Likely Interview Questions and Answers

### Q1. What is ShramikSathi?

ShramikSathi is a Labour Rights Information Assistant that helps Indian workers understand labour laws and employment-related information through an AI-powered question-answering system.

### Q2. Why did you choose this project?

I chose this project because many workers find it difficult to understand lengthy government documents. I wanted to use AI and Python to make this information easier to access.

### Q3. What is RAG?

RAG stands for Retrieval-Augmented Generation.

It is a technique where the system first retrieves relevant information from a knowledge source and then provides that information to an LLM to generate a context-based answer.

### Q4. Why did you use chunking?

Government PDFs contain large amounts of text. Sending entire documents to an LLM is inefficient.

Chunking divides documents into smaller sections, making information retrieval more efficient and relevant.

### Q5. What is ChromaDB?

ChromaDB is a vector database used to store and retrieve vector embeddings.

It helps applications find relevant information based on semantic similarity.

### Q6. Why did you use FastAPI?

I used FastAPI to create REST API endpoints for the application.

It provides request validation, automatic API documentation through Swagger UI and good performance.

### Q7. Why did you use Groq API?

I used Groq API to integrate an LLM into the application and generate natural-language answers using retrieved information.

### Q8. How do you prevent hallucinations?

I provide retrieved context to the LLM and instruct it to answer only using that context.

If sufficient information is unavailable, the system should respond with "I don't know."

### Q9. How did you test your application?

I used Pytest to test API endpoints, RAG functionality, input validation and prompt-injection handling.

I also integrated automated tests into GitHub Actions.

### Q10. How did you improve application performance and reliability?

I implemented response caching to avoid repeated LLM calls for identical questions.

I also added latency logging, token-usage tracking, input limits and Docker-based deployment.

## 3. Hardest Technical Problem – Interview Story

### Problem: Handling Versioned Labour Guidance

One of the most challenging problems in ShramikSathi was handling labour-related information that changes over time.

I had to consider multiple versions of official guidance:

- December 2025 – Original FAQ answers.
- March 2026 – Additional FAQs refining earlier guidance.
- May 2026 – Rules notified later.

The challenge was that the system should not blindly return an older answer when newer official guidance is available.

### My Approach

I treated this as a document-versioning and retrieval problem.

1. Maintain metadata for every document, including its title, source and publication or notification date.
2. Retrieve relevant information from the available documents.
3. Compare the dates and applicable status of retrieved guidance.
4. Prefer the latest applicable official guidance.
5. Clearly flag transition provisions where old rules continue to apply until new rules are notified.

### Important Transition Rule

The system must not assume that a newly published FAQ automatically replaces an existing rule.

It must identify whether the relevant new rules have actually been notified and clearly communicate the transition position supported by the official source.

### Interview Answer

"The hardest problem I worked on was handling versioned labour-law information. Different government FAQs and notifications can contain updated or refined guidance.

I realized that retrieving the most similar text is not enough. The system must also consider document dates, source authority and applicability.

My approach was to maintain source metadata and use date-aware retrieval so that the latest applicable guidance can be presented with its source.

This was important because incorrect or outdated legal information could mislead workers."

**Note:** Explain this as an implemented feature only after date-aware retrieval and transition-rule handling have actually been tested in the application.

## 4. Project Architecture – Explanation

The main RAG workflow is:

1. Collect official labour-related PDFs.
2. Extract text using Python PDF-processing libraries.
3. Clean and preprocess the extracted text.
4. Divide documents into chunks.
5. Generate embeddings and index document content.
6. Receive a user's question through FastAPI.
7. Retrieve relevant information.
8. Pass retrieved context and the question to Groq LLM.
9. Generate a context-based answer.
10. Return the answer and available source citations.

## 5. Important Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend REST API |
| Scikit-learn | TF-IDF retrieval and similarity |
| ChromaDB | Vector storage |
| Groq API | LLM integration |
| Pytest | Automated testing |
| Docker | Containerization |
| GitHub Actions | CI automation |

## 6. Final Interview Tips

- Explain the problem before explaining the technology.
- Explain your own contribution clearly.
- Never claim a feature is implemented unless you can demonstrate it.
- Be ready to explain chunking, embeddings, RAG and caching.
- Demonstrate the application through Swagger UI.
- Explain one technical challenge in detail.
- If you do not know an answer, be honest and explain how you would investigate it.
