import os

def get_files_info(working_directory : str, directory : str =".") -> str:
    dir_report = "Result for current directory:\n"
    if directory != ".":
        dir_report = f"Result for '{directory}' directory:\n"
    try:
        working_directory = os.path.realpath(working_directory)
        full_path = os.path.realpath(os.path.join(working_directory, directory))
        # Without this restriction, the LLM might go running amok anywhere on the
        # machine, reading sensitive files or overwriting important data.
        if not os.path.commonpath([working_directory, full_path]) == working_directory:
            # All of our "tool call" functions, including get_files_info, should
            # always return a string. If errors can be raised inside them, need
            # to catch those errors and return a string describing the error
            # instead. This will allow the LLM to handle the errors gracefully.
            dir_report += f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
            return dir_report

        if not os.path.isdir(full_path):
            dir_report += f'    Error: "{directory}" is not a directory'
            return dir_report

        dir_objects = os.listdir(full_path)
        for dir_obj in dir_objects:
            dir_path = os.path.join(full_path, dir_obj)
            is_dir = False
            if os.path.isdir(dir_path):
                is_dir = True

            dir_report += f" - {dir_obj}: file_size={os.path.getsize(dir_path)} bytes, is_dir={is_dir}\n" 

        return dir_report.rstrip("\n")

    except Exception as e:
        dir_report += f"    Error: {e}"
        return dir_report

if __name__ == "__main__":
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))
