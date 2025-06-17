import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info, get_file_content, write_file
from functions.run_python import run_python_file

MAX_ITERATIONS = 20

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The full path to the file to open.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The full path to the python file to run.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write a file in specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the full path for the file to write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to write to the file, in string format",
            ),
        },
    ),
)



function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
        }

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    func_name = function_call_part.name
    args = dict(function_call_part.args)

    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {func_name}({args})")
    else:
        print(f" - Calling function: {func_name}")

    func = function_map.get(func_name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    try:
        res = func(**args)
    except Exception as e:
        res = f"Error: {e}"
        
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": res},
            )
        ],
    )



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
    iterations = 0
    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            ]

    while iterations < MAX_ITERATIONS:

        response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[available_functions]),
                            )

        for cand in getattr(response, "candidates", []):
            if hasattr(cand, "content") and cand.content:
                messages.append(cand.content)

        func_calls = response.function_calls
        function_called = False

        func_responses = []
        if func_calls: 
            for call in func_calls:
                func_call_res = call_function(call, verbose)

                func_responses.append(func_call_res)
                function_called = True

                if (
                    func_call_res.parts and
                    hasattr(func_call_res.parts[0], "function_response") and
                    func_call_res.parts[0].function_response is not None and
                    hasattr(func_call_res.parts[0].function_response, "response") and
                    func_call_res.parts[0].function_response.response is not None
                ):
                    if verbose:
                        print(f"-> {func_call_res.parts[0].function_response.response}")

                messages.extend(func_responses)

        if not function_called:
            print("Final response:")
            print(response.text)

            metadata = response.usage_metadata
            if verbose and metadata is not None:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {metadata.prompt_token_count}")
                print(f"Response tokens: {metadata.candidates_token_count}")

            break

        iterations += 1




if __name__ == "__main__":
    main()


