import subprocess
import os


def run_command(command, cwd, description):
    """Helper to run a shell command and print status."""
    print(f"⏳ {description}...")
    try:
        # shell=True allows us to run commands like 'git init'
        subprocess.run(
            command, shell=True, cwd=cwd, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to {description}: {e}")


def initialize_git(project_path):
    run_command("git init", project_path, "Initializing Git")


def setup_venv(project_path):
    run_command("python -m venv .venv", project_path, "Creating virtual environment")


# def install_dependencies(project_path):
#     """Installs requirements if a requirements.txt exists."""
#     req_file = project_path / "requirements.txt"
#     if req_file.exists():
#         print("⏳ Installing dependencies (this may take a minute)...")
#         # Use the venv's pip specifically
#         pip_path = os.path.join(project_path, ".venv", "bin", "pip")
#         if os.name == "nt":  # Windows check
#             pip_path = os.path.join(project_path, ".venv", "Scripts", "pip.exe")

#         subprocess.run(
#             [pip_path, "install", "-r", "requirements.txt"],
#             cwd=project_path,
#             capture_output=False,
#             text=True,  # Makes stdout/stderr readable strings instead of bytes
#         )
#         print("✅ Dependencies installed.")
#     else:
#         print("❌ No requirements.txt detected!")

# --- utils.py updates ---


def install_dependencies(project_path):
    """Installs requirements if requirements files exist."""

    # Get the correct pip path based on OS
    pip_path = os.path.join(project_path, ".venv", "bin", "pip")
    precommit_path = os.path.join(project_path, ".venv", "bin", "pre-commit")
    if os.name == "nt":  # Windows check
        pip_path = os.path.join(project_path, ".venv", "Scripts", "pip.exe")
        precommit_path = os.path.join(
            project_path, ".venv", "Scripts", "pre-commit.exe"
        )

    # 1. Install Standard Requirements
    req_file = project_path / "requirements.txt"
    if req_file.exists() and os.path.getsize(req_file) > 0:
        print("⏳ Installing requirements.txt...")
        subprocess.run(
            [pip_path, "install", "-r", "requirements.txt"], cwd=project_path
        )
        print("✅ requirements.txt installed.")

    # 2. Install Dev Requirements
    req_dev_file = project_path / "requirements_dev.txt"
    if req_dev_file.exists() and os.path.getsize(req_dev_file) > 0:
        print("⏳ Installing requirements_dev.txt (pre-commit, tox, etc)...")
        subprocess.run(
            [pip_path, "install", "-r", "requirements_dev.txt"], cwd=project_path
        )
        print("✅ requirements_dev.txt installed.")

    # 3. Setup Pre-commit hooks if the file exists
    pre_commit_yaml = project_path / ".pre-commit-config.yaml"
    if pre_commit_yaml.exists():
        print("⏳ Installing pre-commit git hooks...")
        try:
            subprocess.run(
                [precommit_path, "install"],
                cwd=project_path,
                check=True,
                capture_output=True,
            )
            print("✅ Pre-commit hooks installed.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Pre-commit install failed. Make sure git is initialized. ({e})")
