import os

def is_outside_allowed_dir(allowed_dir, path):
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(os.path.abspath(allowed_dir)): 
        return True
    return False
