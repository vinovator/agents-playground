import os
from dotenv import load_dotenv, find_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load Secrets
success = load_dotenv(find_dotenv())

if success:
    print("Secrets loaded successfully")
    print(os.getenv("GEMINI_API_KEY"))
    
else:
    print("Failed to load secrets")

# Setup the brains

# Manager (Cloud - High Intelligence)
manager_llm = LLM(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Worker (Local - Privay & Free Compute)
worker_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# Define Workers (Using Local LLM)
# Note - Manager Agent is not defined, CrewAI will spawn it automatically

market_analyst_agent = Agent(
    role="Market Analyst",
    goal="Analyse Market demand and competitors.",
    backstory="You are a sharp business analyist. You demand data before believing any hype.",
    verbose=True,
    llm=worker_llm,
    allow_delegation=False
)

tech_analyst_agent = Agent(
    role="CTO",
    goal="Assess techical feasibility.",
    backstory="You are an expert technologist and CTO. you judge if the idea is technologically feasible.",
    verbose=True,
    llm=worker_llm,
    allow_delegation=False
)

# Define the high-level goal. 
# We give the goal to the manager, not the workers.

task_validate = Task(
    description = """
    Validate the startup idea: 'A market for 20000 GBP human-sized and human-looking robot that can be trained to perform household chores, and manual tasks inside a household or indoor industry or businesses'    
    1. Ask the "Market Analyst" to investigate if there is market for this idea.
    2. Ask the "CTO" to check if the idea is technologically feasible.
    3. Synthesize their answers into a final Go/No-Go decision.
    """,
    expected_output = "A final executive summary with Go/No-Go decision.",
    # No agent assigned here. The Manager will handle it.
)

# The Hierarchical crew

crew = Crew(
    agents=[market_analyst_agent, tech_analyst_agent], # The workers
    tasks=[task_validate], # high-level goal
    process=Process.hierarchical, # Boss Mode activated
    manager_llm=manager_llm, # Uses cloud API
    verbose=True
)

print("### Starting the Crew ###")
print("-------------------------")

result = crew.kickoff()
print("\n#################\n")
print(result)
print("#################\n")
