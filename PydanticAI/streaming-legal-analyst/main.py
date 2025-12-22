"""
Usecase to showcase "Streaming" capabilities of PydanticAI
Pydantic AI provides a specialized method agent.run_stream() to stream the output of the agent.
Usecase:
- Streaming Legal Analyst
- Tool for lawyers. 
- Lawyers paste complex contract clause, and the AI must explain it and flag risks.
- Legal is verbose. LLM might take 20 seconds to generate a full analysis. 
- Busy laywer needs to see the analysis as it progresses. 
- we need final output to contain strict risk_score (int) and citations (List) to 
- save into case management database
- Hybrd Approach 
    - Stream the text explanation for the human
    - but return the structured data for the machine
"""

import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from pydantic_ai import Agent
import uvicorn
from dotenv import load_dotenv
from typing import List

# Load Env file
load_dotenv()

# --- 1. The Setup ---
class ContractAnalysis(BaseModel):
    summary: str
    risk_score: int = Field(description="Risk level from 0 to 10")
    flagged_items: List[str]


# Define the agent
legal_analyst_agent = Agent(
    model="gemini-2.5-flash",
    output_type=ContractAnalysis,
    system_prompt=(
        "You are an expert legal analyst. Analyze the user's contract clause."
        "Explain the risks clearl"
    )
)

app = FastAPI()


# --- 2. The Streaming Logic ---
async def stream_contract_analysis(contract_clause: str):
    """
    This is an Async Generator.
    It yields chunks of the analysis as they are generated.
    """
    
    # using run_stream() instead of run() ensures we get streaming output
    async with legal_analyst_agent.run_stream(contract_clause) as result_stream:

        # A. Stream the text (The Thinking Process)
        # Loop over stream. PydanticAI will yield chunks of the output as they are generated.
        # async for chunk in result_stream.stream_text():
        #     # We format it as server side event (data:...)
        #     yield f"data: {chunk.text}\n\n"

        # B. Stream the final structured Data
        # Once the text stream finishes, PydanticAI validates the final output
        # This guaranttees we will still get our strict "ContractAnalysis" model
        final_result = await result_stream.get_output()

        # We send a special event to signal the end of the stream
        yield f"event: final_result\n\n"
        yield f"data: {final_result.model_dump_json()}\n\n"


# --- 3. The Endpoint ---
class AnalysisRequest(BaseModel):
    contract_clause: str

@app.post("/analyze-stream")
async def analyze_clause(request: AnalysisRequest):
    """
    Endpoints that return StreamingResponse allow the 
    conection to stay open and stream the output as it is generated.
    """
    return StreamingResponse(
        stream_contract_analysis(request.contract_clause),
        media_type="text/event-stream" # Standard MIME type for Server-Sent Events (SSE)
    )



if __name__ == "__main__":
    """
    Workflow
    - The lawyer hits the analyze button
    
    Connection Opens
    - The frontend calls POST/analyze-stream 
    - FastAPI sees StreamingResponse and opens a connection
    - It does not close the connection and hands control over to Async Generator function (stream_contract_analysis)

    The Context
    - aync with legal_analyst_agent opens the connection to LLM agent
    - with async for chunk loop, as the LLM thinks the next word, PydanticAI receives it and hands it to our loop
    - This happens multiple times creating a illusion of typing.

    Validation Barrier
    - Standard streaming is risky. What if LLM talks non-sense. 
    - PyndanticAI - even though we streaming text, the framework is silently accumulating the full response in background.
    - when the stream finishes, the line await result_stream.get_data()  is run
    - with this PydanticAI takes the complete generated text and forces it into our Contract Analysis model
    - Then the valid, safe JSON is sent as final payload to the frontend
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







