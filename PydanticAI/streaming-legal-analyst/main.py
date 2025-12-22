import os
import asyncio
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from pydantic_ai import Agent

# 1. FIXED IMPORT: Use GoogleModel instead of GeminiModel
from pydantic_ai.models.google import GoogleModel

import uvicorn
from dotenv import load_dotenv
from typing import List

load_dotenv()

# --- 2. FIXED: Setup the Google Model ---
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing in .env file")

# Use the correct class (GoogleModel) and a valid model name (gemini-2.5-flash)
model = GoogleModel('gemini-2.5-flash')

# --- 3. Define the Data Models ---
class ContractAnalysis(BaseModel):
    summary: str
    risk_score: int = Field(description="Risk level from 0 to 10")
    flagged_items: List[str]

# --- 4. Define the Agent ---
legal_analyst_agent = Agent(
    model=model,                  
    output_type=ContractAnalysis, 
    system_prompt=(
        "You are an expert legal analyst. Analyze the user's contract clause. "
        "Explain the risks clearly."
    )
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 5. Mock Database ---
class Database:
    async def save_analysis(self, clause: str, analysis: ContractAnalysis):
        print(f"💾 DATABASE: Saved analysis | Risk Score: {analysis.risk_score}")
        return True

db = Database()

# --- 6. The Streaming Logic ---
async def stream_contract_analysis(contract_clause: str):
    
    # We use run_stream to keep the connection open
    async with legal_analyst_agent.run_stream(contract_clause) as result_stream:
        
        final_result = None

        # A. Stream Partial Data (The "Thinking" Process)
        async for partial_result in result_stream.stream_output():
            final_result = partial_result
            # Dump the partial model to JSON so the frontend can read it live
            chunk_data = partial_result.model_dump(mode='json', exclude_unset=True)
            yield f"event: partial\ndata: {json.dumps(chunk_data)}\n\n"

        # B. Get Final Validated Data
        # If you streamed to completion, `final_result` is already the final validated object.
        # But for safety (in case nothing was yielded), fall back to get_output().
        if final_result is None:
            final_result = await result_stream.get_output()

        # C. Save to Database
        await db.save_analysis(contract_clause, final_result)

        # D. Send Final Event
        yield f"event: final_result\ndata: {final_result.model_dump_json()}\n\n"

# --- 7. The Endpoint ---
class AnalysisRequest(BaseModel):
    contract_clause: str

@app.post("/analyze-stream")
async def analyze_clause(request: AnalysisRequest):
    return StreamingResponse(
        stream_contract_analysis(request.contract_clause),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"} #To reduce buffering issues
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)