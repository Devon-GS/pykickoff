import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class ProjectGenerator:
	def __init__(self, project_data):
		self.data = project_data  # Dictionary containing name, description, etc.
		self.project_path = Path.cwd() / project_data['project_name']
		
		# Setup Jinja2 to look for templates in our internal folder
		template_dir = Path(__file__).parent / "templates" / "base"
		self.env = Environment(loader=FileSystemLoader(template_dir))

	def create_project_folder(self):
		"""Creates the main directory."""
		if self.project_path.exists():
			print(f"Error: Folder {self.project_path} already exists!")
			return False
		
		self.project_path.mkdir(parents=True)
		return True

	def generate_readme(self):
		"""Fills the README template with data and saves it."""
		template = self.env.get_template("README.md.j2")
		rendered_content = template.render(
			project_name=self.data['project_name'],
			description=self.data.get('description', 'A new Python project.')
		)
		
		with open(self.project_path / "README.md", "w") as f:
			f.write(rendered_content)

	def generate_gitignore(self):
		"""Copies the static gitignore file."""
		template = self.env.get_template("gitignore.txt")
		content = template.render() # No variables needed here
		
		with open(self.project_path / ".gitignore", "w") as f:
			f.write(content)
			
	def generate_pyproject(self):
		"""Generates the pyproject.toml file."""
		template = self.env.get_template("pyproject.toml.j2")
		
		rendered_content = template.render(
			project_name=self.data['project_name'],
			description=self.data.get('description', 'A new Python project.'),
			author_name=self.data.get('author_name', 'Unknown Author'),
			is_cli=self.data.get('is_cli', False)
		)
		
		with open(self.project_path / "pyproject.toml", "w") as f:
			f.write(rendered_content)

	def run(self):
		"""The main execution flow."""
		print(f"🚀 Generating {self.data['project_name']}...")
		if self.create_project_folder():
			self.generate_readme()
			self.generate_gitignore()
			self.generate_pyproject()
			print("✅ Project files created successfully!")






































































# import os
# from pathlib import Path

# def create_structure(answers):
#     project_path = Path.cwd() / answers['project_name']
#     project_path.mkdir(exist_ok=True)
	
#     # Example: Create the src folder
#     src_path = project_path / "src"
#     src_path.mkdir()
	
#     # More logic to copy templates and fill them with Jinja2...
	
# def get_files_to_create(answers):
#     files = ["README.md", "pyproject.toml", ".gitignore"] # Always create
	
#     if answers['use_docker']:
#         files.extend(["Dockerfile", ".dockerignore"])
		
#     if answers['use_github_actions']:
#         files.append(".github/workflows/tests.yml")
		
#     if answers['type'] == "FastAPI":
#         files.extend(["src/main.py", "src/models.py", ".env.example"])
		
#     return files