import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.abspath(working_directory)
    joined_abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    # For extra security, add os.path.sep so that .startswith captures up to '/' and not a short word like 'calc'
    if not joined_abs_file.startswith(abs_path + os.path.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(joined_abs_file):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cp = subprocess.run(
            ['python', joined_abs_file] + args,
            cwd=abs_path,
            timeout=30,
            capture_output=True,
            text=True
        )

        output_parts = []

        if cp.stdout.strip():
            output_parts.append("STDOUT:\n" + cp.stdout.rstrip())
        if cp.stderr.strip():
            output_parts.append("STDERR:\n" + cp.stderr.rstrip())
        if cp.returncode != 0:
            output_parts.append(f"Process exited with code {cp.returncode}")


        if not output_parts:
            return "No output produced."

        return "/n".join(output_parts)

    except Exception as e:
        # Catch any exceptions (e.g. TimeoutExpired, FileNotFoundError etc).
        return f"Error: executing Python file: {e}"

