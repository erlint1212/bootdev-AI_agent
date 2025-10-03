import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import config

def verbose_print(user_prompt, response) -> None:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main() -> None:
    print("Hello from ai-agent!")

    """
    match len(sys.argv):
        case 2:
            if not isinstance(sys.argv[1], str):
                raise Exception(f"Argument must be a string, input was: {type(sys.argv[1])}")
        case 1:
            raise Exception("No prompt given")
        case _:
            raise Exception("Too mangy arguments given")
    """

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

    response = client.models.generate_content(
        model=models[0], 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=config.SYSTEM_PROMPT)
    )
    print(response.text)
    if args.verbose:
        verbose_print(args.user_prompt, response)


if __name__ == "__main__":
    main()
