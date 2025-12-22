# Human-in-the-Loop Refund Agent

A specialized AI agent built with **PydanticAI** and **FastAPI** that handles refund processing with a human-in-the-loop (HITL) approval mechanism for high-value transactions.

## 📋 Scenario

This agent simulates an automated refund system:
- **Low Value (< $50)**: Refunds are automatically approved and processed instantly.
- **High Value (> $50)**: The agent pauses execution, drafts an approval request, and waits for a human manager's decision before proceeding.

## 🚀 Features

- **PydanticAI Integration**: Uses structured outputs (`ApprovalRequest` vs `TransferSuccess`) to drive control flow.
- **State Persistence**: Serializes conversation history to a "database" (mocked in-memory) to resume context after human intervention.
- **FastAPI Endpoints**: Clean REST API for requesting refunds and submitting manager reviews.
- **Tool Usage**: Deterministic tool calling for final value transfer.

## 📂 Project Structure

```
human-in-loop-refund-agent/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application & endpoints
│   ├── agent.py         # Agent definition & tools
│   ├── models.py        # Pydantic models & mocked database
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

## 🛠️ Setup

1.  **Clone the repository** (if you haven't already).
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Environment Variables**:
    Create a `.env` file in the root directory and add your API key (default uses Gemini):
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    # or OPENAI_API_KEY if you switch models
    ```

## ⚡ Usage

Run the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### 1. Automatic Refund (< $50)

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/request-refund?user_reason=broken%20item&amount=20"
```

**Response:**
```json
{
  "status": "COMPLETED",
  "details": {
    "amount": 20.0,
    "status": "COMPLETED"
  }
}
```

### 2. High-Value Refund (> $50) - Approval Flow

**Step 1: Request Refund**
```bash
curl -X POST "http://127.0.0.1:8000/request-refund?user_reason=expensive%20item&amount=500"
```

**Response (Paused):**
```json
{
  "status": "APPROVAL_REQUESTED",
  "job_id": "aa1c6295-...",
  "details": {
    "amount": 500.0,
    "reason": "expensive item",
    "status": "WAITING_FOR_APPROVAL"
  }
}
```

**Step 2: Manager Approval**
Use the `job_id` from the previous step.

```bash
curl -X POST "http://127.0.0.1:8000/manager-review" \
     -H "Content-Type: application/json" \
     -d '{
           "job_id": "aa1c6295-...",
           "approved": true,
           "manager_comment": "Customer is loyal, approve it."
         }'
```

**Response (Resumed & Completed):**
```json
{
  "status": "COMPLETED",
  "details": {
    "amount": 500.0,
    "status": "COMPLETED"
  }
}
```

## 🧠 How It Works

1.  **Phase 1 (User Request)**: The agent analyzes the amount. If > $50, it returns an `ApprovalRequest` structured object.
2.  **State Freezing**: `main.py` detects the `ApprovalRequest`, generates a UUID (`job_id`), limits the agent's execution, and saves the entire message history (User Prompt + Agent Thought + Partial Response) to the `JobStore`.
3.  **Phase 2 (Manager Review)**: When the manager posts to `/manager-review`, the system retrieves the frozen history.
4.  **Resumption**: The system invokes the agent again with `resume_prompt` (simulating the manager's voice) and injects the loaded `message_history`. The agent "remembers" the original context and proceeds to call the `final_transfer` tool.