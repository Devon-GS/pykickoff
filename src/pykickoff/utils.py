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


def install_dependencies(project_path):
    """Installs requirements if a requirements.txt exists."""
    req_file = project_path / "requirements.txt"
    if req_file.exists():
        print("⏳ Installing dependencies (this may take a minute)...")
        # Use the venv's pip specifically
        pip_path = os.path.join(project_path, ".venv", "bin", "pip")
        if os.name == "nt":  # Windows check
            pip_path = os.path.join(project_path, ".venv", "Scripts", "pip.exe")

        subprocess.run(
            [pip_path, "install", "-r", "requirements.txt"],
            cwd=project_path,
            capture_output=False,
            text=True,  # Makes stdout/stderr readable strings instead of bytes
        )
        print("✅ Dependencies installed.")
    else:
        print("❌ No requirements.txt detected!")
