import pytest
import subprocess
import os
from unittest.mock import patch, MagicMock

# Import the class from generator.py
from pykickoff.generator import ProjectGenerator

# Import the shell helper functions from utils.py
from pykickoff.utils import (
    run_command,
    initialize_git,
    setup_venv,
    install_dependencies,
)

# ==========================================
# FIXTURES
# ==========================================


@pytest.fixture
def project_data():
    """Provides standard project data for tests."""
    return {
        "project_name": "my-test-project",
        "description": "A test project description",
        "author_name": "Test Author",
        "is_cli": True,
        "use_docker": True,  # Added for Docker support
    }


@pytest.fixture
def generator(tmp_path, monkeypatch, project_data):
    """Fixture to initialize ProjectGenerator safely without writing real files."""
    module_name = ProjectGenerator.__module__
    monkeypatch.setattr(f"{module_name}.Path.cwd", lambda: tmp_path)

    with patch(f"{module_name}.FileSystemLoader"):
        gen = ProjectGenerator(project_data)

        # Mock the 'base' template environment
        mock_env_base = MagicMock()
        mock_template_base = MagicMock()
        mock_template_base.render.return_value = "mocked_file_content"
        mock_env_base.get_template.return_value = mock_template_base
        gen.base = mock_env_base

        # Mock the 'package' template environment
        mock_env_package = MagicMock()
        mock_template_package = MagicMock()
        mock_template_package.render.return_value = "mocked_file_content"
        mock_env_package.get_template.return_value = mock_template_package
        gen.package = mock_env_package

        # Mock the 'fastapi' template environment
        mock_env_fastapi = MagicMock()
        mock_template_fastapi = MagicMock()
        mock_template_fastapi.render.return_value = "mocked_file_content"
        mock_env_fastapi.get_template.return_value = mock_template_fastapi
        gen.fastapi = mock_env_fastapi

        # Mock the 'docker' template environment
        mock_env_docker = MagicMock()
        mock_template_docker = MagicMock()
        mock_template_docker.render.return_value = "mocked_file_content"
        mock_env_docker.get_template.return_value = mock_template_docker
        gen.docker = mock_env_docker

        yield gen


# ==========================================
# TESTS FOR PROJECTGENERATOR CLASS
# ==========================================


def test_init_sets_correct_paths(generator, tmp_path):
    assert generator.project_path == tmp_path / "my-test-project"
    assert generator.data["project_name"] == "my-test-project"


def test_create_project_folder_success(generator):
    assert generator.create_project_folder() is True
    assert generator.project_path.exists()
    assert generator.project_path.is_dir()


def test_create_project_folder_already_exists(generator):
    generator.project_path.mkdir()
    assert generator.create_project_folder() is False


def test_generate_readme(generator):
    generator.create_project_folder()
    generator.generate_readme()

    readme_path = generator.project_path / "README.md"
    assert readme_path.exists()
    assert readme_path.read_text() == "mocked_file_content"

    generator.base.get_template.assert_called_with("README.md.j2")
    generator.base.get_template().render.assert_called_with(
        project_name="my-test-project", description="A test project description"
    )


def test_generate_gitignore(generator):
    generator.create_project_folder()
    generator.generate_gitignore()

    gitignore_path = generator.project_path / ".gitignore"
    assert gitignore_path.exists()
    assert gitignore_path.read_text() == "mocked_file_content"

    generator.base.get_template.assert_called_with("gitignore.txt")
    generator.base.get_template().render.assert_called_with()


def test_generate_pyproject(generator):
    generator.create_project_folder()
    generator.generate_pyproject()

    pyproject_path = generator.project_path / "pyproject.toml"
    assert pyproject_path.exists()

    generator.package.get_template.assert_called_with("pyproject.toml.j2")
    generator.package.get_template().render.assert_called_with(
        project_name="my-test-project",
        description="A test project description",
        author_name="Test Author",
        is_cli=True,
    )


def test_create_source_dir(generator):
    generator.create_project_folder()
    generator.create_source_dir()

    src_pkg_path = generator.project_path / "src" / "my_test_project"

    assert src_pkg_path.exists()
    assert src_pkg_path.is_dir()
    assert (src_pkg_path / "__init__.py").exists()

    main_py_path = src_pkg_path / "main.py"
    assert main_py_path.exists()
    assert "def main():" in main_py_path.read_text()


def test_generate_hello_world(generator):
    generator.create_project_folder()
    generator.generate_hello_world()

    main_py_path = generator.project_path / "main.py"
    assert main_py_path.exists()
    assert "def main():" in main_py_path.read_text()


def test_generate_fastapi_files(generator):
    generator.create_project_folder()
    generator.generate_fastapi_files()

    app_dir = generator.project_path / "app"
    assert app_dir.exists()
    assert app_dir.is_dir()
    assert (app_dir / "__init__.py").exists()

    main_py_path = app_dir / "main.py"
    assert main_py_path.exists()
    assert main_py_path.read_text() == "mocked_file_content"
    generator.fastapi.get_template.assert_any_call("main.py.j2")

    req_path = generator.project_path / "requirements.txt"
    assert req_path.exists()
    assert req_path.read_text() == "mocked_file_content"
    generator.fastapi.get_template.assert_any_call("requirements.txt.j2")


def test_generate_docker_files(generator):
    """Tests creation of Dockerfile and .dockerignore"""
    generator.create_project_folder()  # Ensure path exists for test
    generator.generate_docker_files()

    # 1. Check Dockerfile
    dockerfile_path = generator.project_path / "Dockerfile"
    assert dockerfile_path.exists()
    assert dockerfile_path.read_text() == "mocked_file_content"
    generator.docker.get_template.assert_any_call("Dockerfile.j2")
    generator.docker.get_template().render.assert_any_call(use_docker=True)

    # 2. Check .dockerignore
    dockerignore_path = generator.project_path / ".dockerignore"
    assert dockerignore_path.exists()
    assert dockerignore_path.read_text() == "mocked_file_content"
    generator.docker.get_template.assert_any_call("dockerignore.txt")


# --- Run Methods Tests ---


@patch.object(ProjectGenerator, "create_project_folder")
@patch.object(ProjectGenerator, "generate_hello_world")
@patch.object(ProjectGenerator, "generate_readme")
@patch.object(ProjectGenerator, "generate_gitignore")
def test_run_basic_success(mock_git, mock_readme, mock_hello, mock_create, generator):
    mock_create.return_value = True
    generator.run_basic()

    mock_create.assert_called_once()
    mock_hello.assert_called_once()
    mock_readme.assert_called_once()
    mock_git.assert_called_once()


@patch.object(ProjectGenerator, "create_project_folder")
@patch.object(ProjectGenerator, "generate_readme")
@patch.object(ProjectGenerator, "generate_gitignore")
@patch.object(ProjectGenerator, "generate_pyproject")
@patch.object(ProjectGenerator, "create_source_dir")
def test_run_package_success(
    mock_src, mock_toml, mock_git, mock_readme, mock_create, generator
):
    mock_create.return_value = True
    generator.run_package()

    mock_create.assert_called_once()
    mock_readme.assert_called_once()
    mock_git.assert_called_once()
    mock_toml.assert_called_once()
    mock_src.assert_called_once()


@patch.object(ProjectGenerator, "create_project_folder")
@patch.object(ProjectGenerator, "generate_readme")
@patch.object(ProjectGenerator, "generate_gitignore")
@patch.object(ProjectGenerator, "generate_fastapi_files")
def test_run_fastapi_success(
    mock_fastapi, mock_git, mock_readme, mock_create, generator
):
    mock_create.return_value = True
    generator.run_fastapi()

    mock_create.assert_called_once()
    mock_readme.assert_called_once()
    mock_git.assert_called_once()
    mock_fastapi.assert_called_once()


@patch.object(ProjectGenerator, "generate_docker_files")
def test_run_docker_success(mock_docker, generator):
    """Tests run_docker execution flow."""
    generator.run_docker()
    mock_docker.assert_called_once()


@patch.object(ProjectGenerator, "create_project_folder")
@patch.object(ProjectGenerator, "generate_readme")
def test_run_aborts_if_folder_exists(mock_readme, mock_create, generator):
    """Tests all standard run commands abort if folder already exists."""
    mock_create.return_value = False

    generator.run_basic()
    generator.run_package()
    generator.run_fastapi()
    # Note: run_docker does not check for folder creation, so we don't test it here.

    assert mock_create.call_count == 3
    mock_readme.assert_not_called()


# ==========================================
# TESTS FOR SUBPROCESS/SHELL COMMANDS (utils.py)
# ==========================================


@patch("pykickoff.utils.subprocess.run")
def test_run_command_success(mock_subprocess_run, capsys):
    run_command("fake command", "/fake/cwd", "Fake Task")
    mock_subprocess_run.assert_called_once_with(
        "fake command",
        shell=True,
        cwd="/fake/cwd",
        check=True,
        capture_output=True,
        text=True,
    )
    captured = capsys.readouterr()
    assert "✅ Fake Task complete." in captured.out


@patch("pykickoff.utils.subprocess.run")
def test_run_command_failure(mock_subprocess_run, capsys):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="fake command", output="Some error occurred"
    )
    run_command("fake command", "/fake/cwd", "Fake Task")
    captured = capsys.readouterr()
    assert "❌ Failed to Fake Task" in captured.out


@patch("pykickoff.utils.run_command")
def test_initialize_git(mock_run_command):
    initialize_git("/my/project/path")
    mock_run_command.assert_called_once_with(
        "git init", "/my/project/path", "Initializing Git"
    )


@patch("pykickoff.utils.run_command")
def test_setup_venv(mock_run_command):
    setup_venv("/my/project/path")
    mock_run_command.assert_called_once_with(
        "python -m venv .venv", "/my/project/path", "Creating virtual environment"
    )


@patch("pykickoff.utils.subprocess.run")
@patch("pykickoff.utils.os.name", "posix")
def test_install_dependencies_posix(mock_subprocess_run, tmp_path, capsys):
    (tmp_path / "requirements.txt").touch()

    install_dependencies(tmp_path)

    expected_pip_path = os.path.join(tmp_path, ".venv", "bin", "pip")
    mock_subprocess_run.assert_called_once_with(
        [expected_pip_path, "install", "-r", "requirements.txt"],
        cwd=tmp_path,
        capture_output=False,
        text=True,
    )
    captured = capsys.readouterr()
    assert "✅ Dependencies installed." in captured.out


@patch("pykickoff.utils.subprocess.run")
@patch("pykickoff.utils.os.name", "nt")
def test_install_dependencies_windows(mock_subprocess_run, tmp_path, capsys):
    (tmp_path / "requirements.txt").touch()

    install_dependencies(tmp_path)

    expected_pip_path = os.path.join(tmp_path, ".venv", "Scripts", "pip.exe")
    mock_subprocess_run.assert_called_once_with(
        [expected_pip_path, "install", "-r", "requirements.txt"],
        cwd=tmp_path,
        capture_output=False,
        text=True,
    )
    captured = capsys.readouterr()
    assert "✅ Dependencies installed." in captured.out


@patch("pykickoff.utils.subprocess.run")
def test_install_dependencies_no_requirements_file(
    mock_subprocess_run, tmp_path, capsys
):
    install_dependencies(tmp_path)
    mock_subprocess_run.assert_not_called()
    captured = capsys.readouterr()
    assert "❌ No requirements.txt detected!" in captured.out
