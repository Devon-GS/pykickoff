import pytest
import subprocess
from unittest.mock import patch, MagicMock

# Import the class from generator.py
from pykickoff.generator import ProjectGenerator

# Import the shell helper functions from utils.py
from pykickoff.utils import run_command, initialize_git, setup_venv

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

    # Note: pyproject uses generator.package now!
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
    """Tests creation of a root-level main.py file for basic projects."""
    generator.create_project_folder()
    generator.generate_hello_world()

    main_py_path = generator.project_path / "main.py"
    assert main_py_path.exists()
    assert "def main():" in main_py_path.read_text()


# --- Run Methods Tests ---


@patch.object(ProjectGenerator, "create_project_folder")
@patch.object(ProjectGenerator, "generate_hello_world")
@patch.object(ProjectGenerator, "generate_readme")
@patch.object(ProjectGenerator, "generate_gitignore")
def test_run_basic_success(mock_git, mock_readme, mock_hello, mock_create, generator):
    """Tests run_basic calls the correct methods."""
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
    """Tests run_package calls the correct methods."""
    mock_create.return_value = True
    generator.run_package()

    mock_create.assert_called_once()
    mock_readme.assert_called_once()
    mock_git.assert_called_once()
    mock_toml.assert_called_once()
    mock_src.assert_called_once()


@patch.object(ProjectGenerator, "create_project_folder")
@patch.object(ProjectGenerator, "generate_readme")
def test_run_aborts_if_folder_exists(mock_readme, mock_create, generator):
    """Tests both run commands abort if folder already exists."""
    mock_create.return_value = False

    generator.run_basic()
    generator.run_package()

    # create_project_folder was called twice (once by each run method)
    assert mock_create.call_count == 2
    # generate_readme should never be called
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
    assert "⏳ Fake Task..." in captured.out
    assert "✅ Fake Task complete." in captured.out


@patch("pykickoff.utils.subprocess.run")
def test_run_command_failure(mock_subprocess_run, capsys):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="fake command", output="Some error occurred"
    )
    run_command("fake command", "/fake/cwd", "Fake Task")
    captured = capsys.readouterr()
    assert "⏳ Fake Task..." in captured.out
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
