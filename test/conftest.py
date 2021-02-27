from pathlib import Path

import pytest

from snipsync.io import read_ultisnips


@pytest.fixture()
def ultisnips_file():
    return Path('../data/sh.snippets')


@pytest.fixture()
def ultisnips(ultisnips_file):
    return read_ultisnips(ultisnips_file)
