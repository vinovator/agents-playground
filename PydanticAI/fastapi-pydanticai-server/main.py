"""
We are building a web endpoint that takes a user's query, 
runs the agent (with database access), and returns a structured response.
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
import uvicorn
from dotenv import load_dotenv

# Load Env file
load_dotenv()

# --- 1. Define the shared data models (The Contract) ---
# Used by both FastAPI (to validate HTTP) and the Agent (to structure output)

class UserQuery(BaseModel):
    user_id: int
    question: str


class AgentResponse(BaseModel):
    answer: str
    confidence_score: float = Field(description="Confidence 0.0 to 1.0")
    requires_followup: bool


# --- 2. Define Dependencies (The Context) ---

class Database:
    """ A mock database """
    async def get_user_history(self, user_id:int) -> list[str]:
        # Simulate a DB lookup
        return ["User asked about the interest rates", "User checked the balance"]

    
@dataclass
class AppDependencies:
    db: Database
    user_id: int


# --- 3. Configure the PydanticAI Agent ---

agent = Agent(
    model="gemini-2.5-flash",
    deps_type=AppDependencies,
    output_type=AgentResponse, # Enforced structured output
    system_prompt="You are a helpful banking assistant. Use user history to personalize answers."
)

@agent.tool
async def get_user_history(ctx: RunContext[AppDependencies]) -> list[str]:
    """ Retrieves the user's previous interaction history """
    history = await ctx.deps.db.get_user_history(ctx.deps.user_id)
    return f"Previous interactions: {': '.join(history)}"


# --- 4. Create the FastAPI app ---

app = FastAPI()

# A FastAPI dependency to initialize our DB connection
# In real app, this would come from a database connection pool
async def get_db() -> Database:
    return Database()

@app.post("/ask", response_model=AgentResponse)
async def ask_agent(
    query: UserQuery,
    db: Database = Depends(get_db)
):
    """ 
    The Endpoint:
    1. Validates 'query' is valid JSON (UserQuery)
    2. Injects the DB dependency
    3. Runs the Agent
    4. Validates the Agent's output (AgentResponse)
    """

    # Initialize the specific context for this single run
    run_deps = AppDependencies(user_id=query.user_id, db=db)

    try:
        # Run the agent
        result = await agent.run(query.question, deps=run_deps)
        
        # Return strictly typed data directly
        return result.data

    except Exception as e:
        # PydanticAI handles retries internally, but if it fails ultimately, we raise an HTTP error
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    """
    To run: uvicorn main:app --reload
    Once above command is run, the server will be on "listening" mode
    you can access the API at http://127.0.0.1:8000 (localhost)
    since --reload is enabled, the server will automatically reload if any changes are made to the code
    Open this link in web browser to see the API documentation: http://127.0.0.1:8000/docs
    The JSON user query should be in the format: 
    {"user_id": 1, "question": "What is the interest rate?"}
    The response will be in the format: 
    {"answer": "The interest rate is 5%", "confidence_score": 0.9, "requires_followup": false}
    ALternative way to run is terminal command: 
    curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"user_id": 1, "question": "What is the interest rate?"}'
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


