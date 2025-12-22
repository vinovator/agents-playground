"""
The Use Case — "High-Value Refund Agent"

Scenario: An automated refund system.
- Refunds < $50: Auto-approved.
Refunds > $50: Agent must calculate the amount, verify the user, 
draft the refund, and wait for a human manager to say "Yes".

Implementation:
This requires two distinct API endpoints: one to Start the process, and one to Resume it.
"""

import sys
import os

# Add project root to sys.path to allow 'from app.models' to work when running script directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables (e.g. GEMINI_API_KEY) BEFORE importing modules that use them
load_dotenv()

# Import from our refactored modules
from app.models import db, ApprovalRequest, TransferSuccess, ManagerDecision
from app.agent import refund_agent

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing in .env file")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/request-refund")
async def request_refund(user_reason: str, amount: float):
    # 1. Run the agent
    prompt = f"User wants refund of ${amount} for reason: {user_reason}"
    result = await refund_agent.run(prompt)
    
    # 2. Check the result type
    # We use result.output to get the structured response
    if isinstance(result.output, ApprovalRequest):
        # --- The PAUSE button ---
        job_id = str(uuid.uuid4())

        # KEY STEP: Serialize the entire conversation history
        # result.all_messages() contains User Prompt + Agent Thought + Tool Calls
        db.save_job(job_id, result.all_messages())

        # Return the job ID to the user
        return {
            "status": "APPROVAL_REQUESTED",
            "job_id": job_id,
            "details": result.output
        }
    
    elif isinstance(result.output, TransferSuccess):
        # --- The RESUME button ---
        return {
            "status": "COMPLETED",
            "details": result.output
        }
    
    return {"status": "UNKNOWN_RESULT", "details": str(result.output)}


# ==== END POINT 2 - MANAGER APPROVES ====

@app.post("/manager-review")
async def manager_review(decision: ManagerDecision):
    # 1. Retrieve the Frozen Memory
    history = db.get_job(decision.job_id)
    if not history:
        return {"error": "Job not found"}

    # 2. Construct the "Resume Signal"
    # We pretend the Manager is a "User" speaking to the Agent
    resume_prompt = (
        f"Manager reviewed the request. "
        f"Approved: {decision.approved}. "
        f"Comment: {decision.manager_comment}. "
        "If approved, proceed to final_transfer. If not, inform the user."
    )

    # 3. RESUME THE AGENT
    # We pass 'message_history=history'. The Agent "remembers" everything!
    result = await refund_agent.run(
        resume_prompt, 
        message_history=history
    )
    
    if isinstance(result.output, TransferSuccess):
        return {"status": "COMPLETED", "details": result.output}
    elif isinstance(result.output, ApprovalRequest):
        # If it asks for approval again (maybe manager denied, or agent is confused)
        return {"status": "APPROVAL_REQUESTED", "details": result.output}
    
    return {"status": "FINALIZED", "result": str(result.output)}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)