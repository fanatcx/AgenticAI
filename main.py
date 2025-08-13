import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# schemas and definitions
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python import *
from functions.write_file import *

# -------- tool dispatcher ----------
def call_function(function_call_part, verbose=False):
    WORKING_DIRECTORY = "./calculator"

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    fname = function_call_part.name
    if verbose:
        print(f"Calling function: {fname}({function_call_part.args})")
    else:
        print(f" - Calling function: {fname}")

    if fname not in function_map:
        # return a tool error response
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fname,
                    response={"error": f"Unknown function: {fname}"}
                )
            ],
        )

    args = dict(function_call_part.args or {})
    args["working_directory"] = WORKING_DIRECTORY
    result = function_map[fname](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fname,
                response={"result": result}
            )
        ],
    )

# -------- one-step generation ----------
def generate_content(client, messages, tools, system_prompt, verbose=False):
    """Make one model call. 
    - Append model's content to messages.
    - If there are function calls, execute them and return None (conversation continues).
    - If there’s final text and no function calls, return that text (we're done)."""
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[tools],
            system_instruction=system_prompt
        )
    )

    if verbose:
        try:
            print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")
        except Exception:
            pass

    # Add the AI's content to history 
    if resp.candidates and resp.candidates[0].content:
        messages.append(resp.candidates[0].content)

    # If the model produced a plain text reply and no tool calls -> we're done
    if getattr(resp, "function_calls", None) in (None, [],):
        text = (resp.text or "").strip()
        if text:
            return text  # final text
        # No function calls and no text keep going, but avoid infinite loops
        return ""

    #Execute all, collect parts into ONE tool Content.
    tool_parts = []
    for fcall in resp.function_calls:
        tool_content = call_function(fcall, verbose=verbose)
        # tool_content is a Content(role="tool", parts=[...]); extend parts
        tool_parts.extend(tool_content.parts)

    # Append a single tool message with multiple parts
    messages.append(types.Content(role="tool", parts=tool_parts))
    return None  # continue loop

def main():
    print(f"Current directory: {os.getcwd()}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    usage = "Usage: python main.py <User question to agent> [--verbose]"

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths should be relative to the working directory. Do not include the working directory path in function calls; it is injected automatically.
"""

    if len(sys.argv) == 1:
        print("Error, no arguments given.")
        print(usage)
        sys.exit(1)

    user_args = sys.argv[1:]
    verbose = "--verbose" in user_args
    while "--verbose" in user_args:
        user_args.remove("--verbose")

    user_prompt = " ".join(user_args)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    MAX_ITERS = 15
    iters = 0

    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_text = generate_content(
                client=client,
                messages=messages,
                tools=available_functions,
                system_prompt=system_prompt,
                verbose=verbose,
            )

            if final_text is None:
                # Tool call path; continue the loop
                continue

            # Got some text; empty string means "model said nothing" — keep looping once more
            if final_text.strip():
                print(final_text)
                break

        except Exception as e:
            print(f"Error in conversation loop: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    main()