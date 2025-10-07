# Simple Gemini based Code agent

Can run, read, list and write into files in the `WORKING_DIRECTORY` (in
config.py) to debug and fix code using gemini API.

Works by: `uv run main.py "Fix some specific stuff" --verbose`
Change `WORKING_DIRECTORY` to specify dir to work in.

## Extending The Project

You've done all the required steps, but have some fun (but carefully... be very cautious about giving an LLM access to your filesystem and python interpreter) with it! See if you can get it to:

* Fix harder and more complex bugs
* Refactor sections of code
* Add entirely new features

You can also try:

* Other LLM providers
* Other Gemini models
* Giving it more functions to call
* Other codebases (Commit your changes before running the agent so you can always revert!)
