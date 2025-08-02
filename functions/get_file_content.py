import os
import config

def get_file_content(working_directory, file_path):

    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    joined_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not joined_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(joined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    try:

        with open(joined_path, "r") as f:
            # define a max
            MAX = config.MAX_CHARS

            # read one more than max
            content = f.read(MAX + 1)

            if len(content) > MAX:
                # replace last character with empty string. #10001
                truncated = content[:MAX]
                return f'{truncated}[...File "{file_path}" truncated at {MAX} characters]'
            
            else:
                return content
            
    except Exception as e:
        return f"Error: Could not read file: {e}"
