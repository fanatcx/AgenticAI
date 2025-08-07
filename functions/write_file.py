import os

def write_file(working_directory, file_path, content):
    # Step 1: Resolve absolute paths
    absolute_path = os.path.abspath(working_directory)
    joined_abs_path = os.path.abspath(os.path.join(absolute_path, file_path))

    # Step 2: Prevent directory traversal
    if not joined_abs_path.startswith(absolute_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        # Step 3: Ensure the parent directory exists
        parent_dir = os.path.dirname(joined_abs_path)
        os.makedirs(parent_dir, exist_ok=True)

        # Step 4: Check if the target path is a directory
        if os.path.isdir(joined_abs_path):
            return f'Error: Cannot write to "{file_path}" because it is a directory'

        # Step 5: Write content to file (create or overwrite)
        print(f'Writing file to.. "{joined_abs_path}"')
        with open(joined_abs_path, 'w') as f:
            f.write(content)

        return f'Successfully wrote to \"{file_path}\" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'
