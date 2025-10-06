import os
from . import config
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to read",
            ),
        },
    ),
)

def get_file_content(working_directory : str, file_path : str) -> str:
    try:
        working_directory = os.path.realpath(working_directory)
        full_path = os.path.realpath(os.path.join(working_directory, file_path))
        # Without this restriction, the LLM might go running amok anywhere on the
        # machine, reading sensitive files or overwriting important data.
        if not os.path.commonpath([working_directory, full_path]) == working_directory:
            # All of our "tool call" functions, including get_files_info, should
            # always return a string. If errors can be raised inside them, need
            # to catch those errors and return a string describing the error
            # instead. This will allow the LLM to handle the errors gracefully.
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content_string = ""
        with open(full_path, "r") as f:
            file_content_string = f.read(config.MAX_CHARS)

        if os.stat(full_path).st_size >= config.MAX_CHARS:
            file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string


    except Exception as e:
        return  f"Error: {e}"
