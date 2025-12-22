from typing import Union
from pydantic_ai import Agent, RunContext
from app.models import ApprovalRequest, TransferSuccess

# a fake bank API
async def process_bank_transfer(amount: float):
    print(f"Bank API: Processing transfer of ${amount}")
    return True

# The Agent can return EITHER a request for help OR a succes
refund_agent = Agent(
    model='gemini-2.5-flash',
    # We use a Union so the Agent can choose what to return
    output_type=Union[ApprovalRequest, TransferSuccess], 
    system_prompt=(
        "You are a refund processor. "
        "If refund > $50, you cannot process it yourself. You must return an ApprovalRequest with the reason. "
        "If refund < $50, you can approve it. Call the final_transfer tool and return TransferSuccess."
    )
)

@refund_agent.tool
async def final_transfer(ctx: RunContext, amount: float) -> str:
    """
    Process the transfer. 
    Only call this tool if the refund amount is < $50, OR if you have received explicit approval from a manager.
    """
    await process_bank_transfer(amount)
    return "Transfer processed successfully"