import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        file_name = os.path.basename(file_path)
        if file_name.split(".")[-1] != "py":
            return f'Error: "{file_path}" is not a Python file.'

        try:
            completed_process = subprocess.run(
                    ["uv", "run", abs_file_path] + args,
                    timeout=30,
                    capture_output=True,
                    cwd=working_directory,
                    text=True
                    )

            if not completed_process.stdout and not completed_process.stderr:
                return "No output produced."

            return_string = ""
            return_string += f"STDOUT: {completed_process.stdout}\n"
            return_string += f"STDERR: {completed_process.stderr}\n"
            if completed_process.returncode != 0:
                return_string += f"Process exited with code {completed_process.returncode}\n"

            return return_string

        except Exception as e:
            raise Exception(f"executing Python file: {e}")

    except Exception as e:
        return  f"Error: {e}"
