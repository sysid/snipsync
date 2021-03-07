import json

import pytest

from snipsync.main import parse_config
from tests.conftest import ROOT_DIR


def test_parse_config():
    config_path = ROOT_DIR / 'tests/data/config.cfg'
    cfg = parse_config(config_path)
    _ = None
    assert list(cfg['snip'].keys()) == ['SHELL', 'PYTHON']
    assert cfg['snip']['SHELL']['contexts'] == ['SHELL_SCRIPT', 'Bash']


def test_parse_invalid_config():
    config_path = ROOT_DIR / 'tests/data/config_invalid.cfg'
    with pytest.raises(json.JSONDecodeError) as e:
        _ = parse_config(config_path)
