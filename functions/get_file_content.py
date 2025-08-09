import os
from google.genai import types
from functions.aux import is_outside_allowed_dir
from config import MAX_CHAR_OUTPUT

def get_file_content(working_directory, file_path):
    try:
        path = os.path.join(working_directory, file_path)

        is_outside_work_dir = is_outside_allowed_dir(working_directory, path) 
        if is_outside_work_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(path):
            return f"Error: File not found or is not a regular file: \"{path}\""
        
        with open(path, "r") as f:
            file_contents = f.read()
            if len(file_contents) > MAX_CHAR_OUTPUT:
                truncate_msg = f'[...File "{path}" truncated at {MAX_CHAR_OUTPUT} characters]'
                file_contents = file_contents[:MAX_CHAR_OUTPUT] + truncate_msg
            return file_contents
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Return the content of a specified file, constrained to the working directory and with a maximum length of {MAX_CHAR_OUTPUT} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will be read, relative to the working directory.",
            )
        },
    ),
)