from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from config import WORKING_DIRECTORY


def call_function(function_call, verbose=False):
    name = function_call.name
    args = function_call.args

    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")
    
    result = None
    match name:
        case "get_file_content":
            result = get_file_content(WORKING_DIRECTORY, **args)
        case "get_files_info":
            result = get_files_info(WORKING_DIRECTORY, **args)
        case "run_python_file":
            result = run_python_file(WORKING_DIRECTORY, **args)
        case "write_file":
            result = write_file(WORKING_DIRECTORY, **args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=name,
                        response={"error": f"Unknown function: {name}"}
                    )
                ]
            )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result}
            )
        ]
    )
