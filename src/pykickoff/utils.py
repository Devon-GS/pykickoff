import subprocess
import os

def run_command(command, cwd, description):
    """Helper to run a shell command and print status."""
    print(f"⏳ {description}...")
    try:
        # shell=True allows us to run commands like 'git init'
        subprocess.run(command, shell=True, cwd=cwd, check=True, 
                       capture_output=True, text=True)
        print(f"✅ {description} complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to {description}: {e}")

def initialize_git(project_path):
    run_command("git init", project_path, "Initializing Git")

def setup_venv(project_path):
    run_command("python -m venv .venv", project_path, "Creating virtual environment")