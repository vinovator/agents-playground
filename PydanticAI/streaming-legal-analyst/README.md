# Streaming Legal Analyst

A **FastAPI + PydanticAI** application demonstrating how to stream structured AI analysis using Server-Sent Events (SSE).

## Use Case
Lawyers need to analyze complex contract clauses. This tool provides:
- **Streaming Output**: Real-time feedback as the AI generates the analysis (simulated via SSE).
- **Structured Data**: A strict JSON object (`ContractAnalysis`) containing a summary, risk score, and flagged items, returned at the end of the stream.

## Features
- **PydanticAI Agent**: Uses `gemini-2.5-flash` for high-quality legal analysis.
- **Server-Sent Events (SSE)**: Streams data to the client using `EventSource`.
- **Hybrid Response**: Streams text chunks (conceptually) and delivers a final structured payload.

## Setup

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Environment Variables**:
    Create a `.env` file with your API key:
    ```env
    GOOGLE_API_KEY=your_key_here
    ```

## Usage

### Run the Server
```bash
uvicorn main:app --reload
```
*Server runs at `http://0.0.0.0:8000`*

### stream Analysis
Use `curl` to see the stream in action:
```bash
curl -N -X POST http://127.0.0.1:8000/analyze-stream \
     -H "Content-Type: application/json" \
     -d '{"contract_clause": "The tenant shall pay rent on the first day of each month."}'
```
You will receive a stream finishing with an `event: final_result` containing the JSON analysis.
