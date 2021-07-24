import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from snipsync.main import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def init_files_empty():
    (Path(__file__).parent / "data/user.xml").unlink(missing_ok=True)
    (Path(__file__).parent / "data/config.cfg").unlink(missing_ok=True)
    shutil.copy(Path(__file__).parent / 'data/config.cfg.bkp', Path(__file__).parent / 'data/config.cfg')
    shutil.copy(Path(__file__).parent / 'data/user_empty.xml.bkp', Path(__file__).parent / 'data/user.xml')
    _ = None


# module level mocking
@pytest.fixture(autouse=True)
def mock_get_app_dir(mocker):
    mocker.patch("snipsync.main.typer.get_app_dir", return_value=str(Path(__file__).parent / "data"))


@pytest.mark.skip("requires to close vim interactively via '.:q<Enter>'")
def test_dir(mock_get_app_dir):
    result = runner.invoke(app, ["dir"], input=":q\n")
    assert result.exit_code == 0


def test_auto_sync(xmlsnips_file):
    result = runner.invoke(app, ["auto-sync"])
    assert result.exit_code == 0
    data = Path(xmlsnips_file).read_text()
    assert 'twlog' in data
    assert "Done snippets for SHELL" in result.stdout
    _ = None


def test_sync(xmlsnips_file):
    result = runner.invoke(app, ["sync", "-c", "Bash", "-c", "Python", "tests/data/python.snippets", "tests/data/user.xml"])
    assert result.exit_code == 0
    data = Path(xmlsnips_file).read_text()
    assert 'twlog' in data
    assert "Done snippets for SHELL" in result.stdout
    _ = None
