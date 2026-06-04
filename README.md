# Pykickoff

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/pykickoff?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/pykickoff)
[![PyPI version](https://badge.fury.io/py/pykickoff.svg)](https://badge.fury.io/py/pykickoff)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pykickoff)](https://pypi.org/project/pykickoff/)
![Tests](https://github.com/Devon-GS/pykickoff/actions/workflows/tests.yml/badge.svg)
![Linux](https://img.shields.io/badge/os-Linux-blue.svg)
![macOS Intel](https://img.shields.io/badge/os-macOS_Intel-lightgrey.svg)
![macOS ARM](https://img.shields.io/badge/os-macOS_ARM-lightgrey.svg)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-2A6DBA.svg)](http://mypy-lang.org/)
<!-- [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) -->
<!-- [![Pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint/tree/main) -->
<!-- [![try/except style: tryceratops](https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black)](https://github.com/guilatrova/tryceratops) -->

Pykickoff is a lightweight, interactive CLI scaffolding tool designed to bootstrap new Python projects. By guiding users through a series of questions, it generates standard project files, sets up package structures, initializes Git repositories, and creates virtual environments automatically.

### If you like the repo, it would be awesome if you could add a star to it! It really helps out the visibility. Also for any questions at all we'd love to hear from you at ds.pydev@gmail.com

## Usage

1. **Install Pykickoff** 

```bash
python -m pip install pykickoff
```
2. **Run Pykickoff**

```bash
python -m pykickoff
```

### Wizard Options

The setup guide will prompt you to configure:
- **Project Name:** The directory name and package namespace.
- **Description:** A short description printed in the package's generated `README.md` and metadata.
- **Author Name:** Used to populate your package author fields in `pyproject.toml`.
- **Project Type:** Selection between "Basic", "FastAPI", or "CLI Tool".
- **CLI configuration:** Option to configure Python CLI entry points.
- **Automation:** Choices to automatically run `git init` and/or `python -m venv .venv` in the generated folder structure.

---

## Features

- **Interactive Setup:** Guided terminal wizard powered by `questionary`.
- **Project Structure Generation:** Creates a standardized source layout (`src/project_name/`) containing a package package setup (`__init__.py` and `main.py`).
- **Template Rendering:** Generates configuration files (`pyproject.toml`, `.gitignore`, and `README.md`) using Jinja2 templating.
- **Automation Support:** Optional automated Git initialization and Python virtual environment (`.venv`) creation during generation.

---

## Directory Layout

This project is structured as a standard Python module package:

```text
pykickoff/
├── __init__.py          # Package entrypoint exporter
├── __main__.py          # Main execution CLI script
├── generator.py         # File creation and Jinja2 rendering logic
├── utils.py             # Automation helpers (Git, venv subprocess calls)
├── wizard.py            # User prompt questions and CLI validation
└── templates/
    └── base/            # Subfolder expected to contain template files
        ├── README.md.j2
        ├── gitignore.txt
        └── pyproject.toml.j2
```

---

## Under the Hood

- **Validation:** Project names are automatically validated using regular expressions to prevent illegal characters in folder and module names.
- **Rendering:** Values gathered by `wizard.py` are mapped into Jinja2 templates. If a project is specified as a CLI, those conditions are handled dynamically when building out the `pyproject.toml` configuration.
- **Process Automation:** The tool uses Python's `subprocess` module to run CLI tools (`git`, `python`) directly inside the generated directory paths to ensure seamless environment preparation.