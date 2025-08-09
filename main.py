import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from config import SYSTEM_PROMPT

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
    is_verbose = flag == "--verbose"

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_file_content,
            schema_run_python_file,
            schema_get_files_info,
            schema_write_file,
        ]
    )
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT, tools=[available_functions]
    )

    if is_verbose:
        print(f"User prompt: {user_prompt}")
    response = client.models.generate_content(
        model=model, contents=messages, config=config
    )
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
