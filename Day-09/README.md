
# Day-09: AI Agent with LangGraph

## Project Overview

ShramikSathi is an AI-powered labour law assistant that helps users with labour-related questions and gratuity calculations.

Day-09 introduces an AI Agent using Groq tool calling and LangGraph.

## Features

- Hand-written AI Agent Loop
- RAG-based Labour Law Search
- Gratuity and Wage Calculator
- 50% Wage Rule
- LangGraph Workflow
- Conversation Memory using MemorySaver
- Human Approval before Gratuity Calculation
- FastAPI POST /agent endpoint
- Swagger API Testing

## Project Structure

Day-09/
- app/
  - __init__.py
  - tools.py
  - agent_loop.py
  - graph.py
  - main.py
- requirements.txt
- README.md

## Available Tools

### 1. search_labour_info

Searches labour law information using the existing ShramikSathi RAG system.

### 2. gratuity_and_wage_calculator

Calculates adjusted monthly wages and gratuity.

Formula:

Adjusted Wages = Total Pay - Excluded Allowances + Excess Allowances Added Back

Gratuity = (15 / 26) × Adjusted Monthly Wages × Completed Years

Maximum gratuity limit: ₹20,00,000

## LangGraph Workflow

1. User submits a question.
2. Agent identifies the required tool.
3. RAG search executes directly for labour questions.
4. Gratuity calculation pauses for user approval.
5. Calculator executes only after approval.
6. Final answer is generated.

## API Endpoint

POST /agent

### Example Request

{
  "question": "Calculate gratuity for total monthly pay Rs. 50000, excluded allowances Rs. 30000 and 10 completed years of service.",
  "thread_id": "test-user-1",
  "approved": null
}

### Approval Request

The API returns approval_required when calculation needs confirmation.

### Approve Calculation

{
  "question": "",
  "thread_id": "test-user-1",
  "approved": true
}

### Reject Calculation

{
  "question": "",
  "thread_id": "test-user-1",
  "approved": false
}

## Testing

Tested successfully:

- Gratuity calculator
- RAG search
- Agent tool calling
- LangGraph workflow
- Approval interrupt
- Approved calculation
- Rejected calculation
- FastAPI Swagger interface

## Example Calculation

Total Monthly Pay: ₹50,000

Excluded Allowances: ₹30,000

Completed Years: 10

Excess Allowances Added Back: ₹5,000

Adjusted Monthly Wages: ₹25,000

Final Gratuity: ₹1,44,230.77

## Run Application

uvicorn main:app --app-dir Day-09/app --reload --port 8009

Swagger Documentation:

http://127.0.0.1:8009/docs

## Memory Note

MemorySaver stores checkpoints in memory during the running application process. Checkpoints are not persistent across application restarts.
