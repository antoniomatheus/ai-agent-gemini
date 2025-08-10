import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function
from config import SYSTEM_PROMPT, MAX_AGENT_LOOP

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    model = "gemini-2.0-flash-001"
    if len(sys.argv) < 2:
        print("Usage: uv run main.py [PROMPT]")
        sys.exit(1)

    user_prompt = sys.argv[1]

    is_verbose = False
    if len(sys.argv) >= 3:
        is_verbose = sys.argv[2] == "--verbose"

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_file_content,
            schema_run_python_file,
            schema_get_files_info,
            schema_write_file,
        ]
    )

    thinking_config = types.ThinkingConfig(
        include_thoughts=False,
        thinking_budget=0
    )
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[available_functions],
        thinking_config=thinking_config
    )

    if is_verbose:
        print(f"User prompt: {user_prompt}")

    loop = MAX_AGENT_LOOP
    break_loop = False

    while loop > 0:
        try:
            response = client.models.generate_content(
                model=model, contents=messages, config=config
            )
            
            for candidate_response in response.candidates:
                messages.append(candidate_response.content)
            
            if break_loop:
                break

            if response.function_calls:
                for function_call in response.function_calls:
                    result = call_function(function_call, is_verbose)
                    if not result.parts[0].function_response.response:
                        raise Exception("No response from function call.")
                    else:
                        messages.append(result)
                        if is_verbose:
                            print(f"-> {result.parts[0].function_response.response}")
            else:
                print(f"Final response: {response.candidates[0].content.parts[0].text}")
                break

            if is_verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

            loop -= 1

        except Exception as e:
            print(f"Something wrong occured: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
