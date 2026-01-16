import os
import asyncio
from dotenv import load_dotenv

# Import the Kernel
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.google.google_ai.services.google_ai_chat_completion import GoogleAIChatCompletion
from semantic_kernel.connectors.ai.google.google_ai.google_ai_prompt_execution_settings import GoogleAIPromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory

load_dotenv() 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_5")

#model  = "gemini-2.5-flash"
MODEL = "gemini-3-flash-preview"

async def main():
    # The Kernel - Operating System for AI
    kernel = Kernel()

    # The Service 
    gemini_service = GoogleAIChatCompletion(
        service_id = "gemini-chat", 
        gemini_model_id = MODEL,
        api_key = GEMINI_API_KEY
        )
    
    # Add the service to the kernel
    kernel.add_service(gemini_service)

    # The Context/ History
    # Initialize the chat history with a system persona
    history = ChatHistory()
    history.add_system_message("""
    You are a helpful assistant that translates everything the user says into 
    17th century pirate speak. Arr !
    """)

    print("Pirate bot initialized! (Type 'exit' to quit)")
    print("-" * 20)

    # Start the chat loop
    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "exit":
            print("Pirate Bot: Fair winds to ye !")
            break

        # Add the user input to the chat history
        history.add_user_message(user_input)

        # Invoke the service
        # We ask the kernel to get a completion from the service
        try:
            result = await kernel.get_service("gemini-chat").get_chat_message_content(
                chat_history = history,
                settings = GoogleAIPromptExecutionSettings() 
                )

            # Print the result and add it to the chat history
            print(f"Pirate Bot: {result}")
            history.add_assistant_message(str(result))

        except Exception as e:
            print(f"Error: {e}")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())