"""
The Database Model (State Storage) and Data Models
"""
from typing import List, Optional
from pydantic import BaseModel 
from pydantic_ai.messages import ModelMessage

# 1. The "Pause" object
class ApprovalRequest(BaseModel):
    amount: float
    reason: str
    status: str = "WAITING_FOR_APPROVAL"

# 2. The "Success" object
class TransferSuccess(BaseModel):
    amount: float
    status: str = "COMPLETED"

# 3. Manager Decision
class ManagerDecision(BaseModel):
    job_id: str
    approved: bool
    manager_comment: str

# In memory "Database" for this tutorial
# In production, use PostgreSQL, Redis, or any other database
class JobStore:
    def __init__(self):
        self.jobs = {}

    def save_job(self, job_id: str, messages: List[ModelMessage]):
        self.jobs[job_id] = messages

    def get_job(self, job_id: str) -> Optional[List[ModelMessage]]:
        return self.jobs.get(job_id)

db = JobStore()