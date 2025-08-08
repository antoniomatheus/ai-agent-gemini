import os

def get_files_info(working_directory, directory="."):
    try:
        path = os.path.join(working_directory, directory)
        abs_path = os.path.abspath(path)
        directory_txt = f"'{directory}'" if directory != "." else "current"
        files_info = f"Result for {directory_txt} directory:\n"

        if not abs_path.startswith(os.path.abspath(working_directory)): 
            return files_info + f'    Error: Cannot list "{path}" as it is outside the permitted working directory'
        if not os.path.isdir(path):
            return files_info + f'    Error: "{path}" is not a directory'
        
        dir_list = os.listdir(path)
        files_info = f"Result for {directory_txt} directory:\n"
        for item in dir_list:
            item_path = os.path.join(path, item)
            is_dir = os.path.isdir(item_path)
            files_info += f" - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={is_dir}\n"

        return files_info.strip()
    except Exception as e:
        return f"Error: {e}"