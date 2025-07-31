import os

def get_files_info(working_directory, directory="."):
    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    joined_dir = os.path.abspath(os.path.join(working_directory, directory))
    files_info_list = []

    # Security check: directory must be inside working_directory
    if not joined_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Check if target is actually a directory
    if not os.path.isdir(joined_dir):
        return f'Error: "{directory}" is not a directory'

    # Build file info
    for item in os.listdir(joined_dir):
        full_path = os.path.join(joined_dir, item)
        is_dir = os.path.isdir(full_path)

        try:
            size = os.path.getsize(full_path)
            files_info_list.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        except OSError as e:
            files_info_list.append(f"- {item}: Error retrieving size: {e}, is_dir={is_dir}")

    return "\n".join(files_info_list)
