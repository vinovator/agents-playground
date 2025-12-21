# FastAPI PydanticAI Server

A simple but powerful agentic web server built with **FastAPI** and **PydanticAI**. This project demonstrates how to wrap a sophisticated AI agent into a standard REST API.

## Features

- **FastAPI Endpoint**: Exposes a POST `/ask` endpoint to interact with the agent.
- **PydanticAI Agent**: Uses `gemini-2.5-flash` model (via Google Vertex AI or Generative AI) for intelligent responses.
- **Structured Outputs**: Returns strictly typed JSON responses (`AgentResponse`).
- **Context Injection**: Simulates database access via dependency injection for personalized answers.
- **Tool Use**: The agent can "call" a mock database tool to retrieve user history.

## Prerequisites

- Python 3.10+
- A Google Cloud Project with Vertex AI enabled OR a Google API Key for Gemini.

## Setup

1.  **Clone the repository** (if you haven't already).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**:
    Create a `.env` file in the root directory and add your API key/credentials.
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    # OR if using Vertex AI
    # GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
    ```

## Usage

### Run the Server

```bash
uvicorn main:app --reload
```
*The server will start at `http://0.0.0.0:8000`.*

### API Documentation

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Example Request

**Endpoint:** `POST /ask`

**Body:**
```json
{
  "user_id": 101,
  "question": "What is the interest rate?"
}
```

**Response:**
```json
{
  "answer": "Based on your history, you asked about interest rates before. The current interest rate is 5%.",
  "confidence_score": 0.95,
  "requires_followup": false
}
```

## Project Structure

- `main.py`: The core application file containing the FastAPI app, PydanticAI agent, data models, and dependency logic.
