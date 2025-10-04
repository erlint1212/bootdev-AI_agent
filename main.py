import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import config
from functions.get_files_info import schema_get_files_info

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
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    if args.verbose:
        verbose_print(args.user_prompt, response)


if __name__ == "__main__":
    main()
