import os
from google.genai import types
from functions.aux import is_outside_allowed_dir


def write_file(working_directory, file_path, content):
    try:
        path = os.path.join(working_directory, file_path)

        if is_outside_allowed_dir(working_directory, path):
            return (
                f'Error: Cannot write to "{file_path}" as it is '
                "outside permitted working directory"
            )

        with open(path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a specified file, creating the file if it does not exist, or overwriting the contents of an existing file. Write is contrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that the contents will be written to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents that will be written to the specified file.",
            ),
        },
    ),
)
