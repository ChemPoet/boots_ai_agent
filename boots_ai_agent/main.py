# Putting all imports at the top lets anyone reading the file see its dependencies at a glance, ensures missing packages fail immediately `(ModuleNotFoundError)` before any other code runs.
import os
from dotenv import load_dotenv
from openai import OpenAI


# Reusable code (functions, classes, constants) that other files might want to import should be defined at the top level of the file—outside of `def main():` and outside the `if __name__ == "__main__":` guard.

def main():
    print("Hello from boots-ai-agent!")
    
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No api key found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ],
    )

    print(response.choices[0].message.content)

# Guard statement ensuring `main()` only runs when you execute the file directly, not when another script imports it.
if __name__ == "__main__":
    main()
