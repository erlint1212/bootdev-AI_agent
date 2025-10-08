# AI Agent Project

This project is an AI-powered coding agent designed to interact with a codebase, specifically within a designated `WORKING_DIRECTORY` (defined in `config.py`). It leverages the Gemini API to perform tasks such as debugging, fixing code, and potentially extending functionality. The agent can list files, read their contents, execute Python files, and write or overwrite files within the specified directory.

## Project Overview

The AI agent is built to assist with code-related tasks in a controlled environment. It operates within the `WORKING_DIRECTORY` (set to `./calculator` by default) and includes a simple calculator application as a sample codebase for testing and demonstration purposes.

### Features
- **File Operations**: List files and directories, read file contents, and write or overwrite files.
- **Code Execution**: Run Python files with optional arguments using the `uv` package manager.
- **Code Debugging**: Use the Gemini API to analyze and fix code issues.
- **Calculator Application**: A sample application in the `calculator` directory that evaluates mathematical expressions and outputs results in JSON format.

### Directory Structure
- `.env`: Stores environment variables, including the Gemini API key.
- `.gitignore`: Ignores Python-generated files, virtual environments, and `config.py`.
- `.python-version`: Specifies Python version (3.12).
- `config.py`: Defines the `WORKING_DIRECTORY` and system prompt for the AI agent.
- `calculator/`: Contains the sample calculator application.
  - `main.py`: Entry point for the calculator app.
  - `pkg/calculator.py`: Core calculator logic for evaluating expressions.
  - `pkg/render.py`: Formats calculator output as JSON.
  - `tests.py`: Unit tests for the calculator.
  - `lorem.txt` and `morelorem.txt`: Placeholder text files.
- `functions/`: Contains utility functions for the AI agent.
  - `get_files_info.py`: Lists files and directories.
  - `get_file_content.py`: Reads file contents.
  - `run_python_file.py`: Executes Python files.
  - `write_file.py`: Writes or overwrites files.
- `main.py`: The main script for running the AI agent.
- `print_directory_tree.py`: Generates a directory tree with file contents.
- `pyproject.toml`: Project metadata and dependencies.
- `shell.nix`: Nix configuration for setting up the development environment.
- `tests.py` and `unittests.py`: Additional test scripts for the AI agent.
- `uv.lock`: Lock file for dependency management with `uv`.

## Getting Started

### Prerequisites
- Python 3.12 or higher
- `uv` package manager
- Gemini API key (set in `.env` as `GEMINI_API_KEY`)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AI_agent
   ```
2. Set up the virtual environment using `uv`:
   ```bash
   uv init .
   source .venv/bin/activate
   uv sync
   ```
3. Add your Gemini API key to `.env`:
   ```bash
   echo "GEMINI_API_KEY=your-api-key" > .env
   ```

### Usage
Run the AI agent with a prompt to perform tasks on the codebase:
```bash
uv run main.py "Fix some specific stuff" --verbose
```
- The `--verbose` flag provides detailed output, including function calls and token usage.
- Modify `WORKING_DIRECTORY` in `config.py` to target a different directory.

To run the calculator application:
```bash
uv run calculator/main.py "3 + 5"
```
This evaluates the expression `3 + 5` and outputs the result in JSON format.

### Running Tests
Run unit tests for the calculator:
```bash
uv run calculator/tests.py
```
Run additional tests for the AI agent:
```bash
uv run tests.py
uv run unittests.py
```

## Extending the Project

You can enhance the AI agent by:
- **Fixing Complex Bugs**: Experiment with more intricate debugging tasks.
- **Refactoring Code**: Use the agent to improve code structure and readability.
- **Adding New Features**: Extend the calculator or add new functionality to the agent.
- **Trying Other LLMs**: Integrate alternative LLM providers or Gemini models.
- **Expanding Functions**: Add new utility functions for additional operations.
- **Targeting Other Codebases**: Change `WORKING_DIRECTORY` to work with different projects (commit changes first to allow reverting).

**Caution**: Be careful when granting the AI agent access to your filesystem or Python interpreter, as it can read, write, and execute files within the `WORKING_DIRECTORY`.

## Dependencies
- `google-genai==1.12.1`: For interacting with the Gemini API.
- `python-dotenv==1.1.0`: For loading environment variables.

See `pyproject.toml` and `uv.lock` for a complete list of dependencies.

## Notes
- Always commit changes to your codebase before running the AI agent to ensure you can revert if needed.
- The agent is restricted to the `WORKING_DIRECTORY` for security, preventing access to sensitive files outside this directory.
- The calculator application supports basic arithmetic operations (`+`, `-`, `*`, `/`) and follows operator precedence.

