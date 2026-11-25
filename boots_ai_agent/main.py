
import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI



def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No api key found.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
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

if __name__ == "__main__":
    main()
