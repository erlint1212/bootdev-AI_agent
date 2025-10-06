import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import config
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def call_function(function_call_part : types.FunctionCall, verbose : bool = False) -> types.Content:
    if not verbose:
        print(f" - Calling function: {function_call_part.name}")
    else:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    function_result = ""
    
    match function_call_part.name:
        case "get_files_info":
            function_result = get_files_info(
                    working_directory=config.WORKING_DIRECTORY, 
                    **function_call_part.args
                    )

        case "get_file_content":
            function_result = get_file_content(
                    working_directory=config.WORKING_DIRECTORY, 
                    **function_call_part.args
                    )

        case "run_python_file":
            function_result = run_python_file(
                    working_directory=config.WORKING_DIRECTORY, 
                    **function_call_part.args
                    )

        case "write_file":
            function_result = write_file(
                    working_directory=config.WORKING_DIRECTORY, 
                    **function_call_part.args
                    )

        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )

    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )
    

def verbose_print(user_prompt : str, response : types.GenerateContentResponse) -> None:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main() -> None:
    print("Hello from ai-agent!")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "user_prompt",
        type=str,
        help="The input string"
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_true"
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    models = ["gemini-2.0-flash-001", "gemini-2.5-flash"]

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    response = client.models.generate_content(
        model=models[0], 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=config.SYSTEM_PROMPT
            )
    )

    functions_called = response.function_calls

    print(response.text)

    if len(functions_called) != 0:
        for function_call_part in functions_called: 
            function_call_result = call_function(function_call_part, verbose = args.verbose)

            try:
                test = function_call_result.parts[0].function_response.response
            except (AttributeError, IndexError, TypeError) as e:
                raise FatalContentError(
                    f"Invalid Content structure — expected content.parts[0].function_response.response, got error: {e}"
                )

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    if args.verbose:
        print()
        verbose_print(args.user_prompt, response)


if __name__ == "__main__":
    main()
