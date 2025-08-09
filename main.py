import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
# schemas
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

# Note to self. Always switch to .venv in the terminal before making changes

def main():
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    usage = "Usage: python main.py <User question to agent> [--verbose]"

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

    # system propmpt
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    if len(sys.argv) == 1:
        print("Error, no arguments given.")
        print(usage)
        sys.exit(1)

    # Capture all args except script name
    user_args = sys.argv[1:]

    # If verbose is in user arguments
    # Will continue being trues here despite us removing verbose from user input
    verbose = "--verbose" in user_args
    if verbose:
        while "--verbose" in user_args:
            user_args.remove("--verbose")

    # Now we join it
    user_prompt = " ".join(user_args)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                              contents=messages,
                                              config=types.GenerateContentConfig(
                                                  tools=[available_functions],
                                                  system_instruction=system_prompt)
                                              )

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # if the list is not empty
    if response.function_calls:
        list_of_responses = response.function_calls
        for function_call_part in list_of_responses:
            function_call_name = function_call_part.name
            function_call_args = function_call_part.args
            print(f"Calling function: {function_call_name}({function_call_args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
