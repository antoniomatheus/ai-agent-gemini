import os
import subprocess
from google.genai import types
from functions.aux import is_outside_allowed_dir


def run_python_file(working_directory, file_path, args=[]):
    try:
        path = os.path.join(working_directory, file_path)

        if is_outside_allowed_dir(working_directory, path):
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the '
                "permitted working directory."
            )

        if not os.path.isfile(path):
            return f'Error: File "{file_path}" not found.'

        if not path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            ["python3", file_path, *args],
            timeout=30,
            cwd=working_directory,
            capture_output=True,
            text=True,
        )
        output_msg = ""

        if completed_process.returncode != 0:
            output_msg += f"Process exited with code {completed_process.returncode}\n"
        if completed_process.stdout:
            output_msg += f"STDOUT:\n{completed_process.stdout}\n"
        if completed_process.stderr:
            output_msg += f"STDERR:\n{completed_process.stderr}"
        if len(output_msg) == 0:
            output_msg += "No output produced."

        return output_msg
    except Exception as e:
        return f"Error: executing python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified python file, constrained by the working directory and allowing arguments to be passed to the file's execution.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An array with the arguments that will be passed to the file that will be executed. If not provided, no argument is provided to the execution.",
            ),
        },
    ),
)
