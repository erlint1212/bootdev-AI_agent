import unittest
import textwrap
import re
from functions.get_files_info import get_files_info


def cleaner(result: str, expected_result: str) -> tuple[list[str], list[str]]:
    """Strip file sizes and split into lines for comparison."""
    clean_result = re.sub(r'file_size.*?bytes', 'file_size=XXX bytes', result)
    clean_expected = re.sub(r'file_size.*?bytes', 'file_size=XXX bytes', expected_result)

    # Normalize whitespace and split into lines
    result_lines = [line.strip() for line in clean_result.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in clean_expected.splitlines() if line.strip()]
    return result_lines, expected_lines


class Test_get_files_info(unittest.TestCase):

    def test_calculator(self):
        result = get_files_info("calculator", ".")
        expected_result = textwrap.dedent("""
            Result for current directory:
             - main.py: file_size=XXX bytes, is_dir=False
             - tests.py: file_size=XXX bytes, is_dir=False
             - pkg: file_size=XXX bytes, is_dir=True
        """)
        clean_result, clean_expected = cleaner(result, expected_result)
        self.assertCountEqual(clean_result, clean_expected)

    def test_calculator_pkg(self):
        result = get_files_info("calculator", "pkg")
        expected_result = textwrap.dedent("""
            Result for 'pkg' directory:
             - calculator.py: file_size=XXX bytes, is_dir=False
             - render.py: file_size=XXX bytes, is_dir=False
             - __pycache__: file_size=XXX bytes, is_dir=True
        """)
        clean_result, clean_expected = cleaner(result, expected_result)
        self.assertCountEqual(clean_result, clean_expected)

    def test_illegal_dir_bin(self):
        result = get_files_info("calculator", "/bin")
        expected_result = textwrap.dedent("""
            Result for '/bin' directory:
                Error: Cannot list "/bin" as it is outside the permitted working directory
        """)
        clean_result, clean_expected = cleaner(result, expected_result)
        self.assertCountEqual(clean_result, clean_expected)

    def test_illegal_dir_jump(self):
        result = get_files_info("calculator", "../")
        expected_result = textwrap.dedent("""
            Result for '../' directory:
                Error: Cannot list "../" as it is outside the permitted working directory
        """)
        clean_result, clean_expected = cleaner(result, expected_result)
        self.assertCountEqual(clean_result, clean_expected)


if __name__ == "__main__":
    unittest.main()

