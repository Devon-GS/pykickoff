import questionary
import re


def validate_project_name(text):
    # Only allow letters, numbers, underscores, and hyphens
    if not re.match(r"^[a-zA-Z0-9_-]+$", text):
        return "Project name can only contain letters, numbers, '-' or '_'"
    return True


def wizard():
    print("\n--- 🛠️  Pykickoff Project Setup ---\n")

    answers = {}

    # Basic questions
    answers["project_name"] = questionary.text(
        "What is your project name?", validate=validate_project_name
    ).ask()

    answers["project_type"] = questionary.select(
        "What type of project?",
        choices=[
            "Basic (Simple script)",
            "Packaged Project",
            "FastAPI (Web API)",
        ],
    ).ask()

    if answers["project_type"] == "Packaged Project":
        answers["description"] = questionary.text(
            "Enter a short description:", default="A new Python project."
        ).ask()

        answers["author_name"] = questionary.text("Author name:").ask()

        # answers["is_cli"] = questionary.confirm(
        # 	"Is this a CLI tool?", default=False
        # ).ask()

    # Ask for docker
    answers["use_docker"] = questionary.confirm(
        "Include Docker setup (Dockerfile & .dockerignore)?", default=False
    ).ask()

    # Ask CI
    answers["use_github_actions"] = questionary.confirm(
        "Setup GitHub Actions (Automated testing)?", default=False
    ).ask()

    # Automation questions
    answers["init_git"] = questionary.confirm(
        "Initialize a Git repository?", default=True
    ).ask()

    answers["create_venv"] = questionary.confirm(
        "Create a virtual environment (.venv)?", default=True
    ).ask()

    return answers
