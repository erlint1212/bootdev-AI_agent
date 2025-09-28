import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    print("Hello from ai-agent!")

    match len(sys.argv):
        case 2:
            if not isinstance(sys.argv[1], str):
                raise Exception(f"Argument must be a string, input was: {type(sys.argv[1])}")
        case 1:
            raise Exception("No prompt given")
        case _:
            raise Exception("Too mangy arguments given")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    prompt = sys.argv[1] #"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    models = ["gemini-2.0-flash-001", "gemini-2.5-flash"]

    response = client.models.generate_content(
        model=models[0], contents=prompt
    )
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
