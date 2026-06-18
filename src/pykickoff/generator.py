from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class ProjectGenerator:
    def __init__(self, project_data):
        self.data = project_data  # Dictionary containing name, description, etc.
        self.project_path = Path.cwd() / project_data["project_name"]

        # Setup Jinja2 to look for templates in our internal folder
        template_base_dir = Path(__file__).parent / "templates" / "base"
        self.base = Environment(loader=FileSystemLoader(template_base_dir))

        template_package_dir = Path(__file__).parent / "templates" / "package"
        self.package = Environment(loader=FileSystemLoader(template_package_dir))

        template_fastapi_dir = Path(__file__).parent / "templates" / "fastapi"
        self.fastapi = Environment(loader=FileSystemLoader(template_fastapi_dir))

        template_docker_dir = Path(__file__).parent / "templates" / "docker"
        self.docker = Environment(loader=FileSystemLoader(template_docker_dir))

        template_ci_dir = Path(__file__).parent / "templates" / "cicd"
        self.ci = Environment(loader=FileSystemLoader(template_ci_dir))

    def create_project_folder(self):
        """Creates the main directory."""
        if self.project_path.exists():
            print(f"Error: Folder {self.project_path} already exists!")
            return False

        self.project_path.mkdir(parents=True)
        return True

    def generate_readme(self):
        """Fills the README template with data and saves it."""
        template = self.base.get_template("README.md.j2")
        rendered_content = template.render(
            project_name=self.data["project_name"],
            description=self.data.get("description", "A new Python project."),
        )

        with open(self.project_path / "README.md", "w") as f:
            f.write(rendered_content)

    def generate_gitignore(self):
        """Copies the static gitignore file."""
        template = self.base.get_template("gitignore.txt")
        content = template.render()  # No variables needed here

        with open(self.project_path / ".gitignore", "w") as f:
            f.write(content)

    def generate_pyproject(self):
        """Generates the pyproject.toml file."""
        template = self.package.get_template("pyproject.toml.j2")

        rendered_content = template.render(
            project_name=self.data["project_name"],
            description=self.data.get("description", "A new Python project."),
            author_name=self.data.get("author_name", "Unknown Author"),
            is_cli=self.data.get("is_cli", False),
        )

        with open(self.project_path / "pyproject.toml", "w") as f:
            f.write(rendered_content)

    def create_source_dir(self):
        """Creates the internal package directory (e.g., my_app/my_app/)"""
        src_path = (
            self.project_path / "src" / self.data["project_name"].replace("-", "_")
        )
        src_path.mkdir(parents=True, exist_ok=True)

        # Create an empty __init__.py to make it a package
        (src_path / "__init__.py").touch()

        # Create a basic main.py
        with open(src_path / "main.py", "w") as f:
            f.write(
                'def main():\n    print("Hello from your new project!")\n\nif __name__ == "__main__":\n    main()'
            )

    def generate_hello_world(self):
        """Create main.py"""
        with open(self.project_path / "main.py", "w") as f:
            f.write(
                'def main():\n    print("Hello from your new project!")\n\nif __name__ == "__main__":\n    main()'
            )

    def generate_fastapi_files(self):
        """Creates FastAPI structure."""
        # 1. Create an 'app' directory inside the project
        app_dir = self.project_path / "app"
        app_dir.mkdir(exist_ok=True)
        (app_dir / "__init__.py").touch()

        # 2. Generate main.py from the FastAPI template
        template = self.fastapi.get_template("main.py.j2")
        content = template.render(project_name=self.data["project_name"])
        with open(app_dir / "main.py", "w") as f:
            f.write(content)

        # 3. Generate requirements.txt
        req_template = self.fastapi.get_template("requirements.txt.j2")
        with open(self.project_path / "requirements.txt", "w") as f:
            f.write(req_template.render())

    def generate_docker_files(self):
        """Generates Dockerfile and .dockerignore."""
        # 1. Generate Dockerfile
        template = self.docker.get_template("Dockerfile.j2")
        content = template.render(use_docker=self.data["use_docker"])
        with open(self.project_path / "Dockerfile", "w") as f:
            f.write(content)

        # 2. Generate .dockerignore
        ignore_template = self.docker.get_template("dockerignore.txt")
        with open(self.project_path / ".dockerignore", "w") as f:
            f.write(ignore_template.render())

    # Github actions
    def generate_github_actions(self):
        """Creates the .github/workflows directory and CI yaml file."""
        # Create .github/workflows/ folder
        github_dir = self.project_path / ".github" / "workflows"
        github_dir.mkdir(parents=True, exist_ok=True)

        # Generate ci.yml
        template = self.ci.get_template("ci.yml.j2")
        with open(github_dir / "ci.yml", "w") as f:
            f.write(template.render())

    def generate_tests(self):
        """Creates a tests folder with a basic passing test."""
        # Create tests/ folder
        test_dir = self.project_path / "tests"
        test_dir.mkdir(exist_ok=True)
        (test_dir / "__init__.py").touch()

        # Generate test file
        template = self.ci.get_template("test_basic.py.j2")
        content = template.render(
            project_type=self.data["project_type"],
            project_name=self.data["project_name"],
        )

        # In FastAPI, we test the API. Otherwise, simple math test.
        file_name = (
            "test_api.py" if "FastAPI" in self.data["project_type"] else "test_basic.py"
        )
        with open(test_dir / file_name, "w") as f:
            f.write(content)

    # RUN FUNCTIONS
    def run_basic(self):
        """The execution flow for basic project."""
        print(f"🚀 Generating {self.data['project_name']}...")
        if self.create_project_folder():
            self.generate_hello_world()
            self.generate_readme()
            self.generate_gitignore()
            print("✅ Project files created successfully!")

    def run_package(self):
        """The main execution flow for package."""
        print(f"🚀 Generating {self.data['project_name']}...")
        if self.create_project_folder():
            self.generate_readme()
            self.generate_gitignore()
            self.generate_pyproject()
            self.create_source_dir()
            print("✅ Project files created successfully!")

    def run_fastapi(self):
        """The main execution flow for fastapi."""
        print(f"🚀 Generating {self.data['project_name']}...")
        if self.create_project_folder():
            self.generate_readme()
            self.generate_gitignore()
            self.generate_fastapi_files()
            print("✅ Project files created successfully!")

    def run_docker(self):
        """The main execution flow for docker."""
        print("🚀 Generating docker files...")
        self.generate_docker_files()
        print("✅ Docker files created successfully!")

    def run_github_actions(self):
        """The main execution flow for github actions."""
        print("🚀 Generating Github Action files...")
        self.generate_github_actions()
        self.generate_tests()
        print("✅ Github Action files created successfully!")
