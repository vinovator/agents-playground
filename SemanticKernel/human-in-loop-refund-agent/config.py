# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# AI Settings
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
# AI_MODEL_ID = "gemini-2.5-flash"
# AI_MODEL_ID = "gemini-3.0-flash-preview"
AI_MODEL_ID = "gemini-2.5-flash-lite"
SERVICE_ID = "gemini_chat"

# Business Rules
REFUND_AUTO_APPROVE_LIMIT = 50.0  # Threshold for human intervention
CURRENCY_SYMBOL = "$"