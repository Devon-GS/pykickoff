import pytest
import subprocess
import os
from unittest.mock import patch, MagicMock

# Import the class from generator.py
from pykickoff.generator import ProjectGenerator

# Import the shell helper functions from utils.py
from pykickoff.utils import run_command, install_dependencies

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
        "use_docker": True,
        "project_type": "Basic",
        "package_extras": [
            ".pre-commit-config.yaml",
            "MANIFEST.in",
            "requirements.txt",
            "requirements_dev.txt",
            "tox.ini",
        ],
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

        # Mock the 'ci' template environment
        mock_env_ci = MagicMock()
        mock_template_ci = MagicMock()
        mock_template_ci.render.return_value = "mocked_file_content"
        mock_env_ci.get_template.return_value = mock_template_ci
        gen.ci = mock_env_ci

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


def test_generate_gitignore(generator):
    generator.create_project_folder()
    generator.generate_gitignore()

    gitignore_path = generator.project_path / ".gitignore"
    assert gitignore_path.exists()
    assert gitignore_path.read_text() == "mocked_file_content"


def test_generate_pyproject(generator):
    generator.create_project_folder()
    generator.generate_pyproject()

    pyproject_path = generator.project_path / "pyproject.toml"
    assert pyproject_path.exists()
    generator.package.get_template.assert_called_with("pyproject.toml.j2")


def test_create_source_dir(generator):
    generator.create_project_folder()
    generator.create_source_dir()

    src_pkg_path = generator.project_path / "src" / "my_test_project"
    assert src_pkg_path.exists()
    assert src_pkg_path.is_dir()
    assert (src_pkg_path / "__init__.py").exists()


def test_generate_package_extras(generator):
    """Tests generation of optional package files."""
    generator.create_project_folder()
    generator.generate_package_extras()

    # 1. pre-commit
    assert (generator.project_path / ".pre-commit-config.yaml").exists()
    generator.package.get_template.assert_any_call("pre-commit-config.yaml.j2")

    # 2. MANIFEST.in
    assert (generator.project_path / "MANIFEST.in").exists()
    generator.package.get_template.assert_any_call("MANIFEST.in.j2")

    # 3. requirements.txt (should be empty)
    req_txt = generator.project_path / "requirements.txt"
    assert req_txt.exists()
    assert req_txt.read_text() == ""

    # 4. requirements_dev.txt (should contain specific text lines)
    req_dev_txt = generator.project_path / "requirements_dev.txt"
    assert req_dev_txt.exists()
    dev_content = req_dev_txt.read_text()
    assert "pytest" in dev_content
    assert "pre-commit" in dev_content
    assert "tox" in dev_content

    # 5. tox.ini
    assert (generator.project_path / "tox.ini").exists()
    generator.package.get_template.assert_any_call("tox.ini.j2")


def test_generate_hello_world(generator):
    generator.create_project_folder()
    generator.generate_hello_world()
    assert (generator.project_path / "main.py").exists()


def test_generate_fastapi_files(generator):
    generator.create_project_folder()
    generator.generate_fastapi_files()
    assert (generator.project_path / "app" / "main.py").exists()


def test_generate_docker_files(generator):
    generator.create_project_folder()
    generator.generate_docker_files()
    assert (generator.project_path / "Dockerfile").exists()
    assert (generator.project_path / ".dockerignore").exists()


def test_generate_github_actions(generator):
    generator.create_project_folder()
    generator.generate_github_actions()
    assert (generator.project_path / ".github" / "workflows" / "ci.yml").exists()


def test_generate_tests_basic(generator):
    generator.create_project_folder()
    generator.generate_tests()
    assert (generator.project_path / "tests" / "test_basic.py").exists()


# --- Run Methods Tests ---


@patch.object(ProjectGenerator, "create_project_folder")
@patch.object(ProjectGenerator, "generate_hello_world")
@patch.object(ProjectGenerator, "generate_readme")
@patch.object(ProjectGenerator, "generate_gitignore")
def test_run_basic_success(mock_git, mock_readme, mock_hello, mock_create, generator):
    mock_create.return_value = True
    generator.run_basic()
    mock_create.assert_called_once()


@patch.object(ProjectGenerator, "create_project_folder")
@patch.object(ProjectGenerator, "generate_readme")
@patch.object(ProjectGenerator, "generate_gitignore")
@patch.object(ProjectGenerator, "generate_pyproject")
@patch.object(ProjectGenerator, "create_source_dir")
@patch.object(ProjectGenerator, "generate_package_extras")
def test_run_package_success(
    mock_extras, mock_src, mock_toml, mock_git, mock_readme, mock_create, generator
):
    mock_create.return_value = True
    generator.run_package()
    mock_create.assert_called_once()
    mock_extras.assert_called_once()


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


# ==========================================
# TESTS FOR SUBPROCESS/SHELL COMMANDS (utils.py)
# ==========================================


@patch("pykickoff.utils.subprocess.run")
def test_run_command_success(mock_subprocess_run, capsys):
    run_command("fake command", "/fake/cwd", "Fake Task")
    mock_subprocess_run.assert_called_once()


@patch("pykickoff.utils.subprocess.run")
def test_run_command_failure(mock_subprocess_run, capsys):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, cmd="fake")
    run_command("fake command", "/fake/cwd", "Fake Task")
    assert "❌ Failed to Fake Task" in capsys.readouterr().out


# --- install_dependencies Tests ---


@patch("pykickoff.utils.subprocess.run")
@patch("pykickoff.utils.os.name", "posix")
def test_install_dependencies_posix_all(mock_subprocess_run, tmp_path, capsys):
    """Tests pip and pre-commit install with Mac/Linux paths."""
    # Write text so the files have a size > 0 (otherwise they are skipped)
    (tmp_path / "requirements.txt").write_text("package1")
    (tmp_path / "requirements_dev.txt").write_text("pytest")
    (tmp_path / ".pre-commit-config.yaml").touch()

    install_dependencies(tmp_path)

    expected_pip_path = os.path.join(tmp_path, ".venv", "bin", "pip")
    expected_precommit_path = os.path.join(tmp_path, ".venv", "bin", "pre-commit")

    # Assert requirements.txt was installed
    mock_subprocess_run.assert_any_call(
        [expected_pip_path, "install", "-r", "requirements.txt"], cwd=tmp_path
    )
    # Assert requirements_dev.txt was installed
    mock_subprocess_run.assert_any_call(
        [expected_pip_path, "install", "-r", "requirements_dev.txt"], cwd=tmp_path
    )
    # Assert pre-commit was installed
    mock_subprocess_run.assert_any_call(
        [expected_precommit_path, "install"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    assert mock_subprocess_run.call_count == 3
    captured = capsys.readouterr()
    assert "✅ requirements.txt installed." in captured.out
    assert "✅ requirements_dev.txt installed." in captured.out
    assert "✅ Pre-commit hooks installed." in captured.out


@patch("pykickoff.utils.subprocess.run")
@patch("pykickoff.utils.os.name", "nt")
def test_install_dependencies_windows_all(mock_subprocess_run, tmp_path):
    """Tests pip and pre-commit install with Windows paths."""
    (tmp_path / "requirements.txt").write_text("package1")
    (tmp_path / "requirements_dev.txt").write_text("pytest")
    (tmp_path / ".pre-commit-config.yaml").touch()

    install_dependencies(tmp_path)

    expected_pip_path = os.path.join(tmp_path, ".venv", "Scripts", "pip.exe")
    expected_precommit_path = os.path.join(
        tmp_path, ".venv", "Scripts", "pre-commit.exe"
    )

    mock_subprocess_run.assert_any_call(
        [expected_pip_path, "install", "-r", "requirements.txt"], cwd=tmp_path
    )
    mock_subprocess_run.assert_any_call(
        [expected_pip_path, "install", "-r", "requirements_dev.txt"], cwd=tmp_path
    )
    mock_subprocess_run.assert_any_call(
        [expected_precommit_path, "install"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )


@patch("pykickoff.utils.subprocess.run")
def test_install_dependencies_skips_empty_files(mock_subprocess_run, tmp_path):
    """Tests that files with 0 bytes size do not trigger pip install."""
    # Touch creates empty files (0 bytes)
    (tmp_path / "requirements.txt").touch()
    (tmp_path / "requirements_dev.txt").touch()

    install_dependencies(tmp_path)

    # Subprocess should not be called because files are empty
    mock_subprocess_run.assert_not_called()


@patch("pykickoff.utils.subprocess.run")
def test_install_dependencies_precommit_failure(mock_subprocess_run, tmp_path, capsys):
    """Tests that pre-commit gracefully handles a CalledProcessError (e.g. no git repo)."""
    (tmp_path / ".pre-commit-config.yaml").touch()

    # Force the subprocess command to raise an error
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        1, cmd="pre-commit install"
    )

    install_dependencies(tmp_path)

    captured = capsys.readouterr()
    assert "⚠️ Pre-commit install failed." in captured.out
