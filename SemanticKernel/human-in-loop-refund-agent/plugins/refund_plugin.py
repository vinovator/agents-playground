from semantic_kernel.functions import kernel_function

import config # Import Business Rules

from database import create_refund_request, get_pending_approvals, update_refund_status


class RefundPlugin:
    """
    A plugin that exposes refund processing functions to the Semantic Kernel.
    """

    @kernel_function(
        description = "Processes a refund request. Use this when user asks for a refund.",
        name = "process_refund"
    )
    def process_refund(self, user_id: str, reason: str, amount: float) -> str:
        """
        Processes a refund request. Handles the logic for auto-approval vs human approval.
        """
        print(f"\nProcessing refund for user {user_id} for amount {amount} due to {reason}")
        
        # Business Logid:
        if amount < config.REFUND_AUTO_APPROVE_LIMIT:
            # Auto-approve small refunds
            create_refund_request(user_id, reason, amount, "APPROVED")
            return f"Refund of {config.CURRENCY_SYMBOL}{amount} for {reason} has been approved automatically."
        else:
            # Human-in-loop Trigger
            create_refund_request(user_id, reason, amount, "PENDING APPROVAL")
            return (f"Approval required: The amount {config.CURRENCY_SYMBOL}{amount} "
            f"exceeds the auto-approval limit of {config.REFUND_AUTO_APPROVE_LIMIT}. "
            f"Manager has been notified.")