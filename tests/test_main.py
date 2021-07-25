import json
from pathlib import Path, PosixPath

import click
import pytest

from snipsync.main import check_intellij_installation, parse_config
from tests.conftest import ROOT_DIR


def test_parse_config():
    config_path = ROOT_DIR / "tests/data/config_valid.cfg"
    cfg = parse_config(config_path)
    _ = None
    assert list(cfg["snip"].keys()) == ["SHELL", "PYTHON"]
    assert cfg["snip"]["SHELL"]["contexts"] == ["SHELL_SCRIPT", "Bash"]


def test_parse_invalid_config():
    config_path = ROOT_DIR / "tests/data/config_invalid.cfg"
    with pytest.raises(json.JSONDecodeError) as e:
        _ = parse_config(config_path)


DIRECTORY_LISTING = [
    PosixPath("~/Library/Application Support/JetBrains/WebStorm2020.1").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/PyCharm2021.1").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/IdeaIC2021.1").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/consentOptions").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/PyCharm2020.3").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/IdeaIC2020.3").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/PyCharm2020.2").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/Pycharm").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/WebStorm2020.3").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/Webstorm").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/WebStorm2021.1").expanduser(),
    PosixPath("~/Library/Application Support/JetBrains/PyCharm2020.1").expanduser(),
]


@pytest.mark.parametrize(
    ("snippet_path", "is_dir"),
    (
        (Path("invalid").expanduser(), False),
        (
            Path(
                "~/Library/Application Support/JetBrains/PyCharm2020.1/jba_config/templates"
            ).expanduser(),
            True,
        ),
        (
            Path(
                "~/Library/Application Support/JetBrains/WebStorm2020.1/jba_config/templates"
            ).expanduser(),
            True,
        ),
        (
            Path(
                "~/Library/Application Support/JetBrains/GoLand2020.1/jba_config/templates"
            ).expanduser(),
            True,
        ),
    ),
)
def test_check_intellij_installation_raise(mocker, snippet_path, is_dir):
    mocker.patch("snipsync.main.Path.glob", return_value=DIRECTORY_LISTING)
    mocker.patch("snipsync.main.Path.is_dir", return_value=is_dir)
    with pytest.raises(click.exceptions.Abort):
        check_intellij_installation(snippet_path)


@pytest.mark.parametrize(
    ("snippet_path", "is_dir", "result"),
    (
        (
            Path(
                "~/Library/Application Support/JetBrains/PyCharm2021.1/jba_config/templates"
            ).expanduser(),
            True,
            True,
        ),
        (
            Path(
                "~/Library/Application Support/JetBrains/WebStorm2021.1/jba_config/templates"
            ).expanduser(),
            True,
            True,
        ),
    ),
)
def test_check_intellij_installation(mocker, snippet_path, is_dir, result):
    mocker.patch("snipsync.main.Path.glob", return_value=DIRECTORY_LISTING)
    mocker.patch("snipsync.main.Path.is_dir", return_value=is_dir)
    # p = Path("~/Library/Application Support/JetBrains/PyCharm2021.1/jba_config/templates").expanduser()
    assert check_intellij_installation(snippet_path)


@pytest.mark.skip("manual testing")
def test_check_intellij_installation_manual():
    snippet_path = Path(
        "~/Library/Application Support/JetBrains/PyCharm2021.1/jba_config/templates"
    ).expanduser()
    assert check_intellij_installation(snippet_path)
