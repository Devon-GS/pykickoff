import questionary

def wizard():
    answers = {}
    answers['project_name'] = questionary.text("What is your project name?").ask()
    answers['type'] = questionary.select(
        "What type of project?",
        choices=["Basic", "FastAPI", "CLI Tool"]
    ).ask()
    answers['use_git'] = questionary.confirm("Initialize git?").ask()
    return answers