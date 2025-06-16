import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from pydantic_core.core_schema import url_schema

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():

    verbose = False
    args = sys.argv

    if len(args) < 2:
        print("Error: No message provided")
        sys.exit(1)

    if len(args) > 2:
        if args[2] == "--verbose":
            verbose = True

    user_prompt = args[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages)

    print(response.text)

    metadata = response.usage_metadata

    if verbose and metadata is not None:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

if __name__ == "__main__":
    main()


