import os
from functions.aux import is_outside_allowed_dir

def write_file(working_directory, file_path, content):
    try:
        path = os.path.join(working_directory, file_path)

        if is_outside_allowed_dir(working_directory, path):
            return (f'Error: Cannot write to "{file_path}" as it is '
                    'outside permitted working directory')
        
        with open(path, "w") as f:
            f.write(content)
        
        return (f'Successfully wrote to "{file_path}" ({len(content)}'
                ' characters written)')
    except Exception as e:
        return f"Error: {e}"
