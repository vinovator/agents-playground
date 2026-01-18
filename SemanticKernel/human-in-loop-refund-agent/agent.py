import asyncio 

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.google.google_ai.services.google_ai_chat_completion import GoogleAIChatCompletion
from semantic_kernel.connectors.ai.google.google_ai.google_ai_prompt_execution_settings import GoogleAIPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory

# import Modules
import config
from plugins.refund_plugin import RefundPlugin

async def get_response_from_agent(user_input: str, chat_history: ChatHistory):
    """
    Initializes the kernel and processes the user input
    """

    # 1. Initialize the Kernel
    kernel = Kernel()
    
    # 2. Add the AI Service
    service = GoogleAIChatCompletion(
        service_id = config.SERVICE_ID,
        gemini_model_id = config.AI_MODEL_ID,
        api_key = config.GOOGLE_API_KEY
    )
    
    kernel.add_service(service)

    # 3. Add the plugin (import from plugins folder)
    kernel.add_plugin(RefundPlugin(), plugin_name="Refunds")

    # 4. Execution Settings
    settings = GoogleAIPromptExecutionSettings(
        service_id = config.SERVICE_ID,
        function_choice_behavior = FunctionChoiceBehavior.Auto()
    )

    # 5. Process Chat
    chat_history.add_user_message(user_input)

    try:
        response = await kernel.get_service(config.SERVICE_ID).get_chat_message_content(
            chat_history = chat_history,
            settings = settings,
            kernel = kernel
        )

        chat_history.add_assistant_message(str(response))
        return response.content

    except Exception as e:
        return f"Error invoking agent: {str(e)}"





    

