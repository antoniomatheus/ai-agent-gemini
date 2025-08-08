import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    model = "gemini-2.0-flash-001"
    if len(sys.argv) < 2:
        print("Usage: uv run main.py [PROMPT]")
        sys.exit(1)

    user_prompt = sys.argv[1]
    
    flag = None
    if len(sys.argv) > 3:
        flag = sys.argv[2]
    is_verbose = (flag == "--verbose")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    if is_verbose:
        print(f"User prompt: {user_prompt}")
    response = client.models.generate_content(model=model, contents=messages)
    print(response.text)
    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
