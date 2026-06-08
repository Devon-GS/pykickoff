from .wizard import wizard
from .generator import ProjectGenerator
from .utils import initialize_git, setup_venv, install_dependencies
import sys


def main() -> None:
    # Ask questions
    user_data = wizard()

    # Check if user cancelled (hit Ctrl+C)
    if not user_data["project_name"]:
        print("Setup cancelled.")
        sys.exit()

    # Start project Class
    start_project = ProjectGenerator(user_data)

    # Generate Files Basic
    if user_data["type"] == "Basic (Simple script)":
        start_project.run_basic()
    elif user_data["type"] == "Packaged Project":
        start_project.run_package()
    elif user_data["type"] == "FastAPI  (Web API)":
        start_project.run_fastapi()

    # Run Automation
    project_path = start_project.project_path  # Get the path from the generator

    if user_data["init_git"]:
        initialize_git(project_path)

    if user_data["create_venv"]:
        setup_venv(project_path)
        if user_data["type"] == "FastAPI  (Web API)":
            install_dependencies(project_path)

    print(f"\n🚀 All done! Your project is ready at: {project_path}")
    print(f"To start: cd {user_data['project_name']} && source .venv/bin/activate")


if __name__ == "__main__":
    main()
