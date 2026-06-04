from .wizard import wizard
from .generator import ProjectGenerator


def main() -> None:
    user_input = wizard()
    start_project = ProjectGenerator(user_input)
    start_project.run()
    

if __name__ == "__main__":
    main()