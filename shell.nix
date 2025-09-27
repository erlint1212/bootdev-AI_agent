# For nix package manager, dependencies
let
  pkgs = import <nixpkgs> { config.allowUnfree = true; };
in pkgs.mkShell {
  packages = [
    pkgs.uv
  ];
  shellHook = ''
    # --- Virtual Environment Setup ---
    if [ ! -d ".venv" ]; then
        echo "Creating Python virtual environment (.venv) with UV..."
        uv init .
        source .venv/bin/activate
        uv add google-genai==1.12.1
        uv add python-dotenv==1.1.0
    else
        source .venv/bin/activate
    fi

    export PS1="\n\[\033[1;32m\][AI_agent_env:\w]\$\[\033[0m\]"
  '';
}
