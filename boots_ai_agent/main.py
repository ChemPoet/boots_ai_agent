    
    
    # Putting all imports at the top lets anyone reading the file see its dependencies at a glance, ensures missing packages fail immediately `(ModuleNotFoundError)` before any other code runs.
import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

# Reusable code (functions, classes, constants) that other files might want to import should be defined at the top level of the file—outside of `def main():` and outside the `if __name__ == "__main__":` guard.

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
    # Now we can access `args.user_prompt` throughout 'main.py'.
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    # Now we can activate verbose outputs using the variable `args.verbose` either BEFORE or AFTER the user prompt.

def main():
    # print("Hello from boots-ai-agent!")
        
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No api key found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    # Conversation history == A list of messages
    #   Each message == dict['role':str,'content':str] 
    messages = [
        {"role": "user", "content": args.user_prompt},
    ]
            
    generate_content(client, messages)
    
def generate_content(client: OpenAI, messages: list) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    if response.usage == None:
        raise RuntimeError ("API request may have failed. Please try again.")
    
    if args.verbose is True:
        print("User prompt: ", args.user_prompt)
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print(f"Response:\n{response.choices[0].message.content}")
    else:
        print(f"Response:\n{response.choices[0].message.content}")

# Guard statement ensuring `main()` only runs when you execute the file directly, not when another script imports it.
if __name__ == "__main__":
    main()
