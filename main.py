import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    usage = "Usage: python main.py <User question to agent> [--verbose]"

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

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # This text is the response from the AI
    print(response.text)

if __name__ == "__main__":
    main()
