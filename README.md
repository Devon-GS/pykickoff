Project Structure

pykickoff/
├── src/
│   └── pykickoff/
│       ├── __init__.py
│       ├── main.py          # The CLI entry point (Typer/Click logic)
│       ├── wizard.py        # The questions (Questionary logic)
│       ├── generator.py     # The logic that creates folders and files
│       ├── utils.py         # Helper functions (git init, venv creation)
│       └── templates/       # Folder containing your blueprints
│           ├── base/        # Files every project gets (.gitignore, README)
│           │   ├── README.md.j2
│           │   └── gitignore.txt
│           ├── fastapi/     # Specific to API projects
│           │   ├── main.py.j2
│           │   └── requirements.txt.j2
│           └── cli/         # Specific to CLI projects
│               └── cli_main.py.j2
├── tests/                   # Essential! You're dealing with File I/O
│   ├── __init__.py
│   └── test_generator.py
├── pyproject.toml           # Defines your package and dependencies
├── README.md
└── .gitignore