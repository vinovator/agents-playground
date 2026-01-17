import asyncio
import os
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.google.google_ai.services.google_ai_chat_completion import GoogleAIChatCompletion
from semantic_kernel.connectors.ai.google.google_ai.google_ai_prompt_execution_settings import GoogleAIPromptExecutionSettings
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory

load_dotenv() 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_5")

#model  = "gemini-2.5-flash"
MODEL = "gemini-2.5-flash"

# -- 1. Define the plugin (The Tools) --
class SmartHomePlugin:
    """
    A plugin for controlling smart home devices.
    """
    @kernel_function(description="Turns on the lights in a specific room", name="turn_on_lights")
    def turn_on_light(self, room_name: str) -> str:
        # In real app, we would call an IOT API here
        print(f"\n[HARDWARE ACTION] Turning on the lights in {room_name}")
        return f"Turned on the lights in {room_name}"
    
    @kernel_function(description="Turns off the lights in a specific room", name="turn_off_lights")
    def turn_off_light(self, room_name: str) -> str:
        print(f"\n[HARDWARE ACTION] Turning off the lights in {room_name}")
        return f"Turned off the lights in {room_name}"
    
    @kernel_function(description="Sets the thermostat temperature", name="set_temperature")
    def set_temperature(self, room_name: str, degrees: int) -> str:
        print(f"\n[HARDWARE ACTION] Setting the temperature to {degrees} degrees Celsius in {room_name}")
        return f"Set the temperature to {degrees} degrees Celsius in {room_name}"


async def main():

    # -- 2. Setup Kernel and Service --
    kernel = Kernel()

    service = GoogleAIChatCompletion(
        service_id = "gemini-chat",
        gemini_model_id = MODEL,
        api_key = GEMINI_API_KEY
    )
    
    kernel.add_service(service)

    # -- 3. Register the Plugin --
    # We import the class and create an instance of it
    kernel.add_plugin(SmartHomePlugin(), plugin_name="SmartHome")

    # -- 4. Configure Auto Tool Calling --
    # This tells the LLM to automatically use tools when needed
    settings = GoogleAIPromptExecutionSettings(
        service_id = "gemini-chat",
        function_choice_behavior = FunctionChoiceBehavior.Auto()
    )

    history = ChatHistory()
    history.add_system_message("""
    You are a smart home assistant that controls smart home devices.
    """)

    print("Smart Home Agent Ready! (Try: 'Its dark in the kitchen!'; Type 'exit' to quit)")
    print("-" * 80)

    # Start the Chat Loop
    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "exit":
            print("Smart Home Agent: Goodbye!")
            break

        history.add_user_message(user_input)

        # -- 5. Invoke the Tools --
        # The Kernel will:
        # 1. Send your text to Gemini
        # 2. Gemini will decide if it needs to use a tool
        # 3. If yes, it tells the Kernel which tool and what arguments
        # 4. Kernel executes the tool and sends the result back to Gemini
        # 5. Gemini generates the final answer

        try:
            result = await kernel.get_service("gemini-chat").get_chat_message_content(
                chat_history = history,
                settings = settings,
                kernel = kernel
            )

            print(f"Smart Home Agent: {result}")
            history.add_assistant_message(str(result))

        except Exception as e:
            print(f"Error: {e}")
            history.add_assistant_message(f"Error: {e}")

# Run the main function
if __name__ == "__main__":
    """
    How to Test It
    Run the script and try these inputs. Watch the console for the [HARDWARE ACTION] 
    logs—that is your Python code running!

    Direct Command:
    User: "Turn on the lights in the living room." Result: [HARDWARE ACTION]
     Lights turned ON...

    Indirect Command (The "Semantic" part):
    User: "It's getting really dark in the kitchen so I can't cook." 
    Result: The agent infers it needs to turn on the kitchen light.

    Multi-Step Command:
    User: "I'm going to bed in the bedroom. Make it 20 degrees and turn off the lights." 
    Result: It should trigger two separate actions: set_temperature AND turn_off_light.
    """
    asyncio.run(main())
    