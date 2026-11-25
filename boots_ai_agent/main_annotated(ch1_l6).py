# Putting all imports at the top lets anyone reading the file see its dependencies at a glance, ensures missing packages fail immediately `(ModuleNotFoundError)` before any other code runs.
    # `argparse` module facilitates command-line interfacing: reading, interpreting, and assigning user typed terminal inputs.
    # `os` module enables script to access and interact with operating system directories.
import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

# Reusable code (functions, classes, constants) that other files might want to import should be defined at the top level of the file—outside of `def main():` and outside the `if __name__ == "__main__":` guard.

def main():
    # print("Hello from boots-ai-agent!")
    parser = argparse.ArgumentParser(description="Chatbot")
    # Create `parser` object. 'description' == helpful summary displayed when 'main.py' is run with `--help` or `-h` flags.
        # `ArgumentParser` has built-in arguments available (e.g., "description"). Custom arguments are added using `parser.add_argument()`.
    parser.add_argument("user_prompt", type=str, help="User prompt")
    # Register unique positional argument `user_prompt`. The `argparse` module expects "unique positional arguments" to be passed (without flags) in the same order that they are defined.
    ''' Now we can access `args.user_prompt` throughout 'main.py'. '''
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    # Registers the **optional flag** `verbose`. Because it starts with `--`, the user does not **have to** include it when running the `main.py` script.
        # Now we can activate verbose outputs using the variable `args.verbose` either BEFORE or AFTER the user prompt.
    args = parser.parse_args()
    '''NB!! Define all parser arguments before placing "parse_args()" fxn call!!'''
    # User inputs from the terminal are transformed into `argparse.Namespace` objects.
        # The `parse_args()` segment attaches our previously defined `add_arguments` (e.g., `user_prompt`, `verbose`) onto the `parser` object in the appropriate `Namespace` ordering for further use.


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
            
    generate_content(client, messages, args.user_prompt, args.verbose)
    
    
def generate_content(client: OpenAI, messages: list, user_prompt: str, verbose: bool) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    if response.usage == None:
        raise RuntimeError ("API request may have failed. Please try again.")
    
    if verbose is True:
        print("User prompt: ", {user_prompt})
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print(f"Response:\n{response.choices[0].message.content}")
        
    else:
        print(f"Response:\n{response.choices[0].message.content}")

# Guard statement ensuring `main()` only runs when you execute the file directly, not when another script imports it.
if __name__ == "__main__":
    main()
